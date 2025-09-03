#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS Multi-language Translation Script
Main program for iOS multi-language translation
"""

import os
import sys
import argparse
import glob
from typing import Dict, List, Set, Optional

from strings_parser import StringsParser, get_language_from_lproj, get_deepl_language_code
from translator import create_translator, TranslatorBase
from code_generator import LocalizationCodeGenerator, generate_objc_header
from config_manager import get_config


class iOSTranslator:
    """iOS multi-language translator main class"""
    
    def __init__(self, root_path: str, translator: TranslatorBase):
        """
        Initialize translator
        
        Args:
            root_path: Project root directory path
            translator: Translator instance
        """
        self.root_path = os.path.abspath(root_path)
        self.translator = translator
        self.parser = StringsParser()
        self.code_generator = LocalizationCodeGenerator()
        
        # Validate path
        if not os.path.exists(self.root_path):
            raise ValueError(f"Root path does not exist: {self.root_path}")
    
    def run(self, generate_swift: bool = True, generate_objc: bool = False, 
            output_dir: str = None) -> bool:
        """
        Run translation process
        
        Args:
            generate_swift: Whether to generate Swift extension code
            generate_objc: Whether to generate Objective-C header file
            output_dir: Code output directory, defaults to root directory
            
        Returns:
            bool: Whether completed successfully
        """
        try:
            print(f"Starting iOS translation for: {self.root_path}")
            
            # 1. Read English strings
            en_strings = self._load_english_strings()
            if not en_strings:
                print("No English strings found. Exiting.")
                return False
            
            print(f"Found {len(en_strings)} English strings")
            
            # 2. Find all language directories
            language_dirs = self._find_language_directories()
            if not language_dirs:
                print("No language directories found. Exiting.")
                return False
            
            print(f"Found language directories: {language_dirs}")
            
            # 3. Process each language directory
            for lang_dir in language_dirs:
                language = get_language_from_lproj(lang_dir)
                if language and language != 'en' and language != 'base':
                    self._process_language_directory(lang_dir, language, en_strings)
            
            # 4. Generate Swift code
            if generate_swift:
                self._generate_swift_extensions(en_strings, output_dir)
            
            # 5. Generate Objective-C header file
            if generate_objc:
                self._generate_objc_header(en_strings, output_dir)
            
            print("Translation completed successfully!")
            return True
            
        except Exception as e:
            print(f"Error during translation: {e}")
            return False
    
    def _load_english_strings(self) -> Dict[str, str]:
        """Load English strings"""
        en_lproj_path = os.path.join(self.root_path, 'en.lproj')
        if not os.path.exists(en_lproj_path):
            print(f"English localization directory not found: {en_lproj_path}")
            return {}
        
        localizable_path = os.path.join(en_lproj_path, 'Localizable.strings')
        if not os.path.exists(localizable_path):
            print(f"English Localizable.strings not found: {localizable_path}")
            return {}
        
        return self.parser.parse_strings_file(localizable_path)
    
    def _find_language_directories(self) -> List[str]:
        """Find all language directories"""
        pattern = os.path.join(self.root_path, '*.lproj')
        language_dirs = glob.glob(pattern)
        
        # Exclude base.lproj
        language_dirs = [d for d in language_dirs if not d.endswith('base.lproj')]
        
        return sorted(language_dirs)
    
    def _process_language_directory(self, lang_dir: str, language: str, en_strings: Dict[str, str]) -> None:
        """
        Process single language directory
        
        Args:
            lang_dir: Language directory path
            language: Language code
            en_strings: English strings dictionary
        """
        print(f"\nProcessing language: {language}")
        
        localizable_path = os.path.join(lang_dir, 'Localizable.strings')
        
        # Read existing localized strings
        existing_strings = self.parser.parse_strings_file(localizable_path)
        print(f"Found {len(existing_strings)} existing strings for {language}")
        
        # Find missing keys
        missing_keys = set(en_strings.keys()) - set(existing_strings.keys())
        
        if not missing_keys:
            print(f"No missing strings for {language}")
            return
        
        print(f"Found {len(missing_keys)} missing strings for {language}")
        
        # Prepare translation
        texts_to_translate = {key: en_strings[key] for key in missing_keys}
        
        # Get target language code
        target_language = get_deepl_language_code(language)
        
        print(f"Translating to {target_language}...")
        
        # Translate missing texts
        translated_texts = self.translator.translate_batch(
            texts_to_translate, 
            target_language, 
            'en'
        )
        
        if translated_texts:
            print(f"Successfully translated {len(translated_texts)} strings")
            
            # Update strings file, preserving the order of English strings
            success = self.parser.update_strings_file(localizable_path, translated_texts, en_strings)
            if success:
                print(f"Updated {localizable_path}")
            else:
                print(f"Failed to update {localizable_path}")
        else:
            print(f"No translations were successful for {language}")
    
    def _generate_swift_extensions(self, en_strings: Dict[str, str], output_dir: str = None) -> None:
        """Generate Swift extension code"""
        if not output_dir:
            output_dir = self.root_path
        
        output_path = os.path.join(output_dir, 'LocalizedStrings.swift')
        
        print(f"\nGenerating Swift extensions...")
        self.code_generator.generate_swift_extensions(en_strings, output_path)
    
    def _generate_objc_header(self, en_strings: Dict[str, str], output_dir: str = None) -> None:
        """Generate Objective-C header file"""
        if not output_dir:
            output_dir = self.root_path
        
        output_path = os.path.join(output_dir, 'LocalizedStrings.h')
        
        print(f"\nGenerating Objective-C header...")
        generate_objc_header(en_strings, output_path)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='iOS Multi-language Translation Script')
    parser.add_argument('root_path', nargs='?', help='Root directory containing .lproj folders')
    # Load configuration
    config = get_config()
    default_auth_key = config.get_deepl_key() or 'your-deepl-api-key-here'
    
    parser.add_argument('--auth-key', default=default_auth_key,
                        help='DeepL API authentication key')
    parser.add_argument('--translator', choices=['deepl', 'mock', 'llm'], 
                        default=config.get('default_translator', 'deepl'),
                        help='Translator type to use')
    parser.add_argument('--llm-url', default=config.get('llm_api_url', 'http://127.0.0.1:11434/api/generate'),
                        help='LLM API URL for LLM translator')
    parser.add_argument('--llm-model', default=config.get('llm_model', 'mistral:latest'),
                        help='LLM model name')
    parser.add_argument('--no-swift', action='store_true',
                        help='Skip Swift extension generation')
    parser.add_argument('--generate-objc', action='store_true',
                        help='Generate Objective-C header file')
    parser.add_argument('--output-dir', default=None,
                        help='Output directory for generated code (default: same as root_path)')
    parser.add_argument('--check-usage', action='store_true',
                        help='Check DeepL API usage and exit')
    parser.add_argument('--show-config', action='store_true',
                        help='Show configuration status and exit')
    
    args = parser.parse_args()
    
    try:
        # Show configuration if requested
        if args.show_config:
            config.print_config_info()
            return
        
        # Check if root_path is provided
        if not args.root_path:
            print("Error: root_path is required unless using --show-config")
            parser.print_help()
            return
        
        # Validate configuration
        if not config.validate_config():
            return
        
        # Create translator
        if args.translator == 'deepl':
            translator = create_translator('deepl', auth_key=args.auth_key)
            
            # Check API usage
            if args.check_usage:
                from translator import DeepLTranslator
                if isinstance(translator, DeepLTranslator):
                    usage = translator.check_api_usage()
                    if usage:
                        print(f"API Usage: {usage}")
                    else:
                        print("Failed to check API usage")
                return
        elif args.translator == 'llm':
            translator = create_translator('llm', 
                                         api_url=args.llm_url, 
                                         model=args.llm_model)
        else:
            translator = create_translator('mock')
        
        # Create translator instance
        ios_translator = iOSTranslator(args.root_path, translator)
        
        # Set default output directory to root_path if not specified
        output_dir = args.output_dir if args.output_dir else args.root_path
        
        # Run translation
        success = ios_translator.run(
            generate_swift=not args.no_swift,
            generate_objc=args.generate_objc,
            output_dir=output_dir
        )
        
        if success:
            print("\n✅ Translation completed successfully!")
        else:
            print("\n❌ Translation failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()