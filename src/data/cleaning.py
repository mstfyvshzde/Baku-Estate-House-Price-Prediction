import json
import unicodedata

import pandas as pd

from src.utils.config import get_project_root


TEXT_COLUMNS = ["district", "location"]
NUMERIC_COLUMNS = ["rooms", "area", "floor", "total_floors", "price"]

#
DISTRICT_MAP = {
    "abseron": "Abşeron",

    "bineqedi": "Binəqədi",

    "xetai": "Xətai",

    "xezer": "Xəzər",

    "qaradag": "Qaradağ",

    "nerimanov": "Nərimanov",
 
    "nesimi": "Nəsimi",

    "nizami": "Nizami",

    "sabuncu": "Sabunçu",

    "sebail": "Səbail",

    "suraxani": "Suraxanı",

   "yasamal": "Yasamal"
}
#
LOCATION_MAP = {
    "ceyranbatan": "Ceyranbatan",
    "masazir": "Masazır",
    "mehdiabad": "Mehdiabad",
    "saray": "Saray",

    "9cu mikrorayon": "9-cu Mikrorayon",
    "8ci mikrorayon": "8-ci Mikrorayon",
    "28may q": "28 May",
    "6ci mikrorayon": "6-cı Mikrorayon",
    "7ci mikrorayon": "7-ci Mikrorayon",
    "bineqedi": "Binəqədi",
    "bileceri": "Biləcəri",

    "ehmedli": "Əhmədli",
    "kohne gunesli": "Köhnə Günəşli",
    "ag seher": "Ağ Şəhər",
    "saray": "Saray",

    "buzovna": "Buzovna",
    "bine": "Binə",
    "merdekan": "Mərdəkan",

    "lokbatan": "Lökbatan",
    "musfiqabad": "Müşfiqabad",
    "sahil": "Sahil",

    "boyuksor": "Böyükşor",

    "1ci mikrorayon": "1-ci Mikrorayon",
    "2ci mikrorayon": "2-ci Mikrorayon",
    "4cu mikrorayon": "4-cü Mikrorayon",
    "kubinka": "Kubinka",
    "5ci mikrorayon": "5-ci Mikrorayon",
    "3cu mikrorayon": "3-cü Mikrorayon",

    "8ci kilometr": "8-ci Kilometr",

    "bakixanov": "Bakıxanov",
    "ramana": "Ramana",
    "zabrat": "Zabrat",
    "savalan": "Savalan",
    "sea breeze": "Sea Breeze",
    "sabuncu": "Sabunçu",

    "badamdar": "Badamdar",
    "sixov": "Şıxov",
    "20ci sahe": "20-ci Sahə",
    "bibiheybet": "Bibiheybət",
    "bayil": "Bayıl",

    "hovsan": "Hövsan",
    "gunesli": "Günəşli",
    "qaracuxur": "Qaraçuxur",
    "zig": "Zığ",

    "yasamal": "Yasamal"  
}

def normalize_text(value):
    if pd.isna(value):
        return pd.NA

    text = str(value).strip().casefold()
    text = unicodedata.normalize("NFKC", text)
    text = " ".join(text.split())

    if text == "":
        return pd.NA

    return text


def load_raw_data(config: dict) -> pd.DataFrame:
    project_root = get_project_root()
    raw_path = project_root / config["paths"]["raw_data"]
    columns = config["schema"]["columns"]

    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data file not found: {raw_path}")

    data = pd.read_csv(
        raw_path,
        header=None,
        names=columns,
        sep=None,
        engine="python",
        encoding="utf-8-sig",
        on_bad_lines="skip",
    )

    return data


def clean_text_columns(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    for col in TEXT_COLUMNS:
        data[col] = data[col].apply(normalize_text)

    return data

def standardize_categories(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    data["district"] = data["district"].replace(DISTRICT_MAP)
    data["location"] = data["location"].replace(LOCATION_MAP)

    return data


def clean_numeric_columns(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


def build_removal_reasons(data: pd.DataFrame, config: dict) -> pd.Series:
    validation = config["validation"]

    reasons = pd.Series("", index=data.index, dtype="object")

    def add_reason(mask, reason):
        reasons.loc[mask] = reasons.loc[mask] + reason + "; "

    # text validation
    add_reason(data["district"].isna(), "missing_district")
    add_reason(data["location"].isna(), "missing_location")

    # numeric missing validation
    for col in NUMERIC_COLUMNS:
        add_reason(data[col].isna(), f"missing_or_invalid_{col}")

    # range validation
    add_reason(
        (data["rooms"] < validation["rooms"]["min"])
        | (data["rooms"] > validation["rooms"]["max"]),
        "invalid_rooms_range",
    )

    add_reason(
        (data["area"] < validation["area"]["min"])
        | (data["area"] > validation["area"]["max"]),
        "invalid_area_range",
    )

    add_reason(
        data["floor"] < validation["floor"]["min"],
        "invalid_floor_range",
    )

    add_reason(
        (data["total_floors"] < validation["total_floors"]["min"])
        | (data["total_floors"] > validation["total_floors"]["max"]),
        "invalid_total_floors_range",
    )

    add_reason(
        data["floor"] > data["total_floors"],
        "floor_greater_than_total_floors",
    )

    add_reason(
        (data["price"] < validation["price"]["min"])
        | (data["price"] > validation["price"]["max"]),
        "invalid_price_range",
    )

    # duplicate validation
    duplicate_mask = data.duplicated(keep="first")
    add_reason(duplicate_mask, "duplicate_row")

    reasons = reasons.str.strip("; ")

    return reasons

def clean_dataset(config: dict):
    data = load_raw_data(config)

    original_shape = data.shape

    data = clean_text_columns(data)
    data = standardize_categories(data)
    data = clean_numeric_columns(data)

    removal_reasons = build_removal_reasons(data, config)

    valid_mask = removal_reasons == ""

    clean_data = data.loc[valid_mask].copy()
    removed_rows = data.loc[~valid_mask].copy()

    removed_rows["removal_reason"] = removal_reasons.loc[~valid_mask]

    clean_data = clean_data.reset_index(drop=True)
    removed_rows = removed_rows.reset_index(drop=True)

    
    summary = {
        "original_rows": int(original_shape[0]),
        "original_columns": int(original_shape[1]),
        "clean_rows": int(clean_data.shape[0]),
        "removed_rows": int(removed_rows.shape[0]),
        "clean_columns": int(clean_data.shape[1]),
    }

    return clean_data, removed_rows, summary


def save_cleaning_outputs(
    clean_data: pd.DataFrame,
    removed_rows: pd.DataFrame,
    summary: dict,
    config: dict,
) -> None:
    project_root = get_project_root()

    clean_path = project_root / config["paths"]["clean_data"]
    removed_path = project_root / config["paths"]["removed_rows"]
    summary_path = project_root / config["paths"]["cleaning_summary"]

    clean_path.parent.mkdir(parents=True, exist_ok=True)
    removed_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    clean_data.to_csv(clean_path, index=False)
    removed_rows.to_csv(removed_path, index=False)

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)