# Calidad del catálogo

> Generado: 2026-11-14 21:10 UTC · versión `0.1.0.dev0` · commit `d97f263` · SCHEMA_VERSION 3 · fuentes `b3dab32ad1adf821`

Conteos calculados desde las tablas `articulos` y `eventos`. Un artículo aporta como máximo un evento; el dedup junta artículos del mismo corte (ver docs/DATOS.md).

- Artículos: **1393**
- Eventos (tras dedup): **177**
- Menciones antes del dedup: **542** → ratio de dedup **3.06** menciones/evento
- Eventos con 1 medio: **138**; con 2+ medios: **39**
- Método: reglas **177**, LLM **0**

## Por fuente

| fuente | método | marcas | artículos | eventos |
|---|---|---|---|---|
| elsubmarino | wordpress_api | estable | 658 | 130 |
| eltribunojujuy | custom | estable | 287 | 31 |
| jujuyaldia | sitemap | estable | 34 | 3 |
| jujuyalmomento | sitemap | estable | 81 | 16 |
| jujuyonline | wordpress_api | republica | 72 | 16 |
| prensajujuy | sitemap |  | 6 | 5 |
| radioazultilcara | wordpress_api | local | 99 | 29 |
| somosjujuy | sitemap |  | 25 | 6 |
| todojujuy | sitemap | estable | 89 | 14 |
| vialidadnacional | custom |  | 42 | 3 |

Sitemaps: artículos por filtro B **185**, C_solo_ruta **50**. Eventos que vienen **solo** de páginas C_solo_ruta: **3** (1.7%). Decisión (Emiliano, 2026-11-13): se mantiene el filtro C aunque el aporte sea < 5 %; la regla del 5 % era por costo de descarga, y las páginas quedan en caché y el incremento nocturno es de un mes.

## Por año (fuentes estables vs nuevas)

| año | con fuente estable | solo fuentes nuevas |
|---|---|---|
| 2016 | 2 | 0 |
| 2017 | 23 | 0 |
| 2018 | 19 | 0 |
| 2019 | 15 | 0 |
| 2020 | 4 | 1 |
| 2021 | 14 | 0 |
| 2022 | 6 | 0 |
| 2023 | 25 | 0 |
| 2024 | 11 | 1 |
| 2025 | 13 | 4 |
| 2026 | 25 | 14 |

## Por ruta

| ruta | eventos |
|---|---|
| RN52 | 99 |
| RN9 | 78 |

## Por causa

| causa | eventos |
|---|---|
| otro | 75 |
| aluvion | 37 |
| nieve | 33 |
| crecida | 14 |
| protesta | 13 |
| obra | 3 |
| accidente | 2 |

## Por punto crítico

| punto | eventos |
|---|---|
| rn52_paso_jama | 61 |
| (sin punto) | 36 |
| rn9_tilcara | 15 |
| rn52_purmamarca_chalala | 12 |
| rn9_volcan | 9 |
| rn52_susques | 8 |
| rn9_tumbaya | 8 |
| rn9_maimara | 7 |
| rn52_ronqui_angosto | 4 |
| rn52_lipan_bajo | 3 |
| rn52_salinas_grandes | 3 |
| rn9_cuesta_barcena | 3 |
| rn9_huacalera | 3 |
| rn9_leon | 3 |
| rn9_yala_lozano | 2 |

## Solo medios locales chicos

13 eventos aparecen solo en medios marcados `local: true` (infotilcara, radioazultilcara).

## Chequeo de recall (WordPress vs sitemaps)

141 de 153 eventos de medios WordPress no tienen ningún evento de medios de sitemap en la misma ruta ±2 días. Los sitemaps hoy cubren solo los meses de muestra, así que este número mide sobre todo esa diferencia de cobertura.

## Muestra aleatoria de 20 eventos (semilla 42)

