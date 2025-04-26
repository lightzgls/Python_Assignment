import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Step 1: Load and preprocess the data
data = pd.read_csv("results.csv") 

# Select the features used in the plot
features = [
    'Age', 'Standard_MP', 'Standard_Starts', 'Standard_Min', 'Standard_Gls', 
    'Standard_Ast', 'Standard_CrdY', 'Standard_CrdR', 'Standard_xG', 'Standard_xAG', 
    'Standard_PrgC', 'Standard_PrgP', 'Standard_PrgR', 'Standard_Gls/90', 
    'Standard_Ast/90', 'Standard_xG/90', 'Standard_xAG/90', 'Goalkeeping_GA90', 
    'Goalkeeping_Save%', 'Goalkeeping_CS%', 'Goalkeeping_Penalty_Save%', 
    'Shooting_SoT%', 'Shooting_SoT/90', 'Shooting_G/Sh', 'Shooting_Dist', 
    'Passing_Cmp', 'Passing_Total_Cmp%', 'Passing_TotDist', 'Passing_Short_Cmp%', 
    'Passing_Medium_Cmp%', 'Passing_Long_Cmp%', 'Passing_KP', 'Passing_1/3', 
    'Passing_PPA', 'Passing_CrsPA', 'Passing_PrgP', 'GCA_SCA', 'GCA_SCA90', 
    'GCA_GCA', 'GCA_GCA90', 'Defense_Tkl', 'Defense_TklW', 'Defense_Att', 
    'Defense_Lost', 'Defense_Blocks', 'Defense_Sh', 'Defense_Pass', 'Defense_Int', 
    'Possession_Touches', 'Possession_Def Pen', 'Possession_Def 3rd', 
    'Possession_Mid 3rd', 'Possession_Att 3rd', 'Possession_Att Pen', 
    'Possession_Att', 'Possession_Succ%', 'Possession_Tkld%', 'Possession_Carries', 
    'Possession_PrgDist', 'Possession_PrgC', 'Possession_1/3', 'Possession_CPA', 
    'Possession_Mis', 'Possession_Dis', 'Possession_Rec', 'Possession_PrgR', 
    'Misc_Fls', 'Misc_Fld', 'Misc_Off', 'Misc_Crs', 'Misc_Recov', 'Misc_Won', 
    'Misc_Lost', 'Misc_Won%'
]

# Subset the data to include only the features
data_features = data[features]

# Replace 'N/a' with NaN and convert to numeric
data_features = data_features.replace('N/a', np.nan)
data_features = data_features.apply(pd.to_numeric, errors='coerce')

# Handle missing values by filling with 0
data_features = data_features.fillna(0)

# Step 2: Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_features)

# Step 3: Apply PCA to reduce to 2 components
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_scaled)

# Create a DataFrame with PCA results
pca_df = pd.DataFrame(data_pca, columns=['PC1', 'PC2'])

# Step 4: Apply K-means clustering
n_cluster = [10, 11, 12]
for k in n_cluster:
    kmeans = KMeans(n_clusters=k, random_state=k)
    clusters = kmeans.fit_predict(data_pca)

    # Add cluster labels and PCA coordinates to the original DataFrame
    data['Cluster'] = clusters
    data['PC1'] = pca_df['PC1']
    data['PC2'] = pca_df['PC2']

    # Step 5: Create a scatter plot with Matplotlib
    plt.figure(figsize=(10, 8))
    plt.scatter(data['PC1'], data['PC2'], c=data['Cluster'], cmap='viridis', s=50, alpha=1)
    plt.title(f'K-means Clustering (K={k}) with PCA Projection', fontsize=16)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    
    # Add a colorbar and legend
    plt.colorbar(label='Cluster')
    plt.legend(title='Clusters', loc='center left', bbox_to_anchor=(1, 0.5))
    
    # Show the plot
    plt.tight_layout()
    plt.show()
