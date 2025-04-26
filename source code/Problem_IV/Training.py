import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt

# === Load dataset ===
df = pd.read_csv("Model_file\Random2.csv")

# === Load important features ===
importance_df = pd.read_csv("Model_file/top_20_feature_importance.csv")
top_features = importance_df['Feature'].tolist()

# === Filter dataset ===
required_columns = top_features + ['Estimated Value']
df = df[required_columns + ['Player']] if 'Player' in df.columns else df[required_columns]

# === Handle missing values ===
df = df.dropna(subset=['Estimated Value'])
df[top_features] = df[top_features].fillna(df[top_features].median())

# === Define X and y ===
X = df[top_features]
y = df['Estimated Value']

# === Split data into training and testing ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# === Define models ===
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1),
    "Random Forest": RandomForestRegressor(random_state=42),
    "XGBoost": xgb.XGBRegressor(random_state=42, verbosity=0)
}

# === Initialize metrics for plotting ===
metrics = {
    'Model': [],
    'MSE': [],
    'MAE': [],
    'R²': []
}

# === Train, Evaluate, Save models ===
for name, model in models.items():
    print(f"\n🔹 Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Store metrics for later plotting
    metrics['Model'].append(name)
    metrics['MSE'].append(mse)
    metrics['MAE'].append(mae)
    metrics['R²'].append(r2)

    # Print the model scores to the terminal
    print(f"{name} - MSE: {mse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")

    # Save the trained model
    filename = f"{name.lower().replace(' ', '_')}_model.pkl"
    joblib.dump(model, filename)
    print(f"💾 Model saved as {filename}")

# === Plotting comparison of models ===
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot MSE
axes[0].bar(metrics['Model'], metrics['MSE'], color='skyblue')
axes[0].set_title('Mean Squared Error (MSE)')
axes[0].set_ylabel('MSE')
axes[0].tick_params(axis='x', rotation=45)

# Plot MAE
axes[1].bar(metrics['Model'], metrics['MAE'], color='lightgreen')
axes[1].set_title('Mean Absolute Error (MAE)')
axes[1].set_ylabel('MAE')
axes[1].tick_params(axis='x', rotation=45)

# Plot R²
axes[2].bar(metrics['Model'], metrics['R²'], color='salmon')
axes[2].set_title('R² Score')
axes[2].set_ylabel('R²')
axes[2].tick_params(axis='x', rotation=45)

# Show the plots
plt.tight_layout()
plt.show()
