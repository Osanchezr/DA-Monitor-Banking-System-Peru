import streamlit as st
import pandas as pd
import sys 
import os 
sys.path.append(os.path.abspath("..")) 
from streamlit_functions import load_data, filtrar_datos, calcular_variacion_anual, grafico_barras, grafico_evolutivo, sidebar_filtros,color_neutro_por_variacion, pagina_analisis_clusters

def pagina_introduccion():
    # Titulo
    st.markdown("""
        <h1 style='text-align: center; color: #2E86C1; margin-bottom: 0;'>Sistema de monitoreo bancario del Perú</h1>
        <h3 style='text-align: center; color: #2E86C1; margin-top: 0;'>Ago 2015 - Set 2024</h3>
    """, unsafe_allow_html=True)
    
    # Subtítulo
    st.markdown("<h2 style='text-align: center; color: #1B4F72;'>Exploración de Indicadores Financieros y Segmentación de Entidades Bancarias</h2>", unsafe_allow_html=True)
    
    # Dividir en dos columnas para agregar una imagen y texto explicativo
    col1, col2 = st.columns([1, 2])
    
    with col1:
        
        st.image("app/images_script/Portada_bancos.png", caption="Indicadores del Sistema Bancario del Perú", use_column_width=True)
    
    
        st.image("app/images_script/Banca.png", 
                caption="Bancos", use_column_width=True)
    with col2:
        st.write("""
        **Este análisis se basa en datos oficiales del sistema bancario peruano, proporcionados por la** **Superintendencia de Banca, Seguros y AFP (SBS)** **del Perú. El objetivo principal es evaluar de manera exhaustiva la evolución y desempeño de las entidades bancarias a lo largo de un período de 9 años (agosto 2015 - septiembre 2024).**

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
    ### Panorama General Septiembre 2024
    **1. Variabilidad en Ratios de Capital**
    El Ratio de Capital Global presenta una mezcla de resultados. Aunque algunos bancos como B. BCI Perú han mostrado caídas significativas en su capital, aún mantienen posiciones competitivas. En contraste, entidades como Mibanco y B. Falabella Perú han visto un crecimiento en sus ratios, sugiriendo un fortalecimiento en su solidez financiera. Este comportamiento refleja una necesidad urgente para bancos con ratios decrecientes de adoptar estrategias que restauren su estabilidad y competitividad en el mercado.

    **2. Gestión de Pasivos y Apalancamiento**
    La evolución del indicador Pasivo Total / Capital Social y Reservas indica que algunos bancos, como Alfin Banco, han incrementado su apalancamiento de manera notable, lo que puede suponer riesgos si no se gestionan adecuadamente. En cambio, bancos como B. BCI Perú mantienen un crecimiento más controlado, lo que sugiere una gestión prudente de sus pasivos. Sin embargo, aquellos con caídas en este ratio, como B. Santander Perú, deben ser evaluados con cuidado, ya que podrían estar enfrentando problemas de gestión.

    **3. Calidad de la Cartera de Créditos**
    La morosidad ha sido un tema recurrente, especialmente con el alarmante aumento en el indicador Créditos Atrasados / Créditos Directos de B. Santander Perú. Este deterioro en la calidad de la cartera es preocupante y sugiere la necesidad de medidas proactivas en la gestión de riesgos. Sin embargo, otros bancos como Alfin Banco y B. Falabella Perú han mostrado mejoras en sus ratios, lo que indica que algunos están gestionando eficazmente sus riesgos crediticios.

    **4. Liquidez y Provisión de Créditos Atrasados**
    La liquidez es un aspecto crítico para la salud financiera de los bancos. Entidades como B. Falabella Perú y B. ICBC han demostrado mejoras significativas en sus ratios de liquidez, mientras que otros, como B. BCI Perú y Bank of China, enfrentan un deterioro alarmante. En cuanto a las provisiones, BANCOM y B. Falabella Perú han mostrado una sólida cobertura de sus créditos en mora, lo que indica una gestión adecuada del riesgo.

    **5. Rentabilidad y Eficiencia Administrativa**
    La rentabilidad sigue siendo un desafío para muchas entidades. B. Pichincha y B. Santander Perú están experimentando pérdidas significativas en relación a su patrimonio y activos. Es evidente que algunas entidades deben revisar y mejorar sus modelos de negocio para garantizar su sostenibilidad en el largo plazo. Además, la gestión de costos debe ser una prioridad, especialmente para bancos que muestran altos gastos operativos en relación con sus ingresos.

    **Conclusión**
    En resumen, el sistema bancario peruano enfrenta una serie de desafíos y oportunidades. Mientras algunos bancos muestran signos de solidez y mejora en su gestión, otros enfrentan problemas serios que pueden comprometer su estabilidad. Es fundamental que las entidades adopten estrategias proactivas para manejar su riesgo crediticio, mejorar su eficiencia operativa y optimizar su capital. La continua vigilancia y adaptación serán claves para navegar el entorno financiero cambiante y asegurar la sostenibilidad en el futuro.
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

    comentarios_indicadores = {"Ratio de Capital Global":"El análisis de los ratios de capital global por entidades bancarias muestra un panorama mixto. B. BCI Perú mantiene el ratio más alto a pesar de una drástica caída del 49.72%, lo que plantea preocupaciones sobre su estabilidad futura. Bank of China y Citibank presentan ratios sólidos, con un crecimiento modesto en 2024, lo que les otorga una posición fuerte. Por otro lado, bancos como B. GNB y B. ICBC experimentan caídas en sus ratios, pero aún permanecen competitivos. Mibanco y B. Falabella Perú muestran tendencias al alza, lo que indica una mejora en su solidez financiera. En general, es crucial que las entidades con ratios decrecientes implementen estrategias para recuperar su estabilidad y competitividad en el mercado.",
        "Pasivo Total / Capital Social y Reservas": "El análisis del indicador Pasivo Total / Capital Social y Reservas muestra que Alfin Banco destaca con un notable incremento del 233.33%, aumentando de 1.26 a 4.2, lo que sugiere un apalancamiento significativo. B. BCI Perú también crece un 116.77% pero mantiene un ratio de 3.36, indicando una gestión prudente. Bank of China y B. ICBC presentan aumentos saludables del 34.23% y 33.95%, respectivamente.Por otro lado, entidades como B. Santander Perú y B. Falabella Perú experimentan caídas en sus ratios, de -25.52% y -7.54%, lo que podría indicar riesgos en su gestión de pasivos. En resumen, mientras algunos bancos muestran un aumento en su apalancamiento, otros enfrentan desafíos que podrían afectar su estabilidad financiera a largo plazo",
        "Créditos Atrasados / Créditos Directos": "El análisis del indicador Créditos Atrasados / Créditos Directos muestra un aumento notable en B. Santander Perú, que experimenta un incremento del 293.85%, pasando de 1.3 a 5.12, lo que indica un deterioro significativo en la calidad de su cartera de créditos. Mibanco y B. Interamericano de Finanzas también presentan aumentos más moderados del 12.24% y 13.46%, respectivamente, reflejando un leve aumento en la morosidad.Por otro lado, Alfin Banco y B. Falabella Perú tienen caídas en sus ratios de -33.06% y -34.59%, sugiriendo mejoras en la gestión de sus créditos atrasados.",
        "Créditos Atrasados con más de 90 días de atraso / Créditos Directos":"El análisis del indicador Créditos Atrasados con más de 90 días de atraso / Créditos Directos muestra que B. Santander Perú presenta un alarmante aumento del 303.31%, pasando de 1.25 a 5.04, lo que indica un grave deterioro en su calidad crediticia. B. Interamericano de Finanzas y B. Pichincha también experimentan incrementos del 23.98% y 12.87%, sugiriendo un leve deterioro en sus carteras. En contraste, B. Falabella Perú y Alfin Banco logran mejoras significativas, con caídas del -34.08% y -35.17%, respectivamente. Mibanco también presenta una reducción del -24.3%, lo que sugiere una mejor gestión de los créditos atrasados. En resumen, mientras algunos bancos enfrentan serios problemas de morosidad, otros han mejorado en la gestión de sus créditos.",
        "Créditos Refinanciados y Reestructurados / Créditos Directos":"El análisis del indicador Créditos Refinanciados y Reestructurados / Créditos Directos muestra que BANCOM presenta un aumento del 44.77% (de 2.39 a 3.46), lo que indica un incremento en la necesidad de refinanciamiento. Mibanco y Scotiabank Perú también reportan aumentos del 25.71% y 18.0%, respectivamente, sugiriendo tendencias similares. En contraste, B. Santander Perú, Alfin Banco y B. GNB experimentan caídas significativas del -53.93%, -64.72% y -65.86%, lo que podría indicar mejoras en la calidad de sus carteras",
        "Créditos Atrasados MN / Créditos Directos MN":"El Indicador Créditos Atrasados MN / Créditos Directos MN refleja el porcentaje de créditos en mora en moneda nacional, indicando la salud financiera de los bancos. B. Pichincha aumenta de 6.4 a 7.33 (+14.53%), mientras que B. Santander Perú sube de 1.3 a 1.47 (+13.08%), lo que sugiere un aumento en la morosidad. Mibanco incrementa de 6.27 a 7.04 (+12.28%). Scotiabank Perú crece de 3.91 a 4.37 (+11.76%). Por el contrario, B. Ripley baja de 4.59 a 4.36 (-5.01%), indicando mejora en cobranzas, al igual que B. De Crédito del Perú que desciende de 5.24 a 4.95 (-5.53%). Interbank cae de 3.84 a 3.5 (-8.85%), sugiriendo eficacia en la gestión de riesgos. B. BBVA Perú baja de 5.03 a 4.51 (-10.34%) y BANCOM de 4.48 a 3.98 (-11.16%). B. GNB disminuye de 3.33 a 2.92 (-12.31%). Alfin Banco desciende de 6.12 a 4.44 (-27.45%), y B. Falabella Perú de 6.65 a 4.35 (-34.59%), mostrando problemas severos en la recuperación de créditos. Finalmente, Citibank, B. BCI Perú, B. ICBC y Bank of China reportan 0, lo que sugiere problemas en la gestión de créditos o la falta de ellos ",
        "Créditos Atrasados ME / Créditos Directos ME":"El Indicador Créditos Atrasados ME / Créditos Directos ME mide el porcentaje de créditos en mora en moneda extranjera, ofreciendo una visión de la gestión de riesgos en los bancos. B. Santander Perú presenta un aumento significativo, pasando de 1.3 a 7.06 (+443.08%), lo que indica un incremento preocupante en la morosidad. B. Falabella Perú también muestra un crecimiento en la morosidad, subiendo de 57.67 a 78.62 (+36.33%). BANCOM incrementa de 9.86 a 12.74 (+29.21%). B. Interamericano de Finanzas crece de 3.33 a 4.11 (+23.42%). Por el contrario, Scotiabank Perú baja de 4.76 a 4.31 (-9.45%), y Mibanco disminuye de 24.61 a 22.16 (-9.96%). B. BBVA Perú desciende de 3.73 a 3.34 (-10.46%). B. De Crédito del Perú cae de 2.71 a 2.37 (-12.55%). B. Pichincha reduce su indicador de 6.55 a 5.64 (-13.89%), y Interbank pasa de 2 a 1.72 (-14.0%). B. GNB disminuye de 4.4 a 3.5 (-20.45%). Las entidades Alfin Banco, B. BCI Perú, B. ICBC, B. Ripley, Bank of China y Citibank no reportan cifras, lo que podría indicar la ausencia de créditos en mora o datos no definidos. ",
        "Provisiones / Créditos Atrasados":"El indicador Provisiones / Créditos Atrasados muestra que BANCOM tiene una ratio de 170.02 en Set-2024, con un aumento del 23.58%, lo que refleja una sólida cobertura de sus créditos en mora. B. Falabella Perú también se destaca con 187.4 y un incremento del 20.97%. B. De Crédito del Perú y Alfin Banco mantienen ratios de 146.07 y 183.68, indicando una gestión prudente.En contraste, B. BBVA Perú y Mibanco presentan descensos en sus ratios a 138.79 y 123.99, lo que puede señalar riesgos en la cobertura. La caída más preocupante es la de B. Santander Perú, que baja a 97.67, sugiriendo debilidades significativas en sus provisiones",
        "Gastos de Administración Anualizados / Activo Productivo Promedio":"El indicador Gastos de Administración Anualizados / Activo Productivo Promedio revela que B. Ripley aumenta a 14.25 (+12.31%), mientras que B. Santander Perú alcanza 2.05 (+10.63%). B. De Crédito del Perú y Scotiabank Perú mantienen ratios de 3.3 y 2.47, indicando un manejo controlado. Sin embargo, Alfin Banco cae a 10.95 (-28.33%), y B. BCI Perú y Bank of China experimentan descensos drásticos a 2.91 y 1.06, reflejando desafíos en la gestión de costos. En general, algunos bancos muestran estabilidad, mientras que otros necesitan mejorar su eficiencia administrativa",
        "Gastos de Operación / Margen Financiero Total":"El indicador Gastos de Operación / Margen Financiero Total revela que B. Pichincha incrementa a 44.66 (+9.51%) y B. ICBC a 36.5 (+8.82%), mostrando eficiencia en el manejo de gastos. B. GNB se mantiene en 70.25, evidenciando una gestión aceptable. Sin embargo, Mibanco y B. De Crédito del Perú experimentan leves caídas a 51.37 y 37.2, respectivamente. En contraste, B. BCI Perú y Bank of China muestran descensos significativos a 67.66 (-21.37%) y 32.69 (-44.58%), lo que sugiere problemas de control en sus gastos operativos. En general, muchas entidades necesitan mejorar la gestión de gastos para asegurar su rentabilidad.",
        "Ingresos Financieros / Ingresos Totales":"El indicador Ingresos Financieros / Ingresos Totales muestra que Bank of China lidera con un aumento a 86.64 (+10.29%), indicando una sólida generación de ingresos financieros. Alfin Banco también presenta un crecimiento positivo a 85.86 (+5.23%). Otras entidades, como B. Falabella Perú y B. ICBC, muestran incrementos más modestos, alcanzando 78.79 y 86.39, respectivamente. En contraste, B. Pichincha cae a 75.84 (-10.08%), sugiriendo una reducción en la proporción de ingresos financieros respecto al total, lo que podría indicar problemas en su modelo de negocio. B. Santander Perú y B. Ripley también sufren disminuciones, lo que resalta la necesidad de mejorar la eficiencia en la generación de ingresos financieros en el contexto actual",
        "Ingresos Financieros Anualizados / Activo Productivo Promedio":"El indicador Ingresos Financieros Anualizados / Activo Productivo Promedio muestra que Citibank presenta un notable incremento a 10.06 (+30.66%), destacándose en la generación de ingresos financieros. B. ICBC también muestra un crecimiento sólido, alcanzando 6.26 (+26.71%). B. Ripley y B. Santander Perú registran aumentos de 27.11 (+12.76%) y 9.71 (+11.81%), respectivamente, lo que sugiere un manejo eficaz de sus activos productivos. En contraste, B. BCI Perú cae a 7.12 (-16.93%), lo que puede reflejar desafíos en la generación de ingresos en relación a sus activos. Otras entidades como Alfin Banco y B. Pichincha también experimentan caídas, indicando una disminución en la efectividad de sus ingresos financieros, lo que resalta la importancia de optimizar la gestión de activos para mejorar la rentabilidad.",
        "Créditos Directos / Personal":"El indicador Créditos Directos / Personal revela un aumento notable para Bank of China, que crece de 4,034 a 5,701 (+41.32%), y B. Pichincha, que incrementa de 5,793 a 6,494 (+12.1%). B. GNB y B. BBVA Perú también presentan aumentos menores, alcanzando 6,562 (+6.9%) y 9,974 (+1.25%), respectivamente. En contraste, B. Santander Perú sufre una caída significativa de 31,528 a 23,256 (-26.24%), evidenciando ineficiencia en su uso del personal. Otras entidades como Scotiabank Perú (-13.94%) y Mibanco (-12.05%) también muestran descensos, sugiriendo desafíos en la gestión de créditos directos. En resumen, algunas entidades optimizan su relación entre créditos y personal, mientras que otras enfrentan problemas significativos en esta área.",
        "Depósitos / Número de Oficinas":"El indicador Depósitos / Número de Oficinas revela que B. BCI Perú experimenta un notable incremento, pasando de 605,235.75 a 1,296,084.56 (+114.15%). B. ICBC también muestra un crecimiento significativo, aumentando de 1,525,661.58 a 2,451,895.26 (+60.71%), seguido por Bank of China, que sube de 1,331,226.75 a 1,824,280.08 (+37.04%). B. Pichincha y Alfin Banco reportan aumentos más moderados del 28.01% y 25.67%, respectivamente. Scotiabank Perú y Interbank continúan con incrementos menores, alcanzando 22.88% y 15.27%. En contraste, entidades como B. Santander Perú muestran una caída significativa, disminuyendo de 7,469,852.92 a 6,475,432.07 (-13.31%), y BANCOM también reduce su cifra de 79,974.12 a 64,405.17 (-19.47%). En general, mientras algunas instituciones mejoran su eficiencia en la relación depósitos/oficinas, otras enfrentan desafíos." ,
        "Utilidad Neta Anualizada / Patrimonio Promedio":"El indicador Utilidad Neta Anualizada / Patrimonio Promedio muestra variaciones significativas. B. Pichincha se deteriora, pasando de -1.29 a -3.77 (+193.17%), mientras que Bank of China mejora de 6.66 a 14.1 (+111.93%) y B. GNB sube de 2.9 a 5.34 (+84.22%). BANCOM y Alfin Banco también reportan incrementos moderados del 27.78% y 22.59%, respectivamente. En contraste, B. Santander Perú baja 5.83%, Citibank 6.34%, y B. BBVA Perú 17.71%. B. ICBC y Interbank caen un 28.09% y 33.01%, respectivamente, y Scotiabank Perú un 48.87%. Por último, B. BCI Perú y B. Falabella Perú enfrentan pérdidas extremas de -133.14% y -209.27%, respectivamente. En general, algunas entidades mejoran su rentabilidad, mientras que otras enfrentan desafíos significativos",
        "Utilidad Neta Anualizada / Activo Promedio":"El indicador Utilidad Neta Anualizada / Activo Promedio revela variaciones significativas entre las entidades. B. Pichincha muestra un deterioro, pasando de -0.12 a -0.39 (+222.65%). B. GNB mejora de 0.42 a 0.73 (+74.92%), y BANCOM también aumenta de 0.19 a 0.26 (+33.12%). Alfin Banco crece de 0.25 a 0.32 (+28.86%), mientras que B. Ripley y B. De Crédito del Perú reportan ligeras caídas. Sin embargo, entidades como B. Santander Perú disminuyen 4.49%, y Bank of China cae 6.22%. B. ICBC presenta una reducción del 8.75%, y B. BBVA Perú del 16.11%. Interbank cae 30.91%, y Scotiabank Perú enfrenta una disminución del 45.15%. Por último, B. BCI Perú y B. Falabella Perú sufren descensos drásticos de -122.54% y -218.88%, respectivamente. En resumen, varias entidades experimentan un compromiso en su rentabilidad, mientras que otras logran mantener o mejorar su desempeño.",
        "Ratio de Liquidez MN":"El Ratio de Liquidez MN revela la capacidad de las entidades para cumplir con obligaciones en moneda nacional. B. Falabella Perú sube de 19.31 a 31.56 (+63.44%). B. ICBC también crece, de 142.54 a 203.69 (+42.9%), seguido por B. Pichincha de 25.31 a 34.62 (+36.78%). B. Interamericano de Finanzas incrementa de 32.68 a 41.56 (+27.17%) y Alfin Banco de 36.03 a 45.73 (+26.92%). B. Ripley sube de 27.7 a 35.06 (+26.57%) y Scotiabank Perú de 22.74 a 27.03 (+18.87%). Mibanco aumenta de 24.3 a 28.17 (+15.93%) y B. BBVA Perú de 25.59 a 28.22 (+10.28%). Citibank pasa de 86.34 a 94.64 (+9.61%) y B. De Crédito del Perú de 29.67 a 31.68 (+6.77%). Interbank crece de 29.13 a 30.63 (+5.15%), mientras que B. GNB baja de 44.12 a 42.01 (-4.78%). BANCOM disminuye de 23.16 a 20.49 (-11.53%) y B. BCI Perú de 65.97 a 57.81 (-12.37%). B. Santander Perú cae de 55.61 a 42.34 (-23.86%) y Bank of China de 455.6 a 264.62 (-41.92%).",
        "Ratio de Liquidez ME":"El Ratio de Liquidez ME muestra las variaciones en la capacidad de las entidades para cumplir con sus obligaciones en moneda extranjera. B. BCI Perú aumenta de 38.57 a 81.11 (+110.29%) y Scotiabank Perú sube de 29.78 a 55.36 (+85.9%). B. De Crédito del Perú crece de 38.77 a 53.4 (+37.74%), mientras que Mibanco pasa de 110.83 a 141.78 (+27.93%). B. ICBC y B. Pichincha también incrementan, alcanzando 63.77 y 46.91, respectivamente. BANCOM crece levemente de 57.23 a 64.73 (+13.11%). B. Interamericano de Finanzas aumenta de 41.12 a 45.66 (+11.04%) y B. BBVA Perú de 48.98 a 53.71 (+9.66%). En contraste, B. Santander Perú disminuye ligeramente de 49.67 a 49.11 (-1.13%). Bank of China y B. Ripley sufren caídas de -3.32% y -4.45%. Citibank baja -6.34%, B. Falabella Perú -11.54%, B. GNB -31.09%, y Alfin Banco presenta la mayor caída con -40.99%, indicando un deterioro en su liquidez en moneda extranjera",
        "Caja y Bancos MN / Obligaciones a la Vista MN":"El Indicador Caja y Bancos MN / Obligaciones a la Vista MN muestra la liquidez de las entidades en moneda nacional. Bank of China aumenta de 0.1 a 1.19 (+1090.0%), y Alfin Banco de 2.44 a 23.53 (+864.34%). B. ICBC crece de 3.32 a 6.28 (+89.16%) y B. Pichincha de 1.18 a 2.09 (+77.12%). B. BBVA Perú sube de 0.15 a 0.25 (+66.67%), mientras que B. Santander Perú pasa de 0.32 a 0.5 (+56.25%). Citibank aumenta de 0.27 a 0.37 (+37.04%) y Interbank de 0.4 a 0.49 (+22.5%). Mibanco baja de 58.92 a 51.1 (-13.27%), mientras que B. Interamericano de Finanzas cae de 0.21 a 0.16 (-23.81%). Scotiabank Perú disminuye de 0.12 a 0.09 (-25.0%) y B. De Crédito del Perú de 0.15 a 0.11 (-26.67%). BANCOM cae de 1.95 a 0.9 (-53.85%), B. GNB de 0.94 a 0.32 (-65.96%), y B. BCI Perú de 40.01 a 0.55 (-98.63%). B. Falabella Perú y B. Ripley reportan valores de 0, por lo que no se definen variaciones",
        "Caja y Bancos en ME / Obligaciones a la Vista ME":"El Indicador Caja y Bancos en ME / Obligaciones a la Vista ME muestra la liquidez de las entidades en moneda extranjera. B. ICBC sube de 1.62 a 6.52 (+302.47%) y Bank of China de 1.55 a 3.27 (+110.97%). Interbank aumenta de 1.39 a 2.31 (+66.19%) y B. Pichincha de 2.96 a 4.35 (+46.96%). Mibanco crece de 144.26 a 208.44 (+44.49%) y B. GNB de 12.25 a 17.43 (+42.29%). Scotiabank Perú aumenta de 1.17 a 1.63 (+39.32%) y B. De Crédito del Perú de 1.3 a 1.72 (+32.31%). BANCOM pasa de 4.78 a 5.98 (+25.1%) y B. Interamericano de Finanzas de 2.07 a 2.33 (+12.56%). Citibank disminuye de 0.74 a 0.7 (-5.41%), B. Santander Perú de 1.38 a 1.04 (-24.64%), B. BBVA Perú de 1.04 a 0.78 (-25.0%) y Alfin Banco de 2.39 a 1.79 (-25.1%). B. BCI Perú cae drásticamente de 42.65 a 3.6 (-91.56%). B. Falabella Perú y B. Ripley reportan valores de 0, por lo que no se definen variaciones"

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
                'Set-2023': '{:.2f}', 
                'Set-2024': '{:.2f}', 
                'Var-Anual': lambda x: '{:.2f}'.format(x) if isinstance(x, (int, float)) else x
            }))

        # Calcular la altura del gráfico en función del número de filas de la tabla
        num_filas = len(df_variacion_sin_indice)
        altura_grafico = num_filas * 15 + 300  # Ajustamos la altura del gráfico

        # Mostrar gráfico de barras (ordenado y con colores)
        with col2:
            st.markdown(f"####  Comparativo Set-2024")
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

    # Construir la ruta relativa al archivo CSV
    ruta_base = os.path.dirname(__file__)  # Carpeta donde está streamlit_app.py

# Construir la ruta relativa al archivo CSV
    ruta_csv = os.path.join(ruta_base, '..', 'data', 'data_procesada', 'data_kpi_procesada.csv')
    df = load_data(ruta_csv)

    ruta_combinado = os.path.join(ruta_base,'..', 'results',"clusters.csv")
    resultado_combinado = pd.read_csv(ruta_combinado)

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