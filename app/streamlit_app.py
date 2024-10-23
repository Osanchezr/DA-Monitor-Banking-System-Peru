
import streamlit as st
from functions import load_data, plot_evolution, filter_data

# Configuración de la app Streamlit
st.set_page_config(
    page_title="Dashboard de Indicadores Financieros",
    layout="wide"
)

# Cargar el dataset
df = load_data()

# Crear la barra lateral de navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Selecciona una página:", ["Introducción", "Banca Múltiple", "Otra Entidad"])

# Página de introducción
if page == "Introducción":
    st.title("Proyecto de Análisis Financiero")
    st.write("""
    Este proyecto tiene como objetivo visualizar la evolución de diferentes indicadores financieros
    a lo largo del tiempo para distintas entidades del sistema financiero.
    """)

# Página de gráficos evolutivos para Banca Múltiple
elif page == "Banca Múltiple":
    st.title("Evolución de Indicadores para Banca Múltiple")
    
    # Filtrar los datos para el tipo de entidad "Banca Múltiple"
    df_filtered = filter_data(df, "Banca Multiple")
    
    # Mostrar un gráfico por cada indicador
    for indicador in df_filtered['Indicador'].unique():
        st.subheader(f'Indicador: {indicador}')
        plot_evolution(df_filtered, "Banca Multiple", indicador)

# Página de gráficos evolutivos para otro tipo de entidad
elif page == "Otra Entidad":
    st.title("Evolución de Indicadores para Otra Entidad")
    
    # Filtrar los datos para el tipo de entidad que quieras (por ejemplo, "Caja Municipal")
    df_filtered = filter_data(df, "Caja Municipal")
    
    # Mostrar un gráfico por cada indicador
    for indicador in df_filtered['Indicador'].unique():
        st.subheader(f'Indicador: {indicador}')
        plot_evolution(df_filtered, "Caja Municipal", indicador)
