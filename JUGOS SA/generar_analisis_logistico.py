# ============================================================================
# GENERADOR DE ANÁLISIS LOGÍSTICO - JUGOS S.A.
# Basado en PROYECTO 1 JUGOS.ipynb
# ============================================================================

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json
import locale
import platform
import os
from cargar_datos_universal import cargar_ingresos_logistica, cargar_tabla

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

print("="*70)
print("GENERADOR DE ANALISIS LOGISTICO - JUGOS S.A.")
print("="*70)
print()

# ============================================================================
# CARGAR CONFIGURACIÓN DESDE config.json
# ============================================================================

# Cargar configuración desde archivo JSON
with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

# Rutas RELATIVAS - funciona desde cualquier carpeta
script_dir = os.path.dirname(os.path.abspath(__file__))

if platform.system() == "Windows":
    ARCHIVO_ACCESS = os.path.join(script_dir, "datos_fuente", "VerDatosGaspar-local.accdb")
    ARCHIVO_SALIDA = os.path.join(script_dir, "logistica.html")
    TEMP1 = os.path.join(script_dir, "temp_logistica1.html")
    TEMP2 = os.path.join(script_dir, "temp_logistica2.html")
    TEMP3 = os.path.join(script_dir, "temp_logistica3.html")
    TEMP4 = os.path.join(script_dir, "temp_logistica4.html")
    TEMP5 = os.path.join(script_dir, "temp_logistica5.html")
    TEMP6 = os.path.join(script_dir, "temp_logistica6.html")
else:
    # Docker/Linux
    ARCHIVO_ACCESS = "/app/datos_fuente/VerDatosGaspar-local.accdb"
    ARCHIVO_SALIDA = "/app/logistica.html"
    TEMP1 = "/app/temp_logistica1.html"
    TEMP2 = "/app/temp_logistica2.html"
    TEMP3 = "/app/temp_logistica3.html"
    TEMP4 = "/app/temp_logistica4.html"
    TEMP5 = "/app/temp_logistica5.html"
    TEMP6 = "/app/temp_logistica6.html"

print("Configuracion cargada desde config.json")
print("Base de datos Access:")
print(f"   - {ARCHIVO_ACCESS}")
print()

# ============================================================================
# CARGAR DATOS (FUNCIONA EN WINDOWS Y DOCKER)
# ============================================================================

df, df_prov = cargar_ingresos_logistica()
print()

# ============================================================================
# ANÁLISIS 1: TEMPORAL (Día, Semana y Mes)
# ============================================================================

print("Generando Analisis 1: Temporal (Diario, Semanal y Mensual)...")

# Convertir fecha a datetime floor
df['FechaDia'] = df['Fecha'].dt.floor('D')

# Agregar columnas de semana y mes (usando lunes como inicio)
df['Semana'] = df['Fecha'].dt.to_period('W-MON').apply(lambda r: r.start_time)
df['Mes'] = df['Fecha'].dt.to_period('M').apply(lambda r: r.start_time)

# Agrupar por día
diario = df.groupby('FechaDia').agg({
    'kgs': 'sum',
    'CantBins': 'sum'
}).reset_index().sort_values('FechaDia')

# Agrupar por semana
semanal = df.groupby('Semana').agg({
    'kgs': 'sum',
    'CantBins': 'sum'
}).reset_index().sort_values('Semana')

# Agrupar por mes
mensual = df.groupby('Mes').agg({
    'kgs': 'sum',
    'CantBins': 'sum'
}).reset_index().sort_values('Mes')

# Calcular KPIs
total_kgs = float(df['kgs'].sum())
promedio_diario_kg = float(diario['kgs'].mean()) if len(diario) else 0
promedio_semanal_kg = float(semanal['kgs'].mean()) if len(semanal) else 0
promedio_mensual_kg = float(mensual['kgs'].mean()) if len(mensual) else 0

max_diario_kg = float(diario['kgs'].max()) if len(diario) else 0
max_diario_fecha = diario.loc[diario['kgs'].idxmax(), 'FechaDia'] if len(diario) else None

max_semanal_kg = float(semanal['kgs'].max()) if len(semanal) else 0
max_semanal_idx = semanal['kgs'].idxmax() if len(semanal) else None
max_semanal_inicio = semanal.loc[max_semanal_idx, 'Semana'] if max_semanal_idx is not None else None

max_mensual_kg = float(mensual['kgs'].max()) if len(mensual) else 0
max_mensual_idx = mensual['kgs'].idxmax() if len(mensual) else None
max_mensual_fecha = mensual.loc[max_mensual_idx, 'Mes'] if max_mensual_idx is not None else None

min_diario_kg = float(diario['kgs'].min()) if len(diario) else 0
min_diario_fecha = diario.loc[diario['kgs'].idxmin(), 'FechaDia'] if len(diario) else None

min_semanal_kg = float(semanal['kgs'].min()) if len(semanal) else 0
min_semanal_idx = semanal['kgs'].idxmin() if len(semanal) else None
min_semanal_inicio = semanal.loc[min_semanal_idx, 'Semana'] if min_semanal_idx is not None else None

min_mensual_kg = float(mensual['kgs'].min()) if len(mensual) else 0
min_mensual_idx = mensual['kgs'].idxmin() if len(mensual) else None
min_mensual_fecha = mensual.loc[min_mensual_idx, 'Mes'] if min_mensual_idx is not None else None

