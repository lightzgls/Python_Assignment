import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt

# === Load dataset ===
df = pd.read_csv("source code\\Model_file\\Random2.csv")

# === Load important features ===
importance_df = pd.read_csv("source code\\Model_file\\top_20_feature_importance.csv")
top_features = ['Age',
             
'Standard_MP', 'Standard_Starts','Standard_Min',

'Standard_Gls', 'Standard_Ast','Standard_CrdY', 'Standard_CrdR',

'Standard_xG','Standard_xAG','Standard_PrgC', 'Standard_PrgP',
'Standard_PrgR',

'Standard_Gls/90', 'Standard_Ast/90','Standard_xG/90', 'Standard_xAG/90',

'Goalkeeping_GA90','Goalkeeping_Save%','Goalkeeping_CS%','Goalkeeping_Penalty_Save%',

'Shooting_SoT%','Shooting_SoT/90','Shooting_G/Sh','Shooting_Dist',

'Passing_Cmp','Passing_Total_Cmp%','Passing_TotDist','Passing_Short_Cmp%','Passing_Medium_Cmp%',
'Passing_Long_Cmp%','Passing_KP', 'Passing_1/3', 'Passing_PPA',
'Passing_CrsPA', 'Passing_PrgP',

'GCA_SCA', 'GCA_SCA90','GCA_GCA', 'GCA_GCA90',

'Defense_Tkl','Defense_TklW','Defense_Att','Defense_Lost',
'Defense_Blocks', 'Defense_Sh', 'Defense_Pass', 'Defense_Int',

'Possession_Touches', 'Possession_Def Pen', 'Possession_Def 3rd',
'Possession_Mid 3rd', 'Possession_Att 3rd', 'Possession_Att Pen',
'Possession_Att','Possession_Succ%','Possession_Tkld%',
'Possession_Carries', 'Possession_PrgDist',
'Possession_PrgC', 'Possession_1/3', 'Possession_CPA', 'Possession_Mis',
'Possession_Dis','Possession_Rec', 'Possession_PrgR',

'Misc_Fls', 'Misc_Fld', 'Misc_Off', 'Misc_Crs','Misc_Recov',
'Misc_Won','Misc_Lost', 'Misc_Won%']

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15,random_state=50)

# === Define models ===
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1),
    "Random Forest": RandomForestRegressor(random_state=0),
    "XGBoost": xgb.XGBRegressor(random_state=0, verbosity=0)
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
