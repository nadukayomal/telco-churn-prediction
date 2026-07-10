import configparser
import os
from unittest import result
import warnings
import yaml
import logging

from datetime import datetime
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s -%(levelname)s -%(message)s')
logger = logging.getLogger(__name__)
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')


def load_config():
    with open(CONFIG_FILE, 'r') as f:
        try :
            config = yaml.safe_load(f)
            if config is None:
                return {}
            return config
        except Exception as e:
            logger.error(f"Error loading configurations {f}")
            return{}

def get_path():
    config = load_config()
    return config.get('paths', {})

def get_columns():
    config = load_config()
    return config.get('columns', {})

def get_preprocessing():
    config = load_config()
    return config.get('preprocessing', {})

def get_modeling():
    config = load_config()
    return config.get('modeling', {})

def get_training():
    config = load_config()
    return config.get('training', {})

def get_evaluation():
    config = load_config()
    return config.get('evaluation', {})

def get_logging():
    config = load_config()
    return config.get('logging', {})

def get_experiment_tracking():
    config = load_config()
    return config.get('experiment_tracking', {})

def get_reproducibility():
    config = load_config()
    return config.get('reproducibility', {})
