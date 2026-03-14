# CONTEXTO DEL PROYECTO - DASHBOARD HIDROCARBUROS CUENCA NEUQUINA

## QUIEN SOY

Soy Gianni Trapani. Tecnico Superior en Ciencias de Datos, recien egresado.
Vivo en General Roca, Rio Negro, Argentina. Zona de la Cuenca Neuquina.
Mi unico proyecto en produccion hasta ahora es el Dashboard de Jugos S.A.
Este es mi segundo proyecto y apunta directamente a empresas petroleras como YPF,
Vista Energy, Pampa Energia, Tecpetrol.

---

## OBJETIVO DEL PROYECTO

Construir un dashboard de analisis de produccion de hidrocarburos de la Cuenca Neuquina
que demuestre tres capacidades especificas:

1. INTEGRACION DE DATOS: cruzar multiples datasets de distintas fuentes mediante claves comunes.
2. ANALITICA PRESCRIPTIVA: no solo mostrar graficos, sino deducir que accion tomar
   en base a los datos. Igual a lo que hice en Jugos S.A. con el umbral critico de bins
   y la lista de deudores.
3. USO DE API EN TIEMPO REAL: los datos se actualizan solos desde la fuente oficial,
   sin descargar archivos a mano.

---

## POR QUE ESTO ME DIFERENCIA

En Jugos S.A. conecte varias bases de Access que no tenian relacion explicita.
Encontre las claves de join a ojo. Calcule pagos cruzando distancia + tipo de camion + kg.
Y deduci que cuando el stock de bins cae, hay que ir a buscar a los que mas bins adeudan.
Esa logica no estaba en los datos. La puse yo.

En este proyecto hago lo mismo pero con datos reales del sector que quiero trabajar.

---

## FUENTE DE DATOS: API OFICIAL DEL MINISTERIO DE ENERGIA

Base URL: http://datos.energia.gob.ar/api/3/action/datastore_search

Todos los datos son publicos, gratuitos y oficiales. Se acceden por API sin autenticacion.

### DATASET 1 - Produccion por pozo (PRINCIPAL)
- Nombre: Produccion de petroleo y gas por pozo (Capitulo IV)
- Resource ID: 876b3746-85e2-4039-adeb-b1354436159f
- Contenido: produccion mensual de cada pozo (petroleo m3, gas miles m3, agua m3)
- Columnas clave: idpozo, sigla, empresa, anio, mes, prod_pet, prod_gas, prod_agua,
  formacion, areayacimiento, cuenca, provincia, tipo_de_recurso, sub_tipo_recurso
- Actualizacion: mensual

### DATASET 2 - Fractura hidraulica (VACA MUERTA)
- Nombre: Datos de fractura de pozos de hidrocarburos (Adjunto IV)
- Resource ID: 2280ad92-6ed3-403e-a095-50139863ab0d
- Contenido: datos de completacion de cada pozo (etapas de fractura, arena, agua inyectada)
- Columnas clave: idpozo, sigla, empresa, longitud_rama_horizontal_m,
  cantidad_etapas, arena_total_tn, agua_inyectada_m3, fecha_inicio, fecha_fin
- Actualizacion: diaria

### DATASET 3 - Perforacion de pozos
- Nombre: Perforacion de pozos de petroleo y gas
- URL dataset: http://datos.energia.gob.ar/dataset/perforacion-de-pozos-de-petroleo-y-gas
- Contenido: pozos terminados por mes, empresa, cuenca, metros perforados
- Actualizacion: mensual

### DATASET 4 - Estado de pozos
- Contenido: si cada pozo esta activo, inactivo o abandonado
- Actualizacion: mensual

### DATASET 5 - Inversiones upstream
- Nombre: Inversiones mercado de hidrocarburos upstream
- URL dataset: http://datos.energia.gob.ar/dataset/energia-inversiones-mercado-hidrocarburos-upstream
- Contenido: inversion por empresa y trimestre
- Actualizacion: mensual

---

## CLAVES DE JOIN ENTRE DATASETS

- idpozo: une produccion <-> fractura <-> estado de pozos
- sigla: identifica el pozo fisico (un pozo puede tener varios idpozo si produce de varias formaciones)
- empresa: une todos los datasets con inversiones
- cuenca + provincia: dimension geografica presente en todos

IMPORTANTE: idpozo no identifica un pozo fisico unico.
Para contar pozos fisicos hay que usar sigla.

---

## ANALITICA PRESCRIPTIVA PLANEADA

Equivalente al semaforo de bins de Jugos S.A., este dashboard debe responder:

EJEMPLO 1: Cuando la produccion de un pozo cae mas del 30% respecto a su pico historico
y el pozo figura como activo pero no tiene fracturas recientes ->
ese pozo es candidato a workover. Accion prescripta: intervenir el pozo.

EJEMPLO 2: Cuando la inversion de una empresa sube un trimestre pero la produccion
del siguiente trimestre no crece proporcionalmente ->
esa empresa tiene ineficiencia operativa. Identificar cuales son esos pozos.

EJEMPLO 3: Correlacion entre cantidad de etapas de fractura y productividad inicial.
Determinar el rango optimo de etapas para maximizar produccion.

---

## TECNOLOGIAS Y ARQUITECTURA

- Exploracion: Jupyter Notebook (notebooks/)
- Procesamiento: Python + pandas + requests + numpy
- Visualizacion: HTML + Bootstrap 5 + Plotly.js
- Datos: API en tiempo real (no CSV estaticos)
- Publicacion: GitHub Pages
- URL final: giannitrapani.github.io/Gianni-Data-Lab/HIDROCARBUROS/dashboard/dashboard.html

El dashboard llama a la API cada vez que se abre. Los datos siempre son los mas actuales.

---

## ESTRUCTURA DE CARPETAS

```
HIDROCARBUROS/
├── CLAUDE.md          <- instrucciones para Claude (leer siempre primero)
├── CONTEXTO.md        <- este archivo
├── PROGRESO.md        <- registro de avance (actualizar en cada sesion)
├── datos/             <- archivos temporales de exploracion (no se suben a GitHub)
├── notebooks/         <- Jupyter Notebooks de exploracion y desarrollo
└── dashboard/         <- el producto final (HTML + assets)
```

---

## PROYECTOS FUTUROS ANOTADOS

1. Crear API propia con Flask para Jugos S.A. (para que el dashboard consuma datos en vivo)
2. Aprender Docker para contenerizar aplicaciones
3. Sumar Power BI o Tableau al portfolio