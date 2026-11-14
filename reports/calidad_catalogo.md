# Calidad del catálogo

> Generado: 2026-11-14 15:34 UTC · versión `0.1.0.dev0` · commit `7b22818` · SCHEMA_VERSION 3 · fuentes `b3dab32ad1adf821`

Conteos calculados desde las tablas `articulos` y `eventos`. Un artículo aporta como máximo un evento; el dedup junta artículos del mismo corte (ver docs/DATOS.md).

- Artículos: **1393**
- Eventos (tras dedup): **179**
- Menciones antes del dedup: **540** → ratio de dedup **3.02** menciones/evento
- Eventos con 1 medio: **141**; con 2+ medios: **38**
- Método: reglas **179**, LLM **0**

## Por fuente

| fuente | método | marcas | artículos | eventos |
|---|---|---|---|---|
| elsubmarino | wordpress_api | estable | 658 | 130 |
| eltribunojujuy | custom | estable | 287 | 31 |
| jujuyaldia | sitemap | estable | 34 | 4 |
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
| 2019 | 16 | 0 |
| 2020 | 4 | 1 |
| 2021 | 14 | 0 |
| 2022 | 6 | 0 |
| 2023 | 25 | 0 |
| 2024 | 12 | 1 |
| 2025 | 13 | 4 |
| 2026 | 25 | 14 |

## Por ruta

| ruta | eventos |
|---|---|
| RN52 | 99 |
| RN9 | 78 |
| otra | 2 |

## Por causa

| causa | eventos |
|---|---|
| otro | 75 |
| aluvion | 39 |
| nieve | 34 |
| crecida | 13 |
| protesta | 13 |
| obra | 3 |
| accidente | 2 |

## Por punto crítico

| punto | eventos |
|---|---|
| rn52_paso_jama | 61 |
| (sin punto) | 38 |
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

143 de 153 eventos de medios WordPress no tienen ningún evento de medios de sitemap en la misma ruta ±2 días. Los sitemaps hoy cubren solo los meses de muestra, así que este número mide sobre todo esa diferencia de cobertura.

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
| 2019-10-14 | RN9 | — | aluvion | 1 | [Las intensas lluvias produjeron cortes sobre la ruta nacional 9 en la Quebrada](https://elsubmarinojujuy.com.ar/las-intensas-lluvias-produjeron-cortes-sobre-la-ruta-nacional-9-en-la-quebrada/) |
| 2019-11-02 | RN9 | rn9_tilcara | crecida | 1 | [Tormenta: Está cortada la Ruta 9 en Volcán y otros puntos de la Quebrada](https://elsubmarinojujuy.com.ar/tormenta-esta-cortada-la-ruta-9-en-volcan-y-otros-puntos-de-la-quebrada/) |
| 2019-11-12 | RN52 | — | aluvion | 1 | [Decenas de personas pasaron la noche en los cortes de rutas: Pasaron 12 horas](https://elsubmarinojujuy.com.ar/decenas-personas-pasaron-la-noche-en-los-cortes-de-rutas-pasaron-12-horas/) |
| 2020-04-02 | RN9 | rn9_huacalera | otro | 1 | [Corte temporal de ruta y daños en viviendas en Huacalera](https://eltribunodejujuy.com/nota/2020-4-2-12-42-0-corte-temporal-de-ruta-y-danos-en-viviendas-en-huacalera) |
| 2021-02-18 | RN52 | rn52_paso_jama | otro | 1 | [Coronavirus: El Paso de Jama fue cerrado por contacto estrecho del lado chileno](https://elsubmarinojujuy.com.ar/coronavirus-el-paso-de-jama-fue-cerrado-por-contacto-estrecho-del-lado-chileno/) |
| 2023-09-17 | RN52 | rn52_purmamarca_chalala | otro | 1 | [Asamblea del Tercer Malón de la Paz en La Quiaca: Siguen los cortes de ruta y las marchas](https://elsubmarinojujuy.com.ar/asamblea-del-tercer-malon-de-la-paz-en-la-quiaca-siguen-los-cortes-de-ruta-y-las-marchas/) |
| 2025-06-16 | RN52 | rn52_paso_jama | nieve | 2 | [Habilitaron el tránsito por el Paso de Jama de ambos lados](https://elsubmarinojujuy.com.ar/habilitaron-el-transito-por-el-paso-de-jama-de-ambos-lados/) |
| 2025-12-27 | RN52 | rn52_paso_jama | otro | 1 | [El Paso de Jama está intransitable por condiciones climáticas: Fue cerrado en forma preventiva](https://elsubmarinojujuy.com.ar/el-paso-de-jama-esta-intransitable-por-condiciones-climaticas-fue-cerrado-en-forma-preventiva/) |
| 2026-05-24 | RN52 | rn52_paso_jama | otro | 1 | [El estado de las rutas en Jujuy encendió las alarmas antes del fin de semana largo](https://radioazultilcara.com.ar/el-estado-de-las-rutas-en-jujuy-encendio-las-alarmas-antes-del-fin-de-semana-largo/) |
| 2026-06-08 | RN52 | rn52_paso_jama | otro | 0 | [Paso de Jama: suspenden el tránsito de camiones por fuertes vientos](https://jujuyonline.com/2026/06/08/paso-de-jama-suspenden-transito-camiones-fuertes-vientos/) |
| 2026-07-28 | RN52 | rn52_paso_jama | otro | 1 | [Paso de Jama cerrado para transporte de carga por fuertes vientos](https://eltribunodejujuy.com/informacion-general/2026-7-28-14-54-0-paso-de-jama-cerrado-para-transporte-de-carga-por-fuertes-vientos) |
| 2026-09-17 | RN52 | rn52_paso_jama | nieve | 3 | [El Paso de Jama está intransitable por nieve y fuertes vientos](https://elsubmarinojujuy.com.ar/el-paso-de-jama-esta-intransitable-por-nieve-y-fuertes-vientos/) |
