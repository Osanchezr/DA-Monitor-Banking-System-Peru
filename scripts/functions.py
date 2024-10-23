
import re
import os
import time
import requests
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import silhouette_score
from tslearn.clustering import TimeSeriesKMeans, KShape
from sklearn.model_selection import ParameterGrid

##FUNCION DE EXTRACCIÓN DE DATOS

def scrape_and_download_excels(chrome_driver_path, url, output_folder):
    """
    Realiza web scraping en una página de la SBS para encontrar y descargar archivos Excel (.XLS) 
    correspondientes a ciertos meses y años. Los archivos se guardan en la carpeta especificada.

    Parámetros:
    - `chrome_driver_path` (str): Ruta al controlador ChromeDriver para Selenium.
    - `url` (str): URL de la página web con los enlaces a los archivos Excel.
    - `output_folder` (str): Ruta de la carpeta donde se descargarán los archivos. Se creará si no existe.

    Funcionamiento:
    1. Se abre la página web especificada en la URL usando Selenium.
    2. Se realiza una búsqueda de todos los elementos de tipo `a` (enlaces) en la página.
    3. Se filtran los enlaces que apunten a archivos Excel (.XLS) y cuyos nombres contengan un mes y año válido.
       - Los meses válidos se definen entre agosto de 2015 y agosto de 2024.
       - Se utilizan las abreviaturas en español de los meses (por ejemplo, "en" para enero, "fe" para febrero, etc.).
    4. Una vez localizados los enlaces válidos, se procede a descargar cada archivo Excel.
    5. Cada archivo descargado se guarda en la carpeta especificada con su nombre original.

    """

    # Verificar si la carpeta existe; si no, crearla
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Inicializa el controlador de Selenium
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Abre el navegador y accede a la URL
    driver.get(url)

    # Esperar a que la página se cargue completamente
    time.sleep(5)  # Ajusta el tiempo según sea necesario

    # Encuentra todos los enlaces a los archivos Excel
    enlaces_excel = []
    links = driver.find_elements(By.TAG_NAME, "a")

    # Diccionario con las abreviaturas de los meses en los enlaces
    meses_abrev = {
        1: "en", 2: "fe", 3: "ma", 4: "ab", 5: "my", 6: "jn", 7: "jl", 8: "ag",
        9: "se", 10: "oc", 11: "no", 12: "di"
    }

    # Definimos los meses válidos desde agosto 2015 hasta agosto 2024
    meses_validos = {
        2015: range(8, 13),  # Desde agosto 2015
        2024: range(1, 9),   # Hasta agosto 2024
    }

    # Llenamos los meses para los años intermedios (2016-2023)
    for year in range(2016, 2024):
        meses_validos[year] = range(1, 13)

    # Recorremos los enlaces y filtramos aquellos que contienen el año y mes correctos
    for link in links:
        href = link.get_attribute('href')
        if href and href.endswith(".XLS"):
            # Buscar si el enlace contiene un año entre 2015 y 2024
            for year in range(2015, 2025):
                if f"{year}" in href:
                    # Buscar si contiene un mes válido dentro de ese año
                    for month in meses_validos[year]:
                        month_abrev = meses_abrev[month]
                        if f"-{month_abrev}{year}" in href:
                            enlaces_excel.append(href)
                            break  # Deja de buscar cuando encuentres un enlace que coincida

    # Cierra el navegador
    driver.quit()

    # Descargar cada archivo Excel
    for enlace in enlaces_excel:
        try:
            # Descargar el archivo Excel
            response = requests.get(enlace)
            archivo = BytesIO(response.content)

            # Extraer el nombre del archivo desde la URL
            nombre_archivo = enlace.split("/")[-1]

            # Ruta completa del archivo donde será guardado
            ruta_guardado = os.path.join(output_folder, nombre_archivo)

            # Guardar el archivo en la carpeta especificada
            with open(ruta_guardado, 'wb') as f:
                f.write(archivo.getbuffer())

            print(f"Archivo {nombre_archivo} descargado correctamente en {ruta_guardado}.")
            
        except Exception as e:
            print(f"Error descargando el archivo {enlace}: {e}")


# FUNCIÓN DE TRANSFORMACIÓN DE ARCHIVOS EXCEL A FORMATO DE BASE DE DATOS

