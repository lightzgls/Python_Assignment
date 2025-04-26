import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, RandomizedSearchCV
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print("Data split into training and testing sets.")

# === Define the XGBoost model ===
model = xgb.XGBRegressor(objective='reg:squarederror', verbosity=0)

# === Define the hyperparameter grid for RandomizedSearchCV ===
param_dist = {
    'learning_rate': [0.01, 0.02, 0.03, 0.1, 0.2, 0.3],
    'n_estimators': [100, 200, 500, 1000],
    'min_child_weight': [1, 5, 8],
    'subsample': [0.7, 0.8, 1.0],
    'colsample_bytree': [0.7, 0.8, 1.0],
    'gamma': [0, 1, 5],
    'reg_alpha': [0.1, 1, 5],
    'reg_lambda': [1, 5, 10]
}

# === Set up RandomizedSearchCV ===
random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_dist,
    n_iter=250,
    cv=3,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    verbose=2,
)

# === Fit RandomizedSearchCV ===
print("🔹 Starting hyperparameter tuning for XGBoost...")
try:
    random_search.fit(X_train, y_train)
    print("Hyperparameter tuning completed.")
except Exception as e:
    print(f"Error during random search: {e}")
    exit()

# === Best hyperparameters ===
print("Best Hyperparameters:", random_search.best_params_)

# === Best model ===
best_model = random_search.best_estimator_

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
    print("💾 Tuned model saved as 'Model_file\xgboost_tuned_model.pkl'")
except Exception as e:
    print(f"Error saving model: {e}")

# === Save best hyperparameters ===
try:
    hyperparams_df = pd.DataFrame([random_search.best_params_])
    hyperparams_df.to_csv('Model_file\xgboost_best_hyperparameters.csv', index=False)
    print("Best hyperparameters saved to 'Model_file\xgboost_best_hyperparameters.csv'")
except Exception as e:
    print(f"Error saving hyperparameters: {e}")

# === Visualize feature importance with performance metrics ===
try:
    fig, ax = plt.subplots(figsize=(10, 8))
    xgb.plot_importance(best_model, max_num_features=10, ax=ax)
    plt.title("Feature Importance (Tuned XGBoost)")

    # Add performance metrics as a textbox inside the plot
    textstr = '\n'.join((
        f'MSE: {mse:.4f}',
        f'MAE: {mae:.4f}',
        f'R²: {r2:.4f}',
    ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.7)
    plt.gcf().text(0.75, 0.25, textstr, fontsize=12, bbox=props)

    plt.tight_layout()
    plt.savefig('Model_file\xgboost_tuned_feature_importance.png')
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
    importance_df.to_csv('Model_file\xgboost_tuned_feature_importance.csv', index=False)
    print("Feature importance saved to 'Model_file\xgboost_tuned_feature_importance.csv'")
except Exception as e:
    print(f"Error saving feature importance: {e}")
