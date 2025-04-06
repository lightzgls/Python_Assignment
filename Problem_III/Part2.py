import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Step 1: Load and preprocess the data
df = pd.read_csv("result.csv")

# Select relevant columns (e.g., stats only)
stats = df.iloc[:, 4:]  # Assuming stats start from the 5th column

# Convert to numeric and handle missing data
stats = stats.apply(pd.to_numeric, errors='coerce')
stats = stats.fillna(stats.mean())  # Replace NaN values with column mean

# Check the number of samples
print(stats)
print(f"Number of samples: {stats.shape[0]}")

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(stats)

# Step 2: Try different values of k
inertia = []
K = range(2, stats.shape[1]+1)  # Ensure k <= number of samples
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)  # Inertia = within-cluster sum of squares

# Step 3: Plot the results
plt.plot(K, inertia, 'bo-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia (within-cluster sum of squares)')
plt.title('Elbow Method For Optimal k')
plt.show()