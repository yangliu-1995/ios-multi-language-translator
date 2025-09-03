#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM translator implementation
Support for local and remote LLM APIs
"""

import json
import requests
from typing import Dict, List, Optional
from .base import TranslatorBase


class LLMTranslator(TranslatorBase):
    """LLM-based translator implementation"""
    
    def __init__(self, api_url: str = "http://127.0.0.1:11434/api/generate", 
                 model: str = "mistral:latest", timeout: int = 60):
        super().__init__()
        self.api_url = api_url
        self.model = model
        self.timeout = timeout
        self.rate_limit_delay = 2.0  # LLM responses can be slower
        
        # Auto-detect available models if using Ollama
        if self._is_ollama_api():
            available_models = self._get_available_models()
            if available_models and model not in available_models:
                print(f"Warning: Model '{model}' not found. Available models: {available_models}")
                if available_models:
                    self.model = available_models[0]
                    print(f"Using first available model: {self.model}")
        
        # Language name mapping for better LLM understanding
        self.language_names = {
            'zh': 'Chinese (Simplified)',
            'zh-hans': 'Chinese (Simplified)',
            'zh-hant': 'Chinese (Traditional)',
            'zh-tw': 'Chinese (Traditional)',
            'ja': 'Japanese',
            'ko': 'Korean',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'it': 'Italian',
            'pt': 'Portuguese',
            'pt-br': 'Brazilian Portuguese',
            'ru': 'Russian',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'tr': 'Turkish',
            'pl': 'Polish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'fi': 'Finnish',
            'no': 'Norwegian',
            'en': 'English'
        }
    
    def translate(self, text: str, target_language: str, source_language: str = 'en') -> Optional[str]:
        """Translate text using LLM API"""
        if not text.strip():
            return text
        
        # Get language names for better LLM understanding
        source_lang_name = self.language_names.get(source_language.lower(), source_language)
        target_lang_name = self.language_names.get(target_language.lower(), target_language)
        
        # Create translation prompt
        prompt = self._create_translation_prompt(text, source_lang_name, target_lang_name)
        
        try:
            # Call LLM API
            response = self._call_llm_api(prompt)
            
            if response:
                # Extract translation from response
                translation = self._extract_translation(response)
                return translation
            else:
                print(f"LLM API call failed for text: {text[:50]}...")
                return None
                
        except Exception as e:
            print(f"LLM translation error: {e}")
            return None
    
    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes"""
        return list(self.language_names.keys())
    
    def _create_translation_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        """Create translation prompt for LLM"""
        prompt = f"""Please translate the following text from {source_lang} to {target_lang}. 
Only return the translated text, nothing else.

Text to translate: "{text}"

Translation:"""
        return prompt
    
    def _call_llm_api(self, prompt: str) -> Optional[str]:
        """Call LLM API with the given prompt"""
        try:
            # Prepare request payload (adjust based on your LLM API format)
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # Make API request
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            # Parse response (adjust based on your LLM API response format)
            result = response.json()
            
            # Extract text from response (this may vary based on API)
            if 'response' in result:
                return result['response']
            elif 'text' in result:
                return result['text']
            elif 'choices' in result and len(result['choices']) > 0:
                # OpenAI-style response
                return result['choices'][0].get('text', '')
            else:
                print(f"Unexpected LLM response format: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"LLM API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response: {e}")
            return None
        except Exception as e:
            print(f"LLM API call error: {e}")
            return None
    
    def _extract_translation(self, response: str) -> str:
        """Extract clean translation from LLM response"""
        if not response:
            return ""
        
        # Clean up the response
        translation = response.strip()
        
        # Remove common LLM artifacts
        lines = translation.split('\n')
        
        # Take the first non-empty line that looks like a translation
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('//') and not line.startswith('Here is'):
                # Remove quotes if present
                if line.startswith('"') and line.endswith('"'):
                    line = line[1:-1]
                elif line.startswith("'") and line.endswith("'"):
                    line = line[1:-1]
                
                # Skip common prefixes
                if line.startswith('Translation:'):
                    line = line[12:].strip()
                
                if line:  # Make sure we have content
                    return line
        
        # If no good line found, return the first line or the whole response
        if lines:
            first_line = lines[0].strip()
            if first_line:
                return first_line
        
        return translation
    
    def translate_batch_optimized(self, texts: Dict[str, str], target_language: str, source_language: str = 'en') -> Dict[str, str]:
        """
        Optimized batch translation for LLM
        
        Args:
            texts: Dictionary of key-value pairs, keys are identifiers, values are texts to translate
            target_language: Target language code
            source_language: Source language code
            
        Returns:
            Dict[str, str]: Dictionary of translated key-value pairs
        """
        if not texts:
            return {}
        
        # Get language names
        source_lang_name = self.language_names.get(source_language.lower(), source_language)
        target_lang_name = self.language_names.get(target_language.lower(), target_language)
        
        # Create batch translation prompt
        prompt = self._create_batch_prompt(texts, source_lang_name, target_lang_name)
        
        try:
            print(f"Batch translating {len(texts)} texts to {target_language} using LLM...")
            
            # Call LLM API
            response = self._call_llm_api(prompt)
            
            if response:
                # Parse batch response
                result = self._parse_batch_response(response, texts)
                
                translated_count = len([key for key in result.keys() if result[key] != texts[key]])
                print(f"Successfully translated {translated_count}/{len(texts)} texts")
                
                return result
            else:
                print("LLM batch translation failed, falling back to individual translations...")
                return self._fallback_individual_translation(texts, target_language, source_language)
                
        except Exception as e:
            print(f"LLM batch translation error: {e}")
            print("Falling back to individual translations...")
            return self._fallback_individual_translation(texts, target_language, source_language)
    
    def _create_batch_prompt(self, texts: Dict[str, str], source_lang: str, target_lang: str) -> str:
        """Create batch translation prompt for LLM"""
        prompt = f"""Please translate the following texts from {source_lang} to {target_lang}.
Return the translations in the same order, one per line, without any additional text or explanations.

Texts to translate:
"""
        
        for i, (key, text) in enumerate(texts.items(), 1):
            prompt += f"{i}. {text}\n"
        
        prompt += f"\nTranslations in {target_lang}:\n"
        
        return prompt
    
    def _parse_batch_response(self, response: str, original_texts: Dict[str, str]) -> Dict[str, str]:
        """Parse batch translation response from LLM"""
        result = {}
        keys = list(original_texts.keys())
        
        # Split response into lines
        lines = response.strip().split('\n')
        
        # Filter and clean lines
        translations = []
        for line in lines:
            line = line.strip()
            if line:
                # Remove numbering if present (e.g., "1. Translation")
                if line[0].isdigit() and '. ' in line:
                    line = line.split('. ', 1)[1]
                
                # Remove quotes
                if line.startswith('"') and line.endswith('"'):
                    line = line[1:-1]
                elif line.startswith("'") and line.endswith("'"):
                    line = line[1:-1]
                
                translations.append(line)
        
        # Match translations to keys
        for i, key in enumerate(keys):
            if i < len(translations):
                result[key] = translations[i]
                print(f"✓ {key}: {original_texts[key][:30]}... -> {translations[i][:30]}...")
            else:
                result[key] = original_texts[key]  # Keep original if no translation
                print(f"✗ {key}: No translation found")
        
        return result
    
    def _is_ollama_api(self) -> bool:
        """Check if this is an Ollama API endpoint"""
        return "11434" in self.api_url or "/api/generate" in self.api_url
    
    def _get_available_models(self) -> List[str]:
        """Get list of available models from Ollama"""
        try:
            tags_url = self.api_url.replace('/api/generate', '/api/tags')
            response = requests.get(tags_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                models = []
                for model in data.get('models', []):
                    models.append(model.get('name', ''))
                return [m for m in models if m]
            else:
                return []
                
        except Exception as e:
            print(f"Failed to get available models: {e}")
            return []
    
    def _fallback_individual_translation(self, texts: Dict[str, str], target_language: str, source_language: str) -> Dict[str, str]:
        """Fallback method for individual translation"""
        result = {}
        total = len(texts)
        
        for i, (key, text) in enumerate(texts.items(), 1):
            print(f"Translating {i}/{total}: {key}")
            
            translated = self.translate(text, target_language, source_language)
            if translated:
                result[key] = translated
            else:
                print(f"Failed to translate: {key} = {text}")
                result[key] = text  # Keep original text
            
            # Add delay to avoid overwhelming the LLM
            if i < total:
                import time
                time.sleep(self.rate_limit_delay)
        
        return result
