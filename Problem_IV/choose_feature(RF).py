from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import matplotlib.pyplot as plt

# === Helper function to convert string price to numeric ===
def convert_value(val):
    if isinstance(val, str):
        val = val.replace('$', '').replace('€', '').strip()
        try:
            if val.endswith('M'):
                return float(val[:-1]) * 1_000_000
            elif val.endswith('K'):
                return float(val[:-1]) * 1_000
            else:
                return float(val)
        except ValueError:
            return pd.NA
    return pd.NA

# === Load datasets ===
try:
    stats = pd.read_csv('results.csv')
    price = pd.read_csv("Transfer_values.csv")
except FileNotFoundError as e:
    raise FileNotFoundError(f"Dataset not found: {e}")

# === Check for empty datasets ===
if stats.empty or price.empty:
    raise ValueError("One or both input datasets are empty.")

# === Debugging: Print dataset info ===
print("Stats columns:", stats.columns)
print("Stats dtypes:", stats.dtypes)
print("Price columns:", price.columns)
print("Price dtypes:", price.dtypes)

# === Convert stats columns to numeric where possible ===
numeric_cols = [col for col in stats.columns if col not in ['Player', 'Nation', 'Squad', 'Pos', 'Unnamed: 0']]
for col in numeric_cols:
    stats[col] = pd.to_numeric(stats[col], errors='coerce')

# === Remove unnecessary columns ===
columns_to_remove = ['Nation', 'Squad', "Pos", "Unnamed: 0"]
stats.drop(columns=columns_to_remove, inplace=True, errors='ignore')
price.drop(columns=['Age', 'Team'], inplace=True, errors='ignore')

# === Merge datasets on 'Player' ===
df = stats.merge(price, on='Player', how='left')

# === Debugging: Check merged DataFrame ===
print("Merged df columns:", df.columns)
print("Merged df dtypes:", df.dtypes)

# === Convert Estimated Value to float ===
if 'Estimated Value' not in df.columns:
    raise ValueError("Column 'Estimated Value' not found in merged dataframe.")
df['Estimated Value'] = df['Estimated Value'].apply(convert_value)
df['Estimated Value'] = pd.to_numeric(df['Estimated Value'], errors='coerce')

# === Debugging: Check Estimated Value ===
print("Sample of Estimated Value:", df['Estimated Value'].head())
print("Estimated Value dtype:", df['Estimated Value'].dtype)

# === Replace string "N/a" with NaN ===
df.replace("N/a", pd.NA, inplace=True)

# === Handle missing values ===
df.dropna(subset=['Estimated Value'], inplace=True)  # Drop rows with missing target
numeric_columns = df.select_dtypes(include=['number']).columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())

# === Debugging: Check numeric columns ===
print("Numeric columns:", numeric_columns)

# === Save processed dataset ===
df.to_csv("Model_file\Random2.csv", index=False)

# === Select only numeric columns ===
df_numeric = df.select_dtypes(include=['number'])

# === Check for valid data ===
if df_numeric.empty or 'Estimated Value' not in df_numeric.columns:
    raise ValueError("No valid numeric data or target column found.")

# === Define features and target ===
X = df_numeric.drop(columns=['Estimated Value'])
y = df_numeric['Estimated Value']

# === Split into training and testing sets ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# === Train Random Forest Regressor ===
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# === Evaluate model ===
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Model Performance:")
print(f"Mean Absolute Error (MAE): {mae:,.2f}")
print(f"R² Score: {r2:.4f}")

# === Get feature importances ===
importances = model.feature_importances_
sorted_indices = importances.argsort()[::-1]
top_20_indices = sorted_indices[:20]
top_20_importances = importances[top_20_indices]
top_20_features = X.columns[top_20_indices]

# === Create DataFrame for top 20 features ===
top_20_feature_importance_df = pd.DataFrame({
    'Feature': top_20_features,
    'Importance': top_20_importances
})

# === Print and save top 20 features ===
print("\nTop 20 Feature Importances:")
print(top_20_feature_importance_df)
top_20_feature_importance_df.to_csv('top_20_feature_importance.csv', index=False)

# === Plot the top 20 most important features ===
plt.figure(figsize=(14, 10))
plt.barh(top_20_features, top_20_importances, color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Top 20 Feature Importance for Predicting Player Transfer Price')
plt.grid(True, axis='x', linestyle='--', alpha=0.7)
plt.yticks(rotation=0, ha='right')
plt.subplots_adjust(left=0.3)
plt.tight_layout()
plt.show()