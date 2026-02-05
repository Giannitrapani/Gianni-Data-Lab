# ============================================================================
# GENERADOR DE PÁGINA INTERACTIVA DE PROVEEDORES - JUGOS S.A.
# ============================================================================

import pandas as pd
import json
from datetime import datetime
import platform
import os
from cargar_datos_universal import cargar_movimientos_bins

print("="*70)
print("GENERADOR DE PAGINA PROVEEDORES - JUGOS S.A.")
print("="*70)
print()

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Rutas RELATIVAS - funciona desde cualquier carpeta
script_dir = os.path.dirname(os.path.abspath(__file__))

if platform.system() == "Windows":
    ARCHIVO_ACCESS = os.path.join(script_dir, "datos_fuente", "VerDatosGaspar-local.accdb")
    ARCHIVO_SALIDA = os.path.join(script_dir, "proveedores.html")
else:
    # Docker/Linux
    ARCHIVO_ACCESS = "/app/datos_fuente/VerDatosGaspar-local.accdb"
    ARCHIVO_SALIDA = "/app/proveedores.html"

# ============================================================================
# CARGAR CONFIGURACIÓN DESDE config.json
# ============================================================================

# Cargar configuración desde archivo JSON
with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

# Parámetros del semáforo (cargados desde config.json)
MARGEN_STOCKEO = CONFIG['proveedores']['margen_stockeo_dias']
DIAS_SIN_DEVOLUCION = CONFIG['proveedores']['dias_sin_devolucion_alerta']
UMBRAL_VERDE = CONFIG['proveedores']['semaforo_deuda_verde']
UMBRAL_AMARILLO_MAX = CONFIG['proveedores']['semaforo_deuda_amarillo']
UMBRAL_ROJO = CONFIG['proveedores']['semaforo_deuda_amarillo']

print("Configuracion (cargada desde config.json):")
print(f"   Margen de stockeo: {MARGEN_STOCKEO} dias")
print(f"   Dias sin devolucion: {DIAS_SIN_DEVOLUCION} dias")
print(f"   Umbral verde: < {UMBRAL_VERDE}%")
print(f"   Umbral amarillo: {UMBRAL_VERDE}% - {UMBRAL_AMARILLO_MAX}%")
print(f"   Umbral rojo: > {UMBRAL_ROJO}%")
print()

# ============================================================================
# CARGAR DATOS (FUNCIONA EN WINDOWS Y DOCKER)
# ============================================================================

MOVIMIENTOS = cargar_movimientos_bins()
print()

# Convertir fechas
MOVIMIENTOS['FECHA_DIA'] = pd.to_datetime(MOVIMIENTOS['FECHA']).dt.date
MOVIMIENTOS['FECHA_DIA'] = pd.to_datetime(MOVIMIENTOS['FECHA_DIA'])

# Usar fecha actual del sistema
FECHA_HOY = pd.to_datetime(datetime.now().date())
FECHA_COSECHA = pd.to_datetime('03-04-2025', format='%d-%m-%Y')
FECHA_MAX_DATOS = MOVIMIENTOS['FECHA_DIA'].max()

print(f"Fecha de analisis (HOY): {FECHA_HOY.strftime('%d/%m/%Y')}")
print(f"Ultima fecha en datos: {FECHA_MAX_DATOS.strftime('%d/%m/%Y')}")
print()

# ============================================================================
# CALCULAR MÉTRICAS POR PRODUCTOR
# ============================================================================

print("Calculando metricas por productor...")

resultados = []
productores = MOVIMIENTOS['PROVEEDOR'].unique()

