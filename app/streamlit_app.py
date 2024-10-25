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

    comentarios_indicadores = {"Ratio de Capital Global": "La tabla y el gráfico muestran las variaciones anuales en el ratio de capital global de varias instituciones financieras entre agosto de 2023 y agosto de 2024. La mayoría de los bancos presentan una tendencia positiva, lo que refleja un fortalecimiento en sus posiciones de capital. Alfin Banco destaca con un aumento del 80.59%, seguido por B. BCI Perú con un crecimiento del 33.74%, mientras que Scotiabank Perú muestra un incremento más moderado del 7.95%. Bank of China, por su parte, registra una mejora constante con una variación del 14.98%.",
        "Pasivo Total / Capital Social y Reservas": "La tabla y el gráfico muestran las variaciones anuales en el ratio de pasivo total sobre capital social y reservas de varias instituciones financieras entre agosto de 2023 y agosto de 2024. La mayoría de los bancos presenta una tendencia positiva, lo que indica un fortalecimiento de sus posiciones de capital. Alfin Banco destaca con un aumento del 226.1%, seguido por B. BCI Perú con un 144.98%. Interbank muestra un incremento del 84%, mientras que Bank of China presenta una mejora constante con una variación del 68%. En conjunto, estos resultados reflejan una mayor capacidad de los bancos para gestionar sus pasivos y mantener la estabilidad financiera.",
        "Créditos Atrasados / Créditos Directos": "La tabla y el gráfico muestran las variaciones anuales en el ratio de Créditos Atrasados / Créditos Directos de varias instituciones financieras entre agosto de 2023 y agosto de 2024. Se observa una tendencia mixta: B. Santander Perú registra un aumento del 300%, seguido por B. Interamericano de Finanzas con un 16.85%. Mibanco sube un 12.14%, mientras que B. Ripley presenta una variación del 6.80%. Estas cifras reflejan distintos niveles de riesgo crediticio y gestión de cartera, con aumentos en los ratios que podrían señalar un mayor riesgo de morosidad.",
        "Créditos Atrasados con más de 90 días de atraso / Créditos Directos":"La tabla y el gráfico muestran las variaciones anuales en el ratio de Créditos Atrasados con más de 90 días de atraso / Créditos Directos entre agosto de 2023 y agosto de 2024. B. Santander Perú presenta un aumento del 204.91%, seguido por Mibanco con un 27.59%, B. Interamericano de Finanzas con un 26.23%, y B. Ripley con una variación del 11.01%. Esta tendencia mixta refleja diferentes niveles de riesgo crediticio y gestión de cartera. Un aumento en este ratio sugiere un incremento en los créditos morosos, lo que podría afectar la estabilidad financiera.",
        "Créditos Refinanciados y Reestructurados / Créditos Directos":"La tabla y el gráfico muestran las variaciones anuales en el ratio de Créditos Refinanciados y Reestructurados / Créditos Directos entre agosto de 2023 y agosto de 2024. BANCOM presenta un aumento del 47.19%, seguido por B. Falabella Perú con un 32.21%, B. Pichincha con un 31.76%, y Mibanco con una variación del 28.79%. Esta tendencia mixta refleja diferentes niveles de gestión de créditos refinanciados y reestructurados, lo que puede indicar un mayor riesgo crediticio y la necesidad de refinanciación, lo cual podría impactar la estabilidad financiera.",
        "Créditos Atrasados MN / Créditos Directos MN":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. B. Santander Perú presenta un aumento del 18.55%, seguido por B. Pichincha con un 15.26%, Scotiabank Perú con un incremento del 12.83%, y Mibanco con una variación del 12.17%. Esta tendencia mixta refleja diferentes niveles de gestión de créditos atrasados en moneda nacional, lo que indica distintos niveles de riesgo crediticio. Un aumento en este ratio puede señalar un incremento en los créditos morosos, lo cual podría afectar la estabilidad financiera del banco.",
        "Créditos Atrasados ME / Créditos Directos ME":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. B. Santander Perú presenta un aumento significativo del 436.92%, seguido por BANCOM con un incremento del 46.49%, B. Falabella Perú con un 35.71%, y B. Interamericano de Finanzas con una variación del 30.89%. Esta tendencia mixta refleja diferentes niveles de gestión de créditos atrasados en moneda extranjera, lo que indica distintos niveles de riesgo crediticio. Un aumento en este ratio puede señalar un incremento en los créditos morosos, lo cual podría afectar la estabilidad financiera del banco.",
        "Provisiones / Créditos Atrasados":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. Alfin Banco presenta un aumento del 17.01%, pasando de 165.90% a 194.12%, seguido por B. Falabella Perú con un incremento del 15.95%, BANCOM con un 15.10% y B. De Crédito del Perú con una variación del 12.66%. Esta tendencia mixta refleja diferentes niveles de provisiones para créditos atrasados, indicando distintos enfoques en la cobertura del riesgo crediticio. Un aumento en este ratio puede señalar una mayor prudencia en la gestión de riesgos por parte del banco.",
        "Gastos de Administración Anualizados / Activo Productivo Promedio":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. B. Ripley presenta un aumento del 11.85%, pasando de 12.65% a 14.15%, seguido por B. ICBC con un incremento del 10.33%, B. Santander Perú con un 8.49% y Scotiabank Perú con una variación del 8.21%. Esta tendencia mixta refleja diferentes niveles de eficiencia en la gestión de gastos administrativos. Un aumento en este ratio puede señalar mayores costos administrativos en relación con los activos productivos del banco.",
        "Gastos de Operación / Margen Financiero Total":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. B. Pichincha presenta un aumento del 10.52%, pasando de 40.49% a 44.75%, mientras que B. GNB experimenta un incremento del 9.69%. B. ICBC muestra un aumento del 7.54% y Interbank tiene una variación del 1.54%. Esta tendencia mixta refleja diferentes niveles de eficiencia operativa. Un aumento en este ratio puede señalar mayores costos operativos en relación con el margen financiero del banco.",
        "Ingresos Financieros / Ingresos Totales":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. Bank of China presenta un aumento del 12.39%, pasando de 77.08% a 86.63%, mientras que Alfin Banco experimenta un incremento del 8.14%. B. ICBC muestra un aumento del 2.93%, y B. Falabella Perú tiene una variación del 1.43%. En general, estos resultados indican una mayor dependencia de las actividades financieras para generar ingresos.",
        "Ingresos Financieros Anualizados / Activo Productivo Promedio":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. Citibank presenta un aumento del 27.14%, pasando de 7.84% a 9.97%. B. ICBC experimenta un incremento del 26.25%, mientras que B. Santander Perú muestra un aumento del 16.40%. B. Ripley tiene una variación del 15.14%. En general, estos resultados indican una mejora en la eficiencia de los bancos para generar ingresos financieros a partir de sus activos productivos.",
        "Créditos Directos / Personal":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. Bank of China presenta un aumento del 24.05%, pasando de 3875 a 4807 créditos directos por empleado. B. Pichincha experimenta un incremento del 15.23%, de 5691 a 6558. B. GNB muestra un aumento del 10.80%, mientras que B. ICBC tiene una variación del 9.16%. Estos resultados indican una mayor eficiencia en la gestión de créditos por parte de la mayoría de las instituciones financieras.",
        "Depósitos / Número de Oficinas":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. B. BCI Perú presenta un notable aumento del 134.71%, pasando de 490,927.68 a 1,152,260.37. Bank of China experimenta un incremento del 69.41%, de 989,070.87 a 1,675,574.84. B. ICBC muestra un aumento del 52.00%, mientras que B. Pichincha tiene una variación del 31.03%. Estos resultados indican una mayor eficiencia de las oficinas bancarias en la captación de depósitos." ,
        "Utilidad Neta Anualizada / Patrimonio Promedio":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. B. Pichincha presenta un aumento del 176.19%, pasando de -1.17% a -3.24%. Bank of China experimenta un incremento del 136.07%, de 6.17% a 14.56%. B. GNB muestra un aumento del 67.89%, mientras que B. Ripley tiene una variación del 60.20%. Estos resultados sugieren una mejora en la eficiencia y gestión de recursos en la mayoría de los bancos.",
        "Utilidad Neta Anualizada / Activo Promedio":"La tabla y el gráfico muestran las variaciones anuales en este ratio entre agosto de 2023 y agosto de 2024. B. Pichincha presenta un aumento significativo del 207.08%, pasando de -0.11% a -0.34%. B. Ripley experimenta un incremento del 69.23%, de -1.89% a -3.19%. B. GNB muestra un aumento del 60.55%, mientras que BANCOM tiene una variación del -0.39%, manteniéndose en 0.24%. Estos resultados sugieren una mejora en la eficiencia y gestión de recursos en la mayoría de los bancos.",
        "Ratio de Liquidez MN":"La tabla y el gráfico muestran las variaciones anuales en este indicador entre agosto de 2023 y agosto de 2024. Bank of China presenta un aumento significativo del 288.74%, pasando de 140.68% a 207.68%. B. ICBC también experimenta un incremento del 47.63%, manteniéndose en el mismo nivel. B. Pichincha muestra un incremento del 39.09%, de 24.38% a 33.91%, mientras que B. Falabella Perú tiene una variación del 34.66%, de 18.29% a 24.63%. Estos resultados indican que la mayoría de los bancos han mejorado su capacidad para manejar obligaciones a corto plazo.",
        "Ratio de Liquidez ME":"La tabla y el gráfico muestran las variaciones anuales en este indicador entre agosto de 2023 y agosto de 2024. B. BCI Perú presenta un aumento significativo del 78.20%, pasando de 44.77% a 79.82%. Scotiabank Perú experimenta un incremento del 68.58%, de 29.95% a 50.49%. B. Falabella Perú muestra un notable aumento del 59.38%, de 69.62% a 110.96%, mientras que BANCOM tiene una variación del 30.27%, de 49.59% a 64.60%. Estos resultados indican que la mayoría de los bancos han mejorado su capacidad para cumplir con obligaciones a corto plazo en divisas.",
        "Ratio de Caja y Bancos MN / Obligaciones a la Vista MN":"La tabla y el gráfico muestran las variaciones anuales en este indicador entre agosto de 2023 y agosto de 2024. Alfin Banco presenta un aumento significativo del 535.76%, pasando de 3.02% a 19.20%. B. ICBC experimenta un incremento del 229.72%, de 2.12% a 6.99%. B. Pichincha muestra un aumento del 113.79%, de 0.87% a 1.86%, mientras que B. BBVA Perú tiene una variación del 85.19%, de 0.27% a 0.50%. Estos resultados indican que la mayoría de los bancos han mejorado su capacidad para cubrir obligaciones a la vista utilizando activos líquidos en moneda nacional.",
        "Ratio de Caja y Bancos en ME / Obligaciones a la Vista ME":"La tabla y el gráfico muestran las variaciones anuales en este indicador entre agosto de 2023 y agosto de 2024. B. ICBC presenta un aumento significativo del 423.28%, pasando de 2.32% a 12.14%. Mibanco experimenta un incremento del 72.56%, de 126.54% a 218.36%. BANCOM muestra un aumento del 71.58%, de 3.66% a 6.28%, mientras que B. Pichincha tiene una variación del 47.37%, de 2.85% a 4.20%. Estos resultados indican que la mayoría de los bancos han mejorado su capacidad para cubrir obligaciones a la vista utilizando activos líquidos en moneda extranjera."

   }
    
    # Filtrar datos por tipo de indicador
    df_tipo = df[df['Tipo de Indicador'] == tipo_indicador]
    
    indicadores = df_tipo['Indicador'].unique()
    for indicador in indicadores:
        st.subheader(f"Indicador: {indicador}")

                # Mostrar el comentario correspondiente al indicador, si existe
        if indicador in comentarios_indicadores:
            st.write(comentarios_indicadores[indicador])
        else:
            st.write("No hay comentarios disponibles para este indicador.")

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