import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer


def perform_clustering(
    input_data_path, output_dir, output_filename, features, plot_features
):
    try:
        synthetic_data = pd.read_csv(input_data_path)
        X = synthetic_data[features.split()]

        model = KMeans()
        visualizer = KElbowVisualizer(model, k=(1, 11))
        visualizer.fit(X)
        visualizer.show(outpath=f"{output_dir}/elbow_visualization.png")

        optimal_k = visualizer.elbow_value_
        print(f"Optimal number of clusters: {optimal_k}")

        kmeans = KMeans(n_clusters=optimal_k, init="k-means++", random_state=42)
        synthetic_data["Cluster"] = kmeans.fit_predict(X)

        # Pairplot for easier interpretation
        sns.pairplot(synthetic_data, hue="Cluster", vars=plot_features.split())
        plt.savefig(f"{output_dir}/pairplot_clusters.png")

        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/{output_filename}"
        synthetic_data.to_csv(output_file, index=False)

        print(f"Clustered data and visualizations saved to {output_file}.")

    except Exception as e:
        print(f"Error in clustering synthetic data: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cluster synthetic monitoring alert data."
    )
    parser.add_argument(
        "--input_data_path", type=str, required=True, help="Path to the synthetic data"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="/mnt/data",
        help="Directory for saving clustered data and visualizations",
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        default="clustered_data.csv",
        help="Filename for saving clustered data",
    )
    parser.add_argument(
        "--features",
        type=str,
        default="Latency_ms CPU_Usage Memory_Usage Disk_Usage",
        help="Features to use for clustering",
    )
    parser.add_argument(
        "--plot_features",
        type=str,
        default="Latency_ms CPU_Usage",
        help="Features to use for plotting",
    )

    args = parser.parse_args()

    try:
        perform_clustering(
            args.input_data_path,
            args.output_dir,
            args.output_filename,
            args.features,
            args.plot_features,
        )
    except Exception as e:
        print(f"Error: {e}")
