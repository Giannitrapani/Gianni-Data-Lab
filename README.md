# Gianni-Data-Lab

Proyecto personal de Data Science



Proyecto de Gestión y Análisis de Bins

Sistema de procesamiento, control y visualización del ciclo completo de envases (bins) – Python + Power BI



Este proyecto implementa un sistema integral para administrar y analizar el flujo de bins utilizados por una empresa productora de jugos.

El objetivo principal es transformar múltiples fuentes Excel en datasets limpios y consolidados, para posteriormente generar análisis avanzados y tableros ejecutivos.



El sistema se divide en 3 notebooks principales:



Preparación del Dataset Global



Análisis de Stock Planta–Campos (Sistema Cerrado)



Análisis por Productor con Semáforo de Riesgo



Los resultados finales alimentan un dashboard en Power BI, utilizado para la toma de decisiones.





Tecnologías utilizadas



Python (pandas, numpy, matplotlib, seaborn, openpyxl)



Jupyter Notebook



Power BI (DAX para medidas, mosaico de productores, gauge de deuda)



Estructura de archivos Excel como fuente de datos



Notebook 1 – Preparación del Dataset Global



Este notebook toma los archivos de origen (BÁSCULA, ENVASES, INGRESOS, MOTIVO, PROVEEDOR) y genera el archivo final MOVIMIENTOS.xlsx, utilizado luego en Power BI y los siguientes notebooks.



✔ Funcionalidades principales



Verificación del entorno y librerías



Carga manual o automática de archivos



Selección automática de columnas relevantes



Identificación de envases tipo bin (gru = 'J')



Filtrado de movimientos en báscula e ingresos



Unificación de todos los movimientos en una sola tabla estandarizada



Exportación a:



C:\\JUGOS\\resultados\\MOVIMIENTOS.xlsx



Backup automático con timestamp



Descripción resumida por celda



(Basado en tu documento)

Las celdas verifican librerías, cargan datos, filtran bins, agregan nombres de proveedores, estandarizan egresos/ingresos, consolidan los registros y generan el dataset final.

Ver archivo PDF para detalle ampliado. 



Descripcion comportamiento de c…



Notebook 2 – Análisis del Stock Planta vs Campos



Este notebook toma MOVIMIENTOS.xlsx y reconstruye día a día el flujo de bins para evaluar si la planta está en niveles de riesgo.



✔ Incluye:



Cálculo de entradas, salidas y neto diario



Reconstrucción del stock (planta + campos = sistema cerrado de 30.000 bins)



Clasificación por semáforo:



Verde: normal



Amarillo: advertencia



Rojo: crítico



Gráficos:



Área apilada Planta vs Campos



Línea de evolución del stock



Sistema de alerta temprana con regresión lineal



Predice cuándo se alcanzarán los niveles amarillo o crítico



Resumen ejecutivo



Notebook 3 – Análisis por Productor



Analiza el comportamiento de cada productor en su uso/devolución de bins.



✔ Métricas calculadas:



Cantidad total enviada y devuelta



Deuda actual en bins



Deuda relativa (%)



Días sin devolver bins



Fecha del primer pedido



Ratio de devolución



Evaluación del semáforo:



Verde → normal



Amarillo → monitoreo



Rojo → riesgo inmediato



✔ Entregables



Archivo Excel: SEMAFORO\_PRODUCTORES.xlsx



Listas de productores críticos, en advertencia y en verde



Resumen ejecutivo final



Power BI – Visualización Ejecutiva



El proyecto incluye un tablero de Power BI con:



✔ Visuales principales:



Mosaico de productores (10xN)



Gauge del % de deuda según productor



Tarjeta ejecutiva (días sin devolver, deuda, ratio, etc.)



Distribución Planta vs Campos



Tabla resumen general



✔ Conclusión (según PDF)



Python = motor matemático



Power BI = tablero ejecutivo



Ambos sistemas coinciden y se complementan

