# app/loader/load_ac.py

import pickle
from flask import Flask, jsonify, request
import pandas as pd
import os
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Paths untuk model .pkl
base_path = os.path.dirname(__file__)  # Mengambil path direktori saat ini
model_paths = {
    'air_conditioners': os.path.join(base_path, '../models-pickle/house-energy/air-conditioners.pkl'),
}

# Fungsi untuk memuat semua model
def load_models():
    models = {}
    for key, path in model_paths.items():
        with open(path, 'rb') as file:
            models[key] = pickle.load(file)
    return models

# Fungsi untuk preprocessing input data
def preprocess_input(data, model_type):
    numeric_columns = {
        'air_conditioners': ['height_inches', 'width_inches', 'depth_inches', 'weight_lbs',
                             'cooling_capacity_btu_hour', 'voltage_volts'],
        'air_cleaner': [],
        'refrigerators': [],
        'televisions': []
    }
    
    categorical_columns = {
        'air_conditioners': ['type', 'installation_mounting_type', 'heating_mode', 'low_noise'],
        'air_cleaner': [],
        'refrigerators': [],
        'televisions': []
    }
    
    if model_type not in numeric_columns or model_type not in categorical_columns:
        raise ValueError("Model type not recognized.")

    for col in numeric_columns[model_type]:
        if col not in data.columns:
            data[col] = data[col].mean()  # Gunakan nilai rerata dari data training
    
    expected_columns = numeric_columns[model_type] + categorical_columns[model_type]
    data = data[expected_columns]
    
    return data

# Fungsi untuk prediksi berdasarkan model yang dipilih
def predict(model_type, input_data):
    models = load_models()
    
    input_data_processed = preprocess_input(input_data.copy(), model_type)
    
    if model_type in models:
        model = models[model_type]
        y_pred = model.predict(input_data_processed)
        return y_pred
    else:
        raise ValueError("Model type not recognized.")

# Route untuk melakukan prediksi AC
@app.route('/predict-ac', methods=['POST'])
def predict_ac():
    try:
        input_data = request.json
        
        # Logging data input
        logging.info(f"Received input data: {input_data}")
        
        # Konversi input_data ke DataFrame
        input_df = pd.DataFrame(input_data)
        
        # Prediksi untuk AC
        model_type = 'air_conditioners'
        result_ac = predict(model_type, input_df)
        
        return jsonify({"result": result_ac.tolist()}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