# Imprimir KPIs
print(f"   Total de kilogramos: {total_kgs:,.0f} kg")
print(f"   Promedio diario: {promedio_diario_kg:,.0f} kg/dia")
print(f"   Promedio semanal: {promedio_semanal_kg:,.0f} kg/semana")
print(f"   Promedio mensual: {promedio_mensual_kg:,.0f} kg/mes")
if max_diario_fecha:
    print(f"   Maximo diario: {max_diario_kg:,.0f} kg ({max_diario_fecha.strftime('%Y-%m-%d')})")
if max_semanal_inicio:
    print(f"   Maximo semanal: {max_semanal_kg:,.0f} kg (Semana {max_semanal_inicio.strftime('%Y-%m-%d')})")
if max_mensual_fecha:
    print(f"   Maximo mensual: {max_mensual_kg:,.0f} kg ({max_mensual_fecha.strftime('%Y-%m')})")

# Detectar el año de los datos
año_datos = df['Fecha'].max().year

# Crear ticks mensuales en español para todo el año
meses_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
tickvals = [f"{año_datos}-{i:02d}-15" for i in range(1, 13)]  # día 15 para centrar
ticktext = [f"{meses_es[i-1]} {año_datos}" for i in range(1, 13)]

# Preparar títulos con estadísticas (título grande, luego stats en línea horizontal)
titulo_diario = f"<b>Kilogramos por Día</b><br><span style='font-size:14px'>Promedio: {format_number(promedio_diario_kg, 0)} kg/día --- Mínimo: {format_number(min_diario_kg, 0)} kg ({min_diario_fecha.strftime('%d/%m/%Y') if min_diario_fecha else 'N/A'}) --- Máximo: {format_number(max_diario_kg, 0)} kg ({max_diario_fecha.strftime('%d/%m/%Y') if max_diario_fecha else 'N/A'})</span>"

titulo_semanal = f"<b>Kilogramos por Semana</b><br><span style='font-size:14px'>Promedio: {format_number(promedio_semanal_kg, 0)} kg/semana --- Mínimo: {format_number(min_semanal_kg, 0)} kg (Semana {min_semanal_inicio.strftime('%d/%m/%Y') if min_semanal_inicio else 'N/A'}) --- Máximo: {format_number(max_semanal_kg, 0)} kg (Semana {max_semanal_inicio.strftime('%d/%m/%Y') if max_semanal_inicio else 'N/A'})</span>"

titulo_mensual = f"<b>Kilogramos por Mes</b><br><span style='font-size:14px'>Promedio: {format_number(promedio_mensual_kg, 0)} kg/mes --- Mínimo: {format_number(min_mensual_kg, 0)} kg ({min_mensual_fecha.strftime('%Y-%m') if min_mensual_fecha else 'N/A'}) --- Máximo: {format_number(max_mensual_kg, 0)} kg ({max_mensual_fecha.strftime('%Y-%m') if max_mensual_fecha else 'N/A'})</span>"

# Crear subplots (3 gráficos de línea, uno debajo del otro)
fig1 = make_subplots(
    rows=3, cols=1,
    subplot_titles=(titulo_diario, titulo_semanal, titulo_mensual),
    vertical_spacing=0.15
)

