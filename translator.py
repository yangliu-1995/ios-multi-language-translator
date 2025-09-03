#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translation API module - Compatibility layer
This module provides backward compatibility for existing code while 
supporting the new modular translator structure.
"""

# Import all translators from the new modular structure
from translators import (
    TranslatorBase,
    DeepLTranslator, 
    MockTranslator,
    LLMTranslator,
    create_translator
)

# Re-export for backward compatibility
__all__ = [
    'TranslatorBase',
    'DeepLTranslator',
    'MockTranslator', 
    'LLMTranslator',
    'create_translator'
]