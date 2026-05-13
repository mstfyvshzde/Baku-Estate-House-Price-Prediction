## Configuration

The project uses a `config.yaml` file to keep important settings in one place.

It stores:

- input and output file paths
- dataset column names
- data validation rules

This makes the code cleaner and easier to maintain.

### Main config sections

- `paths`: defines where raw data, cleaned data, removed rows, and cleaning summary files are stored.
- `schema`: defines the column names used in the dataset.
- `validation`: defines basic rules for detecting invalid rows during data cleaning.

Example validation rules:

- rooms must be between 1 and 10
- area must be between 15 and 500
- floor must be at least 1
- total floors must be between 1 and 60
- price must be between 10,000 and 2,000,000



---


## Configuration Loader

The project uses `src/utils/config.py` to load settings from `config/config.yaml`.

This file helps the project:

- find the project root directory
- load the YAML configuration file
- use paths, schema, and validation rules across the codebase

The main function is:

```python
load_config()
```


## Data Cleaning

The data cleaning logic is implemented in:

`src/data/cleaning.py`

This module is responsible for preparing the raw housing dataset before model training.

It performs the following steps:

- loads the raw CSV file
- assigns column names from the config file
- normalizes text columns
- converts numeric columns to proper numeric types
- detects invalid rows using validation rules
- separates clean rows from removed rows
- saves cleaning outputs and a summary report

### Main functions

- `normalize_text()`  
  Cleans text values by removing extra spaces, converting text to lowercase, and normalizing unicode characters.

- `load_raw_data()`  
  Loads the raw dataset using paths and schema defined in `config.yaml`.

- `clean_text_columns()`  
  Applies text normalization to categorical columns such as district and location.

- `clean_numeric_columns()`  
  Converts numeric columns like rooms, area, floor, total floors, and price into numeric format.

- `build_removal_reasons()`  
  Checks each row against validation rules and records why invalid rows should be removed.

- `clean_dataset()`  
  Runs the full cleaning pipeline and returns clean data, removed rows, and a cleaning summary.

- `save_cleaning_outputs()`  
  Saves the cleaned dataset, removed rows, and cleaning summary to output files.

This structure keeps the cleaning logic reusable, readable, and easier to maintain.

## Cleaning Script

The data cleaning process is executed with:

```bash
python3 scripts/clean_data.py
```

## Feature Engineering

Feature engineering is implemented in:

`src/features/build_features.py`

This module prepares the cleaned dataset for model training.

It performs the following steps:

- loads the cleaned dataset from `data/interim/clean_data.csv`
- checks that all required columns exist
- creates new useful features
- saves the final model dataset to `data/processed/model_data.csv`
- saves a feature summary report

### Added feature

- `area_per_room`: shows the average area per room

This feature helps the model better understand the relationship between apartment size and room count.

## Feature Preparation Script

Feature engineering is executed with:

```bash
python3 scripts/prepare_features.py