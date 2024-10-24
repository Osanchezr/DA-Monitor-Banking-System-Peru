import streamlit as st
import pandas as pd
from streamlit_functions import load_data, filtrar_datos, calcular_variacion_anual, grafico_barras, grafico_evolutivo, sidebar_filtros,color_neutro_por_variacion, pagina_analisis_clusters

def pagina_introduccion():
    # Titulo
    st.markdown("""
        <h1 style='text-align: center; color: #2E86C1; margin-bottom: 0;'>Sistema de monitoreo bancario del Perú</h1>
        <h3 style='text-align: center; color: #2E86C1; margin-top: 0;'>Ago 2015 - Ago 2024</h3>
    """, unsafe_allow_html=True)
    
    # Subtítulo
    st.markdown("<h2 style='text-align: center; color: #1B4F72;'>Exploración de Indicadores Financieros y Segmentación de Entidades Bancarias</h2>", unsafe_allow_html=True)
    
    # Dividir en dos columnas para agregar una imagen y texto explicativo
    col1, col2 = st.columns([1, 2])
    
    with col1:
        
        st.image("C:/Users/osanc/Documents/GitHub/DA-Monitor-Banking-System-Peru/app/images_script/Portada_bancos.png", caption="Indicadores del Sistema Bancario del Perú", use_column_width=True)
    
    
        st.image("C:/Users/osanc/Documents/GitHub/DA-Monitor-Banking-System-Peru/app/images_script/Banca.png", 
                caption="Bancos", use_column_width=True)
    with col2:
        st.write("""
        **Este análisis se basa en datos oficiales del sistema bancario peruano, proporcionados por la** **Superintendencia de Banca, Seguros y AFP (SBS)** **del Perú. El objetivo principal es evaluar de manera exhaustiva la evolución y desempeño de las entidades bancarias a lo largo de un período de 9 años (agosto 2015 - agosto 2024).**

        El reporte abarca múltiples aspectos financieros clave, incluyendo:

        - **Solvencia**, para medir la capacidad de los bancos de enfrentar obligaciones a largo plazo.
        - **Eficiencia y Gestión**, evaluando la administración de los recursos y operaciones bancarias.
        - **Rentabilidad**, que refleja la capacidad de generar beneficios sostenibles.
        - **Liquidez**, centrada en la capacidad de cumplir con compromisos a corto plazo.
        - **Calidad de Activos**, que analiza el riesgo asociado a la cartera de préstamos.

        Adicionalmente, se ha implementado un **análisis temporal detallado** que permite visualizar la evolución de estos indicadores en el tiempo, identificando patrones y tendencias significativas. Además, mediante el uso de técnicas avanzadas de **machine learning** y **clustering no supervisado**, se han identificado grupos o segmentos de bancos con características similares, lo que permite analizar las relaciones y similitudes entre las distintas entidades bancarias.
      
        """)
    
    # Espacio en blanco para separar secciones
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sección sobre la importancia del análisis de clusters y machine learning
    st.markdown("""
    ### Análisis de Clusters Basado en Machine Learning
    Para segmentar a las entidades bancarias según el comportamiento de sus indicadores a lo largo del tiempo, hemos implementado **modelos de clustering no supervisados** basados en **series de tiempo**. Los modelos utilizados incluyen:
    
    - **K-Means con Dynamic Time Warping (DWT)**
    - **K-Means para series temporales**
    - **Shape-Based Clustering**
    
    Estos modelos nos permiten identificar **patrones ocultos** y agrupar a los bancos en **clusters** que comparten características similares en cuanto a su evolución financiera.
    
    Esta segmentación es crucial para **entender mejor** las dinámicas del sector bancario y para ofrecer una visión más profunda de **cómo evolucionan las entidades** a lo largo del tiempo.
    """)    
    
    # Espacio para destacar conclusiones
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""  
    ### ¡Explora cada sección y descubre más detalles sobre el sistema bancario del Perú!
    """, unsafe_allow_html=True)

    # Sección de créditos y enlaces personales
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Añadir tu nombre como autor
    st.markdown("<h3 style='text-align: center;'>Aplicación creada por: Oscar Paul Sanchez Riveros </h3>", unsafe_allow_html=True)
    
    # Añadir tus perfiles de LinkedIn y GitHub
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        # Enlace a LinkedIn
        st.markdown("""
        <a href="https://www.linkedin.com/in/oscar-sanchez-riveros/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo.svg" alt="LinkedIn" width="50" style="margin-right: 10px;">
        </a>
        
        <a href="https://github.com/Osanchezr" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="50">
        </a>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

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
            
            st.markdown(f"#### Tabla de Variación Anual (%)")
            st.write("\n\n")  
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
        altura_grafico = num_filas * 15 + 300  # Ajustamos la altura del gráfico

        # Mostrar gráfico de barras (ordenado y con colores)
        with col2:
            st.markdown(f"####  Comparativo Ago-2024")
            fig_barras = grafico_barras(df_variacion, indicador)
            
            # Actualizamos el gráfico para que tenga la misma altura que la tabla
            fig_barras.update_layout(height=altura_grafico)  # Ajustar la altura del gráfico
            st.plotly_chart(fig_barras)

        # Gráfico evolutivo por indicador (más ancho)
        st.plotly_chart(grafico_evolutivo(df_indicador, indicador))


# Configurar las páginas
def main():
    st.set_page_config(layout="wide")

    opciones_pagina = ['Introducción', 'Solvencia', 'Calidad de Activos', 'Eficiencia y Gestión', 'Rentabilidad', 'Liquidez', 'Análisis de Clusters']
    pagina_seleccionada = st.sidebar.radio('Selecciona una página', opciones_pagina)

    # Cargar los datos
    df = load_data("C:/Users/osanc/Documents/GitHub/DA-Monitor-Banking-System-Peru/data/data_procesada/data_kpi_procesada.csv")
    resultado_combinado = pd.read_csv("C:/Users/osanc/Documents/GitHub/DA-Monitor-Banking-System-Peru/results/clusters.csv")

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
    elif pagina_seleccionada == 'Análisis de Clusters':
        pagina_analisis_clusters(df, resultado_combinado)  


# Ejecutar la aplicación
if __name__ == "__main__":
    main()