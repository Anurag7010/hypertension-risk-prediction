import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Load Data
df = pd.read_csv('hypertension.csv')

# Drop missing values
df.dropna(axis=0,inplace=True)



# 2. Split Features and Target
X = df.drop('Risk', axis=1)
y = df['Risk']

# 3. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train RandomForest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 5. Evaluate
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# 6. Export Model
joblib.dump(rf, 'hypertension_model.pkl')
print("Model saved as hypertension_model.pkl")
