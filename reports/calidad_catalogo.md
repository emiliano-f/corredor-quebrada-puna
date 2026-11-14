# Calidad del catálogo

> Generado: 2026-11-14 01:09 UTC · versión `0.1.0.dev0` · commit `e86aa5e` · SCHEMA_VERSION 2 · fuentes `b3dab32ad1adf821`

Conteos calculados desde las tablas `articulos` y `eventos`. Un artículo aporta como máximo un evento; el dedup junta artículos del mismo corte (ver docs/DATOS.md).

- Artículos: **1393**
- Eventos (tras dedup): **227**
- Menciones antes del dedup: **488** → ratio de dedup **2.15** menciones/evento
- Eventos con 1 medio: **197**; con 2+ medios: **30**
- Método: reglas **227**, LLM **0**

## Por fuente

| fuente | método | marcas | artículos | eventos |
|---|---|---|---|---|
| elsubmarino | wordpress_api | estable | 658 | 143 |
| eltribunojujuy | custom | estable | 287 | 36 |
| jujuyaldia | sitemap | estable | 34 | 10 |
| jujuyalmomento | sitemap | estable | 81 | 20 |
| jujuyonline | wordpress_api | republica | 72 | 17 |
| prensajujuy | sitemap |  | 6 | 2 |
| radioazultilcara | wordpress_api | local | 99 | 32 |
| somosjujuy | sitemap |  | 25 | 3 |
| todojujuy | sitemap | estable | 89 | 18 |
| vialidadnacional | custom |  | 42 | 3 |

Sitemaps: artículos por filtro B **185**, C_solo_ruta **50**. Eventos que vienen **solo** de páginas C_solo_ruta: **7** (3.1%). Decisión (Emiliano, 2026-11-13): se mantiene el filtro C aunque el aporte sea < 5 %; la regla del 5 % era por costo de descarga, y las páginas quedan en caché y el incremento nocturno es de un mes.

## Por año (fuentes estables vs nuevas)

| año | con fuente estable | solo fuentes nuevas |
|---|---|---|
| 2016 | 2 | 0 |
| 2017 | 47 | 0 |
| 2018 | 18 | 0 |
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
| RN9 | 115 |
| RN52 | 111 |
| otra | 1 |

## Por causa

| causa | eventos |
|---|---|
| otro | 107 |
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
| rn52_lipan_bajo | 3 |
| rn52_ronqui_angosto | 3 |
| rn9_cuesta_barcena | 3 |
| rn9_huacalera | 3 |
| rn52_salinas_grandes | 2 |

## Solo medios locales chicos

14 eventos aparecen solo en medios marcados `local: true` (infotilcara, radioazultilcara).

## Chequeo de recall (WordPress vs sitemaps)

156 de 168 eventos de medios WordPress no tienen ningún evento de medios de sitemap en la misma ruta ±2 días. Los sitemaps hoy cubren solo los meses de muestra, así que este número mide sobre todo esa diferencia de cobertura.

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
| 2018-04-01 | RN52 | rn52_paso_jama | otro | 1 | [El Parador del Automóvil Club Argentino en Jama estará cerrado por 10 días](https://elsubmarinojujuy.com.ar/el-parador-de-automovil-club-argentino-en-jama-estara-cerrado-por-10-dias/) |
| 2018-06-15 | RN52 | rn52_paso_jama | nieve | 1 | [Está abierto el tránsito por el Paso de Jama, en ambas direcciones](https://elsubmarinojujuy.com.ar/esta-abierto-el-transito-por-el-paso-de-jama-en-ambas-direcciones/) |
| 2018-07-24 | RN52 | rn52_paso_jama | nieve | 1 | [Por acumulación de nieve del lado chileno, cierran hasta nuevo aviso el Paso de Jama](https://elsubmarinojujuy.com.ar/por-acumulacion-de-nieve-del-lado-chileno-cierran-hasta-nuevo-aviso-el-paso-de-jama/) |
| 2019-02-01 | otra | — | crecida | 1 | [Piden circular con precaución por la ruta nacional N°9: Tránsito por media calzada](https://elsubmarinojujuy.com.ar/piden-circular-con-precaucion-por-la-ruta-nacional-n9-transito-por-media-calzada/) |
| 2022-05-01 | RN52 | rn52_paso_jama | otro | 1 | [Habilitaron el Paso de Jama para el turismo](https://elsubmarinojujuy.com.ar/habilitaron-el-paso-de-jama-para-el-turismo/) |
| 2023-08-11 | RN9 | — | protesta | 1 | [La Ruta Nacional 9 sigue cortada en Abra Pampa y La Quiaca: Se liberarán para las elecciones primarias](https://elsubmarinojujuy.com.ar/la-ruta-nacional-9-sigue-cortada-en-abra-pampa-y-la-quiaca-se-liberaran-para-las-elecciones-primarias/) |
| 2024-03-16 | RN52 | — | otro | 1 | [Cayó puente en la ruta 52, que quedó intransitable](https://eltribunodejujuy.com/informacion-general/2024-3-16-1-0-0-cayo-puente-en-la-ruta-52-que-quedo-intransitable) |
| 2025-02-07 | RN9 | — | otro | 1 | [Corte total en ruta nacional 9](https://eltribunodejujuy.com/informacion-general/2025-2-7-8-27-0-corte-total-en-ruta-nacional-9) |
| 2025-06-28 | RN52 | rn52_paso_jama | nieve | 1 | [El gobierno de Jujuy asiste a personas varadas y trabaja para rehabilitar el tránsito](https://elsubmarinojujuy.com.ar/el-gobierno-de-jujuy-asiste-a-personas-varadas-y-trabaja-para-rehabilitar-el-transito/) |
| 2026-02-24 | RN52 | rn52_paso_jama | nieve | 1 | [Cierre del Paso de Jama por mal tiempo en la cordillera](https://radioazultilcara.com.ar/cierre-del-paso-de-jama-por-mal-tiempo-en-la-cordillera/) |
| 2026-03-30 | RN52 | rn52_paso_jama | aluvion | 2 | [El Paso de Jama cerrado por tormentas mientras Sico opera solo para camiones](https://elsubmarinojujuy.com.ar/el-paso-de-jama-cerrado-por-tormentas-mientras-sico-opera-solo-para-camiones/) |
