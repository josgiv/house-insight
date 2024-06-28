import requests
import subprocess
import streamlit as st
import pickle
import pandas as pd
import os

from sklearn.preprocessing import StandardScaler, LabelEncoder

# Paths untuk model .pkl
base_path = os.path.dirname(__file__)  # Mengambil path direktori saat ini
model_paths = {
    'air_conditioners': os.path.join(base_path, 'app/models-pickle/house-energy/air-conditioners.pkl'),
}

# Fungsi untuk memuat semua model
def load_models():
    models = {}
    for key, path in model_paths.items():
        with open(path, 'rb') as file:
            models[key] = pickle.load(file)
    return models

# Fungsi untuk memproses input data sesuai dengan tipe model
def preprocess_input(data, model_type):
    # Definisi kolom numerik dan kategorikal untuk masing-masing tipe model
    numeric_columns = {
        'air_conditioners': ['height_inches', 'width_inches', 'depth_inches', 'weight_lbs',
                             'cooling_capacity_btu_hour', 'voltage_volts'],
        'televisions': ['Diagonal Viewable Screen Size (in.)', 'Physical Data Ports Available'],
        # Tambahkan kolom numerik sesuai dengan model lainnya jika diperlukan
    }
    
    categorical_columns = {
        'air_conditioners': ['type', 'installation_mounting_type', 'heating_mode', 'low_noise'],
        'televisions': ['Resolution Format', 'Display Type', 'Backlight Technology Type', 
                        'High Contrast Ratio (HCR) Display', 'Ethernet Supported',
                        'Low Power Wireless Technologies Supported', 'Automatic Brightness Control', 
                        'Auto Brightness'],
        # Tambahkan kolom kategorikal sesuai dengan model lainnya jika diperlukan
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

# Streamlit UI untuk input spesifikasi perangkat elektronik
def streamlit_ui():
    st.set_page_config(page_title='Prediksi Konsumsi Listrik Rumah', page_icon=':electric_plug:')
    
    st.title('Prediksi Konsumsi Listrik Rumah')
    st.markdown(
        'Aplikasi ini bertujuan untuk memprediksi konsumsi listrik berdasarkan spesifikasi perangkat elektronik yang dipilih. '
        'Silakan pilih tipe perangkat elektronik dan masukkan spesifikasi untuk melakukan prediksi:'
    )

    # Sidebar untuk bantuan dan informasi tambahan
    st.sidebar.header('Bantuan & Informasi')
    st.sidebar.markdown(
        '### Input yang Diperlukan:\n'
        '- **Tipe Appliance**: Pilih tipe perangkat seperti AC, Kulkas, TV, dll.\n'
        '- **Tinggi, Lebar, Kedalaman**: Ukuran fisik perangkat dalam inch.\n'
        '- **Berat**: Berat perangkat dalam lbs.\n'
        '- **Kapasitas Pendinginan**: Kapasitas pendinginan AC dalam BTU/jam.\n'
        '- **Tegangan**: Tegangan operasional perangkat dalam volts.\n'
        '- **Tipe Pemasangan**: Metode pemasangan perangkat.'
    )

    # Input fields untuk spesifikasi perangkat elektronik
    appliance_type = st.selectbox('Tipe Appliance', ['AC', 'TV'])
    
    if appliance_type == 'AC':
        height_inches = st.number_input('Tinggi (inchi)', min_value=0.0)
        width_inches = st.number_input('Lebar (inchi)', min_value=0.0)
        depth_inches = st.number_input('Kedalaman (inchi)', min_value=0.0)
        weight_lbs = st.number_input('Berat (lbs)', min_value=0.0)
        cooling_capacity_btu_hour = st.number_input('Kapasitas Pendinginan (BTU/jam)', min_value=0.0)
        voltage_volts = st.number_input('Tegangan (volts)', min_value=0.0)
        installation_mounting_type = st.selectbox('Tipe Pemasangan', ['Does Not Straddle Window or Windowsill', 'Wall Mounted', 'Floor Standing', 'Portable'])
        heating_mode = st.selectbox('Mode Pemanasan', ['Yes', 'No'])
        low_noise = st.selectbox('Low Noise', ['Yes', 'No'])

        if st.button('Prediksi Konsumsi Listrik'):
            input_data = {
                "height_inches": [height_inches],
                "width_inches": [width_inches],
                "depth_inches": [depth_inches],
                "weight_lbs": [weight_lbs],
                "cooling_capacity_btu_hour": [cooling_capacity_btu_hour],
                "voltage_volts": [voltage_volts],
                "type": [appliance_type],
                "installation_mounting_type": [installation_mounting_type],
                "heating_mode": [heating_mode],
                "low_noise": [low_noise]
            }

            try:
                result_ac = predict('air_conditioners', pd.DataFrame(input_data))
                st.success(f'Prediksi Konsumsi Listrik: {result_ac} kWh/tahun')
            except ValueError as e:
                st.error(f'Error dalam melakukan prediksi: {e}')
            except requests.exceptions.RequestException as e:
                st.error(f'Terdapat kesalahan dalam koneksi: {e}')

    elif appliance_type == 'TV':
        diagonal_size_inches = st.number_input('Ukuran Layar Diagonal (in.)', min_value=0.0)
        resolution_format = st.selectbox('Format Resolusi', ['HD', 'Full HD', '4K', '8K'])
        physical_ports = st.number_input('Jumlah Port Fisik yang Tersedia', min_value=0)
        brand_name = st.text_input('Nama Brand')
        display_type = st.selectbox('Tipe Display', ['LED', 'OLED', 'LCD', 'Plasma'])
        backlight_technology = st.selectbox('Teknologi Backlight', ['Direct LED', 'Edge LED', 'Full Array LED', 'Local Dimming'])
        high_contrast_ratio = st.selectbox('High Contrast Ratio Display', ['Yes', 'No'])
        ethernet_supported = st.selectbox('Ethernet Supported', ['Yes', 'No'])
        low_power_wireless_supported = st.selectbox('Low Power Wireless Technologies Supported', ['Yes', 'No'])
        automatic_brightness_control = st.selectbox('Automatic Brightness Control', ['Yes', 'No'])
        auto_brightness = st.selectbox('Auto Brightness', ['Yes', 'No'])

        if st.button('Prediksi Konsumsi Listrik'):
            input_data = {
                "Diagonal Viewable Screen Size (in.)": [diagonal_size_inches],
                "Resolution Format": [resolution_format],
                "Physical Data Ports Available": [physical_ports],
                "Brand Name": [brand_name],
                "Display Type": [display_type],
                "Backlight Technology Type": [backlight_technology],
                "High Contrast Ratio (HCR) Display": [high_contrast_ratio],
                "Ethernet Supported": [ethernet_supported],
                "Low Power Wireless Technologies Supported": [low_power_wireless_supported],
                "Automatic Brightness Control": [automatic_brightness_control],
                "Auto Brightness": [auto_brightness],
                "type": [appliance_type]
            }

            try:
                result_tv = predict('televisions', pd.DataFrame(input_data))
                st.success(f'Prediksi Konsumsi Listrik: {result_tv} kWh/tahun')
            except ValueError as e:
                st.error(f'Error dalam melakukan prediksi: {e}')
            except requests.exceptions.RequestException as e:
                st.error(f'Terdapat kesalahan dalam koneksi: {e}')

    else:
        st.warning('Fitur untuk perangkat selain AC dan TV belum tersedia.')

# Main program untuk menjalankan aplikasi Streamlit
if __name__ == '__main__':
    # Menjalankan aplikasi Streamlit
    streamlit_ui()
