from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


from src.utils.config import load_config
from src.models.train import train_model, save_training_outputs


def main():
    config = load_config()

    model, metrics = train_model(config)

    save_training_outputs(
        model=model,
        metrics=metrics,
        config=config,
    )

    print("Model training completed.")
    print(f"Model type: {metrics['model_type']}")
    print(f"Train MAE: {metrics['train_mae']:.2f}")
    print(f"Test MAE: {metrics['test_mae']:.2f}")
    print(f"Train RMSE: {metrics['train_rmse']:.2f}")
    print(f"Test RMSE: {metrics['test_rmse']:.2f}")
    print(f"Train R2: {metrics['train_r2']:.3f}")
    print(f"Test R2: {metrics['test_r2']:.3f}")
    print("Model saved to: models/house_price_stacking_pipeline.pkl")
    print("Metrics saved to: outputs/metrics/training_metrics.json")


if __name__ == "__main__":
    main()