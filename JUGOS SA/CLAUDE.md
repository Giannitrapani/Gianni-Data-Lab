# Sistema de Dashboards - JUGOS S.A.

## ÚLTIMA SESIÓN: 16 de Enero 2026

### Resumen de lo trabajado:
1. **PROBLEMA PRINCIPAL RESUELTO**: Los cambios en Access no se reflejaban en los dashboards
   - **Causa**: El sistema leía de TABLAS ESTÁTICAS (`TBL_Lbascular_formato_final`, `TBL_basculae_formato_final`)
   - **Solución**: Cambiar a QUERIES DINÁMICOS (`10_qry_Lbascular_formato_final`, `11_qry_basculae_formato_final`)

2. **Archivos modificados**:
   - `cargar_datos_universal.py` - Usa queries dinámicos
   - `ACTUALIZAR_CSV.py` - Usa queries dinámicos
   - `generar_dashboard.py` - Eliminado toggle de ajuste, corregido encoding
   - `generar_analisis_logistico.py` - Eliminado toggle de ajuste, corregido encoding

3. **Scripts creados**:
   - `INSTALAR_REQUISITOS.bat` - Instala Python, librerías, Node.js y Claude Code
   - `VERIFICAR_INSTALACION.bat` - Verifica que todo esté instalado

4. **Toggle de ajuste eliminado**: El usuario prefirió que los gráficos muestren el rango fijo enero-diciembre

5. **Flujo de trabajo confirmado**:
   - `ELEGIR_BASE_DATOS.bat` → Selecciona archivo Access
   - Editar datos en Access (Lbascular, Lbasculae, IngresosConKm)
   - `INICIAR_SISTEMA.bat` → Ver cambios reflejados en dashboard

---

## Configuración Actual (PC del Usuario)

```
Python: 3.12.7 (Anaconda) 64-bit
ODBC: Microsoft Access Driver (*.mdb, *.accdb) 64-bit
Node.js: v18.19.0
```

**IMPORTANTE**: Python y ODBC deben ser de la misma arquitectura (ambos 64-bit o ambos 32-bit)

---

## Requisitos para Despliegue en Empresa

### Descargas necesarias:
| Programa | Versión | Link |
|----------|---------|------|
| Python | 3.12.7 (64-bit) | https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe |
| Access Database Engine | 64-bit | https://www.microsoft.com/en-us/download/details.aspx?id=54920 |
| Node.js (opcional) | LTS 64-bit | https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi |

### Librerías Python:
```bash
pip install pandas pyodbc plotly
```

### Pasos de instalación:
1. Copiar carpeta JUGOS-CLAUDE a la PC
2. Ejecutar `INSTALAR_REQUISITOS.bat` (como administrador)
3. Ejecutar `VERIFICAR_INSTALACION.bat` para confirmar
4. Ejecutar `ELEGIR_BASE_DATOS.bat` y seleccionar la base de red
5. Ejecutar `INICIAR_SISTEMA.bat`

---

## Queries Dinámicos (CRÍTICO)

La base de datos Access DEBE tener estos queries para que el sistema funcione:

| Query | Lee de | Propósito |
|-------|--------|-----------|
| `10_qry_Lbascular_formato_final` | Lbascular | Movimientos de bins (formato final) |
| `11_qry_basculae_formato_final` | Lbasculae | Datos de báscula (formato final) |

**Sin estos queries, los cambios en las tablas base NO se reflejan en los dashboards.**

---

## Resumen del Proyecto

Sistema de visualización de datos con dashboards interactivos para JUGOS S.A. que lee datos desde Access, genera gráficos con Plotly, y se actualiza automáticamente.

## Características Principales

- **Auto-adaptativo**: Detecta automáticamente Python y ODBC disponibles
- **Portable**: Funciona desde pendrive, red, o local
- **Compatible**: Python x32/x64, ODBC x32/x64, Windows 7-11
- **Sin permisos admin**: Funciona con usuario común

## Arquitectura del Sistema

### Base de Datos
- **Fuente**: Access (.accdb) - seleccionable con `ELEGIR_BASE_DATOS.bat`
- **Queries dinámicos** (USAR ESTOS):
  - `10_qry_Lbascular_formato_final` - Movimientos de bins
  - `11_qry_basculae_formato_final` - Datos de báscula
- **Tablas de referencia**:
  - `IngresosConKm` - Ingresos con kilómetros
  - `LProveedor` - Lista de proveedores
  - `Lvariedad` - Variedades de productos
  - `LTipo_Camion` - Tipos de camiones

### Flujo de Datos

```
ELEGIR_BASE_DATOS.bat → Guarda ruta en config.json
                              ↓
INICIAR_SISTEMA.bat → ACTUALIZAR_CSV.py → Lee queries dinámicos → CSV
                              ↓
              actualizar_dashboard_completo.py → HTML Dashboards
                              ↓
                    Abre dashboard_completo.html
```

## Archivos Principales

