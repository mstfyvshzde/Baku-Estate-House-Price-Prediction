from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_project_root() -> Path:
    return PROJECT_ROOT



def load_config(config_path: str = "config/config.yaml") -> dict:
    full_path = PROJECT_ROOT / config_path

    if not full_path.exists():
        raise FileNotFoundError(f"Config file not found: {full_path}")

    with open(full_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError("Config file is empty.")

    return config
