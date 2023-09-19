import numpy as np
import pandas as pd
import argparse
import os


def generate_synthetic_data(n_samples=500, start_date="2023-01-01", seed=None):
    """
    Generate synthetic data for Monitoring Alert Grouping.

    Parameters:
    - n_samples: int, Number of data samples
    - start_date: str, Start date for the timestamps
    - seed: int, Random seed for reproducibility
    """

    if seed is not None:
        np.random.seed(seed)

    # Generate random alert types
    alert_types = np.random.choice(
        ["CPU Overload", "Memory Leak", "Disk Full", "Network Latency"], size=n_samples
    )

    # Generate random alert levels
    alert_levels = np.random.choice(
        ["Low", "Medium", "High", "Critical"], size=n_samples
    )

    # Generate random server IDs
    server_ids = ["Server_" + str(i) for i in np.random.randint(1, 20, size=n_samples)]

    # Generate random timestamps
    timestamps = pd.date_range(start=start_date, periods=n_samples, freq="H")

    # Generate random latency (in ms)
    latency = np.round(np.random.randint(20, 500, size=n_samples), 2)

    # Generate random CPU usage (in %)
    cpu_usage = np.round(np.random.uniform(20.0, 100.0, size=n_samples), 2)

    # Generate random Memory usage (in %)
    memory_usage = np.round(np.random.uniform(20.0, 100.0, size=n_samples), 2)

    # Generate random Disk usage (in %)
    disk_usage = np.round(np.random.uniform(20.0, 100.0, size=n_samples), 2)

    # Create a DataFrame
    df = pd.DataFrame(
        {
            "Timestamp": timestamps,
            "Server_ID": server_ids,
            "Alert_Type": alert_types,
            "Alert_Level": alert_levels,
            "Latency_ms": latency,
            "CPU_Usage": cpu_usage,
            "Memory_Usage": memory_usage,
            "Disk_Usage": disk_usage,
        }
    )

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate synthetic data for Monitoring Alert Grouping."
    )
    parser.add_argument(
        "--n_samples", type=int, default=500, help="Number of data samples"
    )
    parser.add_argument(
        "--start_date",
        type=str,
        default="2023-01-01",
        help="Start date for the timestamps",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="/mnt/data",
        help="Output directory for synthetic data",
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        default="synthetic_monitoring_alert_data.csv",
        help="Output filename for synthetic data",
    )

    args = parser.parse_args()

    # Generate synthetic data
    df = generate_synthetic_data(
        n_samples=args.n_samples, start_date=args.start_date, seed=args.seed
    )

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Save the DataFrame to a CSV file in the appropriate folder
    output_path = os.path.join(args.output_dir, args.output_filename)
    df.to_csv(output_path, index=False)

    print(f"Synthetic data has been generated and saved to {output_path}.")
