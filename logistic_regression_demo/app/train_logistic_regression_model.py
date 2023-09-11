import numpy as np
import pandas as pd
import argparse
import os
import ast
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import json
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


def load_data(train_file, validation_file):
    train_data = pd.read_csv(train_file)
    validation_data = pd.read_csv(validation_file)
    return train_data, validation_data


def train_model(train_data, params):
    X_train = train_data.drop("root_cause", axis=1)
    y_train = train_data["root_cause"]
    model = LogisticRegression(**params)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, validation_data, output_dir):
    X_val = validation_data.drop("root_cause", axis=1)
    y_val = validation_data["root_cause"]
    y_pred = model.predict(X_val)
    metrics = classification_report(y_val, y_pred, output_dict=True)
    cm = confusion_matrix(y_val, y_pred)

    sns.set(font_scale=1.2)
    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt="g", cmap="Blues", cbar=False)
    plt.xlabel("Predicted labels")
    plt.ylabel("True labels")
    plt.title("Confusion Matrix")
    plt.savefig(f"{output_dir}/confusion_matrix.png")

    metrics["confusion_matrix"] = cm.tolist()
    with open(f"{output_dir}/metrics.json", "w") as f:
        json.dump(metrics, f)


def save_model(model, model_dir):
    joblib.dump(model, f"{model_dir}/logistic_regression_model.pkl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train Logistic Regression model for Root Cause Analysis."
    )
    parser.add_argument(
        "--train_file", type=str, required=True, help="Training data directory"
    )
    parser.add_argument(
        "--train_file_name",
        type=str,
        default="root_cause_train_data.csv",
        help="Name of the training data file",
    )
    parser.add_argument(
        "--validation_file", type=str, required=True, help="Validation data directory"
    )
    parser.add_argument(
        "--validation_file_name",
        type=str,
        default="root_cause_validation_data.csv",
        help="Name of the validation data file",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./opt/ml/output",
        help="Directory for saving metrics",
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default="./opt/ml/model",
        help="Directory for saving the model",
    )
    parser.add_argument(
        "--params",
        type=str,
        default="{'solver':'lbfgs', 'max_iter':1000}",
        help="Logistic Regression model parameters as a JSON-formatted string",
    )

    args = parser.parse_args()
    params = ast.literal_eval(args.params)

    train_data, validation_data = load_data(
        os.path.join(args.train_file, args.train_file_name),
        os.path.join(args.validation_file, args.validation_file_name),
    )
    model = train_model(train_data, params)
    evaluate_model(model, validation_data, args.output_dir)
    save_model(model, args.model_dir)