# Gráfico diario (línea azul)
fig1.add_trace(
    go.Scatter(
        x=diario['FechaDia'],
        y=diario['kgs'],
        mode='lines',
        name='KG Diario',
        line=dict(color='steelblue', width=2),
        hovertemplate='<b>Fecha:</b> %{x|%d/%m/%Y}<br><b>Kilogramos:</b> %{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

# Gráfico semanal (línea verde)
fig1.add_trace(
    go.Scatter(
        x=semanal['Semana'],
        y=semanal['kgs'],
        mode='lines',
        name='KG Semanal',
        line=dict(color='green', width=2),
        hovertemplate='<b>Semana:</b> %{x|%d/%m/%Y}<br><b>Kilogramos:</b> %{y:,.0f}<extra></extra>'
    ),
    row=2, col=1
)

# Gráfico mensual (línea coral)
fig1.add_trace(
    go.Scatter(
        x=mensual['Mes'],
        y=mensual['kgs'],
        mode='lines',
        name='KG Mensual',
        line=dict(color='coral', width=2),
        hovertemplate='<b>Mes:</b> %{x|%B %Y}<br><b>Kilogramos:</b> %{y:,.0f}<extra></extra>'
    ),
    row=3, col=1
)

# Configurar eje X con meses en español para los 3 gráficos
fig1.update_xaxes(
    title_text="",
    row=1, col=1,
    showspikes=True,
    spikemode='across',
    spikethickness=1,
    spikecolor='gray',
    spikedash='solid',
    tickvals=tickvals,
    ticktext=ticktext,
    tickangle=0,
    range=[f"{año_datos}-01-01", f"{año_datos}-12-31"]
)

fig1.update_xaxes(
    title_text="",
    row=2, col=1,
    showspikes=True,
    spikemode='across',
    spikethickness=1,
    spikecolor='gray',
    spikedash='solid',
    tickvals=tickvals,
    ticktext=ticktext,
    tickangle=0,
    range=[f"{año_datos}-01-01", f"{año_datos}-12-31"]
)

fig1.update_xaxes(
    title_text="",
    row=3, col=1,
    showspikes=True,
    spikemode='across',
    spikethickness=1,
    spikecolor='gray',
    spikedash='solid',
    tickvals=tickvals,
    ticktext=ticktext,
    tickangle=0,
    range=[f"{año_datos}-01-01", f"{año_datos}-12-31"]
)

fig1.update_yaxes(title_text="Kilogramos", row=1, col=1, rangemode='tozero')
fig1.update_yaxes(title_text="Kilogramos", row=2, col=1, rangemode='tozero')
fig1.update_yaxes(title_text="Kilogramos", row=3, col=1, rangemode='tozero')

fig1.update_layout(
    title_text='Evolución Temporal de Kilogramos Transportados<br><br>',
    showlegend=False,
    template='plotly_white',
    height=1000,
    margin=dict(l=50, r=50, t=80, b=50),
    paper_bgcolor='rgb(190, 190, 190)',
    plot_bgcolor='rgb(190, 190, 190)',
    hovermode='x unified'
)

# Actualizar el tamaño de fuente de las anotaciones (títulos de subplots)
fig1.update_annotations(font_size=14)

fig1.write_html(TEMP1, config={'displayModeBar': False}, include_plotlyjs='cdn')
print("   OK Grafico 1 generado (Diario, Semanal y Mensual)")

# ============================================================================
# ANÁLISIS 2: DISTANCIA (KM vs KG) - Rangos de 25 km
# ============================================================================

print("Generando Analisis 2: Distancia...")

# Limpiar datos
dist_df = df[['kgs', 'kms', 'CantBins']].copy()
dist_df['kgs'] = pd.to_numeric(dist_df['kgs'], errors='coerce')
dist_df['kms'] = pd.to_numeric(dist_df['kms'], errors='coerce')
dist_df = dist_df.loc[dist_df['kgs'].notna() & dist_df['kms'].notna()]

# Estadísticas globales
total_viajes = int(len(dist_df))
total_kgs_global = float(dist_df['kgs'].sum())
distance_min_km = float(dist_df['kms'].min())
distance_max_km = float(dist_df['kms'].max())
distance_mean_km = float(dist_df['kms'].mean())

pct_viajes_le_100km = 100.0 * (dist_df['kms'] <= 100).mean()
pct_kgs_le_100km = 100.0 * (dist_df.loc[dist_df['kms'] <= 100, 'kgs'].sum() / total_kgs_global) if total_kgs_global > 0 else 0

# Segmentación cada 25 km
step = 25
max_edge = int(np.ceil(max(distance_max_km, step) / step) * step)
dist_bins_25 = np.arange(0, max_edge + step, step)
dist_labels_25 = [f"{int(dist_bins_25[i])}-{int(dist_bins_25[i+1])}" for i in range(len(dist_bins_25)-1)]

dist_df['rango_km_25'] = pd.cut(
    dist_df['kms'],
    bins=dist_bins_25,
    labels=dist_labels_25,
    include_lowest=True,
    right=False,
    ordered=True
)

# Agregados por rango
kg_por_rango_25 = dist_df.groupby('rango_km_25', observed=True)['kgs'].sum().fillna(0)
viajes_por_rango_25 = dist_df.groupby('rango_km_25', observed=True).size()
participacion_kg_25 = 100.0 * kg_por_rango_25 / total_kgs_global if total_kgs_global > 0 else kg_por_rango_25*0

# Eficiencia (kg/km)
dist_df['eficiencia_kg_km'] = np.where(dist_df['kms'] > 0, dist_df['kgs'] / dist_df['kms'], np.nan)
mask_valid = dist_df['kms'] > 0
sum_kg_valid = dist_df.loc[mask_valid].groupby('rango_km_25', observed=True)['kgs'].sum()
sum_km_valid = dist_df.loc[mask_valid].groupby('rango_km_25', observed=True)['kms'].sum()
eficiencia_ponderada_25 = (sum_kg_valid / sum_km_valid).replace([np.inf, -np.inf], np.nan)

# Extremos
rango_max_kg = (kg_por_rango_25.idxmax(), float(kg_por_rango_25.max())) if len(kg_por_rango_25) else (None, 0)
rango_min_kg = (kg_por_rango_25.idxmin(), float(kg_por_rango_25.min())) if len(kg_por_rango_25) else (None, 0)
rango_max_vj = (viajes_por_rango_25.idxmax(), int(viajes_por_rango_25.max())) if len(viajes_por_rango_25) else (None, 0)
rango_min_vj = (viajes_por_rango_25.idxmin(), int(viajes_por_rango_25.min())) if len(viajes_por_rango_25) else (None, 0)

if len(eficiencia_ponderada_25.dropna()):
    ef_max_rng = (eficiencia_ponderada_25.idxmax(), float(eficiencia_ponderada_25.max()))
    ef_min_rng = (eficiencia_ponderada_25.idxmin(), float(eficiencia_ponderada_25.min()))
else:
    ef_max_rng = (None, 0)
    ef_min_rng = (None, 0)

# Imprimir KPIs
print(f"   Total de viajes: {total_viajes:,}")
print(f"   Total de kilogramos: {total_kgs_global:,.0f} kg")
print(f"   Distancia promedio: {distance_mean_km:,.1f} km")
print(f"   Rango (min-max): {int(distance_min_km)}-{int(distance_max_km)} km")
print(f"   % viajes <=100 km: {pct_viajes_le_100km:5.1f}%")
print(f"   % kg <=100 km: {pct_kgs_le_100km:5.1f}%")
print(f"   Rango con MAS kg: {rango_max_kg[0]} - {rango_max_kg[1]:,.0f} kg")
print(f"   Rango con MENOS kg: {rango_min_kg[0]} - {rango_min_kg[1]:,.0f} kg")
print(f"   Eficiencia MAX: {ef_max_rng[0]} - {ef_max_rng[1]:,.0f} kg/km")
print(f"   Eficiencia MIN: {ef_min_rng[0]} - {ef_min_rng[1]:,.0f} kg/km")

# Crear gráfico de barras
fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=kg_por_rango_25.index.astype(str),
    y=kg_por_rango_25.values,
    marker_color='#0078D4',
    text=[f"{pct:.1f}%" for pct in participacion_kg_25.reindex(kg_por_rango_25.index).fillna(0).values],
    textposition='outside',
    hovertemplate='<b>Rango:</b> %{x}<br><b>Kilogramos:</b> %{y:,.0f}<extra></extra>'
))

