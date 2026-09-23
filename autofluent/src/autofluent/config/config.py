from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[4]
CONFIG_DIR = PROJECT_ROOT / "config"

case_file = "case.yaml"
environment_file = "environment.yaml"

data_disregarded = ("", None, 0)


def load_raw_yaml(filename):
    with open(CONFIG_DIR / filename, "r") as file:
        return yaml.safe_load(file) or {}


def cleanup_config(data):
    if isinstance(data, dict):
        cleaned = {}

        for key, value in data.items():
            value = cleanup_config(value)

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


def load_config(environment):
    case_config = load_raw_yaml(case_file)
    environment_config = load_raw_yaml(environment_file)

    # Support the current environment.yaml structure while the
    # configuration architecture is being finalized.
    environment_config = environment_config.get("type", {}).get(environment, {})

    config = {
        **case_config,
        "environment": {
            "type": environment,
            **environment_config,
        },
    }

    return cleanup_config(config)
