import argparse
import xgboost as xgb
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import os
import ast
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


def load_data(train_file, validation_file):
    train_data = pd.read_csv(train_file)
    validation_data = pd.read_csv(validation_file)
    return train_data, validation_data


def train_model(train_data, params):
    X_train = train_data.drop("label", axis=1)
    y_train = train_data["label"]
    dtrain = xgb.DMatrix(X_train, label=y_train)
    model = xgb.train(params, dtrain)
    return model


def evaluate_model(model, validation_data, output_dir):
    X_val = validation_data.drop("label", axis=1)
    y_val = validation_data["label"]
    dval = xgb.DMatrix(X_val, label=y_val)
    y_pred = model.predict(dval)
    y_pred_binary = [1 if p > 0.5 else 0 for p in y_pred]

    metrics = classification_report(y_val, y_pred_binary, output_dict=True)
    cm = confusion_matrix(y_val, y_pred_binary)

    # Generate Confusion Matrix heatmap
    sns.set(font_scale=1.2)
    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt="g", cmap="Blues", cbar=False)
    plt.xlabel("Predicted labels")
    plt.ylabel("True labels")
    plt.title("Confusion Matrix")
    plt.savefig(f"{output_dir}/confusion_matrix.png")

    # Generate Sankey Diagram
    label = ["Actual True", "Actual False", "Predicted True", "Predicted False"]
    source = [0, 0, 1, 1]
    target = [2, 3, 2, 3]
    value = [cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]]

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=label,
                ),
                link=dict(source=source, target=target, value=value),
            )
        ]
    )

    fig.update_layout(title_text="Sankey Diagram of Model Predictions", font_size=10)
    fig.write_image(f"{output_dir}/sankey_diagram.png")

    metrics["confusion_matrix"] = cm.tolist()
    with open(f"{output_dir}/metrics.json", "w") as f:
        json.dump(metrics, f)


def save_model(model, model_dir):
    model.save_model(f"{model_dir}/xgboost_model.model")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train XGBoost model for anomaly detection."
    )
    parser.add_argument(
        "--train_file", type=str, required=True, help="Training data file path"
    )
    parser.add_argument(
        "--validation_file", type=str, required=True, help="Validation data file path"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="opt/ml/output",
        help="Directory for saving metrics",
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default="opt/ml/model",
        help="Directory for saving the model",
    )
    parser.add_argument(
        "--params",
        type=str,
        default="{'objective':'binary:logistic', 'eval_metric':'logloss'}",
        help="XGBoost model parameters as a JSON-formatted string",
    )

    args = parser.parse_args()
    params = ast.literal_eval(args.params)

    print("Parsed parameters:", params)
    train_data, validation_data = load_data(args.train_file, args.validation_file)
    model = train_model(train_data, params)
    evaluate_model(model, validation_data, args.output_dir)
    save_model(model, args.model_dir)
