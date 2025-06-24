from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load your trained model
model = joblib.load('hypertension_model.pkl')

# Define prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Extract features
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

        # Predict
        prediction = model.predict([features])[0]

        result = 'High Risk' if prediction == 1 else 'Low Risk'
        return jsonify({'prediction': result})
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Run the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)