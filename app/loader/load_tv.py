from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Paths untuk model .pkl
base_path = os.path.dirname(__file__)  # Mengambil path direktori saat ini
model_paths = {
    'air_conditioners': os.path.join(base_path, '../models-pickle/house-energy/.pkl'),
}

# Fungsi untuk memuat semua model
def load_models():
    models = {}
    for key, path in model_paths.items():
        with open(path, 'rb') as file:
            models[key] = pickle.load(file)
    return models

# Fungsi untuk preprocessing input data
def preprocess_input(data):
    # Definisikan kolom numerik dan kategorikal yang digunakan dalam model
    numeric_columns = ['Diagonal Viewable Screen Size (in.)', 'Resolution Format', 'Physical Data Ports Available']
    categorical_columns = ['Brand Name', 'Display Type', 'Backlight Technology Type',
                           'High Contrast Ratio (HCR) Display', 'Ethernet Supported',
                           'Low Power Wireless Technologies Supported', 'Automatic Brightness Control', 'Auto Brightness']

    # Buat salinan data untuk diproses
    processed_data = data.copy()

    # Proses kolom numerik (misalnya, jika perlu, ubah tipe data atau lakukan normalisasi)
    for col in numeric_columns:
        if col in processed_data:
            processed_data[col] = pd.to_numeric(processed_data[col], errors='coerce')  # Ubah ke numerik jika diperlukan

    # Encode kolom kategorikal (misalnya, menggunakan teknik one-hot encoding atau label encoding)
    for col in categorical_columns:
        if col in processed_data:
            processed_data = pd.get_dummies(processed_data, columns=[col], drop_first=True)

    return processed_data

# Fungsi untuk prediksi berdasarkan model yang dipilih
def predict(model_type, input_data):
    models = load_models()

    input_data_processed = preprocess_input(input_data)
    
    if model_type in models:
        model = models[model_type]
        y_pred = model.predict(input_data_processed)
        return y_pred
    else:
        raise ValueError("Model type not recognized.")

# Route untuk melakukan prediksi AC
@app.route('/predict-tv', methods=['POST'])
def predict_energy_consumption():
    try:
        input_data = request.json
        
        # Konversi input_data ke DataFrame
        input_df = pd.DataFrame([input_data])  # Memasukkan dalam list untuk memastikan input_data adalah list of dict
        
        # Prediksi untuk AC
        model_type = 'air_conditioners'
        result_prediction = predict(model_type, input_df)
        
        return jsonify({"predicted_energy_consumption": result_prediction.tolist()}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
