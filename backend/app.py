from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load your trained model, scaler, and imputer
model_bundle = joblib.load('hypertension_model.pkl')
model = model_bundle['model']
scaler = model_bundle['scaler']
imputer = model_bundle['imputer']

# Define prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Extract features in the correct order
        features = [
            data['male'],
            data['age'],
            data['currentSmoker'],
            data['cigsPerDay'],
            data['BPMeds'],
            data['diabetes'],
            data['totChol'],
            data['sysBP'],
            data['diaBP'],
            data['BMI'],
            data['heartRate'],
            data['glucose']
        ]

        # Convert to 2D array for sklearn
        features_array = np.array([features])
        # Impute missing values (if any)
        features_imputed = imputer.transform(features_array)
        # Scale features
        features_scaled = scaler.transform(features_imputed)
        # Predict
        prediction = model.predict(features_scaled)[0]

        result = 'High Risk' if prediction == 1 else 'Low Risk'
        return jsonify({'prediction': result})
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Run the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)