def transformar_desde_carpeta(carpeta_relativa):
    """
    Procesa y estructura los archivos Excel de una carpeta específica, extrae información financiera y 
    combina los datos en un único DataFrame dando fromato de base de datos.

    Parámetros:
    - `carpeta_relativa` (str): Ruta relativa de la carpeta que contiene los archivos Excel a procesar.

    Funcionamiento:
    1. La función toma todos los archivos Excel de la carpeta especificada.
    2. Cada archivo es leído y se extraen los datos relevantes, eliminando filas y columnas vacías.
    3. Se obtiene el nombre de los bancos y la fecha del reporte a partir del nombre del archivo.
    4. Los indicadores financieros y sus valores se organizan por banco y se asignan a categorías predefinidas.
    5. Los datos se limpian de valores no numéricos o inválidos y se normalizan los nombres de los bancos.
    6. Finalmente, todos los archivos procesados se combinan en un solo DataFrame con columnas: 'Fecha', 
       'Tipo de Indicador', 'Indicador', 'Entidad' (nombre del banco) y 'Valor'.
    """

    # Obtener la ruta absoluta del directorio actual (donde está el script)
    directorio_actual = os.getcwd()

    # Crear la ruta absoluta de la carpeta 'data' en el repositorio
    carpeta = os.path.join(directorio_actual, carpeta_relativa)

    # DataFrame final donde se agregarán los datos limpios
    df_final = pd.DataFrame()

    # Recorrer todos los archivos en la carpeta
    for archivo_nombre in os.listdir(carpeta):
        # Verificar que el archivo sea de tipo Excel
        if archivo_nombre.endswith(".XLS") or archivo_nombre.endswith(".xlsx"):
            archivo_ruta = os.path.join(carpeta, archivo_nombre)  # Ruta completa del archivo

            # Leer el archivo Excel
            df = pd.read_excel(archivo_ruta)

            # Extraer la fecha del nombre del archivo (por ejemplo, "ag2024")
            match = re.search(r"(\w{2})(\d{4})", archivo_nombre)
            if match:
                mes_abrev = match.group(1)  # Ejemplo: 'ag'
                year = match.group(2)       # Ejemplo: '2024'

                # Mapa de abreviaturas de meses a números
                meses = {
                    'en': '01', 'fe': '02', 'ma': '03', 'ab': '04', 'my': '05', 'jn': '06',
                    'jl': '07', 'ag': '08', 'se': '09', 'oc': '10', 'no': '11', 'di': '12'
                }

                # Obtener el mes en formato numérico
                mes_num = meses.get(mes_abrev.lower(), '01')  # Por defecto, '01' (enero) si no se encuentra el mes

                # Construir la fecha del reporte (usamos el último día del mes como ejemplo)
                fecha_reporte = f"{year}-{mes_num}-31"
            else:
                # Valor por defecto si no se encuentra el formato esperado en el nombre del archivo
                fecha_reporte = "2024-10-01"  # Ajusta este valor por defecto


            # Paso 1: Eliminar filas y columnas vacías
            df_cleaned = df.dropna(how='all', axis=1).dropna(how='all', axis=0)

            # Paso 2: Eliminar filas que contienen solo un valor no nulo
            df_cleaned = df_cleaned[df_cleaned.notna().sum(axis=1) > 1]

            df_cleaned = df_cleaned.drop(df_cleaned.columns[9], axis=1)

            # Paso 3: Identificar los nombres de los bancos (se supone que están en la fila 4)
            bancos = df_cleaned.iloc[3, 1:].dropna().tolist()

            bancos = [
                ' '.join(
                    re.sub(r'\*.*$', '', banco)    # Elimina asteriscos y texto a su derecha
                    .replace('\n', ' ')            # Reemplaza saltos de línea con espacio
                    .strip()                       # Elimina espacios al inicio y al final
                    .split()                       # Divide en palabras
                )
                for banco in bancos
            ]

            # Eliminar texto entre paréntesis
            bancos = [re.sub(r'\(.*?\)', '', banco).strip() for banco in bancos]
                                    
            # Lista de nombres válidos de bancos (completa con todos los bancos necesarios)
            nombres_bancos_validos = [
                'B. BBVA Perú', 'BANCOM', 'B. De Crédito del Perú', 'B. Pichincha',
                'B. Interamericano de Finanzas', 'Scotiabank Perú', 'Citibank', 'Interbank', 'B. GNB',
                'B. Falabella Perú', 'B. Santander Perú', 'B. Ripley', 'Alfin Banco', 'B. ICBC', 'Bank of China',
                'B. BCI Perú', 'B. Continental', 'B. De Comercio', 'B. Financiero',
                'Interbank', 'Mibanco', 'B. Azteca Perú',
                'Scotiabank Perú', 'B. China Perú', 'Deutsche Bank Perú',
                'HSBC Bank Perú', 'B. Cencosud'
            ]

            # Paso 4: Crear un DataFrame final con las columnas necesarias
            df_resultado = pd.DataFrame(columns=["Fecha", "Tipo de Indicador", "Indicador", "Banco", "Valor"])

            # Categorías de indicadores
            categorias = [
                "SOLVENCIA", "SOLVENCIA**", "SOLVENCIA***", "CALIDAD DE ACTIVOS", "CALIDAD DE ACTIVOS**",
                "CALIDAD DE ACTIVOS***", "EFICIENCIA Y GESTIÓN", "EFICIENCIA Y GESTIÓN**",
                "EFICIENCIA Y GESTIÓN***", "LIQUIDEZ", "LIQUIDEZ**", "LIQUIDEZ***",
                "RENTABILIDAD", "RENTABILIDAD**", "RENTABILIDAD***"
            ]

            # Variables para seguir el tipo de indicador actual
            tipo_actual = None

            # Lista para almacenar filas de datos
            data_list = []

            # Iterar a través de las filas del DataFrame limpio, empezando desde la fila 7 (donde comienzan los indicadores)
            for i in range(4, len(df_cleaned)):
                indicador = df_cleaned.iloc[i, 0]  # Primera columna es el indicador

                # Si el indicador es una de las categorías, actualizamos el tipo_actual
                if indicador in categorias:
                    tipo_actual = indicador
                    continue  # Saltamos esta fila ya que es una categoría, no un indicador

                # Si es una nota o comentario (empieza con "Nota", "*", "**"), la ignoramos
                if isinstance(indicador, str) and (indicador.startswith("Nota") or indicador.startswith("*") or indicador.startswith("**")):
                    continue

                # Iterar a través de las columnas para obtener los valores correspondientes a cada banco
                for j in range(1, len(bancos) + 1):  # Recorremos las columnas de bancos
                    valor = df_cleaned.iloc[i, j]  # Obtener el valor correspondiente
                    banco = bancos[j - 1]  # Obtener el nombre del banco

                    # Validar que el nombre del banco sea un nombre válido y no contenga términos no deseados
                    if banco not in nombres_bancos_validos or "Total" in banco or "Promedio" in banco:
                        continue

                    # Si el valor no es un número, lo ignoramos
                    if pd.isna(valor) or not isinstance(valor, (int, float)):
                        continue

                    # Crear un diccionario con los valores
                    row = {
                        "Fecha": fecha_reporte,  # Añadir la fecha del reporte extraída
                        "Tipo de Indicador": tipo_actual if tipo_actual is not None else "SIN_CATEGORIA",  # Tipo de Indicador actual
                        "Indicador": indicador,  # Nombre del indicador
                        "Entidad": banco,  # Nombre del banco
                        "Valor": valor  # Valor asociado
                    }

                    # Agregar la fila a la lista de datos
                    data_list.append(row)

            # Crear un nuevo DataFrame a partir de la lista de filas
            df_resultado = pd.DataFrame(data_list)

            # Concatenar el DataFrame procesado con el final
            df_final = pd.concat([df_final, df_resultado], ignore_index=True)

    return df_final

