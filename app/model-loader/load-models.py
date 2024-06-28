import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
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

# Fungsi untuk melakukan preprocessing input data
def preprocess_input(data, model_type):
    # Definisi kolom numerik dan kategorikal untuk masing-masing tipe model
    numeric_columns = {
        'air_cleaner': ['room_size_sq_ft', 'dust_free_clean_air_delivery', 'smoke_free_clean_air_delivery',
                        'pollen_free_clean_air_delivery', 'dust_free_clean_air_delivery_1', 
                        'smoke_free_clean_air_delivery_1', 'pollen_free_clean_air_delivery_1',
                        'partial_on_mode_power_watts', 'ozone_emissions_ppb'],
        'air_conditioners': ['height_inches', 'width_inches', 'depth_inches', 'weight_lbs',
                             'cooling_capacity_btu_hour', 'voltage_volts', 'combined_energy_efficiency_ratio_ceer',
                             'percent_less_energy_use_than_us_federal_standard',],
        'refrigerators': ['Height (in)', 'Width (in)', 'Capacity (Total Volume) (ft3)',
                          'Adjusted Volume (ft3)', 'US Federal Standard (kWh/yr)',
                          'Percent Less Energy Use than US Federal Standard'],
        'televisions': ['Display Size (in)'],
    }
    
    categorical_columns = {
        'air_cleaner': ['technology_types', 'filter_1_type', 'filter_2_type', 'filter_3_type', 'filter_4_type',
                        'network_capability'],
        'air_conditioners': ['type', 'installation_mounting_type', 'heating_mode',
                             'variable_speed_compressor', 'low_noise', 'refrigerant_type', 'refrigerant_with_gwp'],
        'refrigerators': ['Type', 'Compact', 'Thru the Door Dispenser', 'Ice Maker', 'Connected Functionality'],
        'televisions': ['Brand Name', 'Display Type', 'Backlight Technology Type',
                        'Resolution Format', 'High Contrast Ratio (HCR) Display',
                        'Ethernet Supported', 'Features', 'Auto Brightness'],
    }
    
    if model_type not in numeric_columns or model_type not in categorical_columns:
        raise ValueError("Model type not recognized.")
    
    # Memastikan semua kolom yang dibutuhkan ada
    required_columns = numeric_columns[model_type] + categorical_columns[model_type]
    missing_columns = set(required_columns) - set(data.columns)
    
    if missing_columns:
        raise ValueError(f"Missing columns in input data: {missing_columns}")
    
    # Urutan kolom harus sesuai dengan yang diharapkan
    expected_columns = numeric_columns[model_type] + categorical_columns[model_type]
    data = data[expected_columns]
    
    # Mengisi nilai NaN dengan median untuk kolom numerik
    for col in numeric_columns[model_type]:
        data[col] = data[col].fillna(data[col].median())
    
    # Mengisi nilai NaN dengan modus untuk kolom kategorikal
    for col in categorical_columns[model_type]:
        data[col] = data[col].fillna(data[col].mode()[0])
    
    # Scaling data numerik dengan StandardScaler
    scaler = StandardScaler()
    data[numeric_columns[model_type]] = scaler.fit_transform(data[numeric_columns[model_type]])
    
    # Encoding kolom kategorikal (jika diperlukan)
    # Di sini perlu menggunakan teknik encoding seperti One-Hot Encoding atau Label Encoding
    # Sesuaikan dengan format yang diterima oleh model Anda
    
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
        'type': ['Split System'],  # Contoh tipe AC (misalnya: Split System, Window AC, dsb)
        'installation_mounting_type': ['Wall Mounted'],  # Contoh tipe pemasangan AC (misalnya: Wall Mounted, Floor Standing, dsb)
        'heating_mode': ['Yes'],  # Contoh apakah AC memiliki mode pemanas atau tidak
        'variable_speed_compressor': ['Yes'],  # Contoh apakah AC menggunakan kompresor variabel kecepatan atau tidak
        'low_noise': ['Yes'],  # Contoh apakah AC memiliki tingkat kebisingan rendah atau tidak
        'refrigerant_type': ['R-410A'],  # Contoh jenis refrigeran yang digunakan oleh AC
        'refrigerant_with_gwp': [2.0],  # Contoh nilai GWP (Global Warming Potential) dari refrigeran AC
        'combined_energy_efficiency_ratio_ceer': [16.0],  # Contoh CEER (Combined Energy Efficiency Ratio) AC
        'percent_less_energy_use_than_us_federal_standard': [30.0],  # Contoh persentase penggunaan energi yang lebih sedikit dibandingkan standar federal AS
    }
    
    # Konversi input_data ke DataFrame
    input_df = pd.DataFrame(input_data)
    
    # Prediksi untuk AC
    model_type = 'air_conditioners'
    result = predict(model_type, input_df)
    print(f"Predicted Annual Energy Consumption (kWh/yr): {result}")
