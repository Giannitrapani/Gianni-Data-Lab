# ============================================================================
# GENERADOR DE DASHBOARD INTERACTIVO - JUGOS S.A.
# ============================================================================
# Este script genera un dashboard HTML interactivo con gráficos de stock de bins
# Autor: Claude Code
# Fecha: Diciembre 2025
# ============================================================================

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
import locale
from cargar_datos_universal import cargar_movimientos_bins

# ============================================================================
# FUNCIÓN AUXILIAR PARA FORMATO NUMÉRICO (PUNTO MILES, COMA DECIMALES)
# ============================================================================

def format_number(num, decimals=0):
    """
    Formatea números con punto como separador de miles y coma para decimales.
    Ejemplo: 1234567.89 -> "1.234.567,89"
    """
    if decimals == 0:
        # Sin decimales
        formatted = f"{int(num):,}".replace(",", ".")
    else:
        # Con decimales
        formatted = f"{num:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted

# Configurar locale a español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except:
        pass

print("="*70)
print("GENERADOR DE DASHBOARD INTERACTIVO - JUGOS S.A.")
print("="*70)
print()

# ============================================================================
# CARGAR CONFIGURACIÓN DESDE config.json
# ============================================================================

# Cargar configuración desde archivo JSON
with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

import platform
import os

TOTAL_BINS = CONFIG['bins']['total_bins']
UMBRAL_MINIMO = CONFIG['bins']['umbral_critico']
UMBRAL_AMARILLO = CONFIG['bins']['umbral_advertencia']

# Rutas RELATIVAS - funciona desde cualquier carpeta
script_dir = os.path.dirname(os.path.abspath(__file__))

if platform.system() == "Windows":
    ARCHIVO_ACCESS = os.path.join(script_dir, "datos_fuente", "VerDatosGaspar-local.accdb")
    ARCHIVO_SALIDA = os.path.join(script_dir, "dashboard.html")
    ARCHIVO_TEMP1 = os.path.join(script_dir, "temp_grafico1.html")
    ARCHIVO_TEMP2 = os.path.join(script_dir, "temp_grafico2.html")
else:
    # Docker/Linux
    ARCHIVO_ACCESS = "/app/datos_fuente/VerDatosGaspar-local.accdb"
    ARCHIVO_SALIDA = "/app/dashboard.html"
    ARCHIVO_TEMP1 = "/app/temp_grafico1.html"
    ARCHIVO_TEMP2 = "/app/temp_grafico2.html"

print("Configuracion (cargada desde config.json):")
print(f"   Total bins en sistema: {TOTAL_BINS:,}")
print(f"   Umbral critico: {UMBRAL_MINIMO:,}")
print(f"   Umbral advertencia: {UMBRAL_AMARILLO:,}")
print()

# ============================================================================
# CARGAR DATOS (FUNCIONA EN WINDOWS Y DOCKER)
# ============================================================================

MOVIMIENTOS = cargar_movimientos_bins()
print()

# ============================================================================
# PROCESAR DATOS
# ============================================================================

print("Procesando datos...")

# Crear columna de fecha sin hora
MOVIMIENTOS['FECHA_DIA'] = pd.to_datetime(MOVIMIENTOS['FECHA']).dt.date
MOVIMIENTOS['FECHA_DIA'] = pd.to_datetime(MOVIMIENTOS['FECHA_DIA'])

# Convertir FVO a datetime si existe en BASCULAR
if 'FVO' in MOVIMIENTOS.columns:
    MOVIMIENTOS['FVO'] = pd.to_datetime(MOVIMIENTOS['FVO'], errors='coerce')

# ============================================================================
# CÁLCULO DE BINS VACÍOS DISPONIBLES
# ============================================================================