# FUNCIONES DE LIMPIEZA DE DATOS

def limpieza_general_data(df):
    """
    Realiza la limpieza general del DataFrame:
    - Elimina caracteres especiales en los nombres de indicadores y entidades.
    - Corrige los nombres de indicadores y entidades eliminando texto entre paréntesis y asteriscos.
    - Quita espacios en blanco al inicio o final de las cadenas de texto.
    
    :param df: DataFrame con los datos financieros.
    :return: DataFrame limpio con las correcciones aplicadas.
    """
    df['Tipo de Indicador'] = df['Tipo de Indicador'].replace("CALIDAD DE ACTIVOS**", "CALIDAD DE ACTIVOS")
    df['Indicador'] = df['Indicador'].str.replace(r"\s*\(.*?\)", "", regex=True).str.strip()
    df['Indicador'] = df['Indicador'].str.replace('*', '', regex=False)
    df['Entidad'] = df['Entidad'].str.replace(r'\s*\(.*?\)', '', regex=True)
    
    # Limpiar espacios en blanco en la columna 'Entidad' y "Tipo de Indicador"
    df['Entidad'] = df['Entidad'].str.strip()
    df['Tipo de Indicador'] = df['Tipo de Indicador'].str.strip()
    
    return df

def reemplazo_nombre_entidades(df):
    """
    Reemplaza los nombres de entidades financieras en el DataFrame con versiones estandarizadas.
    
    :param df: DataFrame con los datos financieros.
    :return: DataFrame con los nombres de entidades corregidos.
    """
    replacements = {
        'B. De Comercio': 'BANCOM',
        'B. Financiero': 'B. Pichincha',
        'B. China Perú': 'Bank of China',
        'B. Azteca Perú': 'Alfin Banco',
        "B. Continental": "BBVA Perú",
    }

    df["Entidad"] = df["Entidad"].replace(replacements)
    df["Entidad"] = df["Entidad"].replace("BBVA Perú", "B. BBVA Perú")
    
    return df


