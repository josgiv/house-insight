from flask import Flask, request, jsonify
import os
import pickle
import pandas as pd

app = Flask(__name__)

# Paths untuk model .pkl
base_path = os.path.dirname(__file__)  # Mengambil path direktori saat ini
model_path = os.path.join(base_path, 'models-pickle/house-energy/televisions.pkl')

# Fungsi untuk memuat model televisi
def load_tv_model():
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Fungsi untuk preprocessing input data televisi
def preprocess_tv_input(input_data):
    # Menentukan urutan kolom yang diharapkan
    expected_columns = [
        'Brand Name', 'Display Type', 'Backlight Technology Type',
        'Diagonal Viewable Screen Size (in.)', 'Resolution Format',
        'High Contrast Ratio (HCR) Display', 'Physical Data Ports Available',
        'Ethernet Supported', 'Low Power Wireless Technologies Supported',
        'Automatic Brightness Control', 'Auto Brightness'
    ]
    
    # Memastikan urutan dan nama kolom sesuai dengan yang diharapkan
    input_data = input_data[expected_columns]
    
    return input_data

# Fungsi untuk melakukan prediksi energi tahunan untuk televisi
def predict_tv_energy_consumption(input_data):
    # Memuat model televisi
    tv_model = load_tv_model()
    
    # Preprocessing input data
    input_data_processed = preprocess_tv_input(input_data.copy())
    
    # Prediksi menggunakan model televisi
    try:
        y_pred = tv_model.predict(input_data_processed)
        return y_pred
    except Exception as e:
        return str(e)  # Mengembalikan pesan kesalahan jika terjadi kesalahan pada prediksi

# Route untuk prediksi konsumsi energi tahunan untuk televisi
@app.route('/predict-tv', methods=['POST'])
def predict_tv():
    # Mengambil input JSON dari POST request
    input_data = request.json
    
    if input_data:
        # Konversi input data ke dalam DataFrame
        input_df = pd.DataFrame(input_data)
        
        # Lakukan prediksi konsumsi energi tahunan untuk televisi
        try:
            result_tv = predict_tv_energy_consumption(input_df)
            return jsonify({"predicted_energy_consumption": result_tv.tolist()}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No input data provided."}), 400

if __name__ == '__main__':
    app.run(debug=True)
