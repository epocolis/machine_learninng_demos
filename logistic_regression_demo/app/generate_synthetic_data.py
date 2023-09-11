import numpy as np
import pandas as pd
import argparse
import os


def generate_root_cause_data(n_samples=1000, seed=None):
    """
    Generate synthetic data for Root Cause Analysis.
    """
    if seed is not None:
        np.random.seed(seed)

    cpu_usage = np.random.normal(50, 10, n_samples)
    memory_usage = np.random.normal(50, 10, n_samples)
    disk_io = np.random.normal(50, 10, n_samples)
    network_latency = np.random.normal(50, 10, n_samples)

    labels = np.random.choice(
        ["CPU Overload", "Memory Leak", "Network Issues"], size=n_samples
    )

    df = pd.DataFrame(
        {
            "cpu_usage": np.clip(cpu_usage, 0, 100),
            "memory_usage": np.clip(memory_usage, 0, 100),
            "disk_io": np.clip(disk_io, 0, 100),
            "network_latency": np.clip(network_latency, 0, 100),
            "root_cause": labels,
        }
    )

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate synthetic data for Root Cause Analysis."
    )
    parser.add_argument("--n_samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--train_dir", type=str, default="./opt/ml/input/data/train")
    parser.add_argument(
        "--train_file_name", type=str, default="synthetic_train_data.csv"
    )
    parser.add_argument(
        "--validation_dir", type=str, default="./opt/ml/input/data/validation"
    )
    parser.add_argument(
        "--validation_file_name", type=str, default="synthetic_validation_data.csv"
    )
    parser.add_argument(
        "--production_dir", type=str, default="./opt/ml/input/data/production"
    )
    parser.add_argument(
        "--production_file_name", type=str, default="synthetic_production_data.csv"
    )

    args = parser.parse_args()

    df_train = generate_root_cause_data(n_samples=args.n_samples, seed=args.seed)
    df_validation = generate_root_cause_data(
        n_samples=args.n_samples // 2, seed=args.seed
    )
    df_production = generate_root_cause_data(
        n_samples=args.n_samples // 2, seed=args.seed
    )

    os.makedirs(args.train_dir, exist_ok=True)
    os.makedirs(args.validation_dir, exist_ok=True)
    os.makedirs(args.production_dir, exist_ok=True)

    df_train.to_csv(f"{args.train_dir}/{args.train_file_name}", index=False)
    df_validation.to_csv(
        f"{args.validation_dir}/{args.validation_file_name}", index=False
    )
    df_production.to_csv(
        f"{args.production_dir}/{args.production_file_name}", index=False
    )

    print("Synthetic data generated and saved to specified directories.")