def eliminar_banco_indicador(df, bancos_a_excluir, indicador_a_eliminar):
    """
    Elimina del DataFrame las filas correspondientes a ciertos bancos y a un indicador específico.
    
    :param df: DataFrame con los datos financieros.
    :param bancos_a_excluir: Lista de nombres de bancos a excluir.
    :param indicador_a_eliminar: Nombre del indicador que se desea eliminar.
    :return: DataFrame filtrado sin los bancos e indicadores excluidos.
    """
    # Eliminar los bancos específicos
    df_limpio = df[~df['Entidad'].isin(bancos_a_excluir)]

    # Normalizar la columna 'Indicador' eliminando espacios adicionales
    df_limpio['Indicador'] = df_limpio['Indicador'].str.strip()

    # Eliminar el indicador específico
    df_limpio = df_limpio[~(df_limpio['Indicador'] == indicador_a_eliminar)]

    return df_limpio



def corregir_fecha(fecha_str):
    """
    Corrige una fecha en formato de cadena (string) en diferentes formatos y la convierte en formato de fecha.
    Si el día es inválido para un mes dado, ajusta al último día válido del mes.
    
    :param fecha_str: Fecha en formato de cadena, con formato 'YYYY-MM-DD' o 'DD/MM/YYYY'.
    :return: Fecha corregida en formato de pandas (pd.Timestamp).
    """
    # Intentar convertir la fecha directamente
    try:
        # Primero, tratamos de detectar el formato
        if '-' in fecha_str:  # Formato YYYY-MM-DD
            fecha = pd.to_datetime(fecha_str, format='%Y-%m-%d')
        else:  # Formato DD/MM/YYYY
            fecha = pd.to_datetime(fecha_str, format='%d/%m/%Y', dayfirst=True)
        
        # Verificamos si la fecha es válida, en caso de que haya un error
        return fecha
    
    except ValueError:
        # Si falla, intentamos manejar la fecha manualmente
        if '-' in fecha_str:  # Formato YYYY-MM-DD
            anio, mes, dia = map(int, fecha_str.split('-'))
        else:  # Formato DD/MM/YYYY
            dia, mes, anio = map(int, fecha_str.split('/'))
        
        # Verificamos si el día es mayor que el último día del mes
        if mes == 2:  # Febrero
            if anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0):  # Año bisiesto
                ultimo_dia = 29
            else:
                ultimo_dia = 28
        elif mes in [4, 6, 9, 11]:  # Meses con 30 días
            ultimo_dia = 30
        else:  # Meses con 31 días
            ultimo_dia = 31
        
        # Si el día es mayor que el último día, corregimos
        if dia > ultimo_dia:
            dia = ultimo_dia
        
        # Regresar la fecha corregida
        if '-' in fecha_str:  # Si era formato YYYY-MM-DD
            return pd.to_datetime(f"{anio}-{mes}-{dia}", format='%Y-%m-%d')
        else:  # Si era formato DD/MM/YYYY
            return pd.to_datetime(f"{dia}/{mes}/{anio}", format='%d/%m/%Y')

#FUNCIONES PARA EXPLORACION DE DATOS

