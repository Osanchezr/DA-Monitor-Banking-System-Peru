# Monitoreo del Sector Bancario en Perú

**Autor:** Oscar Paul Sanchez Riveros  
[LinkedIn](https://www.linkedin.com/in/oscar-sanchez-riveros/)

---

## 📝 Descripción del Proyecto

Este proyecto analiza el sector bancario en Perú mediante indicadores clave como **solvencia**, **calidad de activos**, **eficiencia**, **rentabilidad** y **liquidez**. Utilizando **machine learning no supervisado**, se busca agrupar entidades bancarias en función de la evolución de estos indicadores.

Se aplicaron técnicas como **K-Means** (distancia euclidiana y DTW) y **clustering basado en formas**, evaluando cada modelo con el **índice de silueta** para medir la cohesión y separación de los clústeres.

Los datos fueron extraídos mediante **web scraping** desde la SBS, cubriendo un período de **9 años** (2015-2024), permitiendo identificar patrones de comportamiento diferencial y posibles alertas de riesgo.

---

## 📊 Dataset

Los datos fueron extraídos de la SBS mediante archivos Excel que contienen indicadores financieros de las entidades bancarias en Perú. Estos archivos fueron transformados a un formato de base de datos para facilitar su procesamiento.
[SBS - Datos](https://www.sbs.gob.pe/app/stats_net/stats/EstadisticaBoletinEstadistico.aspx?p=1#)

El dataset final incluye los siguientes columnas: 

- `Fecha` : Contiene las fechas mensuales desde Agosto 2015 hasta Agosto 2024. (último reporte SBS)
- `Tipo de indicador` : Contiene la clasificación de indicadores por Solvencia, Calidad de Activos, Eficiencia y Gestión, Rentabilidad y Liquidez. (5 clasificaciones)
- `Indicador`: Contiene 20 indicadores especificos relacionados a los tipos de indicadores.
- `Entidad`: Contiene 17 entidades del sistema bancario del Perú.
- `Valor`: Contiene el valor del indicador por entidad y por fecha.

Se analizaron un total de 20 indicadores, de los cuales se seleccionaron los 13 que mostraron un índice de silueta mayor a 0.7.

---

## 📂 Estructura del Proyecto

- `data/`: /data_original/: Archivos Excel originales extraídos de la SBS.  /data_procesada/: data transformada y limpia
- `scripts/`: Contiene archivo functions.py que involucran las funciones para web scraping, transformación, limpieza de datos, modelado de datos. 
- `results/`: Carpeta con los resultados de los modelos, mejores modelos por indicadores y clusters para cada indicador.  
- `notebooks/`: Notebooks de Jupyter main que documentan todo el proceso de análisis.  
- `app/`: Aplicación en app_streamlit que permite visualizar los resultados y realizar predicciones , functions_streamlit: funciones aplicados en la app. 
- `requirements.txt`: Archivo con las dependencias del proyecto.  

---

## ⚙️ Requisitos

Para ejecutar este proyecto, necesitas tener instaladas las siguientes librerías:

- pandas
- matplotlib
- seaborn
- scikit-learn
- imbalanced-learn
- tensorflow
- jinja2
- streamlit
- selenium

## 📝 Descripción del Proceso

### 1. Extracción de Datos
Se utilizó Selenium para automatizar el proceso de descarga de los archivos Excel desde la página de la SBS. Este proceso abarcó desde agosto de 2015 hasta agosto de 2024. Los archivos fueron transformados a una estructura de base de datos con campos como:

- Fecha
- Tipo de Indicador
- Entidad
- Valor del Indicador

![Data](https://github.com/Osanchezr/DA-Monitor-Banking-System-Peru/blob/d39855626b0356fe693ba2849deee8ae06daa6da/images/data_image.JPG)

### 2. Transformación y Limpieza de Datos
Los archivos Excel originales fueron convertidos a DataFrames, eliminando filas y columnas innecesarias, estandarizando los nombres de las entidades y formateando las fechas. También se excluyeron entidades con datos incompletos o valores extremos debido a su reciente entrada en el mercado, como Bank of China y B. BCI Perú.

### 3. Exploración de Datos
Se verificó la ausencia de valores nulos y duplicados, se analizaron outliers y se identificaron comportamientos atípicos en algunas entidades. Se realizaron histogramas y gráficos de series temporales para visualizar la evolución de los indicadores.

![Histogramas](https://github.com/Osanchezr/DA-Monitor-Banking-System-Peru/blob/d39855626b0356fe693ba2849deee8ae06daa6da/images/histogramas.png)

### 4. Modelado
Se probaron tres enfoques de clustering no supervisado:

- K-Means (distancia euclidiana)
- K-Means con DTW (Dynamic Time Warping)
- Shape-Based Clustering

Cada modelo fue evaluado con el índice de silueta para identificar el número óptimo de clústeres, probando con 2, 3 y 4 clústeres. Se agruparon las entidades bancarias en función de sus indicadores.

### 5. Evaluación de Resultados
Se obtuvieron los siguientes resultados clave:

![mejoresmodelos](https://github.com/Osanchezr/DA-Monitor-Banking-System-Peru/blob/d39855626b0356fe693ba2849deee8ae06daa6da/images/result_mejor_modelo.JPG)

- **K-Means (distancia euclidiana)** fue el modelo que mejor se adaptó a la mayoría de los indicadores.
- Entidades como **B. Alfin** y **B. ICBC** aparecieron consistentemente en clústeres minoritarios debido a fluctuaciones extremas en sus indicadores históricos.
- El índice de silueta mostró una buena cohesión y separación entre clústeres, con excepción del indicador *Pasivo Total / Capital Social y Reservas*.

![grafico](https://github.com/Osanchezr/DA-Monitor-Banking-System-Peru/blob/d39855626b0356fe693ba2849deee8ae06daa6da/images/resul_evol.JPG)

![grafico](https://github.com/Osanchezr/DA-Monitor-Banking-System-Peru/blob/d39855626b0356fe693ba2849deee8ae06daa6da/images/resul_evol2.JPG)

---

## 📊 Conclusiones

- La mayoría de las entidades financieras mostraron comportamientos similares, agrupándose en clústeres dominantes.
- Las entidades **B. Alfin** y **B. ICBC** presentaron variaciones significativas en el pasado, pero han mostrado signos de estabilización en sus últimos registros.
- Se identificaron entidades con deterioros en la calidad de sus activos, como **Mibanco** y **Falabella**, lo que es preocupante para su solvencia.

---

## 🌐 Aplicación Streamlit

Interactúa con la aplicación de predicción de entidades bancarias accediendo al siguiente link de Streamlit.


