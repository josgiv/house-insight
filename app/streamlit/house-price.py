import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load Dataset
df = pd.read_csv('..\..\ML-preparation\Dataset\Harga-Rumah-Model.csv', delimiter=',')

# Mapping sub-lokasi berdasarkan kota
sub_lokasi_dict = {
    'Jakarta': ['Jakarta Utara', 'Jakarta Barat', 'Jakarta Selatan', 'Jakarta Timur', 'Jakarta Pusat'],
    'Bogor': ['Bogor Utara', 'Bogor Selatan', 'Bogor Timur', 'Bogor Barat', 'Bogor Tengah'],
    'Tangerang': ['Tangerang Kota', 'Tangerang Selatan', 'Tangerang Utara', 'Tangerang Barat'],
    'Depok': ['Depok'],
    'Bekasi': ['Bekasi Barat', 'Bekasi Timur', 'Bekasi Utara', 'Bekasi Selatan']
}

# Ubah nilai 'GRS' menjadi numerik
df['GRS'] = df['GRS'].map({'ADA': 1, 'TIDAK ADA': 0})

# Fungsi untuk preprocessing kolom HARGA
def preprocess_harga(harga_str):
    # Hapus titik sebagai pemisah ribuan dan konversi ke float
    harga_clean = harga_str.replace('.', '')
    return float(harga_clean)

# Preprocessing kolom HARGA
df['HARGA'] = df['HARGA'].apply(preprocess_harga)

# Sidebar Informasi Program
st.sidebar.title("Informasi Program")
st.sidebar.info("""
Aplikasi ini memprediksi harga rumah berdasarkan input parameter yang Anda masukkan. 
Parameter yang digunakan meliputi: luas tanah, luas bangunan, jumlah kamar tidur, jumlah kamar mandi, dan garasi.
Selain itu, aplikasi ini juga memberikan statistik harga rumah berdasarkan lokasi yang dipilih.
""")

# Streamlit App
st.title('Prediksi Harga Rumah')
st.write('Masukkan detail properti untuk mendapatkan prediksi harga rumah dan statistik harga berdasarkan lokasi yang dipilih.')

# Deskripsi Aplikasi
st.markdown("""
### Cara Penggunaan

1. Pilih lokasi dan sub-lokasi dari daftar yang tersedia.
2. Masukkan detail properti seperti luas tanah, luas bangunan, jumlah kamar tidur, jumlah kamar mandi, dan apakah terdapat garasi.
3. Tekan tombol 'Prediksi Harga' untuk melihat perkiraan harga rumah berdasarkan input yang diberikan.
4. Statistik harga rumah untuk sub-lokasi yang dipilih akan ditampilkan di bagian bawah.

### Statistik Harga

Statistik harga rumah mencakup rata-rata, median, serta rentang harga berdasarkan sub-lokasi yang Anda pilih.
""")

# Dropdown Lokasi Utama
lokasi = st.selectbox(
    'Pilih Lokasi',
    ['Jakarta', 'Bogor', 'Tangerang', 'Depok', 'Bekasi']
)

# Dropdown Sub-Lokasi berdasarkan lokasi yang dipilih
sub_lokasi = st.selectbox(
    'Pilih Sub-Lokasi',
    sub_lokasi_dict[lokasi]
)

# Input Parameters
lt = st.number_input('Luas Tanah (m2)', min_value=50, max_value=1000, step=10)
lb = st.number_input('Luas Bangunan (m2)', min_value=50, max_value=1000, step=10)
kamar_tidur = st.number_input('Jumlah Kamar Tidur', min_value=1, max_value=10, step=1)
kamar_mandi = st.number_input('Jumlah Kamar Mandi', min_value=1, max_value=10, step=1)
garasi = st.selectbox('Apakah Ada Garasi?', ['Ya', 'Tidak'])

# Konversi input garasi ke numerik
garasi = 1 if garasi == 'Ya' else 0

# Tombol Prediksi
if st.button('Prediksi Harga'):
    # Filtering Data Berdasarkan Lokasi dan Sub-Lokasi
    df_filtered = df[(df['KOTA'].str.contains(sub_lokasi)) & (df['KOTA'].str.contains(lokasi))]

    # Pastikan data yang ditemukan tidak kosong
    if df_filtered.empty:
        st.error(f"Tidak ada data yang ditemukan untuk sub-lokasi '{sub_lokasi}' di '{lokasi}'. Pilih sub-lokasi lain atau periksa dataset Anda.")
    else:
        # Training Model
        X = df_filtered[['LT', 'LB', 'JKT', 'JKM', 'GRS']]
        y = df_filtered['HARGA']

        model = LinearRegression()
        model.fit(X, y)

        # Prediksi
        input_data = np.array([[lt, lb, kamar_tidur, kamar_mandi, garasi]])
        prediksi = model.predict(input_data)


        # Fungsi untuk mengambil summary statistik berdasarkan lokasi
        def summary_statistics(df, location):
            lokasi_data = df[df['KOTA'] == location]
            mean = lokasi_data['HARGA'].mean()
            median = lokasi_data['HARGA'].median()
            min_price = lokasi_data['HARGA'].min()
            max_price = lokasi_data['HARGA'].max()
            return mean, median, min_price, max_price

        # Menampilkan statistik harga berdasarkan lokasi yang dipilih
        mean, median, min_price, max_price = summary_statistics(df, sub_lokasi)
        st.subheader(f'Statistik Harga Rumah di {sub_lokasi}')
        st.write(f"Rata-rata Harga: Rp {mean:,.2f}")
        st.write(f"Median Harga: Rp {median:,.2f}")
        st.write(f"Rentang Harga: Rp {min_price:,.2f} - Rp {mean:,.2f}")
