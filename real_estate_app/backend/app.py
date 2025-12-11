from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, resources={r"/api/*": {"origins": cors_origins}})

MODEL_PATH = 'artifacts_v2/random_forest_model.pkl'
PREPROCESSOR_PATH = 'artifacts_v2/preprocessor.pkl'

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(PREPROCESSOR_PATH, 'rb') as f:
        preprocessor = pickle.load(f)
    print("✅ Model and preprocessor loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    preprocessor = None

@app.route('/api/health', methods=['GET'])
def health_check():
    status = {
        'status': 'healthy' if model else 'unhealthy',
        'model_loaded': model is not None,
        'service': 'Myanmar Real Estate Price Predictor'
    }
    return jsonify(status)

@app.route('/api/predict', methods=['POST'])
def predict_price():
    if model is None or preprocessor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        property_type = data.get('property_type', 'Condo')
        township = data.get('township', 'Kamayut')
        bedrooms = int(data.get('bedrooms', 3))
        property_size = float(data.get('property_size', 2000))
        
        input_data = pd.DataFrame([{
            'property_type': property_type,
            'township': township,
            'bedrooms': bedrooms,
            'property_size': property_size
        }])
        
        print(f"📊 Prediction request: {property_type} in {township}, {bedrooms} bedrooms, {property_size} sqft")
        
        features = preprocessor.transform(input_data)
        prediction_log = model.predict(features)[0]
        predicted_price = np.expm1(prediction_log)
        
        print(f"💰 Predicted price: ${predicted_price:.2f}")
        
        return jsonify({
            'success': True,
            'prediction': round(float(predicted_price), 2),
            'currency': 'USD',
            'input_details': {
                'property_type': property_type,
                'township': township,
                'bedrooms': bedrooms,
                'property_size': f"{property_size:,} sqft"
            }
        })
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({'error': 'Prediction failed. Please check your input.'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    print(f"🚀 Backend API running on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)