
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils.config import load_config
from src.data.cleaning import clean_dataset, save_cleaning_outputs

def main():
    config = load_config()

    clean_data, removed_rows, summary = clean_dataset(config)

    save_cleaning_outputs(
        clean_data=clean_data,
        removed_rows=removed_rows,
        summary=summary,
        config=config
    )

    print("Data cleaning completed.")
    print(f"Original rows: {summary['original_rows']}")
    print(f"Clean rows: {summary['clean_rows']}")
    print(f"Removed rows: {summary['removed_rows']}")
    print("Clean data saved to: data/interim/clean_data.csv")
    print("Removed rows saved to: outputs/reports/removed_rows.csv")
    print("Summary saved to: outputs/reports/cleaning_summary.json")

if __name__ == '__main__':
    main()


# baku-estate klasorune giridkten sonra terminalde bunu yaz: python3 scripts/clean_data.py