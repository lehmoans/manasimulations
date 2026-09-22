# src/fluent_automation/config/loader.py

"""
loads and cleans config data, removing unset values
    clean_config = load_config(environment, case_file = "case.yaml", environment_str= "mock")
"""

from pathlib import Path
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"

data_disregarded = ("", None, 0)

def load_raw_yaml(filename):
    with open(CONFIG_DIR / filename, "r") as file:
        return yaml.safe_load(file) or {}


def cleanup_config(data):
    if isinstance(data, dict):
        cleaned = {}

        for key, value in data.items():
            value = cleanup_config(value)

            # Remove empty configuration values
            if value not in data_disregarded:
                cleaned[key] = value

        return cleaned

    if isinstance(data, list):
        return [
            cleanup_config(value)
            for value in data
            if value not in data_disregarded
        ]

    return data


def load_config(environment, case_file = "case.yaml", environment_str= "mock"):
    case_config = load_raw_yaml(case_file)

    if environment_str == "mock":
        environment_config = load_raw_yaml('mock.yaml')
    elif environment =="local":
        environment_config = load_raw_yaml('local.yaml')
    elif environment == "m3":
        environment_config = load_raw_yaml('m3.yaml')
    

    config = {
        **case_config,
        **environment_config
    }

    return cleanup_config(config)