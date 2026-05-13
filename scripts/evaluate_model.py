from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


from src.utils.config import load_config
from src.evaluation.metrics import evaluate_model, save_evaluation_outputs


def main():
    config = load_config()

    metrics, reports = evaluate_model(config)

    save_evaluation_outputs(
        metrics=metrics,
        reports=reports,
        config=config,
    )

    print("Model evaluation completed.")
    print(f"Test rows: {metrics['test_rows']}")
    print(f"Test MAE: {metrics['test_mae']:.2f}")
    print(f"Test RMSE: {metrics['test_rmse']:.2f}")
    print(f"Test R2: {metrics['test_r2']:.3f}")
    print(f"Average percentage error: {metrics['avg_percentage_error']:.2f}%")
    print(f"Max absolute error: {metrics['max_absolute_error']:.2f}")
    print("Reports saved:")
    print("- outputs/metrics/evaluation_metrics.json")
    print("- outputs/reports/error_analysis.csv")
    print("- outputs/reports/error_by_district.csv")
    print("- outputs/reports/error_by_location.csv")
    print("- outputs/reports/error_by_rooms.csv")

    print("\nBiggest prediction errors:")
    print(
        reports["error_data"][
            [
                "district",
                "location",
                "rooms",
                "area",
                "actual_price",
                "predicted_price",
                "absolute_error",
                "percentage_error",
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()