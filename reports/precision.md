# Precisión de la extracción

> Generado: 2026-11-14 21:10 UTC · versión `0.1.0.dev0` · commit `d97f263` · SCHEMA_VERSION 3 · fuentes `b3dab32ad1adf821`

Etiquetas leídas de `reports/revision_manual.csv` (valores sí: 1/si/ok/x; no: 0/no/mal; vacío = sin etiquetar). Muestra estratificada por causa (semilla 42: aluvion 8, crecida 8, nieve 8, otras 6).

## ¿Es un corte en el corredor? (`ok_corte`)

si = corte de ruta en el corredor; no = no es un corte; fuera = corte fuera del corredor. Tasa = si / etiquetadas.

| estrato | si | no | fuera | tasa si |
|---|---|---|---|---|
| todos | 31 | 4 | 1 | 86% (n=36) |
| aluvion | 8 | 0 | 0 | 100% (n=8) |
| crecida | 8 | 0 | 0 | 100% (n=8) |
| nieve | 8 | 0 | 0 | 100% (n=8) |
| otras | 7 | 4 | 1 | 58% (n=12) |

## Fecha, punto y causa (solo filas con `ok_corte` = si)

n = filas etiquetadas en ese campo. Precisión = correctos / etiquetados.

| estrato | fecha | punto | causa |
|---|---|---|---|
| todos | 95% (n=20) | 82% (n=17) | 84% (n=25) |
| aluvion | 80% (n=5) | 0% (n=1) | 88% (n=8) |
| crecida | 100% (n=6) | 67% (n=6) | 67% (n=6) |
| nieve | 100% (n=6) | 100% (n=7) | 100% (n=7) |
| otras | 100% (n=3) | 100% (n=3) | 75% (n=4) |

## Etiquetas fuera de la precisión

`revisar` = el valor del catálogo cambió después de etiquetar; `nd` = no se puede decidir con la nota.

| campo | revisar | nd |
|---|---|---|
| fecha | 11 | 0 |
| punto | 14 | 0 |
| causa | 6 | 0 |

## Filas para volver a etiquetar (valor al etiquetar → valor actual)

| cambio | titular | url |
|---|---|---|
| fecha: 2017-01-11 → 2017-01-10; punto_id: — → rn9_volcan | Alud en Jujuy: la ruta 9 aún se encuentra intransitable - Jujuy al día | https://www.jujuyaldia.com.ar/2017/01/11/alud-en-jujuy-la-ruta-9-aun-se-encuentra-intransitable/ |
| punto_id: — → rn9_yala_lozano | Corte total en Ruta 9 desde Lozano | https://www.jujuyalmomento.com/temporal/corte-total-ruta-9-lozano-n40714 |
| fecha: 2017-01-17 → 2017-01-10; punto_id: — → rn9_volcan; causa: otro → aluvion | ¿Quiénes pueden circular por Ruta 9? | https://www.todojujuy.com/jujuy/quienes-pueden-circular-ruta-9-n56829 |
| fecha: 2017-01-17 → 2017-01-10; punto_id: — → rn9_volcan; causa: nieve → aluvion | Logró restablecerse la Ruta 9 por algunas horas | https://www.jujuyalmomento.com/jujuy/logro-restablecerse-la-ruta-9-algunas-horas-n40518 |
| fecha: 2017-01-17 → 2017-01-10; punto_id: — → rn9_volcan; causa: otro → aluvion | Habilitaron hasta las 18 la alternativa a la Ruta 9 para todo tipo vehículos | https://elsubmarinojujuy.com.ar/habilitaron-hasta-las-18-la-alternativa-a-la-ruta-9-para-todo-tipo-vehiculos/ |
| fecha: 2017-01-18 → 2017-01-11; punto_id: — → rn9_yala_lozano | Nuevo horario para transitar por la Ruta 9 | https://www.jujuyalmomento.com/zona-del-alud/nuevo-horario-transitar-la-ruta-9-n40431 |
| fecha: 2017-01-25 → 2017-01-10; punto_id: — → rn9_volcan; causa: otro → aluvion | Por trabajos impostergables: cortarán ruta nacional 9 - Jujuy al día | https://www.jujuyaldia.com.ar/2017/01/24/por-trabajos-impostergables-cortaran-ruta-nacional-9/ |
| punto_id: — → rn52_lipan_bajo | Ruta 52 intransitable por las crecidas de arroyos | https://eltribunodejujuy.com/nota/2018-1-12-20-23-0-ruta-52-intransitable-por-las-crecidas-de-arroyos |
| punto_id: — → rn52_lipan_bajo | Todas las rutas hacia el norte están habilitadas pero recomiendan precaución | https://elsubmarinojujuy.com.ar/todas-las-rutas-hacia-el-norte-estan-habililtadas-pero-recomiendan-precaucion/ |
| punto_id: — → rn9_leon | Cortes de rutas por desmoronamiento por la ruta nacional 9 | https://elsubmarinojujuy.com.ar/cortes-de-rutas-por-desmoronamiento-por-la-ruta-nacional-9/ |
| fecha: 2023-08-10 → 2023-08-05; punto_id: — → rn9_tilcara | Habilitan paso sobre la ruta nacional 9 en Purmamarca, Tilcara y Humahuaca por las PASO | https://elsubmarinojujuy.com.ar/habilitan-paso-sobre-la-ruta-nacional-9-en-purmamarca-tilcara-y-humahuaca-por-las-paso/ |
| punto_id: — → rn9_huacalera | En Jujuy, Vialidad Nacional realizó trabajos de emergencia para habilitar la Ruta Nacional 9 | https://www.argentina.gob.ar/noticias/en-jujuy-vialidad-nacional-realizo-trabajos-de-emergencia-para-habilitar-la-ruta-nacional-9 |
| fecha: 2026-10-27 → 2026-10-23 | El Paso de Jama está cerrado por nieve del lado chileno | https://elsubmarinojujuy.com.ar/el-paso-de-jama-esta-cerrado-por-nieve-del-lado-chileno/ |
| fecha: 2017-01-12 → 2017-01-10; punto_id: — → rn9_leon; ; punto_id: rn9_leon → rn9_volcan | Tras el temporal y alud en Jujuy: la ruta 9 no podría ser habilitada al menos hasta el domingo - Jujuy al día | https://www.jujuyaldia.com.ar/2017/01/12/tras-el-temporal-y-alud-en-jujuy-la-ruta-9-no-podria-ser-habilitada-al-menos-hasta-el-domingo/ |
| causa: crecida → aluvion | Está habilitada media calzada de la Ruta 9 desde Maimará hacia San Salvador | https://elsubmarinojujuy.com.ar/esta-habilitada-media-calzada-de-la-ruta-9-desde-maimara-hacia-san-salvador/ |
| fecha: 2019-02-01 → 2019-01-31; punto_id: — → rn52_paso_jama | Piden circular con precaución por la ruta nacional N°9: Tránsito por media calzada | https://elsubmarinojujuy.com.ar/piden-circular-con-precaucion-por-la-ruta-nacional-n9-transito-por-media-calzada/ |
| fecha: 2019-02-02 → 2019-02-01; causa: crecida → aluvion | Agua y lodo en Volcán produjo un corte sobre la ruta nacional N°9 | https://elsubmarinojujuy.com.ar/agua-y-lodo-en-volcan-produjo-un-corte-sobre-la-ruta-nacional-n9/ |
