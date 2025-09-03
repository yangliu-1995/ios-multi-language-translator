#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management for iOS Translator
Supports multiple configuration sources with priority order
"""

import os
import sys
from typing import Dict, Any, Optional


class ConfigManager:
    """Configuration manager with multiple source support"""
    
    def __init__(self):
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from multiple sources (priority order)"""
        # 1. Default configuration
        self._load_defaults()
        
        # 2. Configuration file
        self._load_config_file()
        
        # 3. Environment variables
        self._load_env_variables()
        
        # 4. .env file
        self._load_env_file()
    
    def _load_defaults(self):
        """Load default configuration"""
        self.config = {
            'deepl_api_key': 'your-deepl-api-key-here',
            'llm_api_url': 'http://127.0.0.1:11434/api/generate',
            'llm_model': 'mistral:latest',
            'llm_timeout': 60,
            'default_translator': 'deepl',
            'rate_limit_delay': 1.0,
            'preserve_order': True,
            'generate_swift': True,
            'generate_objc': False,
            'output_dir': None  # Will default to root_path
        }
    
    def _load_config_file(self):
        """Load configuration from config.py file"""
        try:
            # Try to import config.py
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import config
            
            # Update configuration with values from config.py
            if hasattr(config, 'DEEPL_API_KEY'):
                self.config['deepl_api_key'] = config.DEEPL_API_KEY
            
            if hasattr(config, 'LLM_CONFIG'):
                llm_config = config.LLM_CONFIG
                self.config['llm_api_url'] = llm_config.get('api_url', self.config['llm_api_url'])
                self.config['llm_model'] = llm_config.get('model', self.config['llm_model'])
                self.config['llm_timeout'] = llm_config.get('timeout', self.config['llm_timeout'])
            
            if hasattr(config, 'TRANSLATION_CONFIG'):
                trans_config = config.TRANSLATION_CONFIG
                self.config['default_translator'] = trans_config.get('default_translator', self.config['default_translator'])
                self.config['rate_limit_delay'] = trans_config.get('rate_limit_delay', self.config['rate_limit_delay'])
                self.config['preserve_order'] = trans_config.get('preserve_order', self.config['preserve_order'])
            
            if hasattr(config, 'CODE_GENERATION'):
                code_config = config.CODE_GENERATION
                self.config['generate_swift'] = code_config.get('generate_swift', self.config['generate_swift'])
                self.config['generate_objc'] = code_config.get('generate_objc', self.config['generate_objc'])
                self.config['output_dir'] = code_config.get('output_dir', self.config['output_dir'])
                
        except ImportError:
            # config.py doesn't exist, use defaults
            pass
        except Exception as e:
            print(f"Warning: Error loading config.py: {e}")
    
    def _load_env_variables(self):
        """Load configuration from environment variables"""
        env_mappings = {
            'DEEPL_API_KEY': 'deepl_api_key',
            'LLM_API_URL': 'llm_api_url',
            'LLM_MODEL': 'llm_model',
            'LLM_TIMEOUT': 'llm_timeout',
            'DEFAULT_TRANSLATOR': 'default_translator',
            'DEFAULT_OUTPUT_DIR': 'output_dir'
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Convert types if needed
                if config_key in ['llm_timeout']:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                elif config_key in ['rate_limit_delay']:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                elif config_key in ['preserve_order', 'generate_swift', 'generate_objc']:
                    value = value.lower() in ('true', '1', 'yes', 'on')
                
                self.config[config_key] = value
    
    def _load_env_file(self):
        """Load configuration from .env file"""
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
        
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            
                            # Map environment variable names to config keys
                            env_mappings = {
                                'DEEPL_API_KEY': 'deepl_api_key',
                                'LLM_API_URL': 'llm_api_url',
                                'LLM_MODEL': 'llm_model',
                                'DEFAULT_TRANSLATOR': 'default_translator',
                                'DEFAULT_OUTPUT_DIR': 'output_dir'
                            }
                            
                            if key in env_mappings:
                                self.config[env_mappings[key]] = value
                            elif key == 'DEFAULT_OUTPUT_DIR':
                                self.config['output_dir'] = value
                                
            except Exception as e:
                print(f"Warning: Error loading .env file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_deepl_key(self) -> Optional[str]:
        """Get DeepL API key"""
        key = self.get('deepl_api_key')
        if key == 'your-deepl-api-key-here':
            return None
        return key
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration"""
        return {
            'api_url': self.get('llm_api_url'),
            'model': self.get('llm_model'),
            'timeout': self.get('llm_timeout', 60)
        }
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        issues = []
        
        # Check DeepL key if using DeepL translator
        if self.get('default_translator') == 'deepl':
            deepl_key = self.get_deepl_key()
            if not deepl_key:
                issues.append("DeepL API key is not configured. Please set DEEPL_API_KEY or use --auth-key")
        
        if issues:
            print("Configuration issues:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        
        return True
    
    def print_config_info(self):
        """Print configuration information (without sensitive data)"""
        print("Configuration Status:")
        print("=" * 50)
        
        # Check configuration sources
        config_py_exists = os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.py'))
        env_file_exists = os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))
        
        print(f"✅ config.py: {'Found' if config_py_exists else 'Not found'}")
        print(f"✅ .env file: {'Found' if env_file_exists else 'Not found'}")
        print(f"✅ Environment variables: {len([k for k in os.environ.keys() if k.startswith(('DEEPL_', 'LLM_', 'DEFAULT_'))])} found")
        
        # Show current settings (mask sensitive data)
        print(f"\nCurrent Settings:")
        deepl_key = self.get_deepl_key()
        if deepl_key:
            masked_key = deepl_key[:8] + '*' * (len(deepl_key) - 12) + deepl_key[-4:]
            print(f"  DeepL API Key: {masked_key}")
        else:
            print(f"  DeepL API Key: Not configured")
        
        print(f"  Default Translator: {self.get('default_translator')}")
        print(f"  LLM API URL: {self.get('llm_api_url')}")
        print(f"  LLM Model: {self.get('llm_model')}")
        output_dir = self.get('output_dir')
        print(f"  Output Directory: {output_dir or 'Project root directory (default)'}")


# Global configuration instance
config_manager = ConfigManager()


def get_config() -> ConfigManager:
    """Get global configuration manager instance"""
    return config_manager