def identificar_combinaciones_faltantes(df, entidades_a_excluir):
    """
    Función para identificar las combinaciones faltantes de entidad, indicador y fecha en un DataFrame,
    excluyendo algunas entidades específicas.

    Parámetros:
    df (pd.DataFrame): El DataFrame que contiene los datos a analizar.
    entidades_a_excluir (list): Lista de entidades que se deben excluir del análisis.

    Retorno:
    pd.DataFrame: Un DataFrame que contiene las combinaciones faltantes de entidad, indicador y fecha.
    """
    # Asegúrate de que la columna 'Fecha' está en formato datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    # Paso 1: Identificar todas las entidades, indicadores y fechas únicas, excluyendo las entidades específicas
    df_filtrado = df[~df['Entidad'].isin(entidades_a_excluir)]

    entidades_unicas = df_filtrado['Entidad'].unique()
    indicadores_unicos = df_filtrado['Indicador'].unique()
    fechas_unicas = df_filtrado['Fecha'].unique()

    # Paso 2: Crear un DataFrame con todas las combinaciones posibles
    combinaciones_posibles = pd.MultiIndex.from_product(
        [entidades_unicas, indicadores_unicos, fechas_unicas],
        names=['Entidad', 'Indicador', 'Fecha']
    ).to_frame(index=False)

    # Paso 3: Unir con el DataFrame original para encontrar faltantes
    combinaciones_completas = combinaciones_posibles.merge(df, on=['Entidad', 'Indicador', 'Fecha'], how='left', indicator=True)

    # Paso 4: Filtrar combinaciones faltantes
    faltantes = combinaciones_completas[combinaciones_completas['_merge'] == 'left_only']

    # Mostrar resultados
    if faltantes.empty:
        print("Todas las entidades (excluyendo las especificadas) tienen todos los indicadores en todas las fechas.")
    else:
        print("Faltan las siguientes combinaciones de entidad, indicador y fecha:")
        return faltantes[['Entidad', 'Indicador', 'Fecha']]



def graficar_histogramas_por_tipo(df):
    """
    Función para graficar histogramas de indicadores agrupados por tipo de indicador.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene los datos de los indicadores.

    Retorno:
    None: Muestra los histogramas en un gráfico.
    """
    # Listar los tipos de indicadores únicos
    tipos_unicos = df['Tipo de Indicador'].unique()

    # Inicializar un diccionario para almacenar los datos de cada indicador y tipo
    indicadores_y_datos = {}

    # Recolectar los datos para cada tipo de indicador
    for tipo in tipos_unicos:
        datos_tipo = df[df['Tipo de Indicador'] == tipo]
        indicadores_unicos = datos_tipo['Indicador'].unique()
        indicadores_y_datos[tipo] = {indicador: datos_tipo[datos_tipo['Indicador'] == indicador]['Valor'] for indicador in indicadores_unicos}

    # Calcular el número total de subgráficas
    total_indicadores = sum(len(datos) for datos in indicadores_y_datos.values())
    num_col = 3  # Número de columnas deseadas
    num_row = int(np.ceil(total_indicadores / num_col))  # Calcular el número de filas necesarias

    # Reducir el tamaño del gráfico (puedes ajustar estos valores)
    fig, axes = plt.subplots(num_row, num_col, figsize=(10, 3 * num_row), sharex=False)
    axes = axes.flatten()  # Aplanar la lista de ejes para fácil iteración

    # Variable para el índice de subgráficas
    index = 0

    # Crear un histograma para cada indicador en subgráficas separadas
    for tipo, indicadores in indicadores_y_datos.items():
        for indicador, datos_indicador in indicadores.items():
            if index < len(axes):  # Verificar que aún haya subgráficas disponibles
                axes[index].hist(datos_indicador, bins=20, alpha=0.7)
                axes[index].set_title(f'{tipo}\n{indicador}', fontsize=9, pad=5)  # Tipo de indicador en la parte superior
                axes[index].set_ylabel('Frecuencia', fontsize=8)
                axes[index].grid(axis='y', alpha=0.75)
                axes[index].tick_params(axis='both', which='major', labelsize=8)  # Reducir tamaño de etiquetas
                index += 1

    # Eliminar subgráficas vacías si hay alguna
    for ax in axes[index:]:
        ax.remove()

    # Personalizar el gráfico
    plt.tight_layout(pad=2)  # Ajustar el espacio entre subgráficas
    plt.show()


