#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock translator implementation for testing
"""

from typing import List, Optional
from .base import TranslatorBase


class MockTranslator(TranslatorBase):
    """Mock translator for testing purposes"""
    
    def __init__(self):
        super().__init__()
        self.rate_limit_delay = 0.1  # Use shorter delay for testing
    
    def translate(self, text: str, target_language: str, source_language: str = 'en') -> Optional[str]:
        """Mock translation, adds language prefix"""
        if not text.strip():
            return text
        
        return f"[{target_language.upper()}] {text}"
    
    def get_supported_languages(self) -> List[str]:
        """Return mock supported language list"""
        return ['zh', 'ja', 'ko', 'fr', 'de', 'es', 'it', 'pt', 'ru']
