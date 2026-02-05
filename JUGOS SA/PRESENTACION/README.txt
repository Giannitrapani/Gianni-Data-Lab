================================================================================
PRESENTACION GERENCIA - SISTEMA DASHBOARDS JUGOS S.A.
================================================================================

CONTENIDO DE ESTA CARPETA:

1. presentacion_gerencia.html
   - Presentación interactiva con efecto Prezi
   - Se abre en cualquier navegador (Chrome, Firefox, Edge)
   - Navegación con teclado y mouse

2. estructura_presentacion.txt
   - Archivo editable con toda la jerarquía de contenido
   - Modificar este archivo y avisar a Claude para regenerar el HTML

3. README.txt
   - Este archivo (instrucciones de uso)

================================================================================
COMO USAR LA PRESENTACION
================================================================================

PASO 1: ABRIR LA PRESENTACION
------------------------------
- Hacer doble clic en "presentacion_gerencia.html"
- Se abrirá en tu navegador predeterminado
- Presionar F11 para pantalla completa (recomendado)

PASO 2: NAVEGAR
---------------
Hay 3 formas de navegar:

A) BOTONES EN PANTALLA (margen derecho inferior):
   - "▲" - Siguiente slide
   - "⌂" - Volver a portada
   - "▼" - Slide anterior

B) TECLADO (más rápido - RECOMENDADO):
   - Flecha Derecha (→) o ESPACIO - Siguiente slide
   - Flecha Izquierda (←) - Slide anterior
   - ESC - Volver a la portada
   - F11 - Pantalla completa

NOTA: Solo se ve UN slide a la vez (pantalla completa).
Los demás slides están ocultos para evitar distracciones.

AYUDA DE TECLADO:
- Se muestra automáticamente al inicio (5 segundos)
- Luego desaparece para no distraer
- Para verla nuevamente: Pasa el mouse por la esquina superior derecha

PASO 3: ESTRUCTURA DE LA PRESENTACION
--------------------------------------
Total: 19 slides organizados en 4 niveles

NIVEL 0 - Portada (Slide 1)
    └─ Idea central del sistema

NIVEL 1 - Secciones principales (Slides 2, 10, 12)
    ├─ Stock Global
    ├─ Proveedores
    └─ Logística

NIVEL 2 - Subsecciones (Slides 3-9, 11, 13-18)
    ├─ Stock Global (6 subsecciones)
    │   ├─ KPI 1: Bins Vacíos
    │   ├─ KPI 2: Tendencia
    │   ├─ KPI 3: Días Advertencia
    │   ├─ KPI 4: Días Crítico
    │   ├─ Gráfico 1: Áreas Apiladas
    │   └─ Gráfico 2: Líneas Individuales
    ├─ Proveedores (1 subsección)
    │   └─ Sistema Semáforo
    └─ Logística (6 subsecciones)
        ├─ Análisis Temporal
        ├─ Análisis por Distancia
        ├─ Top 10 Especies
        ├─ Análisis por Origen
        ├─ Tipo de Camión
        └─ Análisis Complementario

NIVEL 3 - Conclusiones (Slide 19)
    └─ ROI y valor generado

================================================================================
ORDEN RECOMENDADO PARA PRESENTAR
================================================================================

1. Slide 1: PORTADA
   - Presentar problema y valor generado
   - Tiempo: 2 minutos

2. Slide 2: STOCK GLOBAL (vista general)
   - Explicar objetivo del dashboard
   - Tiempo: 1 minuto

3. Slides 3-8: DETALLES STOCK GLOBAL
   - Ir KPI por KPI explicando fórmulas
   - Mostrar gráficos
   - Tiempo: 10 minutos (2 min por KPI/gráfico)

4. Slide 9: PROVEEDORES (vista general)
   - Explicar objetivo del dashboard
   - Tiempo: 1 minuto

5. Slide 10: SISTEMA SEMAFORO
   - Explicar lógica de colores
   - Tiempo: 3 minutos

6. Slide 11: LOGISTICA (vista general)
   - Explicar objetivo del dashboard
   - Tiempo: 1 minuto

7. Slide 12: ANALISIS TEMPORAL
   - Explicar métricas
   - Tiempo: 3 minutos

