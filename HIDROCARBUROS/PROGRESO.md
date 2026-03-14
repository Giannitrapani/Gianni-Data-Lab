# REGISTRO DE PROGRESO - PROYECTO HIDROCARBUROS

Actualizar este archivo al final de cada sesion de trabajo.
Nunca borrar lo que ya esta COMPLETADO.

---

## ESTADO ACTUAL: SETUP INICIAL

---

## COMPLETADO

- [x] Definicion del proyecto y objetivos
- [x] Identificacion de datasets y sus URLs
- [x] Definicion de claves de JOIN entre datasets
- [x] Definicion de analitica prescriptiva a implementar
- [x] Eleccion de tecnologias
- [x] Creacion de estructura de carpetas
- [x] Creacion de CLAUDE.md, CONTEXTO.md y PROGRESO.md

---

## PENDIENTE - EN ORDEN DE EJECUCION

- [ ] FASE 1: Exploracion de datos
  - [ ] Conectar a la API y traer primeras filas del Dataset 1 (produccion por pozo)
  - [ ] Ver columnas y valores unicos de cada dimension
  - [ ] Conectar Dataset 2 (fractura) y verificar el JOIN con idpozo/sigla
  - [ ] Explorar Dataset 3 (perforacion)
  - [ ] Definir filtros finales (cuenca, periodo temporal, formaciones)
  - [ ] Guardar notebook de exploracion en notebooks/01_exploracion.ipynb

- [ ] FASE 2: Procesamiento y calculo de indicadores
  - [ ] Cruzar Dataset 1 + Dataset 2 por idpozo/sigla
  - [ ] Calcular decline rate por pozo (caida de produccion respecto al pico)
  - [ ] Identificar pozos activos sin fractura reciente (candidatos a workover)
  - [ ] Calcular correlacion etapas de fractura vs produccion inicial
  - [ ] Calcular produccion por empresa y comparar con inversiones
  - [ ] Guardar notebook en notebooks/02_procesamiento.ipynb

- [ ] FASE 3: Dashboard HTML
  - [ ] Definir estructura de tabs (igual que Jugos S.A.)
  - [ ] Tab 1: Vision general de produccion Cuenca Neuquina
  - [ ] Tab 2: Analisis por pozo (semaforo de estado + alerta workover)
  - [ ] Tab 3: Vaca Muerta - completacion y productividad
  - [ ] Tab 4: Empresas operadoras - produccion vs inversion
  - [ ] Panel de alertas prescriptivas
  - [ ] Guardar en dashboard/dashboard.html

- [ ] FASE 4: Publicacion
  - [ ] Subir todo a GitHub
  - [ ] Verificar que GitHub Pages muestra el dashboard correctamente
  - [ ] Actualizar portfolio en index.html con el nuevo proyecto

---

## PROBLEMAS ENCONTRADOS

(Registrar aqui cualquier error, limitacion de la API, o dato inesperado)

---

## NOTAS TECNICAS

(Registrar aqui decisiones tecnicas que se tomen durante el desarrollo)

---

## HISTORIAL DE SESIONES

| Fecha | Que se hizo | Estado |
|-------|-------------|--------|
| Setup inicial | Creacion de estructura y archivos de contexto | Completado |