import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib

# 1. Load Data
df = pd.read_csv('hypertension.csv')

# 2. Handle missing values
imputer = SimpleImputer(strategy='mean')
X = df.drop('Risk', axis=1)
y = df['Risk']
X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# 3. Feature Scaling
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X_imputed), columns=X.columns)

# 4. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# 5. Try Multiple Algorithms
def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_pred)
    print(f"\nModel: {model.__class__.__name__}")
    print(f"Accuracy: {acc:.4f}")
    print(f"ROC-AUC: {roc:.4f}")
    print(classification_report(y_test, y_pred))
    return acc, roc, model

models = [
    RandomForestClassifier(n_estimators=100, random_state=42),
    GradientBoostingClassifier(n_estimators=100, random_state=42),
    LogisticRegression(max_iter=1000, random_state=42)
]

results = []
for model in models:
    acc, roc, fitted_model = evaluate_model(model, X_train, y_train, X_test, y_test)
    results.append((acc, roc, fitted_model))

# 6. Select the best model (by ROC-AUC, then accuracy)
best_model = sorted(results, key=lambda x: (x[1], x[0]), reverse=True)[0][2]

print(f"\nSelected best model: {best_model.__class__.__name__}")

# 7. Feature Importances (if available)
if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
    for name, importance in zip(X.columns, importances):
        print(f"{name}: {importance:.4f}")
elif hasattr(best_model, 'coef_'):
    for name, coef in zip(X.columns, best_model.coef_[0]):
        print(f"{name}: {coef:.4f}")

# 8. Save the best model and scaler/imputer
joblib.dump({'model': best_model, 'scaler': scaler, 'imputer': imputer}, 'hypertension_model.pkl')
print("Model and preprocessors saved as hypertension_model.pkl")
