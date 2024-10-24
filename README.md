# Monitoreo del Sector Bancario en Perú

**Autor:** Oscar Paul Sanchez Riveros  
[LinkedIn](https://www.linkedin.com/in/oscarpaulsanchezriveros/)

---

## 📝 Descripción del Proyecto

El objetivo de este proyecto es crear un sistema de monitoreo para el sector bancario en Perú a través de un análisis de indicadores financieros clave, como solvencia, calidad de activos, gestión y eficiencia, rentabilidad y liquidez, utilizando algoritmos de aprendizaje automático no supervisados. Los datos fueron extraídos mediante técnicas de web scraping desde la Superintendencia de Banca, Seguros y AFP (SBS), que publica información mensual en archivos Excel. Se recopilaron datos desde agosto de 2015 hasta agosto de 2024, cubriendo un período de 9 años.

El análisis se enfoca en clasificar a las entidades bancarias según la evolución temporal de sus indicadores, aplicando diferentes técnicas de clustering no supervisado, como K-Means (distancia euclidiana), K-Means con DTW (Dynamic Time Warping), y clustering basado en formas. Se evaluaron los modelos mediante el índice de silueta para medir la cohesión y separación de los clústeres.

---

## 📊 Dataset

Los datos fueron extraídos de la SBS mediante archivos Excel que contienen indicadores financieros de las entidades bancarias en Perú. Estos archivos fueron transformados a un formato de base de datos para facilitar su procesamiento.

El dataset final incluye los siguientes indicadores clave:

- Solvencia
- Calidad de Activos
- Gestión y Eficiencia
- Rentabilidad
- Liquidez

Se analizaron un total de 19 indicadores, de los cuales se seleccionaron los 13 que mostraron un índice de silueta mayor a 0.7.

---

## 📂 Estructura del Proyecto

- `data/`: Archivos Excel originales extraídos de la SBS.  
- `scripts/`: Contiene los scripts de web scraping, transformación y limpieza de datos.  
- `modelos/`: Carpeta con los modelos entrenados.  
- `notebooks/`: Notebooks de Jupyter que documentan todo el proceso de análisis.  
- `app.py`: Aplicación en Streamlit que permite visualizar los resultados y realizar predicciones.  
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

Instala todas las dependencias con el siguiente comando:

```bash
pip install -r requirements.txt
```
## 📝 Descripción del Proceso

### 1. Extracción de Datos
Se utilizó Selenium para automatizar el proceso de descarga de los archivos Excel desde la página de la SBS. Este proceso abarcó desde agosto de 2015 hasta agosto de 2024. Los archivos fueron transformados a una estructura de base de datos con campos como:

- Fecha
- Tipo de Indicador
- Entidad
- Valor del Indicador

### 2. Transformación y Limpieza de Datos
Los archivos Excel originales fueron convertidos a DataFrames, eliminando filas y columnas innecesarias, estandarizando los nombres de las entidades y formateando las fechas. También se excluyeron entidades con datos incompletos o valores extremos debido a su reciente entrada en el mercado, como Bank of China y B. BCI Perú.

### 3. Exploración de Datos
Se verificó la ausencia de valores nulos y duplicados, se analizaron outliers y se identificaron comportamientos atípicos en algunas entidades. Se realizaron histogramas y gráficos de series temporales para visualizar la evolución de los indicadores.

### 4. Modelado
Se probaron tres enfoques de clustering no supervisado:

- K-Means (distancia euclidiana)
- K-Means con DTW (Dynamic Time Warping)
- Shape-Based Clustering

Cada modelo fue evaluado con el índice de silueta para identificar el número óptimo de clústeres, probando con 2, 3 y 4 clústeres. Se agruparon las entidades bancarias en función de sus indicadores.

### 5. Evaluación de Resultados
Se obtuvieron los siguientes resultados clave:

- **K-Means (distancia euclidiana)** fue el modelo que mejor se adaptó a la mayoría de los indicadores.
- Entidades como **B. Alfin** y **B. ICBC** aparecieron consistentemente en clústeres minoritarios debido a fluctuaciones extremas en sus indicadores históricos.
- El índice de silueta mostró una buena cohesión y separación entre clústeres, con excepción del indicador *Pasivo Total / Capital Social y Reservas*.

---

## 📊 Conclusiones

- La mayoría de las entidades financieras mostraron comportamientos similares, agrupándose en clústeres dominantes.
- Las entidades **B. Alfin** y **B. ICBC** presentaron variaciones significativas en el pasado, pero han mostrado signos de estabilización en sus últimos registros.
- Se identificaron entidades con deterioros en la calidad de sus activos, como **Mibanco** y **Falabella**, lo que es preocupante para su solvencia.

---

## 🌐 Aplicación Streamlit

Interactúa con la aplicación de predicción de entidades bancarias accediendo al siguiente link de Streamlit.


