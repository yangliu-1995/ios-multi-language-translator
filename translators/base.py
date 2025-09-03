#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base translator class
"""

import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class TranslatorBase(ABC):
    """Base class for translators"""
    
    def __init__(self):
        self.rate_limit_delay = 1.0  # seconds, API call interval
    
    @abstractmethod
    def translate(self, text: str, target_language: str, source_language: str = 'en') -> Optional[str]:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code, defaults to English
            
        Returns:
            Optional[str]: Translated text, None if translation fails
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes
        
        Returns:
            List[str]: List of supported language codes
        """
        pass
    
    def translate_batch(self, texts: Dict[str, str], target_language: str, source_language: str = 'en') -> Dict[str, str]:
        """
        Translate multiple texts in batch
        
        Args:
            texts: Dictionary of key-value pairs, keys are identifiers, values are texts to translate
            target_language: Target language code
            source_language: Source language code
            
        Returns:
            Dict[str, str]: Dictionary of translated key-value pairs
        """
        # Check if this translator supports optimized batch translation
        if hasattr(self, 'translate_batch_optimized'):
            return self.translate_batch_optimized(texts, target_language, source_language)
        
        # Default individual translation approach
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