# Obtener rango completo de fechas
fecha_min = MOVIMIENTOS['FECHA_DIA'].min()
fecha_max = MOVIMIENTOS['FECHA_DIA'].max()
todas_fechas = pd.date_range(start=fecha_min, end=fecha_max, freq='D')
balance_diario = pd.DataFrame({'FECHA_DIA': todas_fechas})

# 1. SALIDAS DE VACÍOS (BASCULAE - SALIDA)
salidas_vacios = MOVIMIENTOS[
    (MOVIMIENTOS['TABLA_ORIGEN'] == 'BASCULAE') &
    (MOVIMIENTOS['MOVIMIENTO'] == 'SALIDA')
].groupby('FECHA_DIA')['CANTIDAD'].sum()

# 2. ENTRADAS DESDE CAMPO (BASCULAR + BASCULAE - ENTRADA)
# Incluye bins que regresan vacíos (BASCULAE) y llenos (BASCULAR)
entradas_desde_campo = MOVIMIENTOS[
    (MOVIMIENTOS['MOVIMIENTO'] == 'ENTRADA')
].groupby('FECHA_DIA')['CANTIDAD'].sum()

# Agregar datos al balance diario
balance_diario['SALIDAS_VACIOS'] = balance_diario['FECHA_DIA'].map(salidas_vacios).fillna(0)
balance_diario['ENTRADAS_DESDE_CAMPO'] = balance_diario['FECHA_DIA'].map(entradas_desde_campo).fillna(0)

# Calcular acumulados
balance_diario['SALIDAS_VACIOS_ACUM'] = balance_diario['SALIDAS_VACIOS'].cumsum()
balance_diario['ENTRADAS_DESDE_CAMPO_ACUM'] = balance_diario['ENTRADAS_DESDE_CAMPO'].cumsum()

# APLICAR FÓRMULAS
# B_campo(d) = Salidas_vacios_acum(d) − Entradas_desde_campo_acum(d)
balance_diario['BINS_EN_CAMPOS'] = (
    balance_diario['SALIDAS_VACIOS_ACUM'] -
    balance_diario['ENTRADAS_DESDE_CAMPO_ACUM']
)

# 3. BINS LLENOS EN PLANTA - CÁLCULO CORRECTO
# B_llenos_planta(d) = COUNT(bins en BASCULAR donde FECHA <= d Y (FVO es NULL O FVO > d))
bins_llenos_por_dia = []
for fecha in todas_fechas:
    if 'FVO' in MOVIMIENTOS.columns:
        # Contar bins que YA ingresaron (FECHA <= d) pero AÚN NO fueron volcados (FVO NULL o FVO > d)
        bins_llenos = MOVIMIENTOS[
            (MOVIMIENTOS['TABLA_ORIGEN'] == 'BASCULAR') &
            (MOVIMIENTOS['MOVIMIENTO'] == 'ENTRADA') &
            (MOVIMIENTOS['FECHA_DIA'] <= fecha) &
            ((MOVIMIENTOS['FVO'].isna()) | (MOVIMIENTOS['FVO'].dt.date > fecha.date()))
        ]['CANTIDAD'].sum()
        bins_llenos_por_dia.append(bins_llenos)
    else:
        # Si no existe FVO, todos los bins que entraron siguen llenos
        bins_llenos = MOVIMIENTOS[
            (MOVIMIENTOS['TABLA_ORIGEN'] == 'BASCULAR') &
            (MOVIMIENTOS['MOVIMIENTO'] == 'ENTRADA') &
            (MOVIMIENTOS['FECHA_DIA'] <= fecha)
        ]['CANTIDAD'].sum()
        bins_llenos_por_dia.append(bins_llenos)

balance_diario['BINS_LLENOS_PLANTA'] = bins_llenos_por_dia

# B_vacios_planta(d) = B_total − B_campo(d) − B_llenos_planta(d)
balance_diario['BINS_VACIOS_PLANTA'] = (
    TOTAL_BINS -
    balance_diario['BINS_EN_CAMPOS'] -
    balance_diario['BINS_LLENOS_PLANTA']
)

