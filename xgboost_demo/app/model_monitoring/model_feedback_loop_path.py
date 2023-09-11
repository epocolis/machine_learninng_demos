import argparse
import xgboost as xgb
import pandas as pd
import json
import os
from sklearn.metrics import classification_report

def load_model(model_path):
    model = xgb.Booster()
    model.load_model(model_path)
    return model

def feedback_loop(model, production_data_path, true_labels_path, output_dir):
    try:
        # Load production data and true labels
        production_data = pd.read_csv(production_data_path)
        true_labels = pd.read_csv(true_labels_path)

        X_prod = production_data.drop("label", axis=1)
        y_true = true_labels["true_label"]

        # Make predictions
        dprod = xgb.DMatrix(X_prod)
        y_pred = model.predict(dprod)
        y_pred_binary = [1 if p > 0.5 else 0 for p in y_pred]

        # Evaluate performance based on feedback (true labels)
        metrics = classification_report(y_true, y_pred_binary, output_dict=True)

        # Save metrics
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/feedback_loop_metrics.json", "w") as f:
            json.dump(metrics, f)
        
        print(f"Feedback loop metrics saved to {output_dir}/feedback_loop_metrics.json.")
        
    except Exception as e:
        print(f"Error in feedback loop: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Feedback loop for XGBoost model performance monitoring.")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the trained XGBoost model")
    parser.add_argument("--production_data_path", type=str, required=True, help="Path to the synthetic production data")
    parser.add_argument("--true_labels_path", type=str, required=True, help="Path to the CSV file containing true labels for feedback")
    parser.add_argument("--output_dir", type=str, default="opt/ml/monitoring", help="Directory for saving feedback loop metrics")

    args = parser.parse_args()
    
    try:
        model = load_model(args.model_path)
        feedback_loop(model, args.production_data_path, args.true_labels_path, args.output_dir)
    except Exception as e:
        print(f"Error: {e}")