def detectar_outliers_y_visualizar(df, indicador, entidades_a_excluir=None):
    """
    Función para detectar outliers en un indicador específico y visualizarlo con un boxplot.

    Parámetros:
    df (pd.DataFrame): DataFrame que contiene los datos de los indicadores.
    indicador (str): Nombre del indicador a analizar.
    entidades_a_excluir (list, optional): Lista de entidades a excluir del análisis.

    Retorno:
    pd.DataFrame: DataFrame con los outliers detectados.
    None: Muestra el boxplot del indicador.
    """
    # Filtrar el DataFrame para el indicador específico
    if entidades_a_excluir:
        df_filtrado = df[~df['Entidad'].isin(entidades_a_excluir)]
    else:
        df_filtrado = df

    df_indicador = df_filtrado[df_filtrado['Indicador'] == indicador]

    # Eliminar valores NaN
    df_indicador_clean = df_indicador.dropna(subset=['Valor'])

    # Paso 1: Detectar outliers utilizando el método del IQR
    Q1 = df_indicador_clean['Valor'].quantile(0.25)
    Q3 = df_indicador_clean['Valor'].quantile(0.75)
    IQR = Q3 - Q1

    # Definir los límites para los outliers
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    # Filtrar los outliers
    outliers = df_indicador_clean[(df_indicador_clean['Valor'] < limite_inferior) | (df_indicador_clean['Valor'] > limite_superior)]

    # Paso 2: Visualización con un Boxplot
    plt.figure(figsize=(6, 4))
    plt.boxplot(df_indicador_clean['Valor'], vert=False, patch_artist=True, boxprops=dict(facecolor="skyblue"))
    plt.title(f'Boxplot del {indicador}')
    plt.xlabel(f'Valor del {indicador}')

    # Mostrar el gráfico
    plt.show()

    return outliers.sort_values(by="Valor", ascending = False).head(10)


# FUNCIONES DE FEATURES ENGINEERING

def estructurar_data(df, indicador_deseado, nuevos_bancos):
    """
    Filtra el DataFrame para obtener solo los datos del indicador deseado y excluye los nuevos bancos.
    Luego pivota la tabla para generar una matriz de series temporales por entidad.

    :param df: DataFrame original con los datos financieros.
    :param indicador_deseado: Indicador específico a filtrar.
    :param nuevos_bancos: Lista de bancos nuevos que deben ser excluidos.
    :return: Matriz de valores (X) y DataFrame pivotado.
    """
    # Filtrar solo el indicador deseado
    df_indicador = df[df['Indicador'] == indicador_deseado]

    # Filtrar entidades para excluir los nuevos bancos
    df_indicador_sin_nuevos = df_indicador[~df_indicador['Entidad'].isin(nuevos_bancos)]

    # Pivotar la tabla para obtener las series de tiempo por entidad
    df_pivot = df_indicador_sin_nuevos.pivot_table(
        index='Fecha', 
        columns=['Entidad'], 
        values='Valor', 
        aggfunc='mean'  # O 'sum', dependiendo de tus necesidades
    ).fillna(0)
    
    # Obtener las series temporales por entidad
    X = df_pivot.T.values
    return X, df_pivot


def apply_scalers(X):
    """
    Aplica tres opciones de escalado a los datos: sin escalado, RobustScaler y StandardScaler.
    Retorna una lista de las matrices escaladas con sus etiquetas correspondientes.

    :param X: Matriz de datos a escalar.
    :return: Lista de tuplas con los datos escalados y el nombre del escalador.
    """
    scalers = [None, RobustScaler(), StandardScaler()]
    scaler_labels = ["Sin escalado", "RobustScaler", "StandardScaler"]
    X_scaled_list = []

    for scaler, label in zip(scalers, scaler_labels):
        if scaler:
            X_scaled = scaler.fit_transform(X)
        else:
            X_scaled = X  # Si no hay escalado
        X_scaled_list.append((X_scaled, label))
    
    return X_scaled_list


# FUNCIONES DE MODELOS Y OBTENCION DE RESULTADOS
def apply_kmeans(X, n_clusters):
    """
    Aplica el algoritmo K-Means a las series temporales y calcula el Silhouette score para los clusters generados.

    :param X: Matriz de datos a clusterizar.
    :param n_clusters: Número de clusters a generar.
    :return: Etiquetas de los clusters y el Silhouette score.
    """
    model = TimeSeriesKMeans(n_clusters=n_clusters, metric="euclidean", random_state=42)
    cluster_labels = model.fit_predict(X)
    if len(set(cluster_labels)) > 1:
        score = silhouette_score(X, cluster_labels)
    else:
        score = -1  # Si hay un solo clúster, el Silhouette score no es válido
    return cluster_labels, score

def apply_kshape(X, n_clusters):
    """
    Aplica el algoritmo K-Shape a las series temporales y calcula el Silhouette score para los clusters generados.

    :param X: Matriz de datos a clusterizar.
    :param n_clusters: Número de clusters a generar.
    :return: Etiquetas de los clusters y el Silhouette score.
    """
    model = KShape(n_clusters=n_clusters, random_state=42)
    cluster_labels = model.fit_predict(X)
    if len(set(cluster_labels)) > 1:
        score = silhouette_score(X, cluster_labels)
    else:
        score = -1
    return cluster_labels, score