# Total bins en planta (para compatibilidad con código existente)
balance_diario['BINS_EN_PLANTA'] = (
    balance_diario['BINS_VACIOS_PLANTA'] +
    balance_diario['BINS_LLENOS_PLANTA']
)

# Calcular también las columnas originales para compatibilidad
balance_diario['ENTRADA'] = balance_diario['ENTRADAS_DESDE_CAMPO']
balance_diario['SALIDA'] = balance_diario['SALIDAS_VACIOS']
balance_diario['ENTRADAS_ACUM'] = balance_diario['ENTRADAS_DESDE_CAMPO_ACUM']
balance_diario['SALIDAS_ACUM'] = balance_diario['SALIDAS_VACIOS_ACUM']
balance_diario['NETO_DIARIO'] = balance_diario['ENTRADA'] - balance_diario['SALIDA']

# Nivel de alerta
balance_diario['NIVEL_ALERTA'] = 'NORMAL'
balance_diario.loc[balance_diario['BINS_VACIOS_PLANTA'] < UMBRAL_AMARILLO, 'NIVEL_ALERTA'] = 'ADVERTENCIA'
balance_diario.loc[balance_diario['BINS_VACIOS_PLANTA'] < UMBRAL_MINIMO, 'NIVEL_ALERTA'] = 'CRITICO'

print(f"   OK {len(balance_diario)} dias procesados")
print()

# ============================================================================
# CALCULAR TENDENCIA Y ALERTAS
# ============================================================================

print("Calculando tendencias...")

# Variables actuales
stock_actual = balance_diario['BINS_EN_PLANTA'].iloc[-1]
bins_vacios_actual = balance_diario['BINS_VACIOS_PLANTA'].iloc[-1]
bins_llenos_actual = balance_diario['BINS_LLENOS_PLANTA'].iloc[-1]
fecha_actual = balance_diario['FECHA_DIA'].iloc[-1]
bins_en_campos_actual = balance_diario['BINS_EN_CAMPOS'].iloc[-1]

# SISTEMA ADAPTATIVO según días disponibles
dias_disponibles = len(balance_diario)
dias_hasta_critico = None
dias_hasta_amarillo = None
nivel_alerta_texto = "NORMAL"
color_alerta = "#2ECC71"  # Verde
pendiente = 0

if dias_disponibles < 7:
    # MODO BÁSICO: Solo umbrales fijos (primeros 6 días del año)
    print(f"   Modo BÁSICO (solo {dias_disponibles} días de historia)")
    pendiente = 0  # No hay suficientes datos para tendencia

    # Alertas por nivel actual
    if bins_vacios_actual < UMBRAL_MINIMO:
        nivel_alerta_texto = "CRÍTICO"
        color_alerta = "#E74C3C"
    elif bins_vacios_actual < UMBRAL_AMARILLO:
        nivel_alerta_texto = "ADVERTENCIA"
        color_alerta = "#F39C12"
    elif bins_vacios_actual < 10000:
        nivel_alerta_texto = "PRECAUCIÓN"
        color_alerta = "#FF9800"
    else:
        nivel_alerta_texto = "NORMAL"
        color_alerta = "#2ECC71"

