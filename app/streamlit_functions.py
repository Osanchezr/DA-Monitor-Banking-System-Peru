import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Función para cargar los datos
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Fecha'] = pd.to_datetime(df['Fecha'])  # Asegurarse de que 'Fecha' sea datetime
    return df

# Función para filtrar los datos según las entidades
def sidebar_filtros(df):
    st.sidebar.title("Filtros de análisis")
    entidades = df['Entidad'].unique().tolist()
    entidades_seleccionadas = st.sidebar.multiselect('Selecciona las entidades', entidades, default=entidades)
    return entidades_seleccionadas

# Filtrar datos
def filtrar_datos(df, entidades_seleccionadas):
    if entidades_seleccionadas:
        df = df[df['Entidad'].isin(entidades_seleccionadas)]
    return df

# Función para aplicar colores neutros basados en la variación
def color_neutro_por_variacion(variacion):
    if variacion == "No Definido":
        return '#D3D3D3'  # Gris claro para "No Definido"
    else:
        # Usar un degradado entre tonos de azul (o cualquier otro color neutro)
        return f'rgb(100, 100, {255 - int(abs(variacion))})'  # Cuanto mayor la variación, más oscuro el azul

# Calcular la variación anual
def calcular_variacion_anual(df, indicador):
    df_2024 = df[df['Fecha'].dt.strftime('%Y-%m') == '2024-08'][['Entidad', 'Valor']].rename(columns={'Valor': 'Ago-2024'})
    df_2023 = df[df['Fecha'].dt.strftime('%Y-%m') == '2023-08'][['Entidad', 'Valor']].rename(columns={'Valor': 'Ago-2023'})
    df_variacion = pd.merge(df_2024, df_2023, on='Entidad', how='outer')  # Mantener todas las entidades

    # Calcular la variación anual
    df_variacion['Var-Anual'] = (df_variacion['Ago-2024'] - df_variacion['Ago-2023']) / df_variacion['Ago-2023'] * 100

    # Redondear los valores a 2 decimales
    df_variacion[['Ago-2024', 'Ago-2023']] = df_variacion[['Ago-2024', 'Ago-2023']].round(2)
    df_variacion['Var-Anual'] = df_variacion['Var-Anual'].round(2)

    # Reemplazar valores NaN o Inf en la columna Var-Anual con "No Definido"
    df_variacion['Var-Anual'] = df_variacion['Var-Anual'].replace([float('inf'), -float('inf'), None, np.nan], "No Definido")

    # Crear una columna auxiliar para el orden (convertir los "No Definido" en NaN temporales)
    df_variacion['Orden'] = df_variacion['Var-Anual'].replace("No Definido", np.nan)

    # Ordenar de mayor a menor según la variación anual, ignorando los "No Definido"
    df_variacion = df_variacion.sort_values(by='Orden', ascending=False)

    # Aplicar colores a la columna Var-Anual
    df_variacion['Color'] = df_variacion['Var-Anual'].apply(color_neutro_por_variacion)

    # Eliminar la columna de orden antes de mostrar la tabla
    df_variacion = df_variacion[['Entidad', 'Ago-2023', 'Ago-2024', 'Var-Anual']]

    return df_variacion

# Gráfico de barras por indicador (con barras horizontales y colores)
def grafico_barras(df, indicador):
    # Ordenar por el valor de 2024 de mayor a menor
    df = df.sort_values(by='Ago-2024', ascending=True)
    
    # Asignar colores a las barras, rojo para valores negativos
    colores = ['red' if x < 0 else 'blue' for x in df['Ago-2024']]
    
    fig = px.bar(df, 
                 x='Ago-2024', y='Entidad', 
                 orientation='h',  # Barras horizontales
                 text='Ago-2024', 
                 color_discrete_sequence=colores, 
                 height=400)  # Aumentar altura

    # Mostrar valores fuera de la barra y con 2 decimales
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    return fig

# Gráfico de líneas por indicador (más ancho)
def grafico_evolutivo(df, indicador):
    df_pivot = df.pivot_table(index='Fecha', columns='Entidad', values='Valor').reset_index()
    df_pivot['Fecha'] = pd.to_datetime(df_pivot['Fecha'])
    
    fig = px.line(df_pivot, 
                  x='Fecha', 
                  y=df_pivot.columns[1:], 
                  title=f'Evolución de {indicador}', 
                  height=500,  # Aumentar la altura
                  width=3000)  # Aumentar el ancho
    return fig
