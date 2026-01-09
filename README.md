Zomato Case Study – End-to-End Data & ML Pipeline
Overview

This project is an end-to-end Data Engineering, Analytics, and Machine Learning case study built using a real-world Zomato restaurant dataset.
It demonstrates how to design a production-ready ETL pipeline, perform analytics using Power BI, and expose a machine learning model through a REST API.

The solution focuses on clean architecture, fault tolerance, secure configuration, logging, and real-world usability.

Key Features

Production-ready ETL pipeline (Extract, Transform, Load)

Secure configuration using environment variables

Structured logging with rotating log files

Robust error handling and recovery strategies

Interactive Power BI dashboard with KPIs and slicers

Restaurant rating prediction using Machine Learning

Model exposed via FastAPI for real-world usage

Project Structure
ZOMATO_CASE_STUDY/
│
├── data/
│   └── raw/                         # Raw city-wise CSV files
│
├── etl/
│   ├── config.py                    # Centralized configuration & env vars
│   ├── db.py                        # Database connection handler
│   ├── exceptions.py                # Custom ETL exceptions
│   ├── extract.py                   # Data extraction logic
│   ├── transform.py                 # Data cleaning & transformation
│   ├── load.py                      # Load data into MySQL
│   ├── logger.py                    # Central logging setup
│   └── main.py                      # ETL pipeline entry point
│
├── ml/
│   ├── train_model.py               # Model training & evaluation
│   ├── predict.py                   # Standalone prediction script
│   ├── app.py                       # FastAPI prediction service
│   ├── rating_model.pkl             # Trained ML model
│   ├── scaler.pkl                   # Feature scaler
│   └── feature_columns.pkl          # Feature schema reference
│
├── powerbi/
│   └── Zomato_Case_Study_Analysis.pbix
│
├── etl.log                      # Rotating ETL logs
│
├── .env                             # Environment variables (not committed)
├── .gitignore
├── requirements.txt
└── README.md

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

Dev & Best Practices

Environment variables (.env)

Structured logging (logging, RotatingFileHandler)

Custom exception handling

Configurable and relative paths (no hardcoding)

REST API using FastAPI

ETL Pipeline Design
1. Extract

Recursively scans city-wise folders for CSV files

Uses | as delimiter

Validates mandatory columns

Handles malformed files gracefully:

Logs errors

Skips corrupted files

Continues pipeline execution

2. Transform

Standardizes column names

Converts numeric fields safely

Applies business rules:

Drops rows with missing restaurant name or rating

Explodes multi-value cuisine fields

Logs data quality actions

3. Load

Validates schema before insertion

Loads data into MySQL staging tables

Uses batch inserts for performance

Logs successful and failed loads

Logging & Error Handling

Centralized logging via logger.py

Logs written to:

Console

logs/etl.log (rotating log file)

Custom exceptions:

ExtractionError

TransformationError

LoadError

Clear recovery strategies:

Skip invalid files

Fail fast on critical errors

Preserve stack traces for debugging

Power BI Dashboard

Clear dashboard title and subtitle

KPIs:

Total Cities

Total Cuisines

Total Restaurants

High Rated Restaurants

Interactive slicers:

City

Cuisine

Rating Category

Appropriate visuals:

Bar charts for comparisons

Donut charts for distribution

Scatter plot for cost vs rating relationship

Corrected map locations (India-only)

Machine Learning & API

Trained ML model to predict restaurant ratings

Feature engineering and scaling applied

Model exposed using FastAPI

Interactive API documentation available via Swagger UI:

http://127.0.0.1:8000/docs

Sample Prediction Input
{
  "price": 500,
  "votes": 250,
  "city": "Bengaluru",
  "region": "Indiranagar",
  "cuisine": "North Indian",
  "cuisine_type": "Casual Dining"
}

How to Run
1. Set environment variables

Create a .env file:

DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=zomato_analytics

2. Run ETL
python etl/main.py

3. Train Model
python ml/train_model.py

4. Start Prediction API
uvicorn ml.app:app --reload

Outcome

This project demonstrates:

Industry-aligned ETL practices

Secure and maintainable configuration

Real-world analytics and visualization

Practical ML deployment via REST API