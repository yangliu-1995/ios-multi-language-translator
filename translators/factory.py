#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translator factory
"""

from .base import TranslatorBase
from .deepl_translator import DeepLTranslator
from .mock_translator import MockTranslator
from .llm_translator import LLMTranslator


def create_translator(translator_type: str = 'deepl', **kwargs) -> TranslatorBase:
    """
    Create translator instance
    
    Args:
        translator_type: Translator type ('deepl', 'mock', 'llm')
        **kwargs: Translator initialization parameters
        
    Returns:
        TranslatorBase: Translator instance
    """
    translator_type = translator_type.lower()
    
    if translator_type == 'deepl':
        auth_key = kwargs.get('auth_key')
        if not auth_key:
            raise ValueError("DeepL translator requires auth_key parameter")
        return DeepLTranslator(auth_key)
    
    elif translator_type == 'mock':
        return MockTranslator()
    
    elif translator_type == 'llm':
        api_url = kwargs.get('api_url', 'http://127.0.0.1:11434/api/generate')
        model = kwargs.get('model', 'mistral:latest')
        timeout = kwargs.get('timeout', 60)
        return LLMTranslator(api_url=api_url, model=model, timeout=timeout)
    
    else:
        supported_types = ['deepl', 'mock', 'llm']
        raise ValueError(f"Unsupported translator type: {translator_type}. Supported types: {supported_types}")