| fecha | ruta | punto | causa | medios | titular |
|---|---|---|---|---|---|
| 2017-01-10 | RN9 | rn9_tumbaya | crecida | 3 | [Aseguran que la asistencia es completa a los damnificados de Volcán, Tumbaya y Bárcena](https://elsubmarinojujuy.com.ar/aseguran-que-la-asistencia-es-completa-a-los-damnificados-de-volcan-tumbaya-y-barcena/) |
| 2017-01-11 | RN9 | rn9_cuesta_barcena | aluvion | 3 | [Aseguran que la asistencia es completa a los damnificados de Volcán, Tumbaya y Bárcena](https://elsubmarinojujuy.com.ar/aseguran-que-la-asistencia-es-completa-a-los-damnificados-de-volcan-tumbaya-y-barcena/) |
| 2017-01-11 | RN9 | rn9_yala_lozano | aluvion | 2 | [Corte total en Ruta 9 desde Lozano](https://www.jujuyalmomento.com/temporal/corte-total-ruta-9-lozano-n40714) |
| 2017-06-29 | RN9 | — | otro | 1 | [Seom retomó corte en Humahuaca](https://eltribunodejujuy.com/nota/2017-6-29-9-56-12-seom-retomo-corte-en-humahuaca) |
| 2017-07-29 | RN9 | rn9_volcan | otro | 1 | [La comunidad Antigal-Tilian corta la Ruta 9 para denunciar la matanza de sus animales](https://elsubmarinojujuy.com.ar/la-comunidad-antigal-tilian-corta-la-ruta-9-denunciar-la-matanza-animales/) |
| 2018-01-12 | RN52 | rn52_lipan_bajo | crecida | 2 | [La ruta 52 esta cortada por lluvias y desmoronamiento de cerros](https://elsubmarinojujuy.com.ar/la-ruta-52-esta-cortada-lluvias-desmoronamiento-cerros/) |
| 2018-01-13 | RN52 | rn52_paso_jama | aluvion | 1 | [Solicitan transitar con precaución por la Ruta Nacional 52 que fue habilitada en un sólo carril](https://elsubmarinojujuy.com.ar/solicitan-transitar-precaucion-la-ruta-nacional-52-fue-habilitada-solo-carril/) |
| 2018-06-27 | RN52 | rn52_paso_jama | otro | 1 | [Está cerrado el Paso de Jama, esta vez por un paro nacional del personal de Aduana](https://elsubmarinojujuy.com.ar/esta-cerrado-el-paso-de-jama-esta-vez-por-un-paro-nacional-del-personal-de-aduana/) |
| 2019-11-02 | RN9 | rn9_volcan | crecida | 1 | [La Ruta Nacional N°9 estará cortada hasta mañana, por prevención](https://elsubmarinojujuy.com.ar/la-ruta-nacional-n9-estara-cortada-hasta-manana-por-prevencion/) |
| 2019-11-12 | RN9 | rn9_tumbaya | aluvion | 1 | [Por las lluvias y la falta de infraestructura la Ruta 9 permaneció cortada por 14 horas](https://elsubmarinojujuy.com.ar/por-las-lluvias-y-la-falta-de-infraestructura-la-ruta-9-permanecio-cortada-por-14-horas/) |
| 2020-01-23 | RN9 | rn9_tilcara | obra | 1 | [Denuncian que el gobierno no construyó el Centro Regional de Rehabilitación en Tilcara (Video)](https://elsubmarinojujuy.com.ar/denuncian-que-el-gobierno-no-construyo-el-centro-regional-de-rehabilitacion-en-tilcara-video/) |
| 2020-06-08 | RN52 | rn52_paso_jama | otro | 1 | [El gobierno solicita el cierre del Paso de Jama por una semana para evitar circulación local](https://elsubmarinojujuy.com.ar/el-gobierno-solicita-el-cierre-del-paso-de-jama-por-una-semana-para-evitar-circulacion-local/) |
| 2021-02-18 | RN9 | rn9_yala_lozano | otro | 1 | [Corte en la Ruta 9 por desmalezamiento y poda](https://elsubmarinojujuy.com.ar/corte-en-la-ruta-9-por-desmalezamiento-y-poda/) |
| 2023-10-31 | RN9 | — | protesta | 1 | [Otro juicio contravencional que se cae: «El objetivo es el disciplinamiento»](https://elsubmarinojujuy.com.ar/otro-juicio-contravencional-que-se-cae-el-objetivo-es-el-disciplinamiento/) |
| 2025-06-28 | RN52 | rn52_paso_jama | nieve | 1 | [El gobierno de Jujuy asiste a personas varadas y trabaja para rehabilitar el tránsito](https://elsubmarinojujuy.com.ar/el-gobierno-de-jujuy-asiste-a-personas-varadas-y-trabaja-para-rehabilitar-el-transito/) |
| 2026-01-22 | RN52 | rn52_paso_jama | otro | 2 | [El Paso de Jama estará cerrado durante cuatro días por las malas condiciones climáticas](https://elsubmarinojujuy.com.ar/el-paso-de-jama-estara-cerrado-durante-cuatro-dias-por-las-malas-condiciones-climaticas/) |
| 2026-05-31 | RN52 | — | otro | 1 | [Operativo vial: Habrá cortes totales sobre la Ruta 52 por camiones de gran porte](https://elsubmarinojujuy.com.ar/operativo-vial-habra-cortes-totales-sobre-la-ruta-52-por-camiones-de-gran-porte/) |
| 2026-06-12 | RN52 | — | otro | 1 | [Corte y demoras en ruta 52 por incidentes con camiones](https://eltribunodejujuy.com/informacion-general/2026-6-12-15-26-0-corte-y-demoras-en-ruta-52-por-incidentes-con-camiones) |
| 2026-08-01 | RN9 | rn9_tilcara | accidente | 1 | [Una moto chocó contra un auto en el puente principal de Tilcara](https://radioazultilcara.com.ar/una-moto-choco-contra-un-auto-en-el-puente-principal-de-tilcara/) |
| 2026-10-08 | RN52 | rn52_paso_jama | otro | 1 | [Paso de Jama habilitado y tramos transitables con precaución](https://eltribunodejujuy.com/informacion-general/2026-10-8-8-1-0-paso-de-jama-habilitado-y-tramos-transitables-con-precaucion) |