elif dias_disponibles < 14:
    # MODO REACTIVO: Tendencia con 7 días (días 7-13 del año)
    print(f"   Modo REACTIVO (tendencia con 7 días)")
    dias_para_tendencia = 7
    datos_recientes = balance_diario.tail(dias_para_tendencia).copy()
    datos_recientes['dias_num'] = (datos_recientes['FECHA_DIA'] - datos_recientes['FECHA_DIA'].min()).dt.days

    x = datos_recientes['dias_num'].values
    y = datos_recientes['BINS_VACIOS_PLANTA'].values
    coef = np.polyfit(x, y, 1)
    pendiente = coef[0]

    # Umbrales más conservadores (alerta más temprano)
    if pendiente < 0:
        if bins_vacios_actual > UMBRAL_MINIMO:
            dias_hasta_critico = (bins_vacios_actual - UMBRAL_MINIMO) / abs(pendiente)
        if bins_vacios_actual > UMBRAL_AMARILLO:
            dias_hasta_amarillo = (bins_vacios_actual - UMBRAL_AMARILLO) / abs(pendiente)

        # Umbrales más estrictos con pocos datos
        if dias_hasta_critico and dias_hasta_critico <= 10:
            nivel_alerta_texto = "CRÍTICO"
            color_alerta = "#E74C3C"
        elif dias_hasta_amarillo and dias_hasta_amarillo <= 10:
            nivel_alerta_texto = "ADVERTENCIA"
            color_alerta = "#F39C12"
        elif dias_hasta_critico and dias_hasta_critico <= 20:
            nivel_alerta_texto = "PRECAUCIÓN"
            color_alerta = "#FF9800"
    else:
        nivel_alerta_texto = "RECUPERACIÓN"
        color_alerta = "#3498DB"

else:
    # MODO NORMAL: Tendencia con 14 días (día 14+ del año)
    print(f"   Modo NORMAL (tendencia con 14 días)")
    dias_para_tendencia = 14
    datos_recientes = balance_diario.tail(dias_para_tendencia).copy()
    datos_recientes['dias_num'] = (datos_recientes['FECHA_DIA'] - datos_recientes['FECHA_DIA'].min()).dt.days

    x = datos_recientes['dias_num'].values
    y = datos_recientes['BINS_VACIOS_PLANTA'].values
    coef = np.polyfit(x, y, 1)
    pendiente = coef[0]

    # Detector de caídas bruscas (cambio > 1000 bins en 1 día)
    cambio_ultimo_dia = balance_diario['BINS_VACIOS_PLANTA'].diff().iloc[-1]
    caida_brusca = cambio_ultimo_dia < -1000

    if pendiente < 0:
        if bins_vacios_actual > UMBRAL_MINIMO:
            dias_hasta_critico = (bins_vacios_actual - UMBRAL_MINIMO) / abs(pendiente)
        if bins_vacios_actual > UMBRAL_AMARILLO:
            dias_hasta_amarillo = (bins_vacios_actual - UMBRAL_AMARILLO) / abs(pendiente)

        # Si hay caída brusca, alerta inmediata
        if caida_brusca or (dias_hasta_critico and dias_hasta_critico <= 7):
            nivel_alerta_texto = "CRÍTICO"
            color_alerta = "#E74C3C"
        elif dias_hasta_amarillo and dias_hasta_amarillo <= 7:
            nivel_alerta_texto = "ADVERTENCIA"
            color_alerta = "#F39C12"
        elif dias_hasta_critico and dias_hasta_critico <= 14:
            nivel_alerta_texto = "PRECAUCIÓN"
            color_alerta = "#FF9800"
    else:
        nivel_alerta_texto = "RECUPERACIÓN"
        color_alerta = "#3498DB"

print(f"   OK Tendencia calculada: {pendiente:,.1f} bins/dia")
print()

# ============================================================================
# CREAR GRAFICOS
# ============================================================================

print("Generando graficos...")

# GRÁFICO 1: OPCIÓN 5 - Áreas Apiladas con Hover Completo
fig1 = go.Figure()

# Preparar datos de fecha en español para tooltip
meses_español = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

def fecha_español(fecha):
    dia = fecha.day
    mes = meses_español[fecha.month]
    año = fecha.year
    return f"{dia:02d}/{mes}/{año}"

balance_diario['FECHA_ESP'] = balance_diario['FECHA_DIA'].apply(fecha_español)