fig2.update_layout(
    title='Kilogramos por Rango (25 km)',
    xaxis_title='Rango KM',
    yaxis_title='Kilogramos (kg)',
    template='plotly_white',
    height=500,
    margin=dict(l=50, r=50, t=50, b=110),
    paper_bgcolor='rgb(190, 190, 190)',
    plot_bgcolor='rgb(190, 190, 190)',
    annotations=[
        dict(
            text="<b>Distribución de kilogramos transportados según rangos de distancia (25 km). Los porcentajes indican la contribución de cada rango al volumen total.</b>",
            xref="paper", yref="paper",
            x=0.5, y=-0.25,
            showarrow=False,
            font=dict(size=12),
            xanchor='center',
            align='center'
        )
    ]
)

fig2.write_html(TEMP2, config={'displayModeBar': False}, include_plotlyjs='cdn')
print("   OK Grafico 2 generado")

# ============================================================================
# ANÁLISIS 3: ESPECIE/VARIEDAD (Top 10 + Pie PERA vs MANZANA)
# ============================================================================

print("Generando Analisis 3: Especie/Variedad...")

TOP_N = 10

# Agrupar por Especie y Variedad
fruit_df = df[['Especie', 'NomVariedad', 'kgs']].copy()
fruit_df['kgs'] = pd.to_numeric(fruit_df['kgs'], errors='coerce')
fruit_df['fruta'] = fruit_df['Especie'].fillna('') + ' - ' + fruit_df['NomVariedad'].fillna('')
fruit_df['fruta'] = fruit_df['fruta'].str.strip(' -')

# KPIs por fruta
kg_por_fruta = fruit_df.dropna(subset=['kgs']).groupby('fruta')['kgs'].sum().sort_values(ascending=False)
participacion_por_fruta = (kg_por_fruta / kg_por_fruta.sum() * 100.0)

# Top 10
top_frutas = kg_por_fruta.head(TOP_N)
top_participacion = participacion_por_fruta.loc[top_frutas.index]

# Estadísticas
total_kgs_fruta = float(kg_por_fruta.sum())
n_categorias = len(kg_por_fruta)
dominante_label = kg_por_fruta.index[0] if len(kg_por_fruta) > 0 else None
dominante_kg = float(kg_por_fruta.iloc[0]) if len(kg_por_fruta) > 0 else 0
dominante_pct = float(participacion_por_fruta.iloc[0]) if len(participacion_por_fruta) > 0 else 0

print(f"   Categorias de fruta: {n_categorias}")
print(f"   Volumen total: {total_kgs_fruta:,.0f} kg")
if dominante_label:
    print(f"   Fruta dominante: {dominante_label} - {dominante_kg:,.0f} kg ({dominante_pct:.1f}%)")

# Cargar tabla de variedades desde Access para el pie chart
try:
    df_var = cargar_tabla('Lvariedad')

    # Normalizar columnas
    df_var.columns = df_var.columns.str.lower()
    df_var['exp'] = df_var['exp'].astype(str).str.strip().str.lower()
    df_var['exp_norm'] = df_var['exp'].replace({'manza': 'manzana'})
    df_var_pm = df_var[df_var['exp_norm'].isin(['pera', 'manzana'])][['gru', 'exp_norm']].dropna().drop_duplicates()

    # Match especie con gru
    merge_df = df[['Especie', 'kgs']].copy()
    merge_df['especie'] = merge_df['Especie'].astype(str).str.strip()
    df_match = merge_df.merge(df_var_pm, left_on='especie', right_on='gru', how='left')

    kg_pm = df_match.dropna(subset=['exp_norm']).groupby('exp_norm')['kgs'].sum()
    kg_pera = float(kg_pm.get('pera', 0.0))
    kg_manzana = float(kg_pm.get('manzana', 0.0))

    print(f"   PERA: {kg_pera:,.0f} kg")
    print(f"   MANZANA: {kg_manzana:,.0f} kg")

    tiene_datos_pie = (kg_pera + kg_manzana) > 0
except Exception as e:
    print(f"   Advertencia: No se pudo cargar tabla Lvariedad - {str(e)}")
    kg_pera = 0
    kg_manzana = 0
    tiene_datos_pie = False

