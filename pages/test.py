import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

DATA = 'DATA2GPT.xlsx'
PD_DATA = pd.read_excel(DATA,sheet_name='DATA').drop('Hoja de entrada', axis=1).drop('Index', axis=1).drop('Liquidación', axis=1).drop('PEP', axis=1).drop('Elem.PEP', axis=1)

title = st.text_input("Ingrese la actividad a buscar")

#st.write("The current movie title is", title)

# Filtrar el DataFrame basado en la entrada del usuario
if title:
    resultados = PD_DATA[PD_DATA['Descripción Operación'].str.contains(title, case=False)].reset_index(drop=True)
    st.write('Resultados de la búsqueda:')
    st.write(resultados,width=900,heitgh=1200)
else:
    st.write('Ingresa un nombre para buscar.')