# Área 1: Bins vacíos en planta (verde) - LA BASE
fig1.add_trace(go.Scatter(
    x=balance_diario['FECHA_DIA'],
    y=balance_diario['BINS_VACIOS_PLANTA'],
    name='Bins Vacíos Disponibles',
    fill='tozeroy',
    fillcolor='rgba(35, 170, 152, 1)',
    line=dict(color='rgba(35, 170, 152, 1)', width=2),
    mode='lines',
    customdata=balance_diario['FECHA_ESP'],
    hovertemplate='<b>%{customdata}</b><br>Vacíos: %{y:,.0f}<extra></extra>',
    stackgroup='one'
))

# Área 2: Bins llenos en planta (morado)
fig1.add_trace(go.Scatter(
    x=balance_diario['FECHA_DIA'],
    y=balance_diario['BINS_LLENOS_PLANTA'],
    name='Bins Llenos (pendientes)',
    fill='tonexty',
    fillcolor='rgba(100, 35, 170, 1)',
    line=dict(color='rgba(100, 35, 170, 1)', width=2),
    mode='lines',
    customdata=balance_diario['FECHA_ESP'],
    hovertemplate='<b>%{customdata}</b><br>Llenos: %{y:,.0f}<extra></extra>',
    stackgroup='one'
))

# Área 3: Bins en campos (rojo)
fig1.add_trace(go.Scatter(
    x=balance_diario['FECHA_DIA'],
    y=balance_diario['BINS_EN_CAMPOS'],
    name='Bins en Campos',
    fill='tonexty',
    fillcolor='rgba(170, 35, 35, 1)',
    line=dict(color='rgba(170, 35, 35, 1)', width=2),
    mode='lines',
    customdata=balance_diario['FECHA_ESP'],
    hovertemplate='<b>%{customdata}</b><br>En Campos: %{y:,.0f}<extra></extra>',
    stackgroup='one'
))

# Líneas de referencia - Umbrales
fig1.add_hline(
    y=UMBRAL_MINIMO,
    line_dash="solid",
    line_color="rgba(0, 3, 243, 1)",
    line_width=2,
    annotation_text=f"Umbral {format_number(UMBRAL_MINIMO, 0)}",
    annotation_position="top left"
)

fig1.add_hline(
    y=UMBRAL_AMARILLO,
    line_dash="solid",
    line_color="rgba(247, 255, 0, 1)",
    line_width=2,
    annotation_text=f"Umbral {format_number(UMBRAL_AMARILLO, 0)}",
    annotation_position="top left"
)

# Crear ticks mensuales en español para todo el año (detectar año automáticamente)
meses_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
año_datos = balance_diario['FECHA_DIA'].max().year
tickvals = [f"{año_datos}-{i:02d}-15" for i in range(1, 13)]  # día 15 para centrar
ticktext = [f"{meses_es[i-1]} {año_datos}" for i in range(1, 13)]

fig1.update_layout(
    title='Distribución Total de Bins (Áreas Apiladas)',
    xaxis_title='Fecha',
    yaxis_title='Cantidad de Bins',
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Segoe UI"
    ),
    height=600,
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    yaxis=dict(range=[0, TOTAL_BINS + 1000]),
    paper_bgcolor='rgb(190, 190, 190)',
    plot_bgcolor='rgb(190, 190, 190)',
    xaxis=dict(
        tickvals=tickvals,
        ticktext=ticktext,
        tickangle=0,
        range=[f"{año_datos}-01-01", f"{año_datos}-12-31"],
        hoverformat='%d/%B/%Y'
    ),
    margin=dict(l=80, r=40, t=50, b=50),
    font=dict(size=12)
)

# GRÁFICO 2: OPCIÓN 4 - Líneas Individuales (No Apiladas)
fig2 = go.Figure()

# Línea 1: Bins vacíos disponibles (verde)
fig2.add_trace(go.Scatter(
    x=balance_diario['FECHA_DIA'],
    y=balance_diario['BINS_VACIOS_PLANTA'],
    name='Bins Vacíos Disponibles',
    line=dict(color='rgba(35, 170, 152, 1)', width=3),
    mode='lines',
    customdata=balance_diario['FECHA_ESP'],
    hovertemplate='<b>%{customdata}</b><br>Vacíos: %{y:,.0f}<extra></extra>'
))

