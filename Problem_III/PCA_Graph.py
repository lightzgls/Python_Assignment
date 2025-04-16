import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

df = pd.read_csv("result.csv")

# Select relevant columns (e.g., stats only)
stats = df.iloc[:, 4:]  # Assuming stats start from the 5th column

# Convert to numeric and drop rows with any non-numeric or missing data
stats = stats.apply(pd.to_numeric, errors='coerce')
stats = stats.fillna(0)


scaler = StandardScaler()
scaled_stats = scaler.fit_transform(stats)

n_clusters = [7,8,9] # Ensure n_clusters <= number of samples


for k in n_clusters:
    kmeans = KMeans(n_clusters=k,random_state=0)   
    kmeans.fit(scaled_stats)

    pca = PCA(n_components=2)
    pca_stats = pca.fit_transform(scaled_stats)

    # Plot the clustered data in 2D space
    plt.scatter(pca_stats[:, 0], pca_stats[:, 1], c=kmeans.labels_, cmap='viridis') 
    plt.title(f"K-means Clustering of Players (k={k}, PCA 2D Projection)")  
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.colorbar(label='Cluster')
    plt.show()