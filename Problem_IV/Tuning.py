import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import matplotlib.pyplot as plt

# === Load dataset ===
try:
    df = pd.read_csv("Model_file/random2.csv")
    print("Dataset loaded successfully.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# === Load important features ===
try:
    importance_df = pd.read_csv("Model_file/top_20_feature_importance.csv")
    top_features = importance_df['Feature'].tolist()
    print("Top features loaded successfully.")
except Exception as e:
    print(f"Error loading feature importance: {e}")
    exit()

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split into training and testing sets.")

# === Define the XGBoost model ===
model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42, verbosity=0)

# === Define the hyperparameter grid ===
param_grid = {
    'learning_rate': [0.01, 0.05,0.1,0.3],        # Step size shrinkage
    'n_estimators': [100, 200, 500, 1000],          # Number of boosting rounds
    'max_depth': [3, 6, 10],                  # Maximum tree depth
    'min_child_weight': [1, 5, 10],           # Minimum sum of instance weight
    'subsample': [0.7, 0.8, 1.0],             # Fraction of samples used per tree
    'colsample_bytree': [0.7, 0.8, 1.0]       # Fraction of features used per tree
}

# === Set up GridSearchCV ===
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,                              # 3-fold cross-validation
    scoring='neg_mean_squared_error',  # Optimize for MSE
    n_jobs=-1,                         # Use all available cores
    verbose=2                          # Print progress
)

# === Fit GridSearchCV ===
print("🔹 Starting hyperparameter tuning for XGBoost...")
try:
    grid_search.fit(X_train, y_train)
    print("Hyperparameter tuning completed.")
except Exception as e:
    print(f"Error during grid search: {e}")
    exit()

# === Best hyperparameters ===
print("Best Hyperparameters:", grid_search.best_params_)

# === Best model ===
best_model = grid_search.best_estimator_

# === Make predictions on test set ===
y_pred = best_model.predict(X_test)

# === Evaluate the model ===
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nXGBoost Tuned Model Performance:")
print(f"MSE: {mse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R²: {r2:.4f}")

# === Save the tuned model ===
try:
    with open('xgboost_tuned_model.pkl', 'wb') as file:
        pickle.dump(best_model, file)
    print("💾 Tuned model saved as 'xgboost_tuned_model.pkl'")
except Exception as e:
    print(f"Error saving model: {e}")

# === Save best hyperparameters ===
try:
    hyperparams_df = pd.DataFrame([grid_search.best_params_])
    hyperparams_df.to_csv('xgboost_best_hyperparameters.csv', index=False)
    print("Best hyperparameters saved to 'xgboost_best_hyperparameters.csv'")
except Exception as e:
    print(f"Error saving hyperparameters: {e}")

# === Visualize feature importance ===
try:
    xgb.plot_importance(best_model, max_num_features=10)  # Show top 10 features
    plt.title("Feature Importance (Tuned XGBoost)")
    plt.tight_layout()
    plt.savefig('xgboost_tuned_feature_importance.png')
    plt.show()
except Exception as e:
    print(f"Error plotting feature importance: {e}")

# === Save feature importance to a file ===
try:
    importance = best_model.get_booster().get_score(importance_type='weight')
    importance_df = pd.DataFrame({
        'Feature': list(importance.keys()),
        'Importance': list(importance.values())
    }).sort_values(by='Importance', ascending=False)
    importance_df.to_csv('xgboost_tuned_feature_importance.csv', index=False)
    print("Feature importance saved to 'xgboost_tuned_feature_importance.csv'")
except Exception as e:
    print(f"Error saving feature importance: {e}")