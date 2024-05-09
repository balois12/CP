import streamlit as st
import pandas as pd
import requests
import numpy as np
import altair as alt
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Control de Proyectos",
    page_icon="🚢"
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
         return None
    return r.json()

lottie_project = load_lottieurl("https://lottie.host/f9fb61b2-f6b7-469a-bbf4-a3108cbf54c9/zNQx5XFoFT.json")
lottie_bar = load_lottieurl("https://lottie.host/45873f27-7b33-4c92-b7de-789a6f045a93/5lqEDCYXdW.json")
lottie_time = load_lottieurl("https://lottie.host/224546ac-5ccd-4c4e-8a1a-b345ca27d189/kWv8IKhYq3.json")

DATA = 'BD.xlsx'
PD_MAT = pd.read_excel(DATA,sheet_name='MAT')
PD_MOD = pd.read_excel(DATA,sheet_name='MAT-MOD')
PD_MAT_CODE = pd.read_excel(DATA,sheet_name='MAT-CODE')
PD_ESFUERZO = pd.read_excel(DATA,sheet_name='ESFUERZO')
PD_ESTADIA = pd.read_excel(DATA,sheet_name='VARADA')

col1, col2 =st.columns([0.2,0.8])
with col1:
    st_lottie(lottie_bar, width=110,key="hello")
with col2:   
    st.title ('Ratios de producción')

st.sidebar.header('Proyectos	:anchor:')
select_proyecto = st.sidebar.multiselect('Seleciona uno o más proyectos',PD_MOD['Proyecto'].drop_duplicates().sort_values(), key='proyectos')
categoria = st.sidebar.multiselect('Selecciona ESTRUCTURA, ADITAMENTOS',['CALD ESTRUCTURA', 'CALD ADITAMENTO'], key='categoria')

# Definir DF de acero que será fijo
y_acero = ['Peso (kg)']
material_acero = ['PLANCHA', 'PLATINA', 'TUBO']
codigo_material_acero = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material_acero)]
df_acero = PD_MAT[PD_MAT['Material'].isin(codigo_material_acero['Material'])]
df_acero= df_acero.groupby(['Proyecto','Categoría'])['Peso (kg)'].sum().reset_index()
df_acero = df_acero[df_acero['Proyecto'].isin(select_proyecto)]
df_acero = df_acero[df_acero['Categoría'].isin(categoria)]

# Graficar usando Altair ACERO
chart_ACERO = alt.Chart(df_acero).mark_bar().encode(
    x='Proyecto:N',
    y= alt.Y(f"{y_acero}:Q", title='Peso (kg)'),
    color=alt.Color('Categoría:N', scale=alt.Scale(domain=['CALD ADITAMENTO', 'CALD ESTRUCTURA'], range=['#F24811', '#F7C90B ']), legend=None),
    tooltip=['Proyecto', 'Categoría', 'Peso (kg)']
).properties(width=1000, height=500)

genre = st.sidebar.radio(
    "Materiales",
    ["Soldadura",  "Oxígeno", "Discos", "Gas Propano", "Gas CO2"],
    captions = [  "Soldadura vs Acero",  "Oxígeno vs Acero","Discos vs Acero", "Gas vs Acero", "Gas CO2 vs Acero"])

if genre == "Soldadura" :
    material = ['SOLDADURA']
    y = ['Cantidad tomada']
    color = ['#0DE51D', '#1CD16E']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    col1, col2 =st.columns([0.5,0.5])
    with col1:
            st.write("Soldadura (kg)")
    with col2:   
            st.write ('Acero (kg)')

if genre == "Oxígeno" :
    material = ['OXIGENO']
    y = ['Cantidad tomada']
    color = ['#0DCEE5','#C8FAF4']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    col1, col2 =st.columns([0.5,0.5])
    with col1:
            st.write("Oxígeno consumido (m2)")
    with col2:   
            st.write ('Acero (kg)')
    
if genre == "Discos" :
    material = ['DISCO CORTE','DISCO DESBASTE']
    y = ['Cantidad tomada']
    color = ['#0D4EE5','#C8E7FA']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    col1, col2 =st.columns([0.5,0.5])
    with col1:
            st.write("Discos consumidos")
    with col2:   
            st.write ('Acero (kg)')
    
if genre == "Gas Propano" :
    material = ['GAS PROPANO']
    y = ['Cantidad tomada']
    color = ['#E50D72','#F9C8FA']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    col1, col2 =st.columns([0.5,0.5])
    with col1:
            st.write("Gas Propano empleado (bot = 10kg)")
    with col2:   
            st.write ('Acero (kg)')
    
if genre == "Gas CO2" :
    material = ['GAS CO2']
    y = ['Cantidad tomada']
    color = ['#AD0DE5','#EFC3E0']
    codigo_material = PD_MAT_CODE[PD_MAT_CODE['Tipo'].isin(material)]
    df = PD_MAT[PD_MAT['Material'].isin(codigo_material['Material'])]
    df = df.groupby(['Proyecto','Categoría'])['Cantidad tomada'].sum().reset_index()
    col1, col2 =st.columns([0.5,0.5])
    with col1:
            st.write("Gas CO2 empleado (kg)")
    with col2:   
            st.write ('Acero (kg)')
    
