import json
import pandas as pd

from src.utils.config import get_project_root


REQUIRED_COLUMNS = [
    "district",
    "location",
    "rooms",
    "area",
    "floor",
    "total_floors",
    "price",
]


def load_clean_data(config: dict) -> pd.DataFrame:
    project_root = get_project_root()
    clean_path = project_root / config["paths"]["clean_data"]

    if not clean_path.exists():
        raise FileNotFoundError(f"Clean data file not found: {clean_path}")

    data = pd.read_csv(clean_path)

    return data


def validate_columns(data: pd.DataFrame) -> None:
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def add_area_features(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    data["area_per_room"] = data["area"] / data["rooms"]

    return data


def build_features(config: dict):
    data = load_clean_data(config)

    validate_columns(data)

    original_shape = data.shape

    data = add_area_features(data)

    data = data.reset_index(drop=True)

    summary = {
        "original_rows": int(original_shape[0]),
        "original_columns": int(original_shape[1]),
        "processed_rows": int(data.shape[0]),
        "processed_columns": int(data.shape[1]),
        "added_features": [
            "area_per_room",
        ],
    }

    return data, summary


def save_feature_outputs(
    model_data: pd.DataFrame,
    summary: dict,
    config: dict,
) -> None:
    project_root = get_project_root()

    processed_path = project_root / config["paths"]["processed_data"]
    summary_path = project_root / config["paths"]["feature_summary"]

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    model_data.to_csv(processed_path, index=False)

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)