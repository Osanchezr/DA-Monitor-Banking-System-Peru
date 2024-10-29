
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import seaborn as sns


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
    df_2024 = df[df['Fecha'].dt.strftime('%Y-%m') == '2024-09'][['Entidad', 'Valor']].rename(columns={'Valor': 'Set-2024'})
    df_2023 = df[df['Fecha'].dt.strftime('%Y-%m') == '2023-09'][['Entidad', 'Valor']].rename(columns={'Valor': 'Set-2023'})
    df_variacion = pd.merge(df_2024, df_2023, on='Entidad', how='outer')  # Mantener todas las entidades

    # Calcular la variación anual
    df_variacion['Var-Anual'] = (df_variacion['Set-2024'] - df_variacion['Set-2023']) / df_variacion['Set-2023'] * 100

    # Redondear los valores a 2 decimales
    df_variacion[['Set-2024', 'Set-2023']] = df_variacion[['Set-2024', 'Set-2023']].round(2)
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
    df_variacion = df_variacion[['Entidad', 'Set-2023', 'Set-2024', 'Var-Anual']]

    return df_variacion

# Gráfico de barras por indicador (con barras horizontales y colores)
def grafico_barras(df, indicador):
    # Ordenar por el valor de 2024 de mayor a menor
    df = df.sort_values(by='Set-2024', ascending=True)
    
    # Asignar colores a las barras, rojo para valores negativos
    colores = ['red' if x < 0 else 'blue' for x in df['Set-2024']]
    
    fig = px.bar(df, 
                 x='Set-2024', y='Entidad', 
                 orientation='h',  # Barras horizontales
                 text='Set-2024', 
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

# Función para graficar resultados
def graficar_resultados(df_kpi_bank, resultado_combinado, nuevos_bancos, indicadores_deseados):
    """
    Genera gráficos interactivos para visualizar la evolución de los indicadores seleccionados
    por entidad, con coloración según los clusters asignados.
    
    Parámetros:
    - df_kpi_bank (pd.DataFrame): DataFrame con los KPIs bancarios, incluyendo 'Fecha', 'Entidad', 'Indicador', y 'Valor'.
    - resultado_combinado (pd.DataFrame): DataFrame con la asignación de clusters por entidad e indicador.
    - nuevos_bancos (list): Lista de entidades (bancos) que se deben excluir del análisis.
    - indicadores_deseados (list): Lista de indicadores financieros que se desean graficar.
    
    El gráfico muestra una línea temporal para cada entidad, y los colores representan los clusters a los que pertenecen.
    Los gráficos se generan con títulos específicos para cada indicador y son interactivos.
    """
    fig = go.Figure()

    for indicador_deseado in indicadores_deseados:
        # Filtrar solo el indicador deseado
        df_indicador = df_kpi_bank[df_kpi_bank['Indicador'] == indicador_deseado]

        # Filtrar entidades para excluir los nuevos bancos
        df_indicador_sin_nuevos = df_indicador[~df_indicador['Entidad'].isin(nuevos_bancos)]

        # Pivotar la tabla para obtener las series de tiempo por entidad
        df_pivot = df_indicador_sin_nuevos.pivot_table(
            index='Fecha',
            columns='Entidad',
            values='Valor',
            aggfunc='mean'
        ).fillna(0)

        # Agregar información de clusters a las entidades
        clusters = resultado_combinado[['Entidad', indicador_deseado]].set_index('Entidad').to_dict()[indicador_deseado]

        # Obtener los clusters únicos y asignar colores
        unique_clusters = np.unique(list(clusters.values()))
        colors = sns.color_palette("hsv", len(unique_clusters))
        cluster_color_map = {cluster: f'rgb({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)})' for cluster, color in zip(unique_clusters, colors)}

        # Crear trazas para cada entidad
        for entidad in df_pivot.columns:
            if entidad in clusters:
                cluster = clusters[entidad]
                color = cluster_color_map[cluster]

                hover_text = [
                    f'Entidad: {entidad}<br>'
                    f'Fecha: {df_pivot.index[i].date()}<br>'
                    f'Valor: {df_pivot[entidad][i]:.2f}'
                    for i in range(len(df_pivot))
                ]

                fig.add_trace(go.Scatter(
                    x=df_pivot.index,
                    y=df_pivot[entidad],
                    mode='lines',
                    name=f'{entidad} (Cluster {cluster})',
                    line=dict(color=color),
                    hoverinfo='text',
                    hovertext=hover_text,
                    showlegend=True
                ))

        fig.update_layout(
            title=f'Evolución de {indicador_deseado} por Entidad (Colores según Cluster)',
            xaxis_title='Fecha',
            yaxis_title=indicador_deseado,
            legend_title='Entidades',
            hovermode='closest',
            margin=dict(t=50, b=50),
            height=400 * len(indicadores_deseados)
        )

    st.plotly_chart(fig)


def pagina_analisis_clusters(df_kpi_bank, resultado_combinado):
    st.title("Análisis de Clusters")

    # Selección de tipo de indicador
    tipos_indicadores = df_kpi_bank['Tipo de Indicador'].unique()
    tipo_indicador_seleccionado = st.selectbox('Selecciona un tipo de indicador', tipos_indicadores)

    # Filtrar indicadores disponibles según el tipo seleccionado
    indicadores_disponibles = df_kpi_bank[df_kpi_bank['Tipo de Indicador'] == tipo_indicador_seleccionado]['Indicador'].unique()
    indicador_seleccionado = st.selectbox('Selecciona un indicador', indicadores_disponibles)

    # Validar si el indicador seleccionado tiene clusters disponibles
    if indicador_seleccionado not in resultado_combinado.columns[1:].tolist():   #df.columns[1:].tolist()
        st.warning(f"El indicador '{indicador_seleccionado}' no muestra una segmentación notoria.")
    else:
        # Filtrar indicadores deseados para graficar
        indicadores_deseados = [indicador_seleccionado]

        # Obtener la lista de nuevos bancos (puedes ajustar esto según tu lógica)
        nuevos_bancos = ['B. BCI Perú', 'Bank of China']  # Aquí podrías definir los nuevos bancos si los tienes

        # Llamar a la función para graficar resultados
        graficar_resultados(df_kpi_bank, resultado_combinado, nuevos_bancos, indicadores_deseados)

         # Agregar un comentario por gráfico
        st.write(f"Comentario para el gráfico del indicador '{indicador_seleccionado}':")
        
        # Ejemplo de comentarios personalizados
        if indicador_seleccionado == 'Ratio de Capital Global':
            st.text(
            """La mayoría de los bancos se agrupan en el Cluster 1, con ratios de capital global relativamente bajos y estables (10-30),
            lo que incluye entidades como BBVA Perú, BCP, e Interbank, mostrando una evolución similar en la gestión de su capital.
            
            En contraste, el Banco ICBC (Cluster 0) tiene un comportamiento atípico, con un ratio de capital mucho más alto (hasta 70),
            pero con una tendencia descendente desde 2017, lo que sugiere ajustes significativos en su capitalización.
            
            Algunas entidades, como Citibank y Alfin Banco, presentan fluctuaciones dentro del Cluster 1, pero sin desviarse de la tendencia
            general de estabilidad.""")

        elif indicador_seleccionado == 'Créditos Atrasados MN / Créditos Directos MN':
            st.text(
            """En la evolución del ratio Créditos Atrasados MN / Créditos Directos MN, B. ICBC del Cluster 0 muestra una
            variación marcada en el 2016, por lo cual el modelo lo categoriza solo en un cluster. Este comportamiento del 
            indicador en el pasado ya se regularizó actualmente.""")

        elif indicador_seleccionado == 'Créditos Atrasados ME / Créditos Directos ME':
            st.text(
            """En la evolución del ratio Créditos Atrasados ME / Créditos Directos ME, las entidades del Cluster 0 demuestran 
            una tendencia estable, lo que indica una gestión eficiente de sus préstamos. En contraste, B. Falabella Perú y Mibanco 
            del Cluster 1 presentan una mayor variabilidad en sus ratios, lo que sugiere una posible exposición a riesgos financieros 
            o cambios en sus estrategias. Se recomienda que las entidades del Cluster 0 continúen con sus prácticas actuales, 
            mientras que las del Cluster 1 deben investigar las causas de su fluctuación y ajustar sus estrategias para mejorar 
            la estabilidad en la gestión de créditos en moneda extranjera.""")

        elif indicador_seleccionado == 'Gastos de Administración Anualizados / Activo Productivo Promedio':
            st.text(
            """En la evolución del ratio Gastos de Administración Anualizados / Activo Productivo Promedio, las entidades del Cluster 0,
            que incluyen a B. BBVA Perú y B. de Crédito del Perú, presentan una tendencia estable, lo que sugiere una gestión eficiente de sus 
            costos administrativos. Por otro lado, Alfin Banco, del Cluster 1, exhibe una mayor variabilidad en su ratio, lo que podría indicar
            una exposición a riesgos o cambios en su estrategia. Se recomienda a las entidades del Cluster 0 que mantengan sus prácticas actuales,
            mientras que Alfin Banco debería investigar las causas de su fluctuación y ajustar sus estrategias para mejorar la gestión de sus costos.""")

        elif indicador_seleccionado == 'Gastos de Operación / Margen Financiero Total':
            st.text(
            """Banco Alfin, la única entidad en el Cluster 1, ha presentado en el pasado una variación significativa en el indicador 
            de 'Gastos de Operación / Margen Financiero Total', aunque actualmente esta variabilidad se ha regularizado.""")

        elif indicador_seleccionado == 'Ingresos Financieros Anualizados / Activo Productivo Promedio':
            st.text(
            """En la evolución de Ingresos Financieros Anualizados / Activo Productivo Promedio, el Cluster 0 
            (B. BBVA Perú, B. de Crédito del Perú, etc.) muestra estabilidad y eficiencia en su gestión de ingresos. 
            El Cluster 1 (B. Falabella Perú, B. Ripley, Mibanco) presenta mayor variabilidad, reflejando diferentes estrategias y niveles de riesgo.
            Alfin Banco, en el Cluster 2, destaca con uno de los ratios más altos, lo que puede ser positivo, pero también implica un mayor riesgo
            si no se gestiona adecuadamente. Se recomienda que Cluster 0 mantenga sus estrategias actuales, que Cluster 1 evalúe sus variabilidades
            y que Alfin Banco diversifique sus fuentes de ingresos para mitigar riesgos.""")

        elif indicador_seleccionado == 'Créditos Directos / Personal':
            st.text(
            """En la evolución de Créditos Directos / Personal, el Cluster 0, representado por B. Santander Perú, muestra una tendencia estable,
            lo que indica una gestión eficiente de sus recursos humanos en relación con los créditos otorgados. En contraste, el Cluster 1, que incluye
            entidades como Alfin Banco, B. BBVA Perú y B. Falabella Perú, presenta mayor variabilidad en sus ratios, sugiriendo diferentes estrategias
            y niveles de eficiencia. Se recomienda que Cluster 0 mantenga sus estrategias actuales y que las entidades del Cluster 1 evalúen las causas
            de su variabilidad para mejorar la estabilidad y eficiencia en la gestión de créditos directos.""")

        elif indicador_seleccionado == 'Depósitos / Número de Oficinas':
            st.text(
            """En la evolución de Depósitos / Número de Oficinas, el Cluster 0, que incluye a B. Santander Perú y Citibank, muestra una tendencia estable,
            indicando una gestión eficiente de sus recursos en relación con la expansión de oficinas. En cambio, el Cluster 1, que comprende entidades como 
            Alfin Banco y B. Falabella Perú, presenta mayor variabilidad en sus ratios, sugiriendo diferencias en las estrategias y niveles de eficiencia.
            Se recomienda que el Cluster 0 mantenga sus estrategias actuales, mientras que el Cluster 1 debe evaluar las causas de su variabilidad
            para mejorar la estabilidad y eficiencia en la gestión de depósitos.""")

        elif indicador_seleccionado == 'Utilidad Neta Anualizada / Patrimonio Promedio':
            st.text(
            """En la evolución de Utilidad Neta Anualizada / Patrimonio Promedio, el Cluster 0, que incluye a B. BBVA Perú, B. Falabella Perú y otras,
            muestra una tendencia estable con fluctuaciones menores, indicando una gestión eficiente de su patrimonio. Por otro lado, Alfin Banco en el Cluster 1 
            presenta mayor variabilidad en su ratio, lo que sugiere una mayor exposición a riesgos o cambios en su estrategia financiera. Se recomienda que las entidades 
            del Cluster 0 mantengan sus estrategias actuales, mientras que Alfin Banco debe evaluar las causas de su variabilidad y ajustar sus estrategias 
            para mejorar su estabilidad y eficiencia.""")

        elif indicador_seleccionado == 'Utilidad Neta Anualizada / Activo Promedio':
            st.text(
            """En la evolución de Utilidad Neta Anualizada / Activo Promedio, Alfin Banco, en el Cluster 0, muestra una tendencia estable, 
            lo que indica una gestión eficiente y consistente de sus activos. En contraste, el Cluster 1, que incluye entidades como B. Ripley y B. Falabella Perú,
            presenta mayor variabilidad en sus ratios, sugiriendo diferencias en estrategias y niveles de eficiencia en la gestión de activos.
            Se recomienda que Alfin Banco mantenga sus estrategias actuales y que las entidades del Cluster 1 evalúen las causas de su variabilidad 
            para mejorar su estabilidad y eficiencia.""")

        elif indicador_seleccionado == 'Caja y Bancos en ME / Obligaciones a la Vista':
            st.text(
            """En la evolución de Caja y Bancos en ME / Obligaciones a la Vista, las entidades del Cluster 0, que incluye a Alfin Banco y B. BBVA Perú,
            muestran una tendencia estable, lo que indica una gestión eficiente de sus recursos en moneda extranjera. Por otro lado, Mibanco, en el Cluster 1,
            presenta mayor variabilidad en su ratio, sugiriendo una posible exposición a riesgos o cambios en su estrategia financiera. Se recomienda que las entidades
            del Cluster 0 mantengan sus estrategias actuales, mientras que Mibanco debe evaluar las causas de su variabilidad para mejorar la estabilidad
            y eficiencia en la gestión de sus recursos.""")

        elif indicador_seleccionado == 'Ratio de Liquidez MN':
            st.text(
            """En la evolución del Ratio de Liquidez MN, B. ICBC, del Cluster 0, muestra una tendencia estable, lo que indica una gestión eficiente de sus recursos líquidos.
            En contraste, el Cluster 1, que incluye a entidades como B. BBVA Perú y B. Falabella Perú, presenta mayor variabilidad en sus ratios de liquidez,
            sugiriendo diferencias en estrategias y niveles de eficiencia en la gestión de recursos. Se recomienda que B. ICBC mantenga sus estrategias actuales,
            mientras que las entidades del Cluster 1 deben evaluar las causas de su variabilidad y ajustar sus estrategias para mejorar la estabilidad
            y eficiencia en la gestión de recursos líquidos.""")

        elif indicador_seleccionado == 'Ratio de Liquidez ME':
            st.text(
            """En la evolución del Ratio de Liquidez ME, las entidades del Cluster 0, que incluyen a Alfin Banco y B. BBVA Perú, presentan una tendencia estable,
            lo que indica una gestión eficiente de sus recursos líquidos. En cambio, B. Ripley, del Cluster 1, muestra una mayor variabilidad en su ratio,
            sugiriendo una posible exposición a riesgos o cambios en su estrategia financiera. Se recomienda que las entidades del Cluster 0 mantengan sus estrategias actuales 
            para asegurar esta estabilidad, mientras que B. Ripley debe evaluar las causas de su variabilidad y ajustar sus estrategias para mejorar la estabilidad 
            y eficiencia en la gestión de sus recursos líquidos.""")

        elif indicador_seleccionado == 'Caja y Bancos MN / Obligaciones a la Vista MN':
            st.text(
            """En la evolución de Caja y Bancos MN / Obligaciones a la Vista MN, las entidades del Cluster 0, que incluyen a Alfin Banco y B. BBVA Perú,
            presentan una tendencia relativamente estable en sus ratios, indicando una gestión eficiente y consistente de sus recursos líquidos.
            No se dispone de datos para los Clusters 1 y 2, lo que limita las recomendaciones para esas entidades. Para el Cluster 0, se sugiere mantener 
            las estrategias actuales que aseguran esta estabilidad y eficiencia.""")


