#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS Localizable.strings parser module
Parse key-value pairs from iOS Localizable.strings files
"""

import re
import os
from typing import Dict, Optional


class StringsParser:
    """Class for parsing and processing iOS Localizable.strings files"""
    
    def __init__(self):
        # Regular expression for matching "key" = "value"; format
        self.key_value_pattern = re.compile(r'"([^"]*?)"\s*=\s*"([^"]*?)"\s*;')
        # For matching comments
        self.comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
        self.line_comment_pattern = re.compile(r'//.*?$', re.MULTILINE)
    
    def parse_strings_file(self, file_path: str) -> Dict[str, str]:
        """
        Parse Localizable.strings file
        
        Args:
            file_path: Path to the .strings file
            
        Returns:
            Dict[str, str]: Dictionary of key-value pairs
        """
        if not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            # Try using utf-16 encoding (some .strings files use this encoding)
            try:
                with open(file_path, 'r', encoding='utf-16') as file:
                    content = file.read()
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                return {}
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return {}
        
        return self.parse_strings_content(content)
    
    def parse_strings_content(self, content: str) -> Dict[str, str]:
        """
        Parse strings file content
        
        Args:
            content: File content string
            
        Returns:
            Dict[str, str]: Dictionary of key-value pairs
        """
        # Remove comments
        content = self.comment_pattern.sub('', content)
        content = self.line_comment_pattern.sub('', content)
        
        # Find all key-value pairs
        matches = self.key_value_pattern.findall(content)
        
        result = {}
        for key, value in matches:
            # Handle escape characters
            key = self._unescape_string(key)
            value = self._unescape_string(value)
            result[key] = value
        
        return result
    
    def write_strings_file(self, strings_dict: Dict[str, str], file_path: str, preserve_order: bool = True) -> bool:
        """
        Write key-value pairs dictionary to .strings file
        
        Args:
            strings_dict: Dictionary of key-value pairs
            file_path: Output file path
            preserve_order: Whether to preserve the order of keys (default: True)
            
        Returns:
            bool: Whether write was successful
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('/* Localizable.strings */\n\n')
                
                # Choose whether to preserve order or sort alphabetically
                items = strings_dict.items() if preserve_order else sorted(strings_dict.items())
                
                for key, value in items:
                    escaped_key = self._escape_string(key)
                    escaped_value = self._escape_string(value)
                    file.write(f'"{escaped_key}" = "{escaped_value}";\n')
            
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return False
    
    def update_strings_file(self, file_path: str, new_strings: Dict[str, str], reference_order: Dict[str, str] = None) -> bool:
        """
        Update existing .strings file, adding new key-value pairs while preserving order
        
        Args:
            file_path: Path to .strings file
            new_strings: New key-value pairs to add
            reference_order: Reference dictionary to maintain key order (usually English strings)
            
        Returns:
            bool: Whether update was successful
        """
        # Read existing strings
        existing_strings = self.parse_strings_file(file_path)
        
        # Merge new strings
        existing_strings.update(new_strings)
        
        # If we have a reference order (from English file), use it to maintain order
        if reference_order:
            ordered_strings = {}
            
            # First, add all keys from reference in their original order
            for key in reference_order.keys():
                if key in existing_strings:
                    ordered_strings[key] = existing_strings[key]
            
            # Then add any remaining keys that weren't in the reference
            for key, value in existing_strings.items():
                if key not in ordered_strings:
                    ordered_strings[key] = value
            
            existing_strings = ordered_strings
        
        # Write back to file
        return self.write_strings_file(existing_strings, file_path)
    
    def _escape_string(self, text: str) -> str:
        """Escape special characters in string"""
        text = text.replace('\\', '\\\\')  # Backslash
        text = text.replace('"', '\\"')    # Double quote
        text = text.replace('\n', '\\n')   # Newline
        text = text.replace('\r', '\\r')   # Carriage return
        text = text.replace('\t', '\\t')   # Tab
        return text
    
    def _unescape_string(self, text: str) -> str:
        """Unescape special characters in string"""
        text = text.replace('\\"', '"')    # Double quote
        text = text.replace('\\n', '\n')   # Newline
        text = text.replace('\\r', '\r')   # Carriage return
        text = text.replace('\\t', '\t')   # Tab
        text = text.replace('\\\\', '\\')  # Backslash (process last)
        return text


def get_language_from_lproj(lproj_path: str) -> Optional[str]:
    """
    Extract language code from .lproj folder path
    
    Args:
        lproj_path: Path to .lproj folder
        
    Returns:
        Optional[str]: Language code, None if extraction fails
    """
    folder_name = os.path.basename(lproj_path)
    if folder_name.endswith('.lproj'):
        return folder_name[:-6]  # Remove '.lproj' suffix
    return None


# Language code mapping for translation API
LANGUAGE_CODE_MAPPING = {
    'en': 'en',
    'zh-Hans': 'zh',
    'zh-Hant': 'zh-TW',
    'ja': 'ja',
    'ko': 'ko',
    'fr': 'fr',
    'de': 'de',
    'es': 'es',
    'it': 'it',
    'pt': 'pt',
    'ru': 'ru',
    'ar': 'ar',
    'hi': 'hi',
    'th': 'th',
    'vi': 'vi',
    'tr': 'tr',
    'pl': 'pl',
    'nl': 'nl',
    'sv': 'sv',
    'da': 'da',
    'fi': 'fi',
    'no': 'no',
    'pt-BR': 'pt-BR',
    'es-MX': 'es',
}


def get_deepl_language_code(ios_language: str) -> str:
    """
    Convert iOS language code to DeepL API supported language code
    
    Args:
        ios_language: iOS language code
        
    Returns:
        str: DeepL language code
    """
    return LANGUAGE_CODE_MAPPING.get(ios_language, ios_language)