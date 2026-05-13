from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


from src.utils.config import load_config
from src.features.build_features import build_features, save_feature_outputs


def main():
    config = load_config()

    model_data, summary = build_features(config)

    save_feature_outputs(
        model_data=model_data,
        summary=summary,
        config=config,
    )

    print("Feature engineering completed.")
    print(f"Original rows: {summary['original_rows']}")
    print(f"Processed rows: {summary['processed_rows']}")
    print(f"Original columns: {summary['original_columns']}")
    print(f"Processed columns: {summary['processed_columns']}")
    print("Added features:")

    for feature in summary["added_features"]:
        print(f"- {feature}")

    print("Model data saved to: data/processed/model_data.csv")
    print("Feature summary saved to: outputs/reports/feature_summary.json")


if __name__ == "__main__":
    main()