import streamlit as st
import pandas as pd
from streamlit_functions import load_data, filtrar_datos, calcular_variacion_anual, grafico_barras, grafico_evolutivo, sidebar_filtros,color_neutro_por_variacion

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
    st.title(f"Análisis de {tipo_indicador.capitalize()}")
    
    # Filtrar datos por tipo de indicador
    df_tipo = df[df['Tipo de Indicador'] == tipo_indicador]
    
    indicadores = df_tipo['Indicador'].unique()
    for indicador in indicadores:
        st.subheader(f"Indicador: {indicador}")

        # Filtrar datos por indicador
        df_indicador = df_tipo[df_tipo['Indicador'] == indicador]

        # Calcular la variación anual
        df_variacion = calcular_variacion_anual(df_indicador, indicador)

        # Crear columnas para la tabla y el gráfico
        col1, col2 = st.columns([2, 2.5])  # Ajustamos la proporción de ancho entre la tabla y el gráfico

        # Mostrar tabla de variación anual
        with col1:
            st.markdown(f"#### Tabla de Variación Anual")
            # Eliminar índice y aplicar formato adecuado
            df_variacion_sin_indice = df_variacion.reset_index(drop=True)  # Eliminamos el índice
            
            # Solo formatear las columnas numéricas para evitar el error de formato con strings
            st.dataframe(df_variacion_sin_indice.style.applymap(
                lambda val: f'background-color: {color_neutro_por_variacion(val)}' if isinstance(val, (int, float)) else '',
                subset=['Var-Anual']
            ).format({
                'Ago-2023': '{:.2f}', 
                'Ago-2024': '{:.2f}', 
                'Var-Anual': lambda x: '{:.2f}'.format(x) if isinstance(x, (int, float)) else x
            }))

        # Calcular la altura del gráfico en función del número de filas de la tabla
        num_filas = len(df_variacion_sin_indice)
        altura_grafico = num_filas * 25 + 300  # Ajustamos la altura del gráfico

        # Mostrar gráfico de barras (ordenado y con colores)
        with col2:
            st.markdown(f"#### Gráfico Comparativo Ago-2024")
            fig_barras = grafico_barras(df_variacion, indicador)
            
            # Actualizamos el gráfico para que tenga la misma altura que la tabla
            fig_barras.update_layout(height=altura_grafico)  # Ajustar la altura del gráfico
            st.plotly_chart(fig_barras)

        # Gráfico evolutivo por indicador (más ancho)
        st.plotly_chart(grafico_evolutivo(df_indicador, indicador))


# Configurar las páginas
def main():
    # Configuraciones de diseño para ampliar la página
    st.set_page_config(layout="wide")  # Establecemos el layout como "wide" para usar más espacio

    # Páginas en la aplicación
    opciones_pagina = ['Introducción', 'Solvencia', 'Calidad de Activos', 'Eficiencia y Gestión', 'Rentabilidad', 'Liquidez']
    pagina_seleccionada = st.sidebar.radio('Selecciona una página', opciones_pagina)

    # Cargar los datos
    df = load_data("C:/Users/osanc/Documents/GitHub/DA-Monitor-Banking-System-Peru/data/data_procesada/data_kpi_procesada.csv")

    # Filtrar los datos según las entidades seleccionadas (FILTRO ÚNICO)
    
    entidades_seleccionadas = sidebar_filtros(df)
    df_filtrado = filtrar_datos(df, entidades_seleccionadas)

    # Mostrar la página seleccionada
    if pagina_seleccionada == 'Introducción':
        pagina_introduccion()
    elif pagina_seleccionada == 'Solvencia':
        pagina_tipo_indicador(df_filtrado, 'SOLVENCIA')
    elif pagina_seleccionada == 'Calidad de Activos':
        pagina_tipo_indicador(df_filtrado, 'CALIDAD DE ACTIVOS')
    elif pagina_seleccionada == 'Eficiencia y Gestión':
        pagina_tipo_indicador(df_filtrado, 'EFICIENCIA Y GESTIÓN')
    elif pagina_seleccionada == 'Rentabilidad':
        pagina_tipo_indicador(df_filtrado, 'RENTABILIDAD')
    elif pagina_seleccionada == 'Liquidez':
        pagina_tipo_indicador(df_filtrado, 'LIQUIDEZ')

# Ejecutar la aplicación
if __name__ == "__main__":
    main()

