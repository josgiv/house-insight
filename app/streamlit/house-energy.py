import requests
import subprocess
import streamlit as st

# Streamlit UI untuk input spesifikasi AC
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
    appliance_type = st.selectbox('Tipe Appliance', ['AC', 'Kulkas', 'TV', 'Lainnya'])
    
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
                response = requests.post('http://127.0.0.1:5000/predict-ac', json=input_data)
                
                if response.status_code == 200:
                    result = response.json()['result']
                    st.success(f'Prediksi Konsumsi Listrik: {result} Kwh')
                else:
                    st.error('Error dalam melakukan prediksi. Silakan coba lagi.')
            
            except requests.exceptions.RequestException as e:
                st.error(f'Terdapat kesalahan dalam koneksi: {e}')

    else:
        st.warning('Fitur untuk perangkat selain AC belum tersedia.')

# Fungsi untuk menjalankan load_ac.py sebagai subproses
def run_load_ac():
    # Path ke file load_ac.py
    app_path = '../loader/load_ac.py'
    
    # Menjalankan subprocess dengan Python
    subprocess.run(['python', app_path])

# Main program untuk menjalankan aplikasi Streamlit
if __name__ == '__main__':
    # Menjalankan aplikasi Streamlit
    streamlit_ui()
    
    # Menjalankan load_ac.py sebagai subproses setelah Streamlit ditutup
    run_load_ac()