# Línea 2: Bins llenos en planta (morado)
fig2.add_trace(go.Scatter(
    x=balance_diario['FECHA_DIA'],
    y=balance_diario['BINS_LLENOS_PLANTA'],
    name='Bins Llenos (pendientes)',
    line=dict(color='rgba(100, 35, 170, 1)', width=3),
    mode='lines',
    customdata=balance_diario['FECHA_ESP'],
    hovertemplate='<b>%{customdata}</b><br>Llenos: %{y:,.0f}<extra></extra>'
))

# Línea 3: Bins en campos (rojo)
fig2.add_trace(go.Scatter(
    x=balance_diario['FECHA_DIA'],
    y=balance_diario['BINS_EN_CAMPOS'],
    name='Bins en Campos',
    line=dict(color='rgba(170, 35, 35, 1)', width=3),
    mode='lines',
    customdata=balance_diario['FECHA_ESP'],
    hovertemplate='<b>%{customdata}</b><br>En Campos: %{y:,.0f}<extra></extra>'
))

# Líneas de referencia - Umbrales
fig2.add_hline(
    y=UMBRAL_MINIMO,
    line_dash="solid",
    line_color="rgba(0, 3, 243, 1)",
    line_width=2,
    annotation_text=f"Umbral {format_number(UMBRAL_MINIMO, 0)}",
    annotation_position="top left"
)

fig2.add_hline(
    y=UMBRAL_AMARILLO,
    line_dash="solid",
    line_color="rgba(247, 255, 0, 1)",
    line_width=2,
    annotation_text=f"Umbral {format_number(UMBRAL_AMARILLO, 0)}",
    annotation_position="top left"
)

fig2.update_layout(
    title='Evolución Individual por Categoría (Líneas)',
    xaxis_title='Fecha',
    yaxis_title='Cantidad de Bins',
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Segoe UI"
    ),
    height=600,
    template='plotly_white',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    paper_bgcolor='rgb(190, 190, 190)',
    plot_bgcolor='rgb(190, 190, 190)',
    xaxis=dict(
        tickvals=tickvals,
        ticktext=ticktext,
        tickangle=0,
        range=[f"{año_datos}-01-01", f"{año_datos}-12-31"],
        hoverformat='%d/%B/%Y'
    ),
    yaxis=dict(
        separatethousands=True
    ),
    margin=dict(l=80, r=40, t=50, b=50),
    font=dict(size=12)
)

print("   OK Graficos creados")
print()

# ============================================================================
# GENERAR HTML
# ============================================================================

print("Generando dashboard HTML...")

# Guardar los graficos como archivos HTML temporales completos
fig1.write_html(ARCHIVO_TEMP1, config={'displayModeBar': False}, include_plotlyjs='cdn')
fig2.write_html(ARCHIVO_TEMP2, config={'displayModeBar': False}, include_plotlyjs='cdn')

