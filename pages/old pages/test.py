import streamlit as st
import subprocess

# Define la función para ejecutar un script de Python
def run_python_script():
    # Ruta al script de Python que deseas ejecutar
    script_path = "SAP.py"
    # Ejecutar el script de Python
    subprocess.Popen(["python", script_path], shell=True)

st.title("Ejecutar Script de Python con Streamlit")
if st.button("Ejecutar Script"):
    run_python_script()
    st.success("El script de Python está ejecutándose!")
