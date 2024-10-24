
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

