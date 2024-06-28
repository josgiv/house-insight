import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

# Paths untuk model .pkl
base_path = os.path.dirname(__file__)  # Mengambil path direktori saat ini
model_paths = {
    'air_cleaner': os.path.join(base_path, '../models-pickle/house-energy/air-cleaner.pkl'),
    'air_conditioners': os.path.join(base_path, '../models-pickle/house-energy/air-conditioners.pkl'),
    'refrigerators': os.path.join(base_path, '../models-pickle/house-energy/refrigerators.pkl'),
    'televisions': os.path.join(base_path, '../models-pickle/house-energy/televisions.pkl'),
}

# Fungsi untuk memuat semua model
def load_models():
    models = {}
    for key, path in model_paths.items():
        with open(path, 'rb') as file:
            models[key] = pickle.load(file)
    return models


from sklearn.preprocessing import LabelEncoder

def preprocess_input(data, model_type):
    # Definisi kolom numerik dan kategorikal untuk masing-masing tipe model
    numeric_columns = {
        'air_conditioners': ['height_inches', 'width_inches', 'depth_inches', 'weight_lbs',
                             'cooling_capacity_btu_hour', 'voltage_volts'],
        'air_cleaner': [],  # Tambahkan kolom numerik sesuai dengan model air_cleaner
        'refrigerators': [],  # Tambahkan kolom numerik sesuai dengan model refrigerators
        'televisions': []  # Tambahkan kolom numerik sesuai dengan model televisions
    }
    
    categorical_columns = {
        'air_conditioners': ['type', 'installation_mounting_type', 'heating_mode', 'low_noise'],
        'air_cleaner': [],  # Tambahkan kolom kategorikal sesuai dengan model air_cleaner
        'refrigerators': [],  # Tambahkan kolom kategorikal sesuai dengan model refrigerators
        'televisions': []  # Tambahkan kolom kategorikal sesuai dengan model televisions
    }
    
    if model_type not in numeric_columns or model_type not in categorical_columns:
        raise ValueError("Model type not recognized.")

    
    # Menambahkan kolom yang hilang dengan nilai default atau rata-rata
    for col in numeric_columns[model_type]:
        if col not in data.columns:
            data[col] = data[col].mean()  # Gunakan nilai rerata dari data training
    
    # Memastikan urutan kolom sesuai dengan yang diharapkan
    expected_columns = numeric_columns[model_type] + categorical_columns[model_type]
    data = data[expected_columns]
    
    return data

# Fungsi untuk prediksi berdasarkan model yang dipilih
def predict(model_type, input_data):
    models = load_models()
    
    # Preprocessing input data
    input_data_processed = preprocess_input(input_data.copy(), model_type)
    
    # Prediksi menggunakan model yang sesuai
    if model_type in models:
        model = models[model_type]
        y_pred = model.predict(input_data_processed)
        return y_pred
    else:
        raise ValueError("Model type not recognized.")

if __name__ == "__main__":
    # Contoh input data untuk AC
    input_data = {
        'height_inches': [30],  # Contoh tinggi AC dalam inci
        'width_inches': [24],   # Contoh lebar AC dalam inci
        'depth_inches': [12],   # Contoh kedalaman AC dalam inci
        'weight_lbs': [100],    # Contoh berat AC dalam lbs
        'cooling_capacity_btu_hour': [12000],  # Contoh kapasitas pendinginan AC dalam BTU/jam
        'voltage_volts': [220],  # Contoh tegangan AC dalam volt
        'type': ['Window'],  # Contoh tipe AC (misalnya: Split System, Window AC, dsb)
        'installation_mounting_type': ['Does Not Straddle Window or Windowsill'],  # Contoh tipe pemasangan AC (misalnya: Wall Mounted, Floor Standing, dsb)
        'heating_mode': ['Yes'],  # Contoh apakah AC memiliki mode pemanas atau tidak
        'low_noise': ['Yes'],  # Contoh apakah AC memiliki tingkat kebisingan rendah atau tidak
    }
    
    # Konversi input_data ke DataFrame
    input_df = pd.DataFrame(input_data)
    
    # Prediksi untuk AC
    model_type = 'air_conditioners'
    result_ac = predict(model_type, input_df)
    print(f"Predicted Annual Energy Consumption (kWh/yr): {result_ac}")
