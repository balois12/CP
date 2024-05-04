# Importing the Libraries
import win32com.client
import pandas as pd
from datetime import datetime
import subprocess
import openpyxl  # Importa la biblioteca openpyxl
import pygetwindow as gw
import time
import os
import glob

# Obtener la fecha actual en el formato deseado (por ejemplo, 'YYYYMMDD')
FECHA = datetime.now().strftime('%d-%m-%y')

# Define la ubicación del directorio donde se guardarán los archivos Excel
output = 'C:\\Users\\barevalo\\OneDrive - Tecnológica de Alimentos S.A\\Balois -2024\\MAT-MOD\\CACHE'
output_DATA = 'C:\\Users\\barevalo\\OneDrive - Tecnológica de Alimentos S.A\\Balois -2024\\MAT-MOD\\2024-1'

# Elimina todos los archivos Excel en la ubicación especificada
excel_files = glob.glob(os.path.join(output, '*.xlsx'))
for excel_file in excel_files:
    os.remove(excel_file)

# Lista para almacenar los marcos de datos
data_frames = []

SapGuiAuto = win32com.client.GetObject('SAPGUI')
application = SapGuiAuto.GetScriptingEngine
connection = application.Children(0)
session = connection.Children(0)
now = datetime.now()

# Solicitar al usuario que ingrese el valor para la variable
#PEP = input("Por favor, el PEP del proyecto: ")
PEP = 'GP/57-124'
# Crear una nueva variable sin el sufijo
PEP_SIMPLE = PEP.split("-")[0]

# Crear una nueva variable sin el /
NAME = PEP_SIMPLE.replace("/","")

NAME = NAME+' '+FECHA+'.xlsx'

REDI_NAME = 'REDI ' + NAME

UTI_NAME = 'UTI ' + NAME

session.findById('wnd[0]').maximize()
session.findById('wnd[0]/tbar[0]/okcd').text = 'ZMMR0097'
session.findById('wnd[0]').sendVKey(0)
session.findById('wnd[0]/usr/ctxtSO_WERKS-LOW').text = 'TAST'
session.findById('wnd[0]/usr/ctxtSO_LGORT-LOW').text = 'L001'
session.findById('wnd[0]/usr/ctxtSO_PS_PS-LOW').text = PEP
session.findById('wnd[0]/usr/ctxtSO_PS_PS-LOW').setFocus()
session.findById('wnd[0]/usr/ctxtSO_PS_PS-LOW').caretPosition = 9
session.findById('wnd[0]').sendVKey(0)
session.findById('wnd[0]/tbar[0]/btn[0]').press()
session.findById('wnd[0]/tbar[1]/btn[8]').press()
session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell').setCurrentCell(- 1, 'ZZOBJ1')
session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell').selectColumn('ZZOBJ1')
session.findById('wnd[0]/tbar[1]/btn[28]').press()
session.findById('wnd[0]/mbar/menu[0]/menu[1]/menu[1]').select()
session.findById('wnd[1]/usr/ctxtDY_PATH').setFocus()
session.findById('wnd[1]/usr/ctxtDY_PATH').caretPosition = 0
session.findById('wnd[1]').sendVKey(4)
session.findById('wnd[2]/usr/ctxtDY_PATH').text = output
session.findById('wnd[2]/usr/ctxtDY_FILENAME').text = REDI_NAME
session.findById('wnd[2]/usr/ctxtDY_FILENAME').caretPosition = 6
session.findById('wnd[2]/tbar[0]/btn[0]').press()
session.findById('wnd[1]/tbar[0]/btn[0]').press()
session.findById('wnd[0]/tbar[0]/btn[15]').press()
session.findById('wnd[0]/tbar[0]/btn[15]').press()

session.findById('wnd[0]/tbar[0]/okcd').text = 'zpsp0008'
session.findById('wnd[0]').sendVKey(0)
session.findById('wnd[0]/usr/ctxtP_PSPID').text = PEP_SIMPLE
session.findById('wnd[0]/usr/ctxtP_PSPID').caretPosition = 5
session.findById('wnd[0]/tbar[1]/btn[8]').press()
session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell').setCurrentCell(- 1, 'AUFNR')
session.findById('wnd[0]/usr/cntlGRID1/shellcont/shell').selectColumn('AUFNR')
session.findById('wnd[0]/tbar[1]/btn[28]').press()
session.findById('wnd[0]/mbar/menu[0]/menu[1]/menu[1]').select()
session.findById('wnd[1]/usr/ctxtDY_PATH').text = output
session.findById('wnd[1]/usr/ctxtDY_FILENAME').text = UTI_NAME
session.findById('wnd[1]/usr/ctxtDY_FILENAME').caretPosition = 4
session.findById('wnd[1]/tbar[0]/btn[0]').press()
session.findById('wnd[0]/tbar[0]/btn[15]').press()
session.findById('wnd[0]/tbar[0]/btn[15]').press()

