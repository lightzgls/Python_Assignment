import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=30)
print("Data split into training and testing sets.")

# === Step 1: Randomized Search for rough tuning ===
model = xgb.XGBRegressor(
    objective='reg:squarederror', 
    verbosity=0
)

param_dist = {
    'learning_rate': [0.01, 0.02, 0.03 ,0.05, 0.1, 0.2, 0.3],
    'n_estimators': [100, 200, 300, 500, 800],
    'min_child_weight': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'subsample': [0.4,0.5,0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.4,0.5,0.6, 0.7, 0.8, 0.9, 1.0],
    'gamma': [0, 1, 5],
    'reg_alpha': [0, 0.1, 0.5],
    'reg_lambda': [1, 5, 10]
}

print("\n🔹 Starting Randomized Search (rough tuning)...")
random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_dist,
    n_iter=100,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    cv=3,
    verbose=2,
)

try:
    random_search.fit(X_train, y_train)
    print("Randomized Search completed.")
except Exception as e:
    print(f"Error during Randomized Search: {e}")
    exit()

best_random_params = random_search.best_params_
print("\nBest parameters from Randomized Search:", best_random_params)

# === Step 2: Grid Search for fine tuning ===
param_grid = {
    'learning_rate': [best_random_params['learning_rate'] * 0.8, best_random_params['learning_rate'], best_random_params['learning_rate'] * 1.2],
    'n_estimators': [best_random_params['n_estimators'] - 100, best_random_params['n_estimators'], best_random_params['n_estimators'] + 100],
    'min_child_weight': [max(1, best_random_params['min_child_weight'] - 1), best_random_params['min_child_weight'], best_random_params['min_child_weight'] + 1],
    'subsample': [max(0.5, best_random_params['subsample'] - 0.1), best_random_params['subsample'], min(1.0, best_random_params['subsample'] + 0.1)],
    'colsample_bytree': [max(0.5, best_random_params['colsample_bytree'] - 0.1), best_random_params['colsample_bytree'], min(1.0, best_random_params['colsample_bytree'] + 0.1)],
    'gamma': [best_random_params['gamma']],
    'reg_alpha': [best_random_params['reg_alpha']],
    'reg_lambda': [best_random_params['reg_lambda']]
}

print("\n🔹 Starting Grid Search (fine tuning)...")
grid_search = GridSearchCV(
    estimator=xgb.XGBRegressor(objective='reg:squarederror', verbosity=0),
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    cv=3,
    verbose=2
)

try:
    grid_search.fit(X_train, y_train)
    print("Grid Search completed.")
except Exception as e:
    print(f"Error during Grid Search: {e}")
    exit()

# === Final best model ===
# Best Hyperparameters after fine tuning: {'colsample_bytree': 0.6, 'gamma': 5, 'learning_rate': 0.08000000000000002, 'min_child_weight': 1, 'n_estimators': 200, 'reg_alpha': 0, 'reg_lambda': 1, 'subsample': 0.8}
# XGBoost Final Tuned Model Performance:
# MSE: 142375383054921.7500
# MAE: 9219452.3278
# R²: 0.6754
best_model = grid_search.best_estimator_
print("\nBest Hyperparameters after fine tuning:", grid_search.best_params_)

# === Make predictions on test set ===
y_pred = best_model.predict(X_test)

# === Evaluate the model ===
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nXGBoost Final Tuned Model Performance:")
print(f"MSE: {mse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R²: {r2:.4f}")

# === Visualize feature importance with performance metrics ===
try:
    fig, ax = plt.subplots(figsize=(10, 8))
    xgb.plot_importance(best_model, max_num_features=20, ax=ax)
    plt.title("Feature Importance (Final Tuned XGBoost)")

    # Add performance metrics as a textbox inside the plot
    textstr = '\n'.join((
        f'MSE: {mse:.4f}',
        f'MAE: {mae:.4f}',
        f'R²: {r2:.4f}',
    ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.7)
    plt.gcf().text(0.75, 0.25, textstr, fontsize=12, bbox=props)

    plt.tight_layout()
    plt.savefig('Model_file/xgboost_tuned_feature_importance.png.png')
    plt.show()
except Exception as e:
    print(f"Error plotting feature importance: {e}")
