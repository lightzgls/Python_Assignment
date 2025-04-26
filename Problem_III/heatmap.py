# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Step 1: Load data
data = pd.read_csv('results.csv')

# Step 2: Drop non-numeric columns except for cluster (if already present)
non_numeric_cols = data.select_dtypes(exclude=['number']).columns.tolist()
non_numeric_cols = [col for col in non_numeric_cols if col != 'cluster']
numeric_data = data.drop(columns=non_numeric_cols)

# Step 3: Check if 'cluster' column exists
if 'cluster' not in data.columns:
    # Step 3.1: Extract features (excluding non-numeric columns)
    features = numeric_data.copy()

    # Step 3.2: Scale the features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features)

    # Step 3.3: Run KMeans with k=11
    kmeans = KMeans(n_clusters=11, random_state=0, n_init=10)
    clusters = kmeans.fit_predict(scaled_data)

    # Step 3.4: Add 'cluster' back to original dataframe
    data['cluster'] = clusters

# Step 4: Group by cluster and calculate mean (on numeric columns only)
cluster_summary = data.drop(columns=non_numeric_cols).groupby('cluster').mean()

# Step 5: Normalize each column (feature-wise)
normalized_summary = (cluster_summary - cluster_summary.min()) / (cluster_summary.max() - cluster_summary.min())

# Step 6: Save to CSV
normalized_summary.to_csv('normalized_cluster_summary.csv')

# Step 7: Display heatmap
plt.figure(figsize=(16, 10))
sns.heatmap(normalized_summary, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title("Normalized Feature Differences Between Clusters", fontsize=18)
plt.xlabel("Features", fontsize=14)
plt.ylabel("Cluster", fontsize=14)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
