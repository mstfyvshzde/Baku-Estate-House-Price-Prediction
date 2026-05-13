import json

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    StackingRegressor
)

from sklearn.impute import SimpleImputer
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.utils.config import get_project_root

target_col = 'price'

base_cat_features = [
    'district',
    'location'
]

base_num_features = [
    "rooms",
    "area",
    "floor",
    "total_floors"
]

optional_num_features = [
    "area_per_room"
]

def create_one_hot_encoder():
    try:
        return OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown='ignore', sparse=False)

def load_model_data(config: dict) -> pd.DataFrame:
    project_root = get_project_root()
    data_path = project_root / config['paths']['processed_data']

    if not data_path.exists():
        raise FileNotFoundError(f'Processed data file not found: {data_path}')

    data = pd.read_csv(data_path)

    return data

def get_feature_columns(data: pd.DataFrame):
    cat_features = [
        col for col in base_cat_features
        if col in data.columns
    ]

    num_features = [
        col for col in base_num_features + optional_num_features
        if col in data.columns
    ]

    return cat_features, num_features


def split_features_target(data: pd.DataFrame):
    if target_col not in data.columns:
        raise ValueError(f"Target column not found: {target_col}")

    X = data.drop(target_col, axis=1)
    y = data[target_col]

    return X, y


def build_preprocessor(cat_features, num_features):
    num_transformer = Pipeline(
        steps=[
            ('impter', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]
    )

    cat_transformer = Pipeline(
        steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', create_one_hot_encoder())
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_features),
            ('cat', cat_transformer, cat_features)
        ]
    )

    return preprocessor

def build_stacking_model(random_state: int):
    base_models = [
        (
            'random_forest',
            RandomForestRegressor(
                n_estimators=300,
                max_depth=18,
                min_samples_leaf=2,
                random_state=random_state,
                n_jobs=-1
            )
        ),
        (
            'extra_trees', 
            ExtraTreesRegressor(
                n_estimators=300,
                min_samples_leaf=2,
                random_state=random_state, 
                n_jobs=-1
            )
        ),
        (
            'gradient_boosting',
            GradientBoostingRegressor(
                n_estimators=250,
                learning_rate=0.05,
                max_depth=3,
                random_state=random_state
            )
        )
    ]

    stacking_model = StackingRegressor(
        estimators=base_models,
        final_estimator=RidgeCV(),
        cv=5,
        passthrough=True,
        n_jobs=-1
    )

    return stacking_model

def train_model(config: dict):
    data = load_model_data(config)

    cat_features, num_features = get_feature_columns(data)
    X, y = split_features_target(data)

    test_size = config['model']['test_size']
    random_state=config['model']['random_state']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    preprocessor = build_preprocessor(
        cat_features=cat_features,
        num_features=num_features
    )

    stacking_model = build_stacking_model(random_state=random_state)

    pipeline = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('model', stacking_model)
        ]
    )

    model = TransformedTargetRegressor(
        regressor=pipeline,
        func=np.log1p,
        inverse_func=np.expm1

    )

    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    test_prediction = model.predict(X_test)
 
    metrics = {
        "model_type": "StackingRegressor",
        "train_rows": int(X_train.shape[0]),
        "test_rows": int(X_test.shape[0]),
        "features": {
            "categorical": cat_features,
            "numeric": num_features,
        },
        "train_mae": float(mean_absolute_error(y_train, train_predictions)),
        "test_mae": float(mean_absolute_error(y_test, test_prediction)),
        "train_rmse": float(np.sqrt(mean_squared_error(y_train, train_predictions))),
"test_rmse": float(np.sqrt(mean_squared_error(y_test, test_prediction))),
        "train_r2": float(r2_score(y_train, train_predictions)),
        "test_r2": float(r2_score(y_test, test_prediction)),
    }

    return model, metrics


def save_training_outputs(model, metrics: dict, config: dict) -> None:
    project_root = get_project_root()

    model_path = project_root / config["paths"]["model_path"]
    metrics_path = project_root / config["paths"]["metrics_path"]

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)

    with open(metrics_path, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4, ensure_ascii=False)