import argparse
import xgboost as xgb
import pandas as pd
import os


def load_model(model_path):
    model = xgb.Booster()
    model.load_model(model_path)
    return model


def classify(model, production_data_path, output_dir):
    try:
        production_data = pd.read_csv(production_data_path)
        X_prod = production_data.drop("label", axis=1)
        dprod = xgb.DMatrix(X_prod)
        y_pred = model.predict(dprod)
        y_pred_binary = [1 if p > 0.5 else 0 for p in y_pred]

        # Add predictions to the original DataFrame
        production_data["Prediction"] = y_pred_binary

        # Save DataFrame to CSV
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/predictions.csv"
        production_data.to_csv(output_file, index=False)

        print(f"Predictions saved to {output_file}.")

    except Exception as e:
        print(f"Error in classifying production data: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Classify instances in synthetic production data using trained XGBoost model."
    )
    parser.add_argument(
        "--model_path",
        type=str,
        required=True,
        help="Path to the trained XGBoost model",
    )
    parser.add_argument(
        "--production_data_path",
        type=str,
        required=True,
        help="Path to the synthetic production data",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="opt/ml/output",
        help="Directory for saving predictions",
    )

    args = parser.parse_args()

    try:
        model = load_model(args.model_path)
        classify(model, args.production_data_path, args.output_dir)
    except Exception as e:
        print(f"Error: {e}")