def apply_dwt(X, n_clusters):
    """
    Aplica el algoritmo K-Means usando la métrica DTW (Dynamic Time Warping) para clusterizar las series temporales.
    Calcula el Silhouette score para los clusters generados.

    :param X: Matriz de datos a clusterizar.
    :param n_clusters: Número de clusters a generar.
    :return: Etiquetas de los clusters y el Silhouette score.
    """
    model = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", random_state=42)
    cluster_labels = model.fit_predict(X)
    if len(set(cluster_labels)) > 1:
        score = silhouette_score(X, cluster_labels)
    else:
        score = -1
    return cluster_labels, score

# FUNCIÓN DE BUSQUEDA DE HIPERPARÁMETRO Y RESULTADOS
def search_hyperparameters(X_scaled_list, n_clusters_list):
    """
    Busca los mejores hiperparámetros (número de clusters y tipo de escalado) para tres algoritmos de clustering:
    K-Means, K-Shape y DWT. Devuelve los resultados en un DataFrame ordenado por el Silhouette score.

    :param X_scaled_list: Lista de matrices escaladas con sus respectivos nombres de escaladores.
    :param n_clusters_list: Lista de valores de número de clusters a probar.
    :return: DataFrame con los resultados de la búsqueda de hiperparámetros.
    """
    results = []  # Para almacenar los resultados
    for X_scaled, scaler_label in X_scaled_list:
        for n_clusters in n_clusters_list:
            # K-Means
            kmeans_labels, kmeans_score = apply_kmeans(X_scaled, n_clusters)
            results.append({
                "Modelo": "K-Means", 
                "Número de Clusters": n_clusters,  
                "Configuración": scaler_label, 
                "Cluster Labels": kmeans_labels.tolist(),
                "Resultado": kmeans_score
            })

            # K-Shape
            kshape_labels, kshape_score = apply_kshape(X_scaled, n_clusters)
            results.append({
                "Modelo": "K-Shape", 
                "Número de Clusters": n_clusters, 
                "Configuración": scaler_label, 
                "Cluster Labels": kshape_labels.tolist(),
                "Resultado": kshape_score
            })

            # DWT
            dwt_labels, dwt_score = apply_dwt(X_scaled, n_clusters)
            results.append({
                "Modelo": "DWT", 
                "Número de Clusters": n_clusters, 
                "Configuración": scaler_label, 
                "Cluster Labels": dwt_labels.tolist(),
                "Resultado": dwt_score
            })

    # Crear un DataFrame con los resultados
    results_df = pd.DataFrame(results)
    return results_df.sort_values(by='Resultado', ascending=False)

# FUNCION PARA EJECUCIÓN DE MODELOS Y OBTENCIÓN DE RESULTADOS

def main_pipeline(df, indicador_deseado, nuevos_bancos, n_clusters_list):
    """
    Pipeline principal que estructura los datos, aplica escalado, realiza una búsqueda de hiperparámetros
    y entrena el mejor modelo de clustering basado en los resultados. Devuelve los resultados y las clasificaciones.

    :param df: DataFrame original con los datos financieros.
    :param indicador_deseado: Indicador a analizar.
    :param nuevos_bancos: Lista de bancos nuevos a excluir.
    :param n_clusters_list: Lista de valores de número de clusters a probar.
    :return: DataFrame con los resultados del clustering y DataFrame con la clasificación final de entidades por cluster.
    """
    # Estructurar los datos
    X, df_pivot = estructurar_data(df, indicador_deseado, nuevos_bancos)
    
    # Aplicar escalado
    X_scaled_list = apply_scalers(X)
    
    # Búsqueda de hiperparámetros
    results_df = search_hyperparameters(X_scaled_list, n_clusters_list)

    # Obtener la mejor configuración
    best_model_config = results_df.iloc[0]

    # Entrenar el mejor modelo
    X_scaled = X_scaled_list[0][0]  # Usar el primer escalador (sin escalado) para el ejemplo
    n_clusters = best_model_config["Número de Clusters"]
    model_name = best_model_config["Modelo"]
    
    # Aplicar el mejor modelo y obtener las etiquetas
    if model_name == "K-Means":
        model = TimeSeriesKMeans(n_clusters=n_clusters, metric="euclidean", random_state=42)
    elif model_name == "K-Shape":
        model = KShape(n_clusters=n_clusters, random_state=42)
    elif model_name == "DWT":
        model = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", random_state=42)
    
    # Entrenar el modelo con la mejor configuración
    cluster_labels = model.fit_predict(X_scaled)

    # Crear el DataFrame de clasificación
    classification_df = pd.DataFrame({
        "Entidad": df_pivot.columns,
        "Cluster": cluster_labels
    })

    # Devolver ambos DataFrames: resultados y clasificaciones
    return results_df, classification_df