### Ejecución
- **ELEGIR_BASE_DATOS.bat** - Selecciona archivo Access a usar
- **INICIAR_SISTEMA.bat** - Inicia todo el sistema
- **INSTALAR_REQUISITOS.bat** - Instala todo lo necesario
- **VERIFICAR_INSTALACION.bat** - Verifica que todo esté instalado

### Generadores Python
- **actualizar_dashboard_completo.py** - Orquestador maestro
- **generar_dashboard.py** - Dashboard Stock Global
- **generar_pagina_proveedores.py** - Página Proveedores
- **generar_analisis_logistico.py** - Análisis Logístico
- **ACTUALIZAR_CSV.py** - Lee Access, genera CSV
- **cargar_datos_universal.py** - Cargador universal de datos

### HTML Generados
- **dashboard_completo.html** - Página principal con 3 pestañas
- **dashboard.html** - Stock Global
- **proveedores.html** - Análisis por Proveedor
- **logistica.html** - Análisis Logístico

### Configuración
- **config.json** - Configuración general (incluye ruta de base de datos)

## Dashboards Generados

### 1. Stock Global (dashboard.html)
- Distribución Total de Bins (áreas apiladas)
- Evolución Individual por Categoría
- KPIs: Bins vacíos, tendencia, días hasta advertencia/crítico
- Rango fijo: Enero a Diciembre del año de datos

### 2. Proveedores (proveedores.html)
- Cuadrícula interactiva con todos los proveedores
- Sistema de semáforo (verde/amarillo/rojo)
- Métricas por proveedor: deuda, bins, días sin devolución
- Filtros y búsqueda

### 3. Logística (logistica.html)
- Análisis temporal (KG diario, semanal, mensual)
- Análisis por distancia
- Análisis por especies/variedad
- Análisis por origen
- Análisis por tipo de camión
- Análisis por productor

## Configuración (config.json)

```json
{
  "sistema": {
    "nombre_empresa": "JUGOS S.A.",
    "ruta_base_datos": "auto",
    "comentario_ruta": "Usar 'auto' para detectar automáticamente o ruta completa"
  },
  "bins": {
    "total_bins": 30000,
    "umbral_critico": 5000,
    "umbral_advertencia": 8000
  },
  "proveedores": {
    "semaforo_deuda_verde": 20,
    "semaforo_deuda_amarillo": 40,
    "margen_stockeo_dias": 0,
    "dias_sin_devolucion_alerta": 14
  }
}
```

## Troubleshooting

### Los cambios en Access no se reflejan
1. Verificar que la base tenga los queries `10_qry_Lbascular_formato_final` y `11_qry_basculae_formato_final`
2. Ejecutar `INICIAR_SISTEMA.bat` después de hacer cambios
3. Si persiste, ejecutar `VERIFICAR_INSTALACION.bat`

### Error de conexión ODBC
- Verificar que Python y ODBC sean de la misma arquitectura (ambos 64-bit o ambos 32-bit)
- Ejecutar `VERIFICAR_INSTALACION.bat` para ver el estado

### Error "No se encuentra el archivo"
- Ejecutar `ELEGIR_BASE_DATOS.bat` para seleccionar la base correcta

## Librerías Python Requeridas

```bash
pip install pandas pyodbc plotly
```

## Estructura de Carpetas

```
JUGOS-CLAUDE/
├── datos_fuente/
│   └── VerDatosGaspar-local.accdb (Access DB local)
├── datos_csv/
│   ├── TBL_Lbascular_formato_final.csv
│   ├── TBL_basculae_formato_final.csv
│   ├── IngresosConKm.csv
│   ├── LProveedor.csv
│   ├── Lvariedad.csv
│   └── LTipo_Camion.csv
├── *.py (scripts Python)
├── *.bat (scripts Windows)
├── *.html (dashboards generados)
├── config.json
└── CLAUDE.md (este archivo)
```

## Notas Importantes

1. **SIEMPRE usar queries dinámicos**: Los queries `10_qry_*` y `11_qry_*` leen de las tablas base y se actualizan automáticamente
2. **Python y ODBC misma arquitectura**: Si usas Python 64-bit, necesitas ODBC 64-bit
3. **Después de editar Access**: Ejecutar `INICIAR_SISTEMA.bat` para ver cambios
4. **Base de datos en red**: Funciona igual, solo elegir con `ELEGIR_BASE_DATOS.bat`

---

## Historial de Cambios

### Versión 3.1 (16 Enero 2026)
- Corregido: Uso de queries dinámicos en lugar de tablas estáticas
- Eliminado: Toggle de ajuste automático (causaba problemas de encoding)
- Agregado: `INSTALAR_REQUISITOS.bat` para instalación automática
- Agregado: `VERIFICAR_INSTALACION.bat` para diagnóstico
- Corregido: Encoding de caracteres especiales (ñ → ni)

### Versión 3.0
- Sistema auto-adaptativo
- Detección automática de Python/ODBC
- Fallback a CSV

---

**Sistema listo para producción.**
**Última actualización: 16 de Enero 2026**