# Crear figura con 2 subplots
fig3 = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'bar'}, {'type': 'pie'}]],
    subplot_titles=('Top 10 Especies/Variedades por kg', 'Participación KG - PERA vs MANZANA<br><br><br><br><br><br><br><br><br><br>'),
    horizontal_spacing=0.2
)

# Gráfico 1: Barras horizontales Top 10
top_frutas_sorted = top_frutas.sort_values()
fig3.add_trace(
    go.Bar(
        y=top_frutas_sorted.index.tolist(),
        x=top_frutas_sorted.values,
        orientation='h',
        marker_color='steelblue',
        text=[f"{pct:.1f}%" for pct in top_participacion.loc[top_frutas_sorted.index].values],
        textposition='inside',  # Dentro de la barra
        textfont=dict(color='white', size=12),  # Texto blanco para contraste
        hovertemplate='<b>%{y}</b><br>Kilogramos: %{x:,.0f}<extra></extra>',
        showlegend=False
    ),
    row=1, col=1
)

# Gráfico 2: Pie PERA vs MANZANA
if tiene_datos_pie:
    fig3.add_trace(
        go.Pie(
            labels=['Pera', 'Manzana'],
            values=[kg_pera, kg_manzana],
            marker=dict(colors=['steelblue', 'orange']),
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Kilogramos: %{value:,.0f}<extra></extra>'
        ),
        row=1, col=2
    )
else:
    # Placeholder vacío
    fig3.add_trace(
        go.Pie(
            labels=['Sin datos'],
            values=[1],
            marker=dict(colors=['#cccccc']),
            showlegend=False
        ),
        row=1, col=2
    )

fig3.update_xaxes(
    title_text="Kilogramos (kg)",
    row=1, col=1
)
fig3.update_yaxes(title_text="Tipo de Fruta", row=1, col=1)

fig3.update_layout(
    title_text='Análisis por Especie y Variedad',
    showlegend=False,
    template='plotly_white',
    height=500,
    margin=dict(l=200, r=200, t=70, b=90),
    paper_bgcolor='rgb(190, 190, 190)',
    plot_bgcolor='rgb(190, 190, 190)',
    annotations=[
        dict(
            text="<b>Izquierda: Top 10 variedades más transportadas con su participación porcentual | Derecha: Distribución del volumen total entre Pera y Manzana</b>",
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor='center',
            align='center'
        )
    ]
)

fig3.write_html(TEMP3, config={'displayModeBar': False}, include_plotlyjs='cdn')
print("   OK Grafico 3 generado")

# ============================================================================
# ANÁLISIS 4: ORIGEN (Top 20 barras horizontales)
# ============================================================================

print("Generando Analisis 4: Origen...")

TOP_N_ORIGEN = 20

# Preparar datos
work_origen = df[['Origen', 'kgs']].copy()
work_origen['origen'] = work_origen['Origen'].astype(str).str.strip()
work_origen['kgs'] = pd.to_numeric(work_origen['kgs'], errors='coerce')

# KPIs por origen
kg_por_origen = work_origen.dropna(subset=['kgs']).groupby('origen')['kgs'].sum().sort_values(ascending=False)
total_kgs_origen = float(kg_por_origen.sum())
n_origenes = len(kg_por_origen)
participacion_origen = (kg_por_origen / total_kgs_origen * 100.0) if total_kgs_origen > 0 else kg_por_origen*0

# Top 20
top_origenes = kg_por_origen.head(TOP_N_ORIGEN)
top_participacion_origen = participacion_origen.loc[top_origenes.index]

# Dominante
dom_origen_label = kg_por_origen.index[0] if len(kg_por_origen) > 0 else None
dom_origen_kg = float(kg_por_origen.iloc[0]) if len(kg_por_origen) > 0 else 0
dom_origen_pct = float(participacion_origen.iloc[0]) if len(participacion_origen) > 0 else 0

print(f"   Total de origenes: {n_origenes}")
print(f"   Volumen total: {total_kgs_origen:,.0f} kg")
if dom_origen_label:
    print(f"   Origen dominante: {dom_origen_label} - {dom_origen_kg:,.0f} kg ({dom_origen_pct:.1f}%)")

# Crear gráfico de barras horizontales
fig4 = go.Figure()

top_origenes_sorted = top_origenes.sort_values()
fig4.add_trace(go.Bar(
    y=top_origenes_sorted.index.tolist(),
    x=top_origenes_sorted.values,
    orientation='h',
    marker_color='steelblue',
    text=[f"{pct:.1f}%" for pct in top_participacion_origen.loc[top_origenes_sorted.index].values],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Kilogramos: %{x:,.0f}<extra></extra>',
    showlegend=False
))

fig4.update_layout(
    title=f'Top {TOP_N_ORIGEN} orígenes por kg',
    xaxis_title='kg',
    yaxis_title='Origen',
    template='plotly_white',
    height=500,
    margin=dict(l=300, r=300, t=50, b=90),
    paper_bgcolor='rgb(190, 190, 190)',
    plot_bgcolor='rgb(190, 190, 190)',
    annotations=[
        dict(
            text="<b>Principales lugares de origen de la fruta transportada, ordenados por volumen de kilogramos. Los porcentajes muestran la participación de cada origen en el total.</b>",
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor='center',
            align='center'
        )
    ]
)

fig4.write_html(TEMP4, config={'displayModeBar': False}, include_plotlyjs='cdn')
print("   OK Grafico 4 generado")

