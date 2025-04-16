import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv("result.csv")
df = df.iloc[:, 4:]  # Select columns starting from the 5th column

# Change NaN value
df.replace("N/a",pd.NA)
df = df.fillna(0)

# Select only numeric columns
data = df.select_dtypes(include=[float, int])

# Scale the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Try different values of k
range_n_clusters = range(2, len(df.columns))

inertias = []
silhouette_avgs = []

for k in range_n_clusters:
    kmeans = KMeans(n_clusters=k,random_state=k).fit(data_scaled)
    cluster_labels = kmeans.labels_
    inertias.append(kmeans.inertia_)
    silhouette_avgs.append(silhouette_score(data_scaled, cluster_labels))

# Plot
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# Elbow plot (inertia)
ax[0].plot(range_n_clusters, inertias, marker='o')
ax[0].set_title("Elbow Method (Inertia)")
ax[0].set_xlabel("Number of Clusters (k)")
ax[0].set_ylabel("Inertia (WCSS)")

# Silhouette plot
ax[1].plot(range_n_clusters, silhouette_avgs, marker='o', color='green')
ax[1].set_title("Silhouette Score")
ax[1].set_xlabel("Number of Clusters (k)")
ax[1].set_ylabel("Average Silhouette Score")

plt.suptitle("Choosing Optimal k: Elbow & Silhouette Method", fontsize=16)
plt.tight_layout()
plt.show()