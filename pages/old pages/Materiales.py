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

st.title ('Ratios de producción Temp 2024-1')
st.sidebar.header('Proyectos	:anchor:')
select_proyecto = st.sidebar.multiselect('Seleciona uno o más proyectos',PD_MOD['Proyecto1'].drop_duplicates().sort_values(), key='proyectos')
categoria = st.sidebar.multiselect('Selecciona ESTRUCTURA, ADITAMENTOS',['CALD ESTRUCTURA', 'CALD ADITAMENTO'], key='categoria')

genre = st.sidebar.radio(
    "Materiales",
    ["Acero", "Soldadura",  "Oxígeno", "Discos", "Gas Propano", "Gas CO2"],
    captions = ["Total de acero procesado",  "Soldadura consumido",  "Oxígeno consumido","Discos consumidos", "Gas consumido"])
if genre == 'Acero':
    material = ['PLANCHA', 'PLATINA']
    y = ['Categoría']
    color = ['#FFA533']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df= df.groupby(['Proyecto','Categoría'])['Peso (kg)'].sum().reset_index()
    st.write("Acero procesado")

if genre == "Soldadura" :
    material = ['SOLDADURA']
    y = ['Cantidad tomada']
    color = ['#0DE51D']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    st.write("Soldadura empleada (kg)")

if genre == "Oxígeno" :
    material = ['OXIGENO']
    y = ['Cantidad tomada']
    color = ['#0DCEE5']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    st.write("Oxígeno consumidos (m2)")

if genre == "Discos" :
    material = ['DISCO CORTE','DISCO DESBASTE']
    y = ['Cantidad tomada']
    color = ['#0D4EE5']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    st.write("Discos consumidos")

if genre == "Gas Propano" :
    material = ['GAS PROPANO']
    y = ['Cantidad tomada']
    color = ['#E50D72']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    st.write("Gas Propano empleado (bot = 10kg)")

if genre == "Gas CO2" :
    material = ['GAS CO2']
    y = ['Cantidad tomada']
    color = ['#AD0DE5']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    st.write("Gas CO2 empleado (kg)")

df = df[df['Proyecto'].isin(select_proyecto)]
df = df[df['Categoría'].isin(categoria)]
print(df)
df = pd.DataFrame(df,columns=["Proyecto","Categoría","Peso (kg)"])
print(df)
st.bar_chart(data=df, x="Proyecto", y=y, color=color, width=0, height=600, use_container_width=True)