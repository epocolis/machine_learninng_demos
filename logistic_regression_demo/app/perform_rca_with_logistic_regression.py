import argparse
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def load_model(model_path):
    model = joblib.load(model_path)
    return model

def classify(model, production_data_path, output_dir):
    try:
        production_data = pd.read_csv(production_data_path)
        X_prod = production_data.drop("root_cause", axis=1)  # Assuming the production data includes the actual root causes for comparison
        
        # Perform prediction
        y_pred = model.predict(X_prod)

        # Add predictions to the original DataFrame
        production_data["Predicted_Root_Cause"] = y_pred

        # Generate Confusion Matrix
        cm = confusion_matrix(production_data["root_cause"], y_pred)
        sns.set(font_scale=1.2)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt="g", cmap="Blues")
        plt.xlabel("Predicted Root Causes")
        plt.ylabel("Actual Root Causes")
        plt.title("Confusion Matrix")
        plt.savefig(f"{output_dir}/confusion_matrix.png")

        # Generate Bar Plot for Actual vs Predicted
        plt.figure(figsize=(10, 6))
        sns.countplot(data=production_data, x="Predicted_Root_Cause", hue="root_cause")
        plt.title("Distribution of Actual vs Predicted Root Causes")
        plt.savefig(f"{output_dir}/actual_vs_predicted.png")

        # Save DataFrame to CSV
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/predictions.csv"
        production_data.to_csv(output_file, index=False)

        print(f"Predictions and visualizations saved to {output_dir}.")

    except Exception as e:
        print(f"Error in classifying production data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Classify instances in synthetic production data using trained Logistic Regression model."
    )
    parser.add_argument(
        "--model_path",
        type=str,
        required=True,
        help="Path to the trained Logistic Regression model",
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