# Crear HTML con estilo profesional
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Dashboard - Jugos S.A.</title>
    <link rel="icon" type="image/png" href="favicon.png">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            color: #e0e0e0;
            overflow-x: hidden;
        }}

        .header {{
            background: #1B5E4E;
            padding: 25px;
            text-align: left;
            border-bottom: 2px solid #2ECC71;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}

        .header h1 {{
            font-size: 1.8em;
            color: #e0e0e0;
            font-weight: 600;
            margin: 0;
        }}

        .header .fecha {{
            font-size: 0.95em;
            margin-top: 5px;
            color: #b0b0b0;
        }}

        .container {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: auto auto auto;
            gap: 15px;
            padding: 20px;
            max-width: 1920px;
            margin: 0 auto;
        }}

        .kpi-card {{
            background: #1B5E4E;
            border-radius: 4px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
            border-left: 4px solid #2ECC71;
        }}

        .kpi-title {{
            font-size: 0.85em;
            color: #b0b0b0;
            text-transform: uppercase;
            margin-bottom: 8px;
            font-weight: 600;
        
            color: #2ECC71;}}

        .kpi-value {{
            font-size: 2em;
            color: #e0e0e0;
            font-weight: 700;
            margin-bottom: 5px;
        }}

        .kpi-subtitle {{
            font-size: 0.85em;
            color: #808080;
        }}

        .chart-container {{
            background: #1B5E4E;
            border-radius: 4px;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
            grid-column: span 2;
            overflow: hidden;
        }}

        .chart-container iframe {{
            display: block;
            overflow: hidden !important;
        }}

        .chart-container.full-width {{
            grid-column: span 4;
        }}

        .stat-label {{
            font-weight: bold;
            font-size: 0.9em;
            opacity: 0.9;
        }}

        .stat-value {{
            font-size: 1.8em;
            font-weight: bold;
            margin-top: 5px;
        }}

        .tendencia {{
            margin-top: 20px;
            padding: 20px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            text-align: center;
        }}

        .full-width {{
            grid-column: 1 / -1;
        }}

        @media (max-width: 1200px) {{
            .container {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Ocultar controles para modo kiosko */
        .modebar {{
            display: none !important;
        }}

        .footer {{
            background: #0d333d;
            color: #b0b0b0;
            padding: 20px;
            text-align: center;
            font-size: 0.85em;
            border-top: 2px solid #2ECC71;
            margin-top: 30px;
        }}

        .footer-title {{
            color: #e0e0e0;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .footer-subtitle {{
            color: #808080;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}

        .footer-contact {{
            display: flex;
            justify-content: center;
            gap: 25px;
            flex-wrap: wrap;
        }}

        .footer-contact-item {{
            color: #b0b0b0;
        }}

        .footer-contact-item a {{
            color: #2ECC71;
            text-decoration: none;
        }}

        .footer-contact-item a:hover {{
            text-decoration: underline;
        }}

        /* Estilos para el control de ajuste automático */
        .chart-control {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
            margin-bottom: 8px;
            font-size: 0.9em;
        }}

        .toggle-switch {{
            position: relative;
            width: 50px;
            height: 24px;
            display: inline-block;
        }}

        .toggle-switch input {{
            opacity: 0;
            width: 0;
            height: 0;
        }}

        .toggle-slider {{
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #555;
            transition: 0.3s;
            border-radius: 24px;
        }}

        .toggle-slider:before {{
            position: absolute;
            content: "";
            height: 18px;
            width: 18px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: 0.3s;
            border-radius: 50%;
        }}

        .toggle-switch input:checked + .toggle-slider {{
            background-color: #2ECC71;
        }}

        .toggle-switch input:checked + .toggle-slider:before {{
            transform: translateX(26px);
        }}

        .chart-control-label {{
            color: #b0b0b0;
            font-weight: 500;
        }}

        .chart-control input:checked ~ .chart-control-label {{
            color: #2ECC71;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>JUGOS S.A. - Control de Stock de Bins</h1>
        <div class="fecha">Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
    </div>

    <div class="container">
        <!-- KPI Cards - Sistema de Alerta -->
        <div class="kpi-card">
            <div class="kpi-title">Bins Vacíos Disponibles</div>
            <div class="kpi-value" style="color: {color_alerta};">{format_number(bins_vacios_actual, 0)}</div>
            <div class="kpi-subtitle">Nivel: {nivel_alerta_texto}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-title">Tendencia (14 días)</div>
            <div class="kpi-value" style="color: {'#E74C3C' if pendiente < 0 else '#2ECC71'};">{pendiente:+.1f}</div>
            <div class="kpi-subtitle">bins por día</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-title">Días hasta Advertencia</div>
            <div class="kpi-value" style="color: {'#F39C12' if dias_hasta_amarillo and dias_hasta_amarillo <= 14 else '#2ECC71'};">{int(dias_hasta_amarillo) if dias_hasta_amarillo else '---'}</div>
            <div class="kpi-subtitle">umbral: {format_number(UMBRAL_AMARILLO, 0)}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-title">Días hasta Crítico</div>
            <div class="kpi-value" style="color: {'#E74C3C' if dias_hasta_critico and dias_hasta_critico <= 7 else '#F39C12' if dias_hasta_critico and dias_hasta_critico <= 14 else '#2ECC71'};">{int(dias_hasta_critico) if dias_hasta_critico else '---'}</div>
            <div class="kpi-subtitle">umbral: {format_number(UMBRAL_MINIMO, 0)}</div>
        </div>

        <!-- GRÁFICO 1: Distribución -->
        <div class="chart-container" style="grid-column: span 4;">
            <iframe id="iframe-grafico1" src="temp_grafico1.html" style="width:100%; height:617px; border:none; overflow:hidden !important;"></iframe>
        </div>

        <!-- GRÁFICO 2: Comparación -->
        <div class="chart-container" style="grid-column: span 4;">
            <iframe id="iframe-grafico2" src="temp_grafico2.html" style="width:100%; height:617px; border:none; overflow:hidden !important;"></iframe>
        </div>
    </div>

    <div class="footer">
        <div class="footer-title">Desarrollado por Gaspar Giannitrapani</div>
        <div class="footer-subtitle">Técnico Superior en Ciencia de Datos</div>
        <div class="footer-contact">
            <div class="footer-contact-item">
                <a href="mailto:giannitrapanigaspar@gmail.com">giannitrapanigaspar@gmail.com</a>
            </div>
            <div class="footer-contact-item">+54 9 298 470-4091</div>
            <div class="footer-contact-item">
                <a href="https://www.linkedin.com/in/giannitrapanigaspar" target="_blank">linkedin.com/in/giannitrapanigaspar</a>
            </div>
        </div>
    </div>

    <script>
        // Auto-fullscreen para modo kiosko
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'F11') {{
                e.preventDefault();
                if (!document.fullscreenElement) {{
                    document.documentElement.requestFullscreen();
                }} else {{
                    document.exitFullscreen();
                }}
            }}
        }});
    </script>
</body>
</html>
"""

# Guardar archivo HTML
with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"   OK Dashboard guardado en: {ARCHIVO_SALIDA}")
print()

# ============================================================================
# RESUMEN
# ============================================================================

print("="*70)
print("DASHBOARD GENERADO EXITOSAMENTE")
print("="*70)
print()
print(f"Estadisticas:")
print(f"   - Total registros procesados: {len(MOVIMIENTOS):,}")
print(f"   - Periodo analizado: {balance_diario['FECHA_DIA'].min().strftime('%d/%m/%Y')} a {balance_diario['FECHA_DIA'].max().strftime('%d/%m/%Y')}")
print(f"   - Bins vacios planta: {bins_vacios_actual:,.0f} bins")
print(f"   - Bins llenos planta: {bins_llenos_actual:,.0f} bins")
print(f"   - Total en planta: {stock_actual:,.0f} bins")
print(f"   - Bins en campos: {bins_en_campos_actual:,.0f} bins")
print(f"   - Nivel de alerta: {nivel_alerta_texto}")
print()

# (Conexión ya cerrada por el módulo universal)
print()

print("Instrucciones:")
print("   1. Abre: dashboard.html (doble clic)")
print("   2. Presiona F11 para pantalla completa")
print("   3. Conecta al TV y listo")
print()
print("Para actualizar:")
print("   1. Los datos se obtienen automaticamente desde Access")
print("   2. Ejecuta este script nuevamente")
print("   3. Recarga dashboard.html en el navegador")
print()
print("="*70)
