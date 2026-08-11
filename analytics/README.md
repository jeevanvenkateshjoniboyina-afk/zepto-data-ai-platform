# Module 2 – Analytics Pipeline

## Overview

This module performs Exploratory Data Analysis (EDA), data preprocessing, machine learning model training, model evaluation, regression analysis, and pipeline serialization using the Titanic dataset.

---

## Dataset

The Titanic dataset was loaded using:

```python
sns.load_dataset("titanic")
```

The dataset was saved locally as:

```
titanic.csv
```

to allow offline grading.

---

## Data Cleaning

Missing values were handled as follows:

- Age (19.87%) → Median Imputation
- Embarked (0.22%) → Mode Imputation
- Embark Town (0.22%) → Mode Imputation
- Deck (77.22%) → Dropped

---

## Exploratory Data Analysis

Performed:

- Dataset Profiling
- Missing Value Analysis
- Histogram and Box Plot
- Outlier Detection using IQR
- Survival Rate Analysis
- Correlation Heatmap
- Multivariate Visualizations
- Standardization Check

---

## Classification Models

Models trained:

- Logistic Regression
- Decision Tree
- Random Forest

Evaluation Metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC Curve
- AUC Score

---

## Hyperparameter Tuning

Random Forest was tuned using GridSearchCV.

Best Parameters:

- max_depth = 5
- max_features = sqrt
- n_estimators = 50

---

## Regression

A Linear Regression model was built to predict passenger fare.

Evaluation Metrics:

- MAE
- RMSE
- R²
- Adjusted R²

Residual analysis was also performed.

---

## Saved Pipeline

The best-performing machine learning pipeline was saved using:

```python
joblib.dump()
```

The pipeline includes preprocessing and the trained estimator.