Zomato Case Study – End-to-End Data & ML Pipeline
Overview

This project is an end-to-end Data Engineering, Analytics, and Machine Learning case study built using a real-world restaurant dataset (Zomato).
It demonstrates how to design and implement a production-ready ETL pipeline, perform exploratory data analysis, build interactive dashboards, and develop a machine learning model for restaurant rating prediction.

The solution emphasizes:

Clean architecture

Fault-tolerant ETL

Secure configuration management

Structured logging

Reproducibility and maintainability

Project Structure
ZOMATO_CASE_STUDY/
│
├── data/
│   └── raw/                       # Raw city-wise CSV files
│
├── etl/
│   ├── config.py                  # Centralized configuration & env vars
│   ├── db.py                      # Database connection handler
│   ├── exceptions.py              # Custom ETL exceptions
│   ├── extract.py                 # Data extraction logic
│   ├── transform.py               # Data cleaning & transformation
│   ├── load.py                    # Load data into MySQL staging tables
│   ├── logger.py                  # Central logging configuration
│   └── main.py                    # ETL pipeline entry point
│
├── ml/
│   ├── train_model.py             # Model training & evaluation
│   ├── predict.py                 # Rating prediction script
│   ├── rating_model.pkl           # Trained ML model
│   ├── scaler.pkl                 # Feature scaler
│   └── feature_columns.pkl        # Feature schema reference
│
├── powerbi/
│   └── Zomato_Case_Study_Analysis.pbix
│
├── .env                           # Environment variables (not committed)
├── .gitignore
├── requirements.txt
├── README.md
└── logs/
    └── etl.log                    # Rotating ETL logs

Tech Stack
Data Engineering

Python

Pandas

MySQL

SQLAlchemy

Machine Learning

Scikit-learn

Random Forest Regressor

Linear Regression

Analytics & Visualization

Power BI

Dev & Ops Best Practices

Environment variables (.env)

Structured logging (logging, RotatingFileHandler)

Custom exception handling

Configurable paths (no hardcoding)

ETL Pipeline Design
1. Extract

Recursively scans all city folders for CSV files

Uses | as delimiter

Validates mandatory columns

Handles malformed files gracefully:

Logs error

Skips corrupted files

Continues pipeline execution

2. Transform

Standardizes column names

Converts numeric fields safely

Enforces business rules:

Drops rows with missing restaurant name or rating

Normalizes multi-value cuisine fields using explosion

Logs data quality actions (rows dropped)

3. Load

Validates schema before database insertion

Loads data into MySQL staging tables

Uses batch inserts for performance

Logs successful and failed loads

Logging & Error Handling

Centralized logging via logger.py

Logs written to:

Console

Rotating file: logs/etl.log

Custom exceptions:

ExtractionError

TransformationError

LoadError

Clear recovery strategies:

Skip invalid files

Stop pipeline on critical failures

Preserve stack traces for debugging