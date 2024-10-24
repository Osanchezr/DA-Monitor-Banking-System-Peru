import streamlit as st
import pandas as pd
from streamlit_functions import load_data, filtrar_datos, calcular_variacion_anual, grafico_barras, grafico_evolutivo, sidebar_filtros

# Configurar las páginas del análisis
def pagina_introduccion():
    st.title("Análisis de Indicadores Bancarios")
    st.write("""  
    Este análisis presenta la evolución de varios indicadores financieros de bancos desde agosto de 2015 a agosto de 2024. 
    Los indicadores están clasificados en las siguientes categorías:
    
    - **Solvencia**
    - **Eficiencia y Gestión**
    - **Rentabilidad**
    - **Liquidez**
    - **Calidad de Activos**
    
    En cada sección, podrás ver tablas y gráficos interactivos que te ayudarán a analizar la situación de los bancos en distintos aspectos financieros.
    """)

# Página de análisis por tipo de indicador
def pagina_tipo_indicador(df, tipo_indicador):
    st.title(f"Análisis de {tipo_indicador}")
    
    # Filtrar datos por tipo de indicador
    df_tipo = df[df['Tipo de Indicador'] == tipo_indicador]
    
    indicadores = df_tipo['Indicador'].unique()
    for indicador in indicadores:
        st.subheader(f"Indicador: {indicador}")

        # Filtrar datos por indicador
        df_indicador = df_tipo[df_tipo['Indicador'] == indicador]

        # Calcular la variación anual
        df_variacion = calcular_variacion_anual(df_indicador, indicador)

        # Mostrar tabla de variación anual (ordenada por Var-Anual y con 2 decimales)
        st.table(df_variacion[['Entidad', 'Ago-2023', 'Ago-2024', 'Var-Anual']])

        # Mostrar gráfico de barras (ordenado y con colores)
        fig_barras = grafico_barras(df_variacion, indicador)
        st.plotly_chart(fig_barras)

        # Gráfico evolutivo por indicador (más ancho)
        fig_evolutivo = grafico_evolutivo(df_indicador, indicador)
        st.plotly_chart(fig_evolutivo)

# Configurar las páginas
def main():
    # Cargar los datos
    df = load_data("C:/Users/osanc/Documents/GitHub/DA-Monitor-Banking-System-Peru/data/data_procesada/data_kpi_procesada.csv")

    # Filtros en la barra lateral
    st.sidebar.title("Filtros de análisis")
    entidades_seleccionadas = sidebar_filtros(df)

    # Filtrar los datos según las entidades seleccionadas
    df_filtrado = filtrar_datos(df, entidades_seleccionadas)

    # Páginas en la aplicación
    opciones_pagina = ['Introducción', 'Solvencia', 'Eficiencia y Gestión', 'Rentabilidad', 'Liquidez', 'Calidad de Activos']
    pagina_seleccionada = st.sidebar.radio('Selecciona una página', opciones_pagina)

    # Mostrar la página seleccionada
    if pagina_seleccionada == 'Introducción':
        pagina_introduccion()
    elif pagina_seleccionada == 'Solvencia':
        pagina_tipo_indicador(df_filtrado, 'SOLVENCIA')
    elif pagina_seleccionada == 'Eficiencia y Gestión':
        pagina_tipo_indicador(df_filtrado, 'EFICIENCIA Y GESTIÓN')
    elif pagina_seleccionada == 'Rentabilidad':
        pagina_tipo_indicador(df_filtrado, 'RENTABILIDAD')
    elif pagina_seleccionada == 'Liquidez':
        pagina_tipo_indicador(df_filtrado, 'LIQUIDEZ')
    elif pagina_seleccionada == 'Calidad de Activos':
        pagina_tipo_indicador(df_filtrado, 'CALIDAD DE ACTIVOS')

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