# ============================================================================
# ANÁLISIS 5: TIPO DE CAMIÓN (% participación con nombres)
# ============================================================================

print("Generando Analisis 5: Tipo de Camion...")

# Preparar datos
truck_df = df[['TipoCamion', 'kgs', 'kms']].copy()
truck_df['TipoCamion'] = truck_df['TipoCamion'].astype(str).str.strip()
truck_df['kgs'] = pd.to_numeric(truck_df['kgs'], errors='coerce')
truck_df['kms'] = pd.to_numeric(truck_df['kms'], errors='coerce')

# Filtrar válidos
mask = truck_df['TipoCamion'].notna() & truck_df['TipoCamion'].ne('') & truck_df['kgs'].notna()
truck_df = truck_df.loc[mask]

# KPIs por tipo
kg_por_tipo = truck_df.groupby('TipoCamion')['kgs'].sum().sort_values(ascending=False)
total_kgs_tipo = float(kg_por_tipo.sum())
participacion_por_tipo = (100.0 * kg_por_tipo / total_kgs_tipo) if total_kgs_tipo > 0 else kg_por_tipo * 0

# Eficiencia
sum_km_tipo = truck_df.groupby('TipoCamion')['kms'].sum().reindex(kg_por_tipo.index)
eficiencia_ponderada_tipo = (kg_por_tipo / sum_km_tipo).replace([np.inf, -np.inf], np.nan)

n_tipos = len(kg_por_tipo)
tipo_dom_label = kg_por_tipo.index[0] if n_tipos > 0 else None
tipo_dom_kg = float(kg_por_tipo.iloc[0]) if n_tipos > 0 else 0
tipo_dom_pct = float(participacion_por_tipo.iloc[0]) if n_tipos > 0 else 0

# Cargar nombres de camiones desde Access
try:
    df_tipo_camion = cargar_tabla('LTipo_Camion')
    df_tipo_camion.columns = df_tipo_camion.columns.str.lower()
    cam_map = {str(row['codigo']).strip(): str(row['nombre']).strip()
               for _, row in df_tipo_camion[['codigo', 'nombre']].dropna().iterrows()}
    tiene_nombres = True
except Exception as e:
    print(f"   Advertencia: No se pudo cargar tabla LTipo_Camion - {str(e)}")
    cam_map = {}
    tiene_nombres = False

# Función para etiquetar con nombre
def _label_with_name(code):
    name = cam_map.get(str(code).strip())
    return f"{code} ({name})" if name else str(code)

print(f"   Tipos de camion: {n_tipos}")
print(f"   Volumen total: {total_kgs_tipo:,.0f} kg")
if tipo_dom_label:
    dom_name = cam_map.get(str(tipo_dom_label))
    dom_label_show = f"{tipo_dom_label} ({dom_name})" if dom_name else f"{tipo_dom_label}"
    print(f"   Tipo dominante: {dom_label_show} - {tipo_dom_kg:,.0f} kg ({tipo_dom_pct:.1f}%)")

if len(eficiencia_ponderada_tipo.dropna()):
    ef_max_label = eficiencia_ponderada_tipo.idxmax()
    ef_max_val = float(eficiencia_ponderada_tipo.max())
    ef_min_label = eficiencia_ponderada_tipo.idxmin()
    ef_min_val = float(eficiencia_ponderada_tipo.min())
    print(f"   Mejor eficiencia: {_label_with_name(ef_max_label)} - {ef_max_val:,.0f} kg/km")
    print(f"   Peor eficiencia: {_label_with_name(ef_min_label)} - {ef_min_val:,.0f} kg/km")

# Crear gráfico de barras horizontales con nombres
pct_ordered = participacion_por_tipo.sort_values()
pct_ordered_labels = [_label_with_name(idx) for idx in pct_ordered.index]

fig5 = go.Figure()

fig5.add_trace(go.Bar(
    y=pct_ordered_labels,
    x=pct_ordered.values,
    orientation='h',
    marker_color='steelblue',
    text=[f"{val:.1f}%" for val in pct_ordered.values],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Participación: %{x:.1f}%<extra></extra>',
    showlegend=False
))

fig5.update_layout(
    title='Participación por Tipo de Camión — % del total',
    xaxis_title='% del volumen total',
    yaxis_title='Tipo de Camión',
    template='plotly_white',
    height=500,
    margin=dict(l=200, r=200, t=50, b=90),
    paper_bgcolor='rgb(190, 190, 190)',
    plot_bgcolor='rgb(190, 190, 190)',
    annotations=[
        dict(
            text="<b>Distribución del volumen transportado según el tipo de camión utilizado. Los porcentajes indican qué proporción del total fue transportada por cada tipo.</b>",
            xref="paper", yref="paper",
            x=0.5, y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor='center',
            align='center'
        )
    ]
)

fig5.write_html(TEMP5, config={'displayModeBar': False}, include_plotlyjs='cdn')
print("   OK Grafico 5 generado")

# ============================================================================
# ANÁLISIS 6: PRODUCTOR/PROVEEDOR (Segmentación por volumen)
# ============================================================================

print("Generando Analisis 6: Productor...")

TOP_N_PROD = 20

# Umbrales de segmentación
UMBRAL_SEGMENTOS = {
    'Pequeño': (0, 100_000),
    'Mediano': (100_000, 500_000),
    'Grande': (500_000, 1_000_000),
    'Mega': (1_000_000, np.inf),
}

