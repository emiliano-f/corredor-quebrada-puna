# Cobertura contra la lista de control

> Generado: 2026-11-14 21:21 UTC · versión `0.1.0.dev0` · commit `806c21d` · SCHEMA_VERSION 3 · fuentes `b3dab32ad1adf821`

Lista: `cortes_conocidos.csv` (54 eventos; E003–E005 cuentan como uno). Coincide un evento del catálogo con la misma ruta, el mismo punto (o sin punto) y fechas que se superponen con las de control ±2 días.

Optimista: un evento sin punto cuenta para un evento de control con lugar. Estricta: no cuenta.

| grupo | optimista: cubiertos / n (%) | estricta: cubiertos / n (%) |
|---|---|---|
| todos | 38/54 (70%) | 37/54 (69%) |
| fecha confirmada | 26/39 (67%) | 25/39 (64%) |
| fecha aproximada | 12/15 (80%) | 12/15 (80%) |
| solo medios que recolectamos | 13/23 (57%) | 13/23 (57%) |
| algún medio que no recolectamos | 25/31 (81%) | 24/31 (77%) |

## Faltantes (optimista)

| id | fecha | ruta | lugar | medios |
|---|---|---|---|---|
| E010 | 2018-07-17 | RN52 | Paso de Jama; Ruta CH-27 con nieve y viento blanco | Diario Panorama; El Tribuno; Cooperativa |
| E018 | 2021-05-28 | RN52 | Ruta CH-27 km 20-34, San Pedro de Atacama hacia Jama | Cooperativa |
| E019 | 2022-01-15 | RN9 | Huichaira, cerca de Tilcara (km 1772,50) | Pregón |
| E020 | 2022-01-17 | RN9 | Angosto de Perchel y Huacalera (km 1790-1795 con precaución extrema) | Todo Jujuy |
| E022 | 2022-07-06 | RN52 | Paso de Jama, ambos lados | Todo Jujuy |
| E023 | 2022-12-08 | RN9 | 'Rutas de la Quebrada' (tramo y ruta no verificados) | El Tribuno de Jujuy |
| E026 | 2023-11-09 | RN9 | Cerca del río Huichaira (Tilcara) y El Perchel | Todo Jujuy |
| E027 | 2023-11-10 | RN52 | Ruta CH-27 km 40-55 | El América; UPF en X |
| E028 | 2024-01-16 | RN9 | Paraje Arjona (km 1745) y Paraje Chañarcito (km 1747,85), Tumbaya–Purmamarca | El Tribuno de Jujuy |
| E031 | 2024-05-18 | RN52 | Ruta CH-27 más allá del km 60 | El Mercurio de Calama vía Chululo; Pregón |
| E032 | 2024-11-25 | RN52 | ~1 km de Purmamarca | Todo Jujuy |
| E037 | 2025-09-05 | RN52 | Ruta CH-27 desde km 53,89 (>200 camiones varados en Jama) | Todo Jujuy |
| E038 | 2025-11-27 | RN52 | km 45 | Todo Jujuy |
| E039 | 2025-11-28 | RN52 | Purmamarca | Todo Jujuy |
| E040 | 2025-12-27 | RN52 | Purmamarca | Todo Jujuy |
| E042 | 2026-02-19 | RN9 | Huacalera | Somos Jujuy; Que Pasa Jujuy |

## Cubiertos solo con eventos sin punto (faltan en la estricta)

- E049: Zona Volcán: cerrado en la báscula de Volcán (norte) y en León (sur)

## Coincidencias