for proveedor in productores:
    df_prod = MOVIMIENTOS[MOVIMIENTOS['PROVEEDOR'] == proveedor].copy()

    nombre = df_prod['NOMBRE'].iloc[0]

    salidas_total = df_prod[df_prod['MOVIMIENTO'] == 'SALIDA']['CANTIDAD'].sum()
    entradas_total = df_prod[df_prod['MOVIMIENTO'] == 'ENTRADA']['CANTIDAD'].sum()
    deuda_actual = salidas_total - entradas_total

    if salidas_total > 0:
        deuda_relativa = (deuda_actual / salidas_total) * 100
        ratio_devolucion = (entradas_total / salidas_total) * 100
    else:
        deuda_relativa = 0
        ratio_devolucion = 0

    df_salidas = df_prod[df_prod['MOVIMIENTO'] == 'SALIDA']
    if len(df_salidas) > 0:
        fecha_primer_pedido = df_salidas['FECHA_DIA'].min()
        dias_desde_primer_pedido = (FECHA_HOY - fecha_primer_pedido).days
    else:
        fecha_primer_pedido = None
        dias_desde_primer_pedido = 0

    df_entradas = df_prod[df_prod['MOVIMIENTO'] == 'ENTRADA']
    if len(df_entradas) > 0:
        fecha_ultima_entrada = df_entradas['FECHA_DIA'].max()
        dias_sin_devolucion = (FECHA_HOY - fecha_ultima_entrada).days
    else:
        fecha_ultima_entrada = None
        dias_sin_devolucion = 999

    # Calcular ritmo de devolución (últimos 30 días)
    fecha_hace_30_dias = FECHA_HOY - pd.Timedelta(days=30)
    entradas_ultimos_30 = df_entradas[df_entradas['FECHA_DIA'] >= fecha_hace_30_dias]['CANTIDAD'].sum()
    ritmo_devolucion = entradas_ultimos_30 / 30  # bins por día

    # Calcular días estimados para saldar deuda (a ritmo actual)
    if ritmo_devolucion > 0 and deuda_actual > 0:
        dias_para_saldar = int(deuda_actual / ritmo_devolucion)
    else:
        dias_para_saldar = 9999 if deuda_actual > 0 else 0

    # Determinar si ritmo es preocupante
    # Consideramos "ritmo lento" si tardará más de 180 días en saldar
    ritmo_alerta = 'LENTO' if dias_para_saldar > 180 else 'NORMAL' if dias_para_saldar > 60 else 'RÁPIDO'

    # Determinar semáforo SOLO por % de deuda
    # Verde: < 20%, Amarillo: 20-40%, Rojo: > 40%
    if deuda_relativa < 20:
        semaforo = 'VERDE'
        razon = f'Deuda baja ({deuda_relativa:.1f}%)'
    elif deuda_relativa <= 40:
        semaforo = 'AMARILLO'
        razon = f'Deuda moderada ({deuda_relativa:.1f}%)'
    else:
        semaforo = 'ROJO'
        razon = f'Deuda alta ({deuda_relativa:.1f}%)'

    resultados.append({
        'proveedor': proveedor,
        'nombre': nombre,
        'salidas': int(salidas_total),
        'entradas': int(entradas_total),
        'deuda': int(deuda_actual),
        'deuda_pct': round(deuda_relativa, 1),
        'ratio_dev': round(ratio_devolucion, 1),
        'dias_sin_dev': int(dias_sin_devolucion),
        'ritmo_devolucion': round(ritmo_devolucion, 2),
        'dias_para_saldar': dias_para_saldar,
        'ritmo_alerta': ritmo_alerta,
        'semaforo': semaforo,
        'razon': razon
    })

df_productores = pd.DataFrame(resultados)

# Ordenar por semáforo y deuda
orden_semaforo = {'ROJO': 0, 'AMARILLO': 1, 'VERDE': 2}
df_productores['orden'] = df_productores['semaforo'].map(orden_semaforo)
df_productores = df_productores.sort_values(['orden', 'deuda_pct'], ascending=[True, False])

print(f"   OK Metricas calculadas para {len(df_productores):,} productores")
print()

conteo = df_productores['semaforo'].value_counts()
print(f"   Verde: {conteo.get('VERDE', 0)} productores")
print(f"   Amarillo: {conteo.get('AMARILLO', 0)} productores")
print(f"   Rojo: {conteo.get('ROJO', 0)} productores")
print()

# ============================================================================
# GENERAR HTML
# ============================================================================

print("Generando pagina HTML...")

# Convertir datos a JSON para JavaScript
datos_json = df_productores.to_dict('records')

