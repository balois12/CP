import streamlit as st
import pandas as pd
import statistics
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import numpy as np
#PC CASA
#DATA = 'D:\OneDrive - Tecnológica de Alimentos S.A\Balois -2024\MAT-MOD\Ratios 2024-1\BD.xlsx'

#LAPTOP TASA
DATA = 'C:\\Users\\barevalo\\OneDrive - Tecnológica de Alimentos S.A\\Balois -2024\\MAT-MOD\\Ratios 2024-1\\BD.xlsx'

PD_MAT = pd.read_excel(DATA,sheet_name='MAT')
PD_MOD = pd.read_excel(DATA,sheet_name='MAT-MOD')
PD_MAT_CODE = pd.read_excel(DATA,sheet_name='MAT-CODE')
PD_ESFUERZO = pd.read_excel(DATA,sheet_name='ESFUERZO') 

st.title ('Ratios de producción Temp 2024-1')
st.sidebar.header('Proyectos	:anchor:')
select_proyecto = st.sidebar.multiselect('Seleciona uno o más proyectos',PD_MOD['Proyecto1'].drop_duplicates().sort_values(), key='proyectos1')

df2 = PD_MOD[PD_MOD['Descripción Grafo'].isin(['ESFUERZO ADICIONAL'])]
df2 = df2[df2['Proyecto1'].isin(select_proyecto)] 

genre = st.sidebar.radio(
    "Categorías",
    ["Calderería", "Sist. auxiliares",  "Propulsión y Gobierno"],
    captions = ["Esfuerzo adicional calderería",  "Esfuerzo adicional tuberías",  "Esfuerzo adicional PG"])
if genre == 'Calderería':
    categoria = ['CALDERERÍA']
    color = ['#FFA533']
    codigo_proveedor = PD_ESFUERZO[PD_ESFUERZO['Categoría'].isin(categoria)]
    df2 = df2 [df2 ['Proveedor'].isin(codigo_proveedor['Codigo'])]
    df2= df2.groupby(['Proyecto1','Nombre Acreedor'])['MOD'].sum().reset_index()
    st.write("Esfuerzo adicional Calderería (S/.)")
    
if genre == 'Sist. auxiliares':
    categoria = ['SISTEMAS AUXILIARES']
    color = ['#E50D72']
    codigo_proveedor = PD_ESFUERZO[PD_ESFUERZO['Categoría'].isin(categoria)]
    df2 = df2 [df2 ['Proveedor'].isin(codigo_proveedor['Codigo'])]
    df2= df2.groupby(['Proyecto1'])['MOD'].sum().reset_index()
    st.write("Esfuerzo adicional tuberías (S/.)")

if genre == 'Propulsión y Gobierno':
    categoria = ['PROPULSION Y GOBIERNO']
    color = ['#AD0DE5']
    codigo_proveedor = PD_ESFUERZO[PD_ESFUERZO['Categoría'].isin(categoria)]
    df2 = df2 [df2 ['Proveedor'].isin(codigo_proveedor['Codigo'])]
    df2= df2.groupby(['Proyecto1'])['MOD'].sum().reset_index()
    st.write("Esfuerzo adicional tuberías (S/.)")


st.bar_chart(data=df2, x="Proyecto1", y="MOD", color=color, width=0, height=600, use_container_width=True)

# Tabla con los datos
st.write("Detalle de los proyectos y esfuerzo adicional:")
st.dataframe(df2, width=800, height=None)