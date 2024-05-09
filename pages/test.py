import streamlit as st
import pandas as pd
import numpy as np
import requests
import altair as alt
from streamlit_lottie import st_lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
         return None
    return r.json()

lottie_404 = load_lottieurl("https://lottie.host/47c35943-c26b-401a-ab2f-1f2109a4f8ce/yTXFsB8QRf.json")

st_lottie(lottie_404, width=700,key="hello")

st.title ('PAGINA EN DESARROLLO')

DATA = 'DATA2GPT.xlsx'
PD_DATA = pd.read_excel(DATA,sheet_name='DATA').drop('Hoja de entrada', axis=1).drop('Index', axis=1).drop('Liquidación', axis=1).drop('PEP', axis=1).drop('Elem.PEP', axis=1)

title = st.text_input("Ingrese la actividad a buscar")

#st.write("The current movie title is", title)

# Filtrar el DataFrame basado en la entrada del usuario
if title:
    resultados = PD_DATA[PD_DATA['Descripción Operación'].str.contains(title, case=False)].reset_index(drop=True)
    st.write('Resultados de la búsqueda:')
    st.write(resultados,width=900,heitgh=1200)