html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proveedores - Jugos S.A.</title>
    <link rel="icon" type="image/png" href="favicon.png">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
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
            padding: 20px 25px;
            border-bottom: 2px solid #2ECC71;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
        }}

        .header-left {{
            flex: 1;
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

        .header-right {{
            flex: 0 0 400px;
        }}

        .search-container {{
            position: relative;
        }}

        #searchInput {{
            width: 100%;
            padding: 12px 40px 12px 15px;
            font-size: 1em;
            border: 2px solid #2C6E5D;
            border-radius: 4px;
            background: #0d3d2f;
            color: #e0e0e0;
            transition: all 0.3s;
        }}

        #searchInput:focus {{
            outline: none;
            border-color: #2ECC71;
            background: #1a1a1a;
        }}

        #searchInput::placeholder {{
            color: #808080;
        }}

        #clearSearch {{
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: #b0b0b0;
            font-size: 1.2em;
            cursor: pointer;
            padding: 5px;
            display: none;
        }}

        #clearSearch:hover {{
            color: #2ECC71;
        }}

        .autocomplete-dropdown {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            margin-top: 5px;
            background: #0d3d2f;
            border: 2px solid #2ECC71;
            border-radius: 4px;
            max-height: 300px;
            overflow-y: auto;
            z-index: 9999;
            display: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }}

        .autocomplete-item {{
            padding: 12px 15px;
            cursor: pointer;
            color: #e0e0e0;
            border-bottom: 1px solid #2C6E5D;
            transition: all 0.2s;
        }}

        .autocomplete-item:last-child {{
            border-bottom: none;
        }}

        .autocomplete-item:hover {{
            background: #1B5E4E;
            color: #2ECC71;
        }}

        .autocomplete-item .codigo {{
            font-weight: 600;
            color: #2ECC71;
        }}

        .autocomplete-item .nombre {{
            margin-left: 5px;
            color: #e0e0e0;
        }}

        .autocomplete-no-results {{
            padding: 12px 15px;
            color: #808080;
            text-align: center;
            font-style: italic;
        }}

        @media (max-width: 1200px) {{
            .header {{
                flex-direction: column;
                align-items: stretch;
            }}

            .header-right {{
                flex: 1;
                width: 100%;
            }}
        }}

        .container {{
            display: grid;
            grid-template-columns: 1fr 380px;
            gap: 15px;
            padding: 15px;
            max-width: 1920px;
            margin: 0 auto;
            height: calc(100vh - 170px);
        }}

        .grid-container {{
            background: #1B5E4E;
            border-radius: 4px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
            overflow-y: auto;
            height: 100%;
        }}

        .grid-title {{
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 12px;
            color: #e0e0e0;
        }}

        .proveedores-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 8px;
        }}

        .proveedor-card {{
            padding: 15px 10px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
            border: 2px solid transparent;
            text-align: center;
        }}

        .proveedor-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}

        .proveedor-card.selected {{
            border: 2px solid #0078D4;
            box-shadow: 0 4px 12px rgba(0,120,212,0.3);
        }}

        .proveedor-card.VERDE {{
            background: #d4edda;
            color: #155724;
        }}

        .proveedor-card.AMARILLO {{
            background: #fff3cd;
            color: #856404;
        }}

        .proveedor-card.ROJO {{
            background: #f8d7da;
            color: #721c24;
        }}

        .proveedor-nombre {{
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 5px;
            line-height: 1.2;
        }}

        .proveedor-deuda {{
            font-size: 1.3em;
            font-weight: 700;
        }}

        .panel-derecho {{
            background: #1B5E4E;
            border-radius: 4px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
            height: 100%;
            overflow-y: auto;
        }}

        .gauge-container {{
            margin-bottom: 15px;
        }}

        .detalles-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

        .detalle-titulo {{
            font-size: 0.9em;
            font-weight: 600;
            margin-bottom: 8px;
            color: #e0e0e0;
            grid-column: 1 / -1;
        }}

        .detalle-item {{
            margin-bottom: 6px;
            padding-bottom: 6px;
            border-bottom: 1px solid #2ECC71;
        }}

        .detalle-item:last-child {{
            border-bottom: none;
        }}

        .detalle-label {{
            font-size: 0.65em;
            color: #b0b0b0;
            text-transform: uppercase;
            margin-bottom: 2px;
            font-weight: 600;
        }}

        .detalle-valor {{
            font-size: 0.95em;
            font-weight: 700;
            color: #e0e0e0;
        }}

        .detalle-subtitulo {{
            font-size: 0.65em;
            color: #808080;
            margin-top: 1px;
        }}

        .semaforo-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            margin-top: 5px;
        }}

        .semaforo-badge.VERDE {{
            background: #28a745;
            color: white;
        }}

        .semaforo-badge.AMARILLO {{
            background: #ffc107;
            color: #e0e0e0;
        }}

        .semaforo-badge.ROJO {{
            background: #dc3545;
            color: white;
        }}

        .placeholder {{
            text-align: center;
            padding: 40px;
            color: #808080;
        }}

        .placeholder-icon {{
            font-size: 4em;
            margin-bottom: 10px;
        }}

        .footer {{
            background: #0d333d;
            color: #b0b0b0;
            padding: 8px 15px;
            text-align: center;
            font-size: 0.7em;
            border-top: 2px solid #2ECC71;
        }}

        .footer-title {{
            color: #e0e0e0;
            font-weight: 600;
            margin-bottom: 2px;
        }}

        .footer-subtitle {{
            color: #808080;
            font-size: 0.9em;
            margin-bottom: 4px;
        }}

        .footer-contact {{
            display: flex;
            justify-content: center;
            gap: 15px;
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
    </style>
</head>
<body>
    <div class="header">
        <div class="header-left">
            <h1>JUGOS S.A. - Análisis por Proveedor</h1>
            <div class="fecha">Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
        </div>
        <div class="header-right">
            <div class="search-container">
                <input
                    type="text"
                    id="searchInput"
                    placeholder="Buscar proveedor (código o nombre)..."
                    autocomplete="off"
                >
                <button id="clearSearch" onclick="limpiarBusqueda()">✕</button>
                <div id="autocompleteDropdown" class="autocomplete-dropdown"></div>
            </div>
        </div>
    </div>

    <div class="container">
        <!-- Grid de proveedores -->
        <div class="grid-container">
            <div class="grid-title">Proveedores ({len(df_productores)})</div>
            <div class="proveedores-grid" id="proveedoresGrid">
                <!-- Se llenará con JavaScript -->
            </div>
        </div>

        <!-- Panel derecho -->
        <div class="panel-derecho">
            <!-- Gauge -->
            <div class="gauge-container">
                <div id="gaugeChart"></div>
            </div>

            <!-- Detalles -->
            <div class="detalles-container" id="detallesContainer">
                <div class="placeholder">
                    <div class="placeholder-icon">📊</div>
                    <p>Selecciona un proveedor para ver sus detalles</p>
                </div>
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
        // Datos de proveedores
        const proveedores = {json.dumps(datos_json, ensure_ascii=False)};

        let proveedorSeleccionado = null;

        // Renderizar grid de proveedores
        function renderizarGrid() {{
            const grid = document.getElementById('proveedoresGrid');
            grid.innerHTML = '';

            proveedores.forEach((prov, index) => {{
                const card = document.createElement('div');
                card.className = `proveedor-card ${{prov.semaforo}}`;
                card.innerHTML = `
                    <div class="proveedor-nombre">${{prov.nombre}}</div>
                    <div class="proveedor-deuda">${{prov.deuda_pct}}%</div>
                `;
                card.onclick = () => seleccionarProveedor(index);
                grid.appendChild(card);
            }});
        }}

        // Seleccionar proveedor
        function seleccionarProveedor(index) {{
            proveedorSeleccionado = proveedores[index];

            // Actualizar selección visual
            document.querySelectorAll('.proveedor-card').forEach((card, i) => {{
                if (i === index) {{
                    card.classList.add('selected');
                }} else {{
                    card.classList.remove('selected');
                }}
            }});

            // Actualizar gauge
            actualizarGauge(proveedorSeleccionado.deuda_pct, proveedorSeleccionado.semaforo);

            // Actualizar detalles
            actualizarDetalles(proveedorSeleccionado);
        }}

        // Actualizar gauge
        function actualizarGauge(valor, semaforo) {{
            const data = [{{
                type: "indicator",
                mode: "gauge+number",
                value: valor,
                number: {{
                    suffix: "%",
                    font: {{ size: 36, color: "#333" }},
                    y: 0.45
                }},
                gauge: {{
                    axis: {{
                        range: [0, 100],
                        tickwidth: 2,
                        tickcolor: "#333",
                        tickmode: "linear",
                        tick0: 0,
                        dtick: 20,
                        visible: true
                    }},
                    bar: {{
                        color: "rgb(27, 61, 166)",
                        thickness: 0.15,
                        line: {{ color: "rgb(27, 61, 166)", width: 0 }}
                    }},
                    bgcolor: "rgb(190, 190, 190)",
                    borderwidth: 3,
                    bordercolor: "#333",
                    steps: [
                        {{ range: [0, {UMBRAL_VERDE}], color: "rgb(0, 126, 91)" }},
                        {{ range: [{UMBRAL_VERDE}, {UMBRAL_AMARILLO_MAX}], color: "rgb(255, 234, 0)" }},
                        {{ range: [{UMBRAL_AMARILLO_MAX}, 100], color: "rgb(150, 0, 0)" }}
                    ],
                    shape: "angular"
                }}
            }}];

            const layout = {{
                margin: {{ t: 40, r: 40, l: 40, b: 30 }},
                font: {{ family: "Segoe UI", size: 14 }},
                paper_bgcolor: "rgb(190, 190, 190)",
                height: 280,
                showlegend: false
            }};

            const config = {{ displayModeBar: false }};

            Plotly.newPlot('gaugeChart', data, layout, config);
        }}

        // Actualizar detalles
        function actualizarDetalles(prov) {{
            const container = document.getElementById('detallesContainer');

            container.innerHTML = `
                <div class="detalle-titulo">${{prov.nombre}}</div>

                <div class="detalle-item">
                    <div class="detalle-label">Estado</div>
                    <div><span class="semaforo-badge ${{prov.semaforo}}">${{prov.semaforo}}</span></div>
                    <div class="detalle-subtitulo">${{prov.razon}}</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">Código Proveedor</div>
                    <div class="detalle-valor">${{prov.proveedor}}</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">Bins Pedidos</div>
                    <div class="detalle-valor">${{prov.salidas.toLocaleString()}}</div>
                    <div class="detalle-subtitulo">Total de salidas</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">Bins Devueltos</div>
                    <div class="detalle-valor">${{prov.entradas.toLocaleString()}}</div>
                    <div class="detalle-subtitulo">Total de entradas</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">Bins Pendientes</div>
                    <div class="detalle-valor" style="color: ${{prov.deuda > 0 ? '#dc3545' : '#28a745'}}">${{prov.deuda.toLocaleString()}}</div>
                    <div class="detalle-subtitulo">Deuda actual</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">% Bins sin Devolver</div>
                    <div class="detalle-valor" style="color: ${{prov.deuda_pct > {UMBRAL_AMARILLO_MAX} ? '#dc3545' : prov.deuda_pct > {UMBRAL_VERDE} ? '#ffc107' : '#28a745'}}">${{prov.deuda_pct}}%</div>
                    <div class="detalle-subtitulo">Deuda relativa</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">% Bins Devueltos</div>
                    <div class="detalle-valor">${{prov.ratio_dev}}%</div>
                    <div class="detalle-subtitulo">Ratio de devolución</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">Días sin Devolución</div>
                    <div class="detalle-valor" style="color: ${{prov.dias_sin_dev > {DIAS_SIN_DEVOLUCION} ? '#dc3545' : '#28a745'}}">${{prov.dias_sin_dev}}</div>
                    <div class="detalle-subtitulo">Desde última entrada</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">Ritmo de Devolución</div>
                    <div class="detalle-valor">${{prov.ritmo_devolucion.toFixed(2)}} bins/día</div>
                    <div class="detalle-subtitulo">Promedio últimos 30 días</div>
                </div>

                <div class="detalle-item">
                    <div class="detalle-label">Tiempo para Saldar</div>
                    <div class="detalle-valor" style="color: ${{prov.dias_para_saldar > 180 ? '#dc3545' : prov.dias_para_saldar > 60 ? '#ffc107' : '#28a745'}}">
                        ${{prov.dias_para_saldar === 9999 ? '∞' : prov.dias_para_saldar === 0 ? 'N/A' : prov.dias_para_saldar + ' días'}}
                    </div>
                    <div class="detalle-subtitulo">A ritmo actual (${{prov.ritmo_alerta}})</div>
                </div>
            `;
        }}

        // ============================================================
        // FUNCIONALIDAD DE BÚSQUEDA CON AUTOCOMPLETADO
        // ============================================================

        const searchInput = document.getElementById('searchInput');
        const clearBtn = document.getElementById('clearSearch');
        const dropdown = document.getElementById('autocompleteDropdown');

        // Mostrar/ocultar botón de limpiar
        searchInput.addEventListener('input', function() {{
            if (this.value.trim() !== '') {{
                clearBtn.style.display = 'block';
                mostrarAutocompletado(this.value);
            }} else {{
                clearBtn.style.display = 'none';
                ocultarDropdown();
            }}
        }});

        // Función para mostrar autocompletado
        function mostrarAutocompletado(texto) {{
            const filtro = texto.toLowerCase().trim();

            if (filtro === '') {{
                ocultarDropdown();
                return;
            }}

            // Filtrar proveedores que coincidan
            const coincidencias = proveedores.filter((prov, index) => {{
                const codigo = String(prov.proveedor || '').toLowerCase();
                const nombre = String(prov.nombre || '').toLowerCase();
                return codigo.includes(filtro) || nombre.includes(filtro);
            }});

            // Mostrar resultados
            if (coincidencias.length > 0) {{
                dropdown.innerHTML = '';

                // Limitar a 10 resultados
                const resultados = coincidencias.slice(0, 10);

                resultados.forEach(prov => {{
                    const item = document.createElement('div');
                    item.className = 'autocomplete-item';
                    item.innerHTML = `
                        <span class="codigo">${{prov.proveedor}}</span>
                        <span class="nombre">- ${{prov.nombre}}</span>
                    `;

                    // Click en item
                    item.onclick = function() {{
                        seleccionarProveedorPorCodigo(prov.proveedor);
                        searchInput.value = `${{prov.proveedor}} - ${{prov.nombre}}`;
                        ocultarDropdown();
                    }};

                    dropdown.appendChild(item);
                }});

                // Mostrar mensaje si hay más resultados
                if (coincidencias.length > 10) {{
                    const moreItem = document.createElement('div');
                    moreItem.className = 'autocomplete-no-results';
                    moreItem.textContent = `... y ${{coincidencias.length - 10}} más resultados`;
                    dropdown.appendChild(moreItem);
                }}

                dropdown.style.display = 'block';
            }} else {{
                // Sin resultados
                dropdown.innerHTML = '<div class="autocomplete-no-results">No se encontraron proveedores</div>';
                dropdown.style.display = 'block';
            }}
        }}

        // Función para ocultar dropdown
        function ocultarDropdown() {{
            dropdown.style.display = 'none';
        }}

        // Función para limpiar búsqueda
        function limpiarBusqueda() {{
            searchInput.value = '';
            clearBtn.style.display = 'none';
            ocultarDropdown();
            searchInput.focus();
        }}

        // Seleccionar proveedor por código
        function seleccionarProveedorPorCodigo(codigo) {{
            const index = proveedores.findIndex(p => p.proveedor === codigo);
            if (index !== -1) {{
                seleccionarProveedor(index);

                // Scroll hacia la tarjeta seleccionada
                const cards = document.querySelectorAll('.proveedor-card');
                if (cards[index]) {{
                    cards[index].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                }}
            }}
        }}

        // Cerrar dropdown al hacer click fuera
        document.addEventListener('click', function(e) {{
            if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {{
                ocultarDropdown();
            }}
        }});

        // Atajo de teclado: Ctrl+F para enfocar búsqueda
        document.addEventListener('keydown', function(e) {{
            if (e.ctrlKey && e.key === 'f') {{
                e.preventDefault();
                searchInput.focus();
            }}

            // Enter en búsqueda: seleccionar primer resultado
            if (e.key === 'Enter' && document.activeElement === searchInput) {{
                const firstItem = dropdown.querySelector('.autocomplete-item');
                if (firstItem) {{
                    firstItem.click();
                }}
            }}

            // Escape: cerrar dropdown
            if (e.key === 'Escape') {{
                ocultarDropdown();
                searchInput.blur();
            }}
        }});

        // Inicializar
        renderizarGrid();

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

# Guardar archivo
with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"   OK Pagina guardada en: {ARCHIVO_SALIDA}")
print()

print("="*70)
print("PAGINA GENERADA EXITOSAMENTE")
print("="*70)
print()
print(f"Estadisticas:")
print(f"   - Total proveedores: {len(df_productores):,}")
print(f"   - Verde: {conteo.get('VERDE', 0):,}")
print(f"   - Amarillo: {conteo.get('AMARILLO', 0):,}")
print(f"   - Rojo: {conteo.get('ROJO', 0):,}")
print()

# (Conexión ya cerrada por el módulo universal)
print()

print("Para ver:")
print("   Abre proveedores.html en tu navegador")
print()
print("="*70)