# Preparar datos
prod_df = df[['pro', 'kgs', 'NombreProveedor']].copy()
prod_df['kgs'] = pd.to_numeric(prod_df['kgs'], errors='coerce')
prod_df = prod_df.loc[prod_df['pro'].notna() & prod_df['kgs'].notna()]

# KPIs por productor
kg_por_prod = prod_df.groupby('pro')['kgs'].sum().sort_values(ascending=False)
total_kgs_prod = float(kg_por_prod.sum())
total_productores = len(kg_por_prod)
participacion_por_prod = (100.0 * kg_por_prod / total_kgs_prod) if total_kgs_prod > 0 else kg_por_prod * 0

# Pareto 80/20
cum_pct_prod = (kg_por_prod.cumsum() / total_kgs_prod * 100.0) if total_kgs_prod > 0 else kg_por_prod * 0
n_80_prod = int((cum_pct_prod <= 80).sum())
pct_productores_80 = (100.0 * n_80_prod / total_productores) if total_productores > 0 else 0

# Dominante
prod_dom_id = kg_por_prod.index[0] if total_productores > 0 else None
prod_dom_kg = float(kg_por_prod.iloc[0]) if total_productores > 0 else 0
prod_dom_pct = float(participacion_por_prod.iloc[0]) if total_productores > 0 else 0

# Obtener nombre del productor dominante
prod_dom_nom = None
if prod_dom_id is not None:
    nom_match = prod_df[prod_df['pro'] == prod_dom_id]['NombreProveedor'].dropna()
    if len(nom_match):
        prod_dom_nom = nom_match.iloc[0]

print(f"   Total productores: {total_productores}")
print(f"   Volumen total: {total_kgs_prod:,.0f} kg")
if prod_dom_id is not None:
    dom_txt = f"{prod_dom_id}"
    if prod_dom_nom:
        dom_txt += f" ({prod_dom_nom})"
    print(f"   Productor dominante: {dom_txt} - {prod_dom_kg:,.0f} kg ({prod_dom_pct:.1f}%)")
print(f"   Concentracion 80/20: {n_80_prod} productores ({pct_productores_80:.1f}%) alcanzan el 80% del volumen")

# Segmentación por volumen
def _segmento(kg):
    for seg, (lo, hi) in UMBRAL_SEGMENTOS.items():
        if (kg >= lo) and (kg < hi):
            return seg
    return 'Sin segmento'

segmento_por_prod = kg_por_prod.apply(_segmento)

segmentacion_df = (
    pd.DataFrame({
        'kg_total': kg_por_prod,
        'segmento': segmento_por_prod,
    })
    .groupby('segmento')
    .agg(kg_total=('kg_total', 'sum'), productores=('kg_total', 'count'))
    .sort_values('kg_total', ascending=False)
)

print(f"   Segmentos detectados: {len(segmentacion_df)}")

# Crear figura con 2 subplots (Pie + Barras)
fig6 = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'pie'}, {'type': 'bar'}]],
    subplot_titles=('Volumen por Segmento', 'Cantidad de Productores por Segmento'),
    horizontal_spacing=0.15
)

