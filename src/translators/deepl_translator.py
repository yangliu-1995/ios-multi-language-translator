#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepL translator implementation
"""

import time
from typing import Dict, List, Optional

try:
    import deepl
except ImportError:
    print("Warning: deepl library not found. Please install it with: pip install deepl")
    deepl = None

from .base import TranslatorBase


class DeepLTranslator(TranslatorBase):
    """DeepL API translator implementation"""
    
    def __init__(self, auth_key: str):
        super().__init__()
        self.auth_key = auth_key
        self.rate_limit_delay = 1.2  # DeepL free tier has stricter limits
        
        # Check if deepl library is available
        if deepl is None:
            raise ImportError("deepl library is required. Please install it with: pip install deepl")
        
        # Initialize DeepL translator
        try:
            self.translator = deepl.Translator(auth_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize DeepL translator: {e}")
        
        # DeepL supported language code mapping (iOS -> DeepL)
        # Using lowercase keys to match the _convert_language_code method
        self.language_mapping = {
            'zh': 'ZH',
            'zh-hans': 'ZH',
            'zh-hant': 'ZH-HANT',
            'zh-tw': 'ZH-HANT',
            'ja': 'JA',
            'ko': 'KO',
            'fr': 'FR',
            'de': 'DE',
            'es': 'ES',
            'it': 'IT',
            'pt': 'PT',
            'pt-br': 'PT-BR',
            'ru': 'RU',
            'ar': 'AR',
            'hi': 'HI',
            'tr': 'TR',
            'pl': 'PL',
            'nl': 'NL',
            'sv': 'SV',
            'da': 'DA',
            'fi': 'FI',
            'no': 'NB',
        }
    
    def translate(self, text: str, target_language: str, source_language: str = 'en') -> Optional[str]:
        """Translate text using DeepL API"""
        if not text.strip():
            return text
        
        # Convert language codes
        target_lang = self._convert_language_code(target_language)
        source_lang = self._convert_language_code(source_language) if source_language != 'en' else 'EN'
        
        if not target_lang:
            print(f"Unsupported target language: {target_language}")
            return None
        
        try:
            # Use official DeepL library for translation
            result = self.translator.translate_text(
                text, 
                target_lang=target_lang,
                source_lang=source_lang
            )
            return result.text
            
        except deepl.exceptions.AuthorizationException:
            print(f"DeepL API authorization failed. Please check your API key.")
            return None
        except deepl.exceptions.QuotaExceededException:
            print(f"DeepL API quota exceeded. Please check your usage.")
            return None
        except deepl.exceptions.TooManyRequestsException:
            print(f"Too many requests to DeepL API. Please try again later.")
            return None
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of DeepL supported language codes"""
        try:
            # Get supported target languages
            target_languages = self.translator.get_target_languages()
            return [lang.code for lang in target_languages]
            
        except Exception as e:
            print(f"Failed to get supported languages: {e}")
            return list(self.language_mapping.values())
    
    def _convert_language_code(self, language_code: str) -> Optional[str]:
        """Convert common language code to DeepL API format"""
        if language_code.upper() in ['EN', 'EN-US', 'EN-GB']:
            return 'EN'
        
        return self.language_mapping.get(language_code.lower())
    
    def check_api_usage(self) -> Optional[Dict]:
        """Check API usage statistics"""
        try:
            usage = self.translator.get_usage()
            return {
                'character_count': usage.character.count,
                'character_limit': usage.character.limit,
                'character_limit_reached': usage.character.limit_reached,
                'document_count': usage.document.count if usage.document else 0,
                'document_limit': usage.document.limit if usage.document else 0,
                'document_limit_reached': usage.document.limit_reached if usage.document else False
            }
        except Exception as e:
            print(f"Failed to check API usage: {e}")
            return None
    
    def translate_batch_optimized(self, texts: Dict[str, str], target_language: str, source_language: str = 'en') -> Dict[str, str]:
        """
        Optimized batch translation using DeepL's batch translation feature
        
        Args:
            texts: Dictionary of key-value pairs, keys are identifiers, values are texts to translate
            target_language: Target language code
            source_language: Source language code
            
        Returns:
            Dict[str, str]: Dictionary of translated key-value pairs
        """
        if not texts:
            return {}
        
        # Convert language codes
        target_lang = self._convert_language_code(target_language)
        source_lang = self._convert_language_code(source_language) if source_language != 'en' else 'EN'
        
        if not target_lang:
            print(f"Unsupported target language: {target_language}")
            return {}
        
        # Prepare text list and key mapping
        keys = list(texts.keys())
        text_list = [texts[key] for key in keys]
        
        # Filter empty texts
        non_empty_indices = []
        non_empty_texts = []
        for i, text in enumerate(text_list):
            if text.strip():
                non_empty_indices.append(i)
                non_empty_texts.append(text)
        
        if not non_empty_texts:
            return texts  # If no non-empty texts, return original texts
        
        result = {}
        
        try:
            print(f"Batch translating {len(non_empty_texts)} texts to {target_language}...")
            
            # Use DeepL batch translation
            translations = self.translator.translate_text(
                non_empty_texts,
                target_lang=target_lang,
                source_lang=source_lang
            )
            
            # Process translation results
            for i, key in enumerate(keys):
                if i in non_empty_indices:
                    # Find corresponding translation result
                    translation_index = non_empty_indices.index(i)
                    if translation_index < len(translations):
                        translation = translations[translation_index]
                        result[key] = translation.text
                        print(f"✓ {key}: {texts[key][:50]}{'...' if len(texts[key]) > 50 else ''}")
                    else:
                        result[key] = texts[key]  # Keep original text
                        print(f"✗ {key}: Translation failed")
                else:
                    result[key] = texts[key]  # Keep empty text as is
            
            translated_count = len([key for key in result.keys() if result[key] != texts[key]])
            print(f"Successfully translated {translated_count}/{len(texts)} texts")
            
        except deepl.exceptions.AuthorizationException:
            print(f"DeepL API authorization failed. Please check your API key.")
            return texts  # Return original texts
        except deepl.exceptions.QuotaExceededException:
            print(f"DeepL API quota exceeded. Please check your usage.")
            return texts  # Return original texts
        except deepl.exceptions.TooManyRequestsException:
            print(f"Too many requests to DeepL API. Please try again later.")
            return texts  # Return original texts
        except Exception as e:
            print(f"Batch translation error: {e}")
            print("Falling back to individual translations...")
            # If batch translation fails, fallback to individual translation
            return self._fallback_individual_translation(texts, target_language, source_language)
        
        return result
    
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
            
            # Add delay to avoid triggering API limits
            if i < total:
                time.sleep(self.rate_limit_delay)
        
        return result
