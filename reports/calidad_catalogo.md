# Calidad del catálogo

> Generado: 2026-11-14 00:47 UTC · versión `0.1.0.dev0` · commit `664cfbe` · SCHEMA_VERSION 2 · fuentes `b3dab32ad1adf821`

Conteos calculados desde las tablas `articulos` y `eventos`. Un artículo aporta como máximo un evento; el dedup junta artículos del mismo corte (ver docs/DATOS.md).

- Artículos: **1393**
- Eventos (tras dedup): **228**
- Menciones antes del dedup: **489** → ratio de dedup **2.14** menciones/evento
- Eventos con 1 medio: **198**; con 2+ medios: **30**
- Método: reglas **228**, LLM **0**

## Por fuente

| fuente | método | marcas | artículos | eventos |
|---|---|---|---|---|
| elsubmarino | wordpress_api | estable | 658 | 144 |
| eltribunojujuy | custom | estable | 287 | 36 |
| jujuyaldia | sitemap | estable | 34 | 10 |
| jujuyalmomento | sitemap | estable | 81 | 20 |
| jujuyonline | wordpress_api | republica | 72 | 17 |
| prensajujuy | sitemap |  | 6 | 2 |
| radioazultilcara | wordpress_api | local | 99 | 32 |
| somosjujuy | sitemap |  | 25 | 3 |
| todojujuy | sitemap | estable | 89 | 18 |
| vialidadnacional | custom |  | 42 | 3 |

Sitemaps: artículos por filtro B **185**, C_solo_ruta **50**. Eventos que vienen **solo** de páginas C_solo_ruta: **7** (3.1%). Si es < 5 %, se propone volver al filtro B.

## Por año (fuentes estables vs nuevas)

| año | con fuente estable | solo fuentes nuevas |
|---|---|---|
| 2016 | 2 | 0 |
| 2017 | 47 | 0 |
| 2018 | 19 | 0 |
| 2019 | 17 | 0 |
| 2020 | 4 | 1 |
| 2021 | 16 | 0 |
| 2022 | 6 | 0 |
| 2023 | 34 | 0 |
| 2024 | 15 | 2 |
| 2025 | 15 | 5 |
| 2026 | 30 | 15 |

## Por ruta

| ruta | eventos |
|---|---|
| RN9 | 116 |
| RN52 | 111 |
| otra | 1 |

## Por causa

| causa | eventos |
|---|---|
| otro | 108 |
| aluvion | 45 |
| nieve | 36 |
| protesta | 20 |
| crecida | 15 |
| accidente | 2 |
| obra | 2 |

## Por punto crítico

| punto | eventos |
|---|---|
| (sin punto) | 92 |
| rn52_paso_jama | 71 |
| rn9_tilcara | 13 |
| rn52_purmamarca_chalala | 12 |
| rn9_volcan | 8 |
| rn9_maimara | 7 |
| rn9_tumbaya | 6 |
| rn52_susques | 4 |
| rn9_huacalera | 4 |
| rn52_lipan_bajo | 3 |
| rn52_ronqui_angosto | 3 |
| rn9_cuesta_barcena | 3 |
| rn52_salinas_grandes | 2 |

## Solo medios locales chicos

14 eventos aparecen solo en medios marcados `local: true` (infotilcara, radioazultilcara).

## Chequeo de recall (WordPress vs sitemaps)

157 de 169 eventos de medios WordPress no tienen ningún evento de medios de sitemap en la misma ruta ±2 días. Los sitemaps hoy cubren solo los meses de muestra, así que este número mide sobre todo esa diferencia de cobertura.

## Muestra aleatoria de 20 eventos (semilla 42)