df = df[df['Proyecto'].isin(select_proyecto)]
df = df[df['Categoría'].isin(categoria)]
#ESTADIA
df_estadia = PD_ESTADIA[PD_ESTADIA['Proyecto'].isin(select_proyecto)].drop('PEP', axis=1).drop('PEP2', axis=1)
# Resetear los índices
df = df.reset_index(drop=True)

# Graficar usando Altair
chart = alt.Chart(df).mark_bar().encode(
    x='Proyecto:N',
    y= alt.Y(f"{y}:Q", title=y),
    color=alt.Color('Categoría:N', scale=alt.Scale(domain=['CALD ADITAMENTO', 'CALD ESTRUCTURA'], range=color), legend=None),
    tooltip=['Proyecto', 'Categoría', y[0]]
).properties(width=1000, height=500)

col1, col2 =st.columns([0.5,0.5])
with col2:
    st.altair_chart(chart_ACERO, use_container_width=True)
with col1:   
   st.altair_chart(chart, use_container_width=True)

st.write("Detalle de los materiales:")
#df_acero = df_acero.drop('PEP2', axis=1) // SERIA MEJOR TENER LA DATA COMPLETA CON EL ACERO DESDE LAS OPCIONES EN UN MISMO DATAFRAME
#df = pd.merge(df, df_acero, on='Proyecto', how='inner')
st.dataframe(df, width=800, height=None)
#-----------------------------------------------------------------------------------------------------------------
col1, col2 =st.columns([0.2,0.8])
with col1:
    st_lottie(lottie_project, width=110,key="project")
with col2:   
    st.title ('Costo de MOD')

#-----------------------------------------------------------------------------------------------------------------
genre = st.sidebar.radio(
    "MOD y esfuerzo adicional",
    ["Calderería", "Sist. auxiliares",  "Propulsión y Gobierno",'Tratamiento superficial'],
    captions = ["Esfuerzo adicional calderería",  "Esfuerzo adicional tuberías",  "Esfuerzo adicional PG", "Esfuerzo adicional Arenado y pintado"])
if genre == 'Calderería':
    categoria = ['CALD ADITAMENTO', 'CALD ESTRUCTURA']
    color = ['#FFA533']
    st.write("MOD Calderería (S/.)")
    text = 'Esfuerzo adicional calderería (S/.)'
    
if genre == 'Sist. auxiliares':
    categoria = ['SISTEMAS AUXILIARES']
    color = ['#E50D72']
    st.write("MOD tuberías (S/.)")
    text = 'Esfuerzo adicional sistemas auxiliares (S/.)'

if genre == 'Propulsión y Gobierno':
    categoria = ['PROPULSION Y GOBIERNO']
    color = ['#AD0DE5']
    st.write("MOD tuberías (S/.)")
    text = 'Esfuerzo adicional sistemas PG(S/.)'

if genre == 'Tratamiento superficial':
    categoria = ['TRATAMIENTO SUPERFICIES']
    color = ['#2CC8A0']
    st.write("MOD Arenado y pintado (S/.)")
    text = 'Esfuerzo adicional arenado y pintado PG(S/.)'
    
df1 = PD_MOD[PD_MOD['Categoría'].isin(categoria)]
df1 = df1[df1['Proyecto'].isin(select_proyecto)] 
df1= df1.groupby(['Proyecto'])['MOD'].sum().reset_index()
st.bar_chart(data=df1, x="Proyecto", y="MOD", color=color, width=0, height=600, use_container_width=True)

# Tabla con los datos
st.write("Costo directo de mano de obra:")
df1 = pd.merge(df1, df_estadia, on='Proyecto', how='inner')
st.dataframe(df1, width=800, height=None)

#-----------------------------------------------------------------------------------------------------------------

col1, col2 =st.columns([0.2,0.8])
with col1:
    st_lottie(lottie_time, width=110,key="time")
with col2:   
    st.title ('Esfuerzo adicional')
#-----------------------------------------------------------------------------------------------------------------
st.write(text)    
codigo_proveedor = PD_ESFUERZO[PD_ESFUERZO['Categoría'].isin(categoria)]    
df2 = PD_MOD[PD_MOD['Descripción Grafo'].isin(['ESFUERZO ADICIONAL'])]
df2 = df2[df2['Proyecto'].isin(select_proyecto)] 
df2 = df2 [df2 ['Proveedor'].isin(codigo_proveedor['Codigo'])]
df2= df2.groupby(['Proyecto','Nombre Acreedor'])['MOD'].sum().reset_index()
st.bar_chart(data=df2, x="Proyecto", y="MOD", color=color, width=0, height=600, use_container_width=True)

# Tabla con los datos
st.write("Detalle del esfuerzo adicional:")
df2 = pd.merge(df2, df_estadia, on='Proyecto', how='inner')
st.dataframe(df2, width=800, height=None)
