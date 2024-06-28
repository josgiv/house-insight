from flask import Flask, request, jsonify
from loader.load_ac import predict_energy_consumption as predict_energy_ac
from loader.load_tv import predict_tv_energy_consumption as predict_energy_tv
import pandas as pd

app = Flask(__name__)

# Route untuk prediksi konsumsi energi tahunan untuk televisi
@app.route('/predict-tv', methods=['POST'])
def predict_tv():
    # Mengambil input JSON dari POST request
    input_data = request.json
    
    if isinstance(input_data, dict):  # Memastikan input_data adalah dictionary
        # Konversi input data ke dalam DataFrame
        input_df = pd.DataFrame([input_data])  # Membuat DataFrame dari dictionary input_data
        
        # Lakukan prediksi konsumsi energi tahunan untuk televisi
        try:
            result_tv = predict_energy_tv(input_df)
            return jsonify({"predicted_energy_consumption": result_tv.tolist()}), 200
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid input data format. Expected JSON object."}), 400



# Route untuk prediksi konsumsi energi berdasarkan AC
@app.route('/predict-ac', methods=['POST'])
def predict_energy_route():
    try:
        input_data = request.json  # Mengambil input JSON dari POST request
        result_ac = predict_energy_ac(input_data)  # Memanggil fungsi prediksi energi AC
        return jsonify({"predicted_energy_consumption": result_ac.tolist()}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
