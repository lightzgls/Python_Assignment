import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import matplotlib.pyplot as plt

# Load dataset
try:
    df = pd.read_csv("source code\\Model_file\\Random2.csv")
    print("Dataset loaded successfully.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()
df = df[df["Player"] != "Mohamed Salah"]

# Load important features
try:
    importance_df = pd.read_csv("source code\\Model_file\\top_20_feature_importance.csv")
    top_features = [
        "Age", "Shooting_SoT%", "Passing_Long_Cmp%", "Standard_MP", "Passing_Total_Cmp%",
        "Shooting_Dist", "Shooting_SoT/90", "Standard_xG", "Passing_Short_Cmp%", "Standard_Gls/90",
        "Standard_PrgP", "Possession_Succ%", "Possession_Tkld%", "Misc_Fls", "Passing_Medium_Cmp%",
        "Standard_PrgC", "Standard_xAG", "Standard_xG/90", "Passing_1/3", "Misc_Won%"
    ]
    print("Top features loaded successfully.")
except Exception as e:
    print(f"Error loading feature importance: {e}")
    exit()

# Filter dataset
required_columns = top_features + ['Estimated Value']
df = df[required_columns + ['Player']] if 'Player' in df.columns else df[required_columns]

# Handle missing values
df = df.dropna(subset=['Estimated Value'])
df[top_features] = df[top_features].fillna(df[top_features].median())

# Define X and y
X = df[top_features]
y = df['Estimated Value']

# Log-transform target
y_log = np.log1p(y)

# Split data
X_train, X_temp, y_train, y_temp = train_test_split(X, y_log, test_size=0.40, random_state=30)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.25, random_state=30)

print("Data split into training, validation, and testing sets.")

# Step 1: Randomized Search
model = xgb.XGBRegressor(objective='reg:squarederror', verbosity=0)
param_dist = {
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'n_estimators': [100, 300, 500, 700],
    'min_child_weight': [1, 3, 5, 7],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'gamma': [0, 1, 5],
    'reg_alpha': [0, 0.5, 1.0, 2.0],
    'reg_lambda': [1, 5, 10, 20]
}

print("\n🔹 Starting Randomized Search...")
random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_dist,
    n_iter=100,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    cv=3,
    verbose=2,
)
random_search.fit(X_train, y_train)
print("Randomized Search completed.")
best_random_params = random_search.best_params_
print("\nBest parameters from Randomized Search:", best_random_params)

# Step 2: Grid Search
param_grid = {
    'learning_rate': [best_random_params['learning_rate'] * 0.8, best_random_params['learning_rate'], best_random_params['learning_rate'] * 1.2],
    'n_estimators': [best_random_params['n_estimators'] - 100, best_random_params['n_estimators'], best_random_params['n_estimators'] + 100],
    'min_child_weight': [max(1, best_random_params['min_child_weight'] - 1), best_random_params['min_child_weight'], best_random_params['min_child_weight'] + 1],
    'subsample': [max(0.5, best_random_params['subsample'] - 0.1), best_random_params['subsample'], min(1.0, best_random_params['subsample'] + 0.1)],
    'colsample_bytree': [max(0.5, best_random_params['colsample_bytree'] - 0.1), best_random_params['colsample_bytree'], min(1.0, best_random_params['colsample_bytree'] + 0.1)],
    'gamma': [best_random_params['gamma']],
    'reg_alpha': [0, 0.5, 1.0, 2.0],
    'reg_lambda': [1, 5, 10, 20]
}

print("\n🔹 Starting Grid Search...")
grid_search = GridSearchCV(
    estimator=xgb.XGBRegressor(objective='reg:squarederror', verbosity=0),
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    cv=3,
    verbose=2
)
grid_search.fit(X_val, y_val)
print("Grid Search completed.")
best_model = grid_search.best_estimator_
print("\nBest Hyperparameters after fine tuning:", grid_search.best_params_)

# Early stopping
early_stopping_model = xgb.XGBRegressor(
    **grid_search.best_params_,
    objective='reg:squarederror',
    verbosity=0,
    early_stopping_rounds=50
)
early_stopping_model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

# Predictions
y_pred_log = early_stopping_model.predict(X_test)
y_pred = np.expm1(y_pred_log)  # Convert back to original scale
y_test_orig = np.expm1(y_test)

# Evaluate
y_train_pred_log = early_stopping_model.predict(X_train)
y_val_pred_log = early_stopping_model.predict(X_val)
train_r2 = r2_score(np.expm1(y_train), np.expm1(y_train_pred_log))
val_r2 = r2_score(np.expm1(y_val), np.expm1(y_val_pred_log))
mse = mean_squared_error(y_test_orig, y_pred)
mae = mean_absolute_error(y_test_orig, y_pred)
r2 = r2_score(y_test_orig, y_pred)

print(f"\nXGBoost Final Tuned Model Performance:")
print(f"Train R²: {train_r2:.4f}")
print(f"Validation R²: {val_r2:.4f}")
print(f"Test R²: {r2:.4f}")
print(f"MSE: {mse:.4f}")
print(f"MAE: {mae:.4f}")

# Cross-validation
cv_scores = cross_val_score(early_stopping_model, X, y_log, cv=5, scoring='r2')
print(f"Cross-validated R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Visualize feature importance
try:
    fig, ax = plt.subplots(figsize=(10, 8))
    xgb.plot_importance(early_stopping_model, max_num_features=20, ax=ax)
    plt.title("Feature Importance (Final Tuned XGBoost)")
    textstr = '\n'.join((
        f'Train R²: {train_r2:.4f}',
        f'Validation R²: {val_r2:.4f}',
        f'Test R²: {r2:.4f}',
        f'MSE: {mse:.4f}',
        f'MAE: {mae:.4f}',
        f'CV R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}'
    ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.7)
    plt.gcf().text(0.75, 0.25, textstr, fontsize=12, bbox=props)
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"Error plotting feature importance: {e}")

# Save model
with open("xgboost_model.pkl", "wb") as f:
    pickle.dump(early_stopping_model, f)