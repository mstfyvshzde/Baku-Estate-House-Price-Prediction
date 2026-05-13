from pathlib import Path
import sys

import joblib
import pandas as pd


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

# Model path
MODEL_PATH = PROJECT_ROOT / "models" / "house_price_stacking_pipeline.pkl"


def make_prediction():
    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Sample input
    sample = pd.DataFrame([
        {
            "district": "Sabunçu",
            "location": "Bakıxanov",
            "rooms": 2,
            "area": 50,
            "floor": 5,
            "total_floors": 5,
        }
    ])

    # Feature engineering
    sample["area_per_room"] = sample["area"] / sample["rooms"]

    # Prediction
    prediction = model.predict(sample)[0]

    # Price range: ±10%
    min_price = prediction * 0.90
    max_price = prediction * 1.10

    # Output
    print("Input:")
    print(sample)

    print("\nPredicted price range:")
    print(f"{round(min_price)} - {round(max_price)} AZN")


if __name__ == "__main__":
    make_prediction()