import json 
import joblib 
import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from src.utils.config import get_project_root

target_column = 'price'

def load_model(config: dict):
    project_root = get_project_root()
    model_path = project_root / config['paths']['model_path']

    if not model_path.exists():
        raise FileNotFoundError(f'Model file not found: {model_path}')
    
    model = joblib.load(model_path)

    return model



def load_processed_data(config: dict) -> pd.DataFrame:
    project_root = get_project_root()
    data_path = project_root / config["paths"]["processed_data"]

    if not data_path.exists():
        raise FileNotFoundError(f'Processed data file not found: {data_path}')
    
    data = pd.read_csv(data_path)

    return data



def split_features_target(data: pd.DataFrame):
    if target_column not in data.columns:
        raise ValueError(f'Target column not found: {target_column}')
    
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    return X, y

def create_error_analysis(X_test, y_test, predictions) -> pd.DataFrame:
    error_data = X_test.copy()

    error_data['actual_price'] = y_test.values
    error_data['predicted_price'] = predictions.round(2)
    error_data['absolute_error'] = abs(
        error_data['actual_price'] - error_data['predicted_price']
    )

    error_data['percentage_error'] = (
        error_data['absolute_error'] / error_data['actual_price'] * 100
    ).round(2)

    error_data = error_data.sort_values(
        by='absolute_error',
        ascending=False
    )

    return error_data

def create_group_error_report(
    error_data: pd.DataFrame,
    group_column: str
) -> pd.DataFrame:
    report = (
        error_data
        .groupby(group_column)
        .agg(
            sample_count=("absolute_error", "count"),
            avg_actual_price=("actual_price", "mean"),
            avg_predicted_price=("predicted_price", "mean"),
            avg_absolute_error=("absolute_error", "mean"),
            median_absolute_error=("absolute_error", "median"),
            avg_percentage_error=("percentage_error", "mean")
        )
        .round(2)
        .sort_values(by='avg_absolute_error', ascending=False)
        .reset_index()
    )

    return report

def evaluate_model(config: dict):
    data = load_processed_data(config)
    model = load_model(config)

    X, y = split_features_target(data)

    test_size = config['model']['test_size']
    random_state = config['model']['random_state']

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    predictions = model.predict(X_test)


    error_data = create_error_analysis(
        X_test=X_test,
        y_test=y_test,
        predictions=predictions
    )

    district_report = create_group_error_report(error_data, 'district')
    location_report = create_group_error_report(error_data, 'location')
    rooms_report = create_group_error_report(error_data, 'rooms')

    metrics = {
        "test_rows": int(X_test.shape[0]),
        "test_mae": float(mean_absolute_error(y_test, predictions)),
        "test_rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
        "test_r2": float(r2_score(y_test, predictions)),
        "avg_percentage_error": float(error_data["percentage_error"].mean()),
        "max_absolute_error": float(error_data["absolute_error"].max()),
        "min_absolute_error": float(error_data["absolute_error"].min())
    }

    reports = {
        "error_data": error_data,
        "district_report": district_report,
        "location_report": location_report,
        "rooms_report": rooms_report
    }

    return metrics, reports



def save_evaluation_outputs(
    metrics: dict,
    reports: dict,
    config: dict,
) -> None:
    project_root = get_project_root()

    metrics_path = project_root / config["paths"]["evaluation_metrics"]
    error_path = project_root / config["paths"]["error_analysis"]
    district_path = project_root / config["paths"]["error_by_district"]
    location_path = project_root / config["paths"]["error_by_location"]
    rooms_path = project_root / config["paths"]["error_by_rooms"]

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    error_path.parent.mkdir(parents=True, exist_ok=True)

    with open(metrics_path, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4, ensure_ascii=False)

    reports["error_data"].to_csv(error_path, index=False)
    reports["district_report"].to_csv(district_path, index=False)
    reports["location_report"].to_csv(location_path, index=False)
    reports["rooms_report"].to_csv(rooms_path, index=False)