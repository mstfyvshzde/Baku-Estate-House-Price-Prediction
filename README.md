# Baku Estate House Price Prediction

A machine learning regression project for predicting house prices in Baku.

## Overview

Baku Estate House Price Prediction is a real-world machine learning project focused on estimating property prices using structured housing data.

The project includes data cleaning, validation, feature engineering, model preparation, and a reusable project structure.

The goal is to build a clean machine learning pipeline that can process raw real estate data and prepare it for house price prediction.

## Problem

Real estate prices can depend on many factors such as:

* district
* location
* property type
* number of rooms
* area
* floor
* total floors
* repair status

This project uses these features to build a structured machine learning workflow for price prediction.

## Project Goals

* Load raw Baku real estate data
* Clean and normalize text columns
* Convert numeric columns into correct data types
* Detect and remove invalid rows
* Save cleaned data and cleaning reports
* Create useful features for model training
* Prepare a maintainable ML project structure
* Build a foundation for future model training and prediction

## Dataset Features

Main dataset columns:

```text
district
location
property_type
rooms
area
floor
total_floors
repair
price
```

Target column:

```text
price
```

## Data Validation Rules

The project uses validation rules to detect unrealistic or invalid values.

Example rules:

```text
rooms: between 1 and 10
area: between 15 and 500
floor: at least 1
total_floors: between 1 and 60
price: between 10,000 and 2,000,000
```

Invalid rows are separated from clean rows so the cleaning process can be reviewed later.

## Feature Engineering

The project creates additional useful features from the cleaned data.

Example feature:

```text
area_per_room = area / rooms
```

This helps the model better understand the relationship between apartment size and room count.

## Project Structure

```text
Baku-Estate-House-Price-Prediction/
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── outputs/
│   ├── metrics/
│   └── reports/
│
├── scripts/
│   ├── clean_data.py
│   └── prepare_features.py
│
├── src/
│   ├── data/
│   │   └── cleaning.py
│   │
│   ├── features/
│   │   └── build_features.py
│   │
│   └── utils/
│       └── config.py
│
├── README.md
└── requirements.txt
```

## Main Components

### `config/config.yaml`

Stores project settings in one place.

It includes:

* input and output file paths
* dataset column names
* validation rules
* cleaning output locations

This keeps the project easier to maintain and update.

### `src/utils/config.py`

Loads the configuration file and helps other modules access shared project settings.

Main function:

```python
load_config()
```

### `src/data/cleaning.py`

Handles the data cleaning pipeline.

Main responsibilities:

* Load raw CSV data
* Assign column names from the config file
* Normalize text columns
* Convert numeric columns
* Detect invalid rows
* Separate clean and removed rows
* Save cleaning outputs and summary reports

### `src/features/build_features.py`

Prepares the cleaned dataset for model training.

Main responsibilities:

* Load cleaned data
* Check required columns
* Create new features
* Save processed model data
* Save feature summary report

## How to Run

### 1. Install requirements

```bash
python3 -m pip install -r requirements.txt
```

### 2. Clean the raw dataset

```bash
python3 scripts/clean_data.py
```

### 3. Prepare features

```bash
python3 scripts/prepare_features.py
```

## Example Workflow

```text
Raw real estate data
    ↓
Data cleaning
    ↓
Invalid row detection
    ↓
Clean dataset
    ↓
Feature engineering
    ↓
Processed model dataset
    ↓
Model training and price prediction
```

## Tech Stack

* Python
* pandas
* NumPy
* scikit-learn
* XGBoost
* YAML configuration
* Modular ML project structure

## Model Results

Example result from the project development process:

```text
MAE: around 36,000 AZN
R² Score: around 0.87
```

These values may change depending on dataset version, feature engineering, and model settings.

## Why This Project Matters

This project shows the full machine learning workflow:

* raw data handling
* data cleaning
* validation
* feature engineering
* structured project organization
* regression problem solving

It is useful as a portfolio project because it demonstrates practical machine learning skills on a real-world style dataset.

## Future Improvements

* Add more advanced feature engineering
* Add model comparison
* Add final training script documentation
* Add prediction examples
* Add visualizations
* Add FastAPI prediction endpoint
* Build a simple interface for user input
* Improve model evaluation reports

## Project Status

In progress as a real estate machine learning pipeline.
