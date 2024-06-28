import subprocess

# Path ke file house-energy.py
app = 'app\\streamlit\\house-energy.py'

# Menjalankan subprocess dengan Python dan Streamlit
subprocess.run(['streamlit', 'run', app], shell=True)