# FUNCIONES PARA ANÁLISIS DE RESULTADOS

def combinar_clasificaciones(clasificaciones_totales, df_mejores_resultados, umbral_silhouette=0.7):
    """
    Combina las clasificaciones de entidades en un DataFrame único a partir de clasificaciones_totales y 
    un DataFrame de mejores resultados. Obtiene la clasificación por indicador elaborado por los mejores 
    modelos en cada indicador

    :param clasificaciones_totales: Lista de clasificaciones para cada indicador.
    :param df_mejores_resultados: DataFrame que contiene los indicadores y sus Silhouette Scores.
    :param umbral_silhouette: Umbral para filtrar los indicadores basado en su Silhouette Score.
    :return: DataFrame combinado con las clasificaciones por indicador.
    """
    
    # Diccionario para almacenar resultados por indicador
    resultados_por_indicador = {}

    # Procesar cada clasificación
    for clasificacion in clasificaciones_totales:
        indicador = clasificacion['Indicador']
        df_clasificacion = clasificacion['Clasificación']
        
        # Crear DataFrame
        df_resultado_indicador = pd.DataFrame({
            'Entidad': df_clasificacion['Entidad'],
            'Clasificación': df_clasificacion['Cluster']
        })
        
        # Renombrar columna 'Clasificación' al nombre del indicador
        df_resultado_indicador.rename(columns={'Clasificación': indicador}, inplace=True)
        
        # Agregar DataFrame al diccionario
        resultados_por_indicador[indicador] = df_resultado_indicador

    # Filtrar indicadores con Silhouette Score mayor al umbral especificado
    indicadores_a_ver = df_mejores_resultados["Indicador"][df_mejores_resultados["Silhouette Score"] > umbral_silhouette].unique()

    # Inicializar el DataFrame combinado
    resultado_combinado = pd.DataFrame()

    # Bucle para combinar todos los DataFrames
    for indicador in indicadores_a_ver:
        if indicador in resultados_por_indicador:  # Asegurarse de que el indicador esté en los resultados
            df_indicador = resultados_por_indicador[indicador]
            df_indicador = df_indicador.rename(columns={'Cluster': f'Cluster {indicador}'})
            
            if resultado_combinado.empty:
                resultado_combinado = df_indicador
            else:
                resultado_combinado = pd.merge(resultado_combinado, df_indicador, on='Entidad', how='outer')

    return resultado_combinado


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
        colors = sns.color_palette("hsv", len(unique_clusters))  # Paleta de colores para cada cluster
        cluster_color_map = {cluster: f'rgb({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)})' for cluster, color in zip(unique_clusters, colors)}

        # Crear trazas para cada entidad
        for entidad in df_pivot.columns:
            if entidad in clusters:  # Asegurarse de que la entidad esté en los clusters
                cluster = clusters[entidad]  # Obtener el cluster de la entidad
                color = cluster_color_map[cluster]  # Obtener el color correspondiente

                # Generar el hover text
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
                    name=f'{entidad} (Cluster {cluster})',  # Mostrar el nombre de la entidad en la leyenda
                    line=dict(color=color),
                    hoverinfo='text',
                    hovertext=hover_text,  # Usar el texto generado para el hover
                    showlegend=True  # Mantener la leyenda
                ))

        # Añadir un título para cada gráfico (indicador)
        fig.update_layout(
            title=f'Evolución de {indicador_deseado} por Entidad (Colores según Cluster)',
            xaxis_title='Fecha',
            yaxis_title=indicador_deseado,
            legend_title='Entidades',
            hovermode='closest',  # Cambiar a 'closest' para mostrar solo la entidad señalada
        )

        # Añadir un espaciado vertical si hay más gráficos
        fig.update_layout(
            margin=dict(t=50, b=50),
            height=400 * len(indicadores_deseados)  # Ajustar la altura en función del número de indicadores
        )

    # Mostrar el gráfico con todos los indicadores
    fig.show()





