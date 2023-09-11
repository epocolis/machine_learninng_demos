import numpy as np
import pandas as pd
import argparse
import os


def generate_anomaly_data(n_samples=1000, anomaly_ratio=0.1, seed=None):
    """
    Generate synthetic data for anomaly detection.

    Parameters:
    - n_samples: int, Number of data samples
    - anomaly_ratio: float, Proportion of anomalies in the dataset
    - seed: int, Random seed for reproducibility

    Returns:
    - DataFrame containing the synthetic data
    """
    if seed is not None:
        np.random.seed(seed)

    # Generate synthetic data for system metrics
    cpu_usage = np.random.normal(50, 10, n_samples).astype(int)
    memory_usage = np.random.normal(50, 10, n_samples).astype(int)
    disk_io = np.random.normal(50, 10, n_samples).astype(int)
    network_activity = np.random.normal(50, 10, n_samples).astype(int)

    # Generate labels (0 for normal, 1 for anomalous)
    labels = np.random.choice(
        [0, 1], size=n_samples, p=[1 - anomaly_ratio, anomaly_ratio]
    )

    # Create a DataFrame
    df = pd.DataFrame(
        {
            "cpu_usage": np.clip(cpu_usage, 0, 100),
            "memory_usage": np.clip(memory_usage, 0, 100),
            "disk_io": np.clip(disk_io, 0, 100),
            "network_activity": np.clip(network_activity, 0, 100),
            "label": labels,
        }
    )

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate synthetic data for anomaly detection."
    )
    parser.add_argument(
        "--n_samples", type=int, default=1000, help="Number of data samples"
    )
    parser.add_argument(
        "--anomaly_ratio",
        type=float,
        default=0.1,
        help="Proportion of anomalies in the dataset",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--train_dir",
        type=str,
        default="opt/ml/input/data/train",
        help="Output directory for training data",
    )
    parser.add_argument(
        "--validation_dir",
        type=str,
        default="opt/ml/input/data/validation",
        help="Output directory for validation data",
    )
    parser.add_argument(
        "--production_dir",
        type=str,
        default="opt/ml/input/data/production",
        help="Output directory for production data",
    )

    args = parser.parse_args()

    # Generate synthetic data
    df_train = generate_anomaly_data(
        n_samples=args.n_samples, anomaly_ratio=args.anomaly_ratio, seed=args.seed
    )
    df_validation = generate_anomaly_data(
        n_samples=args.n_samples // 2, anomaly_ratio=args.anomaly_ratio, seed=args.seed
    )
    df_production = generate_anomaly_data(
        n_samples=args.n_samples // 2, anomaly_ratio=0, seed=args.seed
    )  # Assuming no anomalies in production data

    # Ensure the output directories exist
    os.makedirs(args.train_dir, exist_ok=True)
    os.makedirs(args.validation_dir, exist_ok=True)
    os.makedirs(args.production_dir, exist_ok=True)

    # Save the DataFrames to CSV files in the appropriate folders
    df_train.to_csv(f"{args.train_dir}/synthetic_train_data.csv", index=False)
    df_validation.to_csv(
        f"{args.validation_dir}/synthetic_validation_data.csv", index=False
    )
    df_production.to_csv(
        f"{args.production_dir}/synthetic_production_data.csv", index=False
    )

    print("Synthetic data generated and saved to specified directories.")