8. Slide 13: CONCLUSIONES Y ROI
   - Cerrar con valor generado
   - Tiempo: 3 minutos

TIEMPO TOTAL: ~25 minutos

================================================================================
AGREGAR CAPTURAS DE PANTALLA
================================================================================

IMPORTANTE: La presentación tiene placeholders para capturas de pantalla.

Para agregar las capturas:

1. Tomar screenshots de los dashboards reales
2. Guardarlas en esta carpeta PRESENTACION con estos nombres:
   - dashboard_stock_completo.png
   - kpi_bins_vacios.png
   - kpi_tendencia.png
   - kpi_dias_advertencia.png
   - kpi_dias_critico.png
   - grafico_areas_apiladas.png
   - grafico_lineas_individuales.png
   - dashboard_proveedores_completo.png
   - cuadricula_proveedores.png
   - dashboard_logistica_completo.png
   - analisis_temporal.png

3. Avisar a Claude: "Integrar capturas de pantalla en presentacion_gerencia.html"

================================================================================
EDITAR CONTENIDO
================================================================================

Para modificar el contenido de la presentación:

1. Abrir "estructura_presentacion.txt"
2. Editar el contenido que necesites cambiar
3. Guardar el archivo
4. Avisar a Claude: "Regenerar presentacion_gerencia.html desde estructura_presentacion.txt"
5. Claude generará el nuevo HTML automáticamente

EJEMPLOS DE EDICIONES:
- Cambiar fórmulas si se actualizan en el código
- Modificar umbrales (ej: cambiar 8,000 a 10,000)
- Agregar nuevas subsecciones
- Actualizar precios/valores de ROI

================================================================================
CONSEJOS PARA LA PRESENTACION
================================================================================

ANTES DE PRESENTAR:
-------------------
✓ Probar la presentación al menos 1 vez completa
✓ Verificar que todas las capturas estén cargadas
✓ Conectar la laptop al proyector/TV
✓ Configurar resolución de pantalla adecuada
✓ Cerrar otras aplicaciones para mejor rendimiento
✓ Tener el sistema real abierto en otra ventana (por si preguntan)

DURANTE LA PRESENTACION:
------------------------
✓ Usar pantalla completa (F11)
✓ Navegar con flechas del teclado (más profesional)
✓ Pausar en cada slide el tiempo necesario
✓ No apurarse en las fórmulas (son importantes)
✓ Mostrar el sistema real si preguntan detalles

TIPS:
-----
• Si pierdes el rumbo: Presiona ESC para volver al inicio
• Los slides tienen hover effect (brillan al pasar mouse)
• El indicador muestra en qué slide estás (arriba izquierda)
• Los botones de navegación siempre están visibles

================================================================================
ESTILO Y COLORES
================================================================================

La presentación usa los mismos colores del sistema:

- Fondo: #0a0a0a (negro)
- Tarjetas: #1B5E4E (verde oscuro)
- Bordes: #2ECC71 (verde brillante)
- Texto principal: #e0e0e0 (gris claro)
- Acentos: #F39C12 (naranja), #3498DB (azul)
- Fuente: Segoe UI (igual que los dashboards)

Esto crea continuidad visual entre la presentación y el sistema real.

================================================================================
RESOLUCION DE PROBLEMAS
================================================================================

PROBLEMA: No se ve bien en pantalla completa
SOLUCION: Ajustar zoom del navegador (Ctrl + / Ctrl -)

PROBLEMA: Los slides están muy cerca/lejos
SOLUCION: Editar el HTML, buscar "scale:" y ajustar valores

PROBLEMA: No navega con teclado
SOLUCION: Click en la página primero para dar foco

PROBLEMA: Se ve cortado en proyector
SOLUCION: Configurar resolución 1920x1080 o inferior

================================================================================
CONTACTO
================================================================================

Para modificaciones o consultas:
- Avisar a Claude Code con los cambios deseados
- Claude regenerará automáticamente el HTML

Desarrollado por: Gaspar Giannitrapani
Email: giannitrapanigaspar@gmail.com
Teléfono: +54 9 298 470-4091

================================================================================
FIN
================================================================================