| id | eventos del catálogo |
|---|---|
| E001 | 2016-05-31→2016-05-31 rn52_paso_jama |
| E002 | 2017-01-05→2017-01-05 rn9_tilcara, 2017-01-05→2017-01-05 sin punto |
| E003–E005 | 2017-01-10→2017-01-28 rn9_volcan, 2017-01-11→2017-01-20 rn9_cuesta_barcena, 2017-01-18→2017-01-18 sin punto |
| E006 | 2017-03-10→2017-03-10 rn9_maimara, 2017-03-10→2017-03-10 rn9_tilcara |
| E007 | 2017-06-08→2017-06-08 rn52_paso_jama |
| E008 | 2018-01-12→2018-01-12 rn52_paso_jama, 2018-01-13→2018-01-13 rn52_paso_jama |
| E009 | 2018-06-12→2018-06-12 rn52_paso_jama |
| E011 | 2018-12-21→2018-12-21 rn9_tilcara, 2018-12-21→2018-12-21 rn9_maimara |
| E012 | 2019-02-01→2019-02-01 rn9_tumbaya, 2019-02-01→2019-02-03 rn9_volcan |
| E013 | 2019-02-01→2019-02-03 rn9_volcan |
| E014 | 2019-11-12→2019-11-12 rn9_tumbaya |
| E015 | 2020-02-18→2020-02-18 rn9_tilcara |
| E016 | 2020-06-08→2020-06-09 rn52_paso_jama, 2021-02-18→2021-02-18 rn52_paso_jama, 2021-05-13→2021-05-13 rn52_paso_jama, 2021-09-07→2021-09-07 rn52_paso_jama, 2022-01-10→2022-01-10 rn52_paso_jama, 2022-01-15→2022-01-15 rn52_paso_jama, 2022-01-20→2022-01-21 rn52_paso_jama, 2022-05-01→2022-05-01 rn52_paso_jama |
| E017 | 2021-01-25→2021-01-25 rn9_tilcara |
| E021 | 2022-01-20→2022-01-21 rn52_paso_jama |
| E024 | 2023-06-17→2023-06-17 sin punto, 2023-06-18→2023-06-18 sin punto, 2023-06-18→2023-06-18 sin punto, 2023-06-21→2023-06-21 sin punto, 2023-06-25→2023-06-25 sin punto, 2023-06-27→2023-07-19 rn9_tilcara, 2023-07-09→2023-07-09 sin punto, 2023-07-18→2023-07-18 sin punto, 2023-07-22→2023-07-28 sin punto, 2023-07-22→2023-07-22 sin punto, 2023-07-27→2023-07-27 sin punto, 2023-07-31→2023-07-31 sin punto, 2023-08-05→2023-08-11 rn9_tilcara |
| E025 | 2023-06-17→2023-06-17 rn52_purmamarca_chalala, 2023-06-17→2023-06-17 sin punto, 2023-06-18→2023-06-18 sin punto, 2023-06-18→2023-06-18 sin punto, 2023-06-21→2023-06-21 sin punto, 2023-06-22→2023-06-23 rn52_purmamarca_chalala, 2023-06-25→2023-06-25 sin punto, 2023-07-02→2023-07-02 rn52_purmamarca_chalala, 2023-07-09→2023-07-09 sin punto, 2023-07-12→2023-07-19 rn52_purmamarca_chalala, 2023-07-18→2023-07-18 sin punto, 2023-07-22→2023-07-23 rn52_purmamarca_chalala, 2023-07-22→2023-07-28 sin punto, 2023-07-22→2023-07-22 sin punto, 2023-07-27→2023-07-27 sin punto, 2023-07-31→2023-07-31 sin punto, 2023-08-07→2023-08-08 rn52_purmamarca_chalala |
| E029 | 2024-03-16→2024-03-17 sin punto, 2024-03-19→2024-03-26 rn52_ronqui_angosto |
| E030 | 2024-03-22→2024-03-28 rn52_paso_jama |
| E033 | 2025-04-23→2025-04-23 rn52_paso_jama |
| E034 | 2025-06-16→2025-06-17 rn52_paso_jama |
| E035 | 2025-06-25→2025-06-25 rn52_paso_jama, 2025-06-28→2025-07-01 rn52_paso_jama |
| E036 | 2025-07-30→2025-08-04 rn52_paso_jama |
| E041 | 2026-01-22→2026-01-30 rn52_paso_jama |
| E043 | 2026-04-01→2026-04-01 rn52_lipan_bajo |
| E044 | 2026-03-30→2026-04-05 rn52_paso_jama |
| E045 | 2026-06-08→2026-06-08 rn52_paso_jama |
| E046 | 2026-06-08→2026-06-08 rn52_paso_jama, 2026-06-11→2026-06-11 rn52_paso_jama, 2026-06-12→2026-06-12 sin punto |
| E047 | 2026-06-17→2026-06-19 rn52_paso_jama |
| E048 | 2026-07-16→2026-07-24 rn52_paso_jama |
| E049 | 2026-07-21→2026-07-21 sin punto, 2026-07-22→2026-07-22 sin punto |
| E050 | 2026-08-11→2026-09-13 rn52_paso_jama |
| E051 | 2026-08-11→2026-09-13 rn52_paso_jama |
| E052 | 2026-09-17→2026-09-22 rn52_paso_jama |
| E053 | 2026-09-29→2026-10-03 rn52_paso_jama |
| E054 | 2026-10-08→2026-10-09 rn52_paso_jama, 2026-10-12→2026-10-17 rn52_paso_jama |
| E055 | 2026-10-23→2026-11-07 rn52_paso_jama |
| E056 | 2026-11-12→2026-11-12 rn9_maimara |