# Run SAP Scriptsession = None
connection = None
application = None
SapGuiAuto = None

# Obtén una lista de todas las ventanas abiertas
all_windows = gw.getWindowsWithTitle('Excel')

# Cierra todas las ventanas de Excel
for window in all_windows:
    window.close()

time.sleep(5)

#Lee los archivos de utilitarios y REDIS creado y almacena la información en dos dataframe
file_REDI = os.path.join(output, REDI_NAME)
df_REDI = pd.read_excel(file_REDI)

file_UTI = os.path.join(output, UTI_NAME)
df_UTI = pd.read_excel(file_UTI)

# Cambiar el nombre de la columna "Operación" a "Oper."
df_UTI.rename(columns={'Operación': 'Oper.'}, inplace=True)

# Cambiar el nombre de la columna "Denominacion de operacion" a "Dem. operacion"
df_UTI.rename(columns={'Descripción Operación': 'Denom.Operación'}, inplace=True)

# Reemplaza el símbolo | que se colocó por error en la operación
#df_UTI['Oper.'] = df_UTI['Oper.'].str.replace('|', '', regex=False).str.strip()

# Agrupa por nombre y suma los montos Material Estimado
redi_data2 = df_REDI.groupby(['Denom.Operación','Grafo','Oper.'])['Imp.Estimado'].sum().reset_index()

# Agrupa por nombre y suma los montos Material despachado
redi_data3 = df_REDI.groupby(['Denom.Operación','Grafo','Oper.'])['Importe Despacho'].sum().reset_index()

# Agrupa por nombre y suma los montos Material despachado
redi_data4 = df_REDI.groupby(['Denom.Operación','Grafo','Oper.'])['Cantidad'].sum().reset_index()

# Agrupa por nombre y suma los montos Material despachado
redi_data5 = df_REDI.groupby(['Denom.Operación','Grafo','Oper.'])['Cantidad tomada'].sum().reset_index()

#print(redi_data2)

#Convierte los datos a objetos por si en las operaciones se usó una letra en vez de un número
#df_UTI['Oper.'] = df_UTI['Oper.'].astype(str)
#redi_data2['Oper.'] = redi_data2['Oper.'].astype(str)
#redi_data3['Oper.'] = redi_data3['Oper.'].astype(str)

#print(df_UTI['Oper.'])

# Unir el DataFrame redi_data2 al Combined.xlsx
combined_df = df_UTI.merge(redi_data2, on=['Denom.Operación','Grafo','Oper.'], how='left')

# Unir el DataFrame redi_data3 al Combined.xlsx
combined_df = combined_df.merge(redi_data3, on=['Denom.Operación','Grafo','Oper.'], how='left')

# Unir el DataFrame redi_data3 al Combined.xlsx
combined_df = combined_df.merge(redi_data4, on=['Denom.Operación','Grafo','Oper.'], how='left')

# Unir el DataFrame redi_data3 al Combined.xlsx
combined_df = combined_df.merge(redi_data5, on=['Denom.Operación','Grafo','Oper.'], how='left')

# Define una función para asignar los valores según las condiciones
def asignar_categoria(elem_pep):
    elem_pep = str(elem_pep)  # Convierte el valor a cadena
    if "CA" in elem_pep:
        return "MANT CASCO"
    elif "CE" in elem_pep:
        return "MANT ESTRUCTURA"
    elif "LI" in elem_pep:
        return "LIMPIEZA"
    elif "PG" in elem_pep:
        return "MANT DE PROPULSION Y GOBIERNO"
    elif "SA" in elem_pep:
        return "MANT DE SISTEMAS AUXILIARES"
    elif "PM" in elem_pep:
        return "PROYECTO MEJORA"
    elif "SI" in elem_pep:
        return "SERVICIOS INTERNOS"
    else:
        return "Otro"  # Si no cumple con ninguna condición

# Cambiar el nombre de la columna
combined_df.rename(columns={'Precio': 'MOD'}, inplace=True)
combined_df.rename(columns={'Imp.Estimado': 'MAT Estimado'}, inplace=True)
combined_df.rename(columns={'Importe Despacho': 'MAT Despachado'}, inplace=True)

# Aplica la función a la columna "Elem.PEP" y crea una nueva columna "Categoría"
combined_df['Categoría'] = combined_df['Elem.PEP'].apply(asignar_categoria)

combined_df['Mont Liquidado'] = combined_df.apply(lambda row: 0 if row['Liquidación'] == 0 else row['MOD'] / combined_df['MOD'].sum(), axis=1)

# Eliminar la última fila
combined_df = combined_df.drop(combined_df.index[-1])

# Guardar el resultado en el archivo Combined.xlsx (sobrescribiendo el archivo existente)
combined_df.to_excel(os.path.join(output_DATA, NAME), index=False)