| fecha | ruta | punto | causa | medios | titular |
|---|---|---|---|---|---|
| 2017-01-10 | RN9 | rn9_tumbaya | crecida | 1 | [Corte total de la ruta 9 rumbo a la Quebrada](https://www.todojujuy.com/jujuy/corte-total-la-ruta-9-rumbo-la-quebrada-n56638) |
| 2017-01-11 | RN9 | — | aluvion | 1 | [Alud en Jujuy: la ruta 9 aún se encuentra intransitable - Jujuy al día](https://www.jujuyaldia.com.ar/2017/01/11/alud-en-jujuy-la-ruta-9-aun-se-encuentra-intransitable/) |
| 2017-01-11 | RN9 | — | aluvion | 1 | [Corte total en Ruta 9 desde Lozano](https://www.jujuyalmomento.com/temporal/corte-total-ruta-9-lozano-n40714) |
| 2017-01-17 | RN9 | — | otro | 1 | [¿Quiénes pueden circular por Ruta 9?](https://www.todojujuy.com/jujuy/quienes-pueden-circular-ruta-9-n56829) |
| 2017-01-17 | RN9 | — | nieve | 1 | [Logró restablecerse la Ruta 9 por algunas horas](https://www.jujuyalmomento.com/jujuy/logro-restablecerse-la-ruta-9-algunas-horas-n40518) |
| 2017-01-17 | RN9 | — | otro | 1 | [Habilitaron hasta las 18 la alternativa a la Ruta 9 para todo tipo vehículos](https://elsubmarinojujuy.com.ar/habilitaron-hasta-las-18-la-alternativa-a-la-ruta-9-para-todo-tipo-vehiculos/) |
| 2017-01-18 | RN9 | — | aluvion | 1 | [Nuevo horario para transitar por la Ruta 9](https://www.jujuyalmomento.com/zona-del-alud/nuevo-horario-transitar-la-ruta-9-n40431) |
| 2017-01-25 | RN9 | — | otro | 1 | [Por trabajos impostergables: cortarán ruta nacional 9 - Jujuy al día](https://www.jujuyaldia.com.ar/2017/01/24/por-trabajos-impostergables-cortaran-ruta-nacional-9/) |
| 2018-03-29 | RN52 | — | aluvion | 1 | [Todas las rutas hacia el norte están habilitadas pero recomiendan precaución](https://elsubmarinojujuy.com.ar/todas-las-rutas-hacia-el-norte-estan-habililtadas-pero-recomiendan-precaucion/) |
| 2018-03-31 | RN9 | rn9_huacalera | otro | 1 | [En tres procedimientos, la gendarmería incautó más de 27 mil dosis de cocaína](https://elsubmarinojujuy.com.ar/en-tres-procedimientos-la-gendarmeria-incauto-mas-de-27-mil-dosis-de-cocaina/) |
| 2018-06-12 | RN52 | rn52_paso_jama | nieve | 1 | [Continúa cerrado el Paso de Jama por acumulación de nieve](https://elsubmarinojujuy.com.ar/continua-cerrado-el-paso-de-jama-por-acumulacion-de-nieve/) |
| 2018-07-21 | RN52 | rn52_paso_jama | nieve | 1 | [El Paso de Jama está cerrado por las condiciones climáticas](https://elsubmarinojujuy.com.ar/el-paso-de-jama-esta-cerrado-por-las-condiciones-climaticas/) |
| 2019-02-01 | RN9 | — | aluvion | 1 | [Cortes de rutas por desmoronamiento por la ruta nacional 9](https://elsubmarinojujuy.com.ar/cortes-de-rutas-por-desmoronamiento-por-la-ruta-nacional-9/) |
| 2022-01-20 | RN52 | rn52_paso_jama | otro | 1 | [Covid: Alrededor de medio millar camiones están varados en Jama](https://elsubmarinojujuy.com.ar/covid-alrededor-de-medio-millar-camiones-estan-varados-en-jama/) |
| 2023-08-10 | RN9 | — | protesta | 1 | [Habilitan paso sobre la ruta nacional 9 en Purmamarca, Tilcara y Humahuaca por las PASO](https://elsubmarinojujuy.com.ar/habilitan-paso-sobre-la-ruta-nacional-9-en-purmamarca-tilcara-y-humahuaca-por-las-paso/) |
| 2024-03-15 | RN52 | rn52_paso_jama | aluvion | 1 | [Estado de las rutas en Jujuy por las tormentas: Personas varadas en Catua](https://elsubmarinojujuy.com.ar/estado-de-las-rutas-en-jujuy-por-las-tormentas-personas-varadas-en-catua/) |
| 2025-01-16 | RN9 | — | otro | 1 | [Corte con desvio a colectora en ruta 9 altura de Chango Mas](https://eltribunodejujuy.com/informacion-general/2025-1-16-19-59-0-corte-con-desvio-a-colectora-en-ruta-9-altura-de-chango-mas) |
| 2025-06-25 | RN52 | rn52_paso_jama | nieve | 1 | [Cerraron temporalmente el Paso de JAMA por las condiciones climáticas](https://radioazultilcara.com.ar/cerraron-temporalmente-el-paso-de-jama-por-las-condiciones-climaticas/) |
| 2026-02-19 | RN52 | rn52_paso_jama | otro | 1 | [Panorama actual en el Paso de Jama: gran cantidad de jujeños intentan cruzar hacia Chile](https://radioazultilcara.com.ar/panorama-actual-en-el-paso-de-jama-gran-cantidad-de-jujenos-intentan-cruzar-hacia-chile/) |
| 2026-02-24 | RN52 | rn52_paso_jama | nieve | 1 | [Cierre del Paso de Jama por mal tiempo en la cordillera](https://radioazultilcara.com.ar/cierre-del-paso-de-jama-por-mal-tiempo-en-la-cordillera/) |