# Gráfico 1: Pie - Volumen por segmento
if len(segmentacion_df):
    fig6.add_trace(
        go.Pie(
            labels=segmentacion_df.index.tolist(),
            values=segmentacion_df['kg_total'].values,
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Kilogramos: %{value:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )

# Hacer la torta 10% más grande (dominio de 0.0-0.50 en lugar de 0.0-0.45)
fig6.update_xaxes(domain=[0.58, 0.95], row=1, col=2)
fig6.update_xaxes(domain=[0.0, 0.50], row=1, col=1)

# Gráfico 2: Barras - Cantidad de productores por segmento
if len(segmentacion_df):
    fig6.add_trace(
        go.Bar(
            x=segmentacion_df.index.tolist(),
            y=segmentacion_df['productores'].values,
            marker_color='steelblue',
            text=segmentacion_df['productores'].values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Productores: %{y}<extra></extra>',
            showlegend=False
        ),
        row=1, col=2
    )

fig6.update_xaxes(title_text="Segmento", row=1, col=2)
fig6.update_yaxes(title_text="productores", row=1, col=2)

fig6.update_layout(
    title_text='Segmentación de Productores por Volumen',
    showlegend=False,
    template='plotly_white',
    height=500,
    margin=dict(l=50, r=50, t=50, b=140),
    paper_bgcolor='rgb(190, 190, 190)',
    plot_bgcolor='rgb(190, 190, 190)',
    annotations=[
        dict(
            text="<b>Clasificación por volumen: Pequeño (0-100 mil kg) | Mediano (100-500 mil kg) | Grande (500 mil-1M kg) | Mega (>1M kg)<br>Izquierda: Porcentaje del volumen total que aporta cada segmento | Derecha: Cantidad de productores en cada segmento</b>",
            xref="paper", yref="paper",
            x=0.5, y=-0.35,
            showarrow=False,
            font=dict(size=12),
            xanchor='center',
            align='center'
        )
    ]
)

fig6.write_html(TEMP6, config={'displayModeBar': False}, include_plotlyjs='cdn')
print("   OK Grafico 6 generado")

# ============================================================================
# CALCULAR ESTADÍSTICAS GLOBALES
# ============================================================================

print()
print("Calculando estadisticas globales...")

total_kg = df['kgs'].sum()
total_bins = df['CantBins'].sum()
km_promedio = df['kms'].mean()
kg_por_bin = total_kg / total_bins if total_bins > 0 else 0
viajes_totales = len(df)
proveedores_unicos = df['pro'].nunique()

stats = {
    'total_kg': total_kg,
    'total_bins': int(total_bins),
    'kg_por_bin': round(kg_por_bin, 1),
    'viajes': viajes_totales
}

print(f"   Total KG: {total_kg:,.0f}")
print(f"   Total Bins: {total_bins:,.0f}")
print(f"   KM Promedio: {km_promedio:.1f}")
print(f"   KG por Bin: {kg_por_bin:.1f}")
print()

# ============================================================================
# GENERAR HTML PRINCIPAL
# ============================================================================

print("Generando pagina HTML principal...")

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis Logístico - Jugos S.A.</title>
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
        }}

        .header {{
            background: #1B5E4E;
            padding: 20px 25px;
            border-bottom: 2px solid #2ECC71;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}

        .header h1 {{
            font-size: 1.8em;
            color: #e0e0e0;
            font-weight: 600;
        }}

        .header .fecha {{
            font-size: 0.95em;
            margin-top: 5px;
            color: #b0b0b0;
        }}

        .kpis {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            padding: 20px;
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
        }}

        .kpi-subtitle {{
            font-size: 0.85em;
            color: #808080;
            margin-top: 5px;
        }}

        .charts-container {{
            padding: 0 20px 20px 20px;
        }}

        .chart-row {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .chart-full {{
            grid-column: 1 / -1;
        }}

        .chart-box {{
            background: #1B5E4E;
            border-radius: 4px;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        }}

        iframe {{
            width: 100%;
            border: none;
            display: block;
            overflow: hidden !important;
        }}

        /* Alturas específicas por gráfico */
        #grafico-1 {{
            height: 1021px;  /* Temporal (3 subgráficos) - reducido por toggle */
        }}

        #grafico-2 {{
            height: 517px;   /* Distancia */
        }}

        #grafico-3 {{
            height: 517px;   /* Especie/Variedad */
        }}

        #grafico-4 {{
            height: 517px;   /* Origen */
        }}

        #grafico-5 {{
            height: 517px;   /* Tipo de Camión */
        }}

        #grafico-6 {{
            height: 517px;   /* Productor */
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
        <h1>JUGOS S.A. - Análisis Logístico y Operacional</h1>
        <div class="fecha">Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
    </div>

    <!-- KPIs -->
    <div class="kpis">
        <div class="kpi-card">
            <div class="kpi-title">Cantidad de kg de fruta procesada</div>
            <div class="kpi-value">{format_number(stats['total_kg'], 0)}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-title">Total de cantidad de bins ingresados</div>
            <div class="kpi-value">{format_number(stats['total_bins'], 0)}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-title">Promedio de kilogramos por bin</div>
            <div class="kpi-value">{format_number(stats['kg_por_bin'], 1)}</div>
        </div>

        <div class="kpi-card">
            <div class="kpi-title">Cantidad de Ingresos Registrados</div>
            <div class="kpi-value">{format_number(stats['viajes'], 0)}</div>
        </div>
    </div>

    <!-- Gráficos -->
    <div class="charts-container">
        <!-- Fila 1: Temporal (full width) -->
        <div class="chart-row">
            <div class="chart-box chart-full">
                <iframe id="grafico-1" src="temp_logistica1.html?v={datetime.now().timestamp()}"></iframe>
            </div>
        </div>

        <!-- Fila 2: Distancia y Especie -->
        <div class="chart-row">
            <div class="chart-box">
                <iframe id="grafico-2" src="temp_logistica2.html?v={datetime.now().timestamp()}"></iframe>
            </div>
            <div class="chart-box">
                <iframe id="grafico-3" src="temp_logistica3.html?v={datetime.now().timestamp()}"></iframe>
            </div>
        </div>

        <!-- Fila 3: Origen y Camión -->
        <div class="chart-row">
            <div class="chart-box">
                <iframe id="grafico-4" src="temp_logistica4.html?v={datetime.now().timestamp()}"></iframe>
            </div>
            <div class="chart-box">
                <iframe id="grafico-5" src="temp_logistica5.html?v={datetime.now().timestamp()}"></iframe>
            </div>
        </div>

        <!-- Fila 4: Productor (full width) -->
        <div class="chart-row">
            <div class="chart-box chart-full">
                <iframe id="grafico-6" src="temp_logistica6.html?v={datetime.now().timestamp()}"></iframe>
            </div>
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
        // Auto-fullscreen
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

with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"   OK Pagina guardada en: {ARCHIVO_SALIDA}")
print()

# (Conexión ya cerrada por el módulo universal)
print()

print("="*70)
print("ANALISIS LOGISTICO GENERADO EXITOSAMENTE")
print("="*70)
print()
print("Archivos generados:")
print("   - logistica.html (pagina principal)")
print("   - temp_logistica1.html (grafico temporal)")
print("   - temp_logistica2.html (grafico distancia)")
print("   - temp_logistica3.html (grafico especie)")
print("   - temp_logistica4.html (grafico origen)")
print("   - temp_logistica5.html (grafico camion)")
print("   - temp_logistica6.html (grafico productor)")
print()
print("Para ver: Abre logistica.html en tu navegador")
print()
print("="*70)
