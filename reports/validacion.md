# Validación de umbrales

> Generado: 2026-11-14 21:25 UTC · versión `0.1.0.dev0` · commit `50b4971` · SCHEMA_VERSION 3 · fuentes `b3dab32ad1adf821`

Causas meteorológicas: aluvión y crecida contra lluvia, nieve contra nieve. Una regla por causa, igual para todos los puntos; ajuste 2016–2022, prueba 2023→hoy. Acierto = evento con alarma ese día o el anterior; falsa alarma = día con alarma sin evento ese día o el siguiente. Los mm de ERA5 no son lluvia local (ver docs/DATOS.md): por eso cada variable va también como percentil de su celda en la misma estación. Cada sección trae también la variante con aluvión y crecida juntos como una sola causa "lluvia". Junto a cada número va n = días-evento (punto, fecha) del período en que se basa; en prueba, n < 10 se marca "muestra chica". Vos elegís la regla final.

Fuentes estables (archivo desde ≤ 2016-01-01): elsubmarino, eltribunojujuy, jujuyaldia, jujuyalmomento, todojujuy.

## Todas las fuentes

Eventos con punto crítico usados: aluvión 32, crecida 13 (lluvia 45), nieve 33.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 20 | 17.9 | 4.0 | 83 |
| aluvion | `lluvia_48h_mm` | 20 | 22.0 | 9.2 | 81 |
| aluvion | `lluvia_72h_mm` | 20 | 28.4 | 15.3 | 75 |
| aluvion | `lluvia_7d_mm` | 20 | 79.4 | 43.9 | 80 |
| aluvion | `lluvia_max_horaria_24h_mm` | 20 | 2.7 | 0.8 | 86 |
| aluvion | `lluvia_max_horaria_72h_mm` | 20 | 3.4 | 1.7 | 79 |
| crecida | `lluvia_24h_mm` | 8 | 12.3 | 4.0 | 82 |
| crecida | `lluvia_48h_mm` | 8 | 18.6 | 9.5 | 77 |
| crecida | `lluvia_72h_mm` | 8 | 24.6 | 15.8 | 71 |
| crecida | `lluvia_7d_mm` | 8 | 59.4 | 42.9 | 77 |
| crecida | `lluvia_max_horaria_24h_mm` | 8 | 2.5 | 0.9 | 78 |
| crecida | `lluvia_max_horaria_72h_mm` | 8 | 3.0 | 1.8 | 75 |
| nieve | `nieve_24h_cm` | 13 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 13 | 1.3 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 13 | 2.2 | 0.0 | 89 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 3.9 mm | 18 (n=23) | 5 (n=23) | 8482 (n=23) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 4459 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 6 mm | 18 (n=23) | 5 (n=23) | 6167 (n=23) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 3186 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 17.9 mm | 12 (n=23) | 11 (n=23) | 1419 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 695 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 34.2 mm | 5 (n=23) | 18 (n=23) | 350 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 159 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 14.8 mm | 18 (n=23) | 5 (n=23) | 5285 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2645 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 16.7 mm | 18 (n=23) | 5 (n=23) | 4617 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2283 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 22 mm | 11 (n=23) | 12 (n=23) | 3177 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1510 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 50.1 mm | 5 (n=23) | 18 (n=23) | 528 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 219 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 20.5 mm | 18 (n=23) | 5 (n=23) | 5995 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3022 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 24.9 mm | 16 (n=23) | 7 (n=23) | 4699 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2356 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 28.4 mm | 14 (n=23) | 9 (n=23) | 3886 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1953 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 54.5 mm | 5 (n=23) | 18 (n=23) | 1074 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 437 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 32.4 mm | 18 (n=23) | 5 (n=23) | 9131 (n=23) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 4868 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 48.6 mm | 15 (n=23) | 8 (n=23) | 6155 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3028 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 79.4 mm | 10 (n=23) | 13 (n=23) | 2744 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1212 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 116 mm | 6 (n=23) | 17 (n=23) | 870 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 381 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.8 mm | 19 (n=23) | 4 (n=23) | 9209 (n=23) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 4717 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.4 mm | 18 (n=23) | 5 (n=23) | 5424 (n=23) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 2710 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 2.7 mm | 13 (n=23) | 10 (n=23) | 2008 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 968 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 5.8 mm | 5 (n=23) | 18 (n=23) | 347 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 177 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.9 mm | 18 (n=23) | 5 (n=23) | 7571 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3866 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 17 (n=23) | 6 (n=23) | 7122 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3583 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.4 mm | 13 (n=23) | 10 (n=23) | 3088 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 1530 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.7 mm | 5 (n=23) | 18 (n=23) | 962 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 501 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 4.5 mm | 8 (n=9) | 1 (n=9) | 7708 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 4061 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 6.5 mm | 6 (n=9) | 3 (n=9) | 5741 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 2966 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 12.3 mm | 4 (n=9) | 5 (n=9) | 2696 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1297 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 24.2 mm | 2 (n=9) | 7 (n=9) | 787 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 380 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 9.7 mm | 8 (n=9) | 1 (n=9) | 7828 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 4114 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 10.1 mm | 8 (n=9) | 1 (n=9) | 7580 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3975 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 18.6 mm | 4 (n=9) | 5 (n=9) | 4025 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 1979 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 40.2 mm | 2 (n=9) | 7 (n=9) | 1020 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 431 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 16.3 mm | 7 (n=9) | 2 (n=9) | 7459 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3872 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 17.7 mm | 7 (n=9) | 2 (n=9) | 6928 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3531 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 24.6 mm | 6 (n=9) | 3 (n=9) | 4808 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2389 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 42.6 mm | 4 (n=9) | 5 (n=9) | 1965 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 869 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 40.5 mm | 7 (n=9) | 2 (n=9) | 7514 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3812 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 48.2 mm | 6 (n=9) | 3 (n=9) | 6243 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3059 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 59.4 mm | 4 (n=9) | 5 (n=9) | 4616 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2242 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 88.8 mm | 2 (n=9) | 7 (n=9) | 2113 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 900 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.8 mm | 8 (n=9) | 1 (n=9) | 9228 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 4723 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.1 mm | 8 (n=9) | 1 (n=9) | 7095 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3574 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.5 mm | 5 (n=9) | 4 (n=9) | 2350 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1141 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 3.1 mm | 3 (n=9) | 6 (n=9) | 1569 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 721 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 1.9 mm | 7 (n=9) | 2 (n=9) | 7591 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3875 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 2.2 mm | 7 (n=9) | 2 (n=9) | 6285 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3227 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 6 (n=9) | 3 (n=9) | 3944 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1923 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.4 mm | 5 (n=9) | 4 (n=9) | 1875 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 902 (n=4 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 9 (n=13) | 4 (n=13) | 272 (n=13) | 7 (n=20) | 13 (n=20) | 112 (n=20) |
| nieve | `nieve_24h_cm` | 0.2 cm | 8 (n=13) | 5 (n=13) | 233 (n=13) | 7 (n=20) | 13 (n=20) | 100 (n=20) |
| nieve | `nieve_24h_cm` | 1.1 cm | 5 (n=13) | 8 (n=13) | 80 (n=13) | 3 (n=20) | 17 (n=20) | 32 (n=20) |
| nieve | `nieve_72h_cm` | 0.1 cm | 11 (n=13) | 2 (n=13) | 643 (n=13) | 11 (n=20) | 9 (n=20) | 236 (n=20) |
| nieve | `nieve_72h_cm` | 0.8 cm | 8 (n=13) | 5 (n=13) | 312 (n=13) | 6 (n=20) | 14 (n=20) | 113 (n=20) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=13) | 7 (n=13) | 202 (n=13) | 3 (n=20) | 17 (n=20) | 78 (n=20) |
| nieve | `nieve_72h_cm` | 2.6 cm | 3 (n=13) | 10 (n=13) | 78 (n=13) | 1 (n=20) | 19 (n=20) | 36 (n=20) |
| nieve | `nieve_7d_cm` | 0.2 cm | 10 (n=13) | 3 (n=13) | 1140 (n=13) | 12 (n=20) | 8 (n=20) | 443 (n=20) |
| nieve | `nieve_7d_cm` | 0.9 cm | 9 (n=13) | 4 (n=13) | 636 (n=13) | 6 (n=20) | 14 (n=20) | 232 (n=20) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=13) | 7 (n=13) | 269 (n=13) | 2 (n=20) | 18 (n=20) | 88 (n=20) |
| nieve | `nieve_7d_cm` | 3.2 cm | 3 (n=13) | 10 (n=13) | 178 (n=13) | 0 (n=20) | 20 (n=20) | 66 (n=20) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 15 (n=23) | 8 (n=23) | 5799 (n=23) | 8 (n=9 muestra chica) | 1 (n=9 muestra chica) | 3342 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 11 (n=23) | 12 (n=23) | 3058 (n=23) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1713 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 7 (n=23) | 16 (n=23) | 1594 (n=23) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 910 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 5 (n=23) | 18 (n=23) | 666 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 386 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 4 (n=23) | 19 (n=23) | 310 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 171 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 11 (n=23) | 12 (n=23) | 6080 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3341 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 8 (n=23) | 15 (n=23) | 3148 (n=23) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 1745 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 6 (n=23) | 17 (n=23) | 1630 (n=23) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 904 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 5 (n=23) | 18 (n=23) | 664 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 330 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 2 (n=23) | 21 (n=23) | 308 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 162 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 8 (n=23) | 15 (n=23) | 6171 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3344 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 8 (n=23) | 15 (n=23) | 3222 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 1761 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 6 (n=23) | 17 (n=23) | 1648 (n=23) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 872 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 3 (n=23) | 20 (n=23) | 667 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 293 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 2 (n=23) | 21 (n=23) | 316 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 133 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 11 (n=23) | 12 (n=23) | 6440 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3542 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 8 (n=23) | 15 (n=23) | 3290 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 1756 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 3 (n=23) | 20 (n=23) | 1654 (n=23) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 823 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 3 (n=23) | 20 (n=23) | 657 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 296 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 3 (n=23) | 20 (n=23) | 304 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 138 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 14 (n=23) | 9 (n=23) | 5797 (n=23) | 8 (n=9 muestra chica) | 1 (n=9 muestra chica) | 3228 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 12 (n=23) | 11 (n=23) | 3017 (n=23) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 1621 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 6 (n=23) | 17 (n=23) | 1586 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 870 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 5 (n=23) | 18 (n=23) | 651 (n=23) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 311 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=23) | 20 (n=23) | 314 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 149 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 10 (n=23) | 13 (n=23) | 6091 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3199 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 7 (n=23) | 16 (n=23) | 3198 (n=23) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1732 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 6 (n=23) | 17 (n=23) | 1618 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 794 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 3 (n=23) | 20 (n=23) | 649 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 291 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 3 (n=23) | 20 (n=23) | 301 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 158 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p80 | 5 (n=9) | 4 (n=9) | 5814 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3352 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 1 (n=9) | 8 (n=9) | 3070 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1717 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 1 (n=9) | 8 (n=9) | 1602 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 911 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 1 (n=9) | 8 (n=9) | 672 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 386 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 314 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 171 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 4 (n=9) | 5 (n=9) | 6091 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3349 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 1 (n=9) | 8 (n=9) | 3159 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1751 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 1 (n=9) | 8 (n=9) | 1638 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 905 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 0 (n=9) | 9 (n=9) | 672 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 331 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 312 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 162 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 4 (n=9) | 5 (n=9) | 6179 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3355 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 3 (n=9) | 6 (n=9) | 3231 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1772 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 1 (n=9) | 8 (n=9) | 1656 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 878 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 0 (n=9) | 9 (n=9) | 672 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 294 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 318 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 133 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 3 (n=9) | 6 (n=9) | 6456 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3554 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 2 (n=9) | 7 (n=9) | 3300 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1766 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 2 (n=9) | 7 (n=9) | 1658 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 825 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 1 (n=9) | 8 (n=9) | 662 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 298 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 308 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 140 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 6 (n=9) | 3 (n=9) | 5812 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3238 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 2 (n=9) | 7 (n=9) | 3032 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1630 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 1 (n=9) | 8 (n=9) | 1595 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 873 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 1 (n=9) | 8 (n=9) | 657 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 313 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 319 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 149 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 3 (n=9) | 6 (n=9) | 6104 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 3212 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 3 (n=9) | 6 (n=9) | 3205 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1739 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 3 (n=9) | 6 (n=9) | 1624 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 797 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=9) | 8 (n=9) | 654 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 291 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=9) | 8 (n=9) | 306 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 158 (n=4 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 10 (n=13) | 3 (n=13) | 325 (n=13) | 9 (n=20) | 11 (n=20) | 141 (n=20) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=13) | 3 (n=13) | 298 (n=13) | 9 (n=20) | 11 (n=20) | 132 (n=20) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=13) | 3 (n=13) | 265 (n=13) | 9 (n=20) | 11 (n=20) | 113 (n=20) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=13) | 9 (n=13) | 186 (n=13) | 4 (n=20) | 16 (n=20) | 71 (n=20) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=13) | 11 (n=13) | 117 (n=13) | 3 (n=20) | 17 (n=20) | 41 (n=20) |
| nieve | `nieve_72h_cm_pct` | p80 | 12 (n=13) | 1 (n=13) | 702 (n=13) | 12 (n=20) | 8 (n=20) | 276 (n=20) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=13) | 2 (n=13) | 608 (n=13) | 11 (n=20) | 9 (n=20) | 236 (n=20) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=13) | 6 (n=13) | 450 (n=13) | 8 (n=20) | 12 (n=20) | 170 (n=20) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=13) | 10 (n=13) | 265 (n=13) | 4 (n=20) | 16 (n=20) | 84 (n=20) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=13) | 11 (n=13) | 162 (n=13) | 2 (n=20) | 18 (n=20) | 50 (n=20) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=13) | 2 (n=13) | 1271 (n=13) | 12 (n=20) | 8 (n=20) | 490 (n=20) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=13) | 7 (n=13) | 971 (n=13) | 9 (n=20) | 11 (n=20) | 359 (n=20) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=13) | 8 (n=13) | 658 (n=13) | 6 (n=20) | 14 (n=20) | 211 (n=20) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=13) | 11 (n=13) | 359 (n=13) | 3 (n=20) | 17 (n=20) | 100 (n=20) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=13) | 12 (n=13) | 181 (n=13) | 1 (n=20) | 19 (n=20) | 68 (n=20) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 28 | 15.4 | 3.9 | 83 |
| lluvia | `lluvia_48h_mm` | 28 | 21.6 | 9.0 | 80 |
| lluvia | `lluvia_72h_mm` | 28 | 27.3 | 15.0 | 75 |
| lluvia | `lluvia_7d_mm` | 28 | 69.9 | 41.8 | 79 |
| lluvia | `lluvia_max_horaria_24h_mm` | 28 | 2.6 | 0.8 | 82 |
| lluvia | `lluvia_max_horaria_72h_mm` | 28 | 3.0 | 1.7 | 78 |
| nieve | `nieve_24h_cm` | 13 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 13 | 1.3 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 13 | 2.2 | 0.0 | 89 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 4 mm | 26 (n=32) | 6 (n=32) | 8343 (n=32) | 7 (n=13) | 6 (n=13) | 4390 (n=13) |
| lluvia | `lluvia_24h_mm` | 6 mm | 25 (n=32) | 7 (n=32) | 6157 (n=32) | 6 (n=13) | 7 (n=13) | 3182 (n=13) |
| lluvia | `lluvia_24h_mm` | 17.9 mm | 15 (n=32) | 17 (n=32) | 1415 (n=32) | 2 (n=13) | 11 (n=13) | 694 (n=13) |
| lluvia | `lluvia_24h_mm` | 30.9 mm | 8 (n=32) | 24 (n=32) | 472 (n=32) | 0 (n=13) | 13 (n=13) | 199 (n=13) |
| lluvia | `lluvia_48h_mm` | 9.7 mm | 27 (n=32) | 5 (n=32) | 7794 (n=32) | 7 (n=13) | 6 (n=13) | 4106 (n=13) |
| lluvia | `lluvia_48h_mm` | 16.2 mm | 22 (n=32) | 10 (n=32) | 4800 (n=32) | 5 (n=13) | 8 (n=13) | 2371 (n=13) |
| lluvia | `lluvia_48h_mm` | 21.6 mm | 15 (n=32) | 17 (n=32) | 3266 (n=32) | 2 (n=13) | 11 (n=13) | 1548 (n=13) |
| lluvia | `lluvia_48h_mm` | 47.6 mm | 7 (n=32) | 25 (n=32) | 624 (n=32) | 0 (n=13) | 13 (n=13) | 272 (n=13) |
| lluvia | `lluvia_72h_mm` | 16.3 mm | 25 (n=32) | 7 (n=32) | 7426 (n=32) | 5 (n=13) | 8 (n=13) | 3866 (n=13) |
| lluvia | `lluvia_72h_mm` | 23.4 mm | 22 (n=32) | 10 (n=32) | 5131 (n=32) | 5 (n=13) | 8 (n=13) | 2564 (n=13) |
| lluvia | `lluvia_72h_mm` | 27.3 mm | 20 (n=32) | 12 (n=32) | 4141 (n=32) | 2 (n=13) | 11 (n=13) | 2059 (n=13) |
| lluvia | `lluvia_72h_mm` | 53.1 mm | 9 (n=32) | 23 (n=32) | 1149 (n=32) | 0 (n=13) | 13 (n=13) | 482 (n=13) |
| lluvia | `lluvia_7d_mm` | 31.1 mm | 25 (n=32) | 7 (n=32) | 9428 (n=32) | 5 (n=13) | 8 (n=13) | 5068 (n=13) |
| lluvia | `lluvia_7d_mm` | 48.2 mm | 21 (n=32) | 11 (n=32) | 6215 (n=32) | 4 (n=13) | 9 (n=13) | 3054 (n=13) |
| lluvia | `lluvia_7d_mm` | 69.9 mm | 14 (n=32) | 18 (n=32) | 3523 (n=32) | 2 (n=13) | 11 (n=13) | 1635 (n=13) |
| lluvia | `lluvia_7d_mm` | 116 mm | 8 (n=32) | 24 (n=32) | 867 (n=32) | 1 (n=13) | 12 (n=13) | 379 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.8 mm | 27 (n=32) | 5 (n=32) | 9195 (n=32) | 8 (n=13) | 5 (n=13) | 4713 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.2 mm | 26 (n=32) | 6 (n=32) | 6478 (n=32) | 8 (n=13) | 5 (n=13) | 3226 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 2.7 mm | 17 (n=32) | 15 (n=32) | 2002 (n=32) | 1 (n=13) | 12 (n=13) | 967 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 5.2 mm | 7 (n=32) | 25 (n=32) | 487 (n=32) | 0 (n=13) | 13 (n=13) | 232 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.8 mm | 25 (n=32) | 7 (n=32) | 8014 (n=32) | 9 (n=13) | 4 (n=13) | 4099 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 2.1 mm | 23 (n=32) | 9 (n=32) | 6646 (n=32) | 7 (n=13) | 6 (n=13) | 3431 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 3 mm | 19 (n=32) | 13 (n=32) | 3924 (n=32) | 1 (n=13) | 12 (n=13) | 1923 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 5.2 mm | 10 (n=32) | 22 (n=32) | 1255 (n=32) | 0 (n=13) | 13 (n=13) | 618 (n=13) |
| nieve | `nieve_24h_cm` | 0.1 cm | 9 (n=13) | 4 (n=13) | 272 (n=13) | 7 (n=20) | 13 (n=20) | 112 (n=20) |
| nieve | `nieve_24h_cm` | 0.2 cm | 8 (n=13) | 5 (n=13) | 233 (n=13) | 7 (n=20) | 13 (n=20) | 100 (n=20) |
| nieve | `nieve_24h_cm` | 1.1 cm | 5 (n=13) | 8 (n=13) | 80 (n=13) | 3 (n=20) | 17 (n=20) | 32 (n=20) |
| nieve | `nieve_72h_cm` | 0.1 cm | 11 (n=13) | 2 (n=13) | 643 (n=13) | 11 (n=20) | 9 (n=20) | 236 (n=20) |
| nieve | `nieve_72h_cm` | 0.8 cm | 8 (n=13) | 5 (n=13) | 312 (n=13) | 6 (n=20) | 14 (n=20) | 113 (n=20) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=13) | 7 (n=13) | 202 (n=13) | 3 (n=20) | 17 (n=20) | 78 (n=20) |
| nieve | `nieve_72h_cm` | 2.6 cm | 3 (n=13) | 10 (n=13) | 78 (n=13) | 1 (n=20) | 19 (n=20) | 36 (n=20) |
| nieve | `nieve_7d_cm` | 0.2 cm | 10 (n=13) | 3 (n=13) | 1140 (n=13) | 12 (n=20) | 8 (n=20) | 443 (n=20) |
| nieve | `nieve_7d_cm` | 0.9 cm | 9 (n=13) | 4 (n=13) | 636 (n=13) | 6 (n=20) | 14 (n=20) | 232 (n=20) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=13) | 7 (n=13) | 269 (n=13) | 2 (n=20) | 18 (n=20) | 88 (n=20) |
| nieve | `nieve_7d_cm` | 3.2 cm | 3 (n=13) | 10 (n=13) | 178 (n=13) | 0 (n=20) | 20 (n=20) | 66 (n=20) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 20 (n=32) | 12 (n=32) | 5793 (n=32) | 10 (n=13) | 3 (n=13) | 3339 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 12 (n=32) | 20 (n=32) | 3057 (n=32) | 6 (n=13) | 7 (n=13) | 1711 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 8 (n=32) | 24 (n=32) | 1593 (n=32) | 3 (n=13) | 10 (n=13) | 909 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 6 (n=32) | 26 (n=32) | 665 (n=32) | 0 (n=13) | 13 (n=13) | 386 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 4 (n=32) | 28 (n=32) | 310 (n=32) | 0 (n=13) | 13 (n=13) | 171 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 15 (n=32) | 17 (n=32) | 6075 (n=32) | 9 (n=13) | 4 (n=13) | 3337 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 9 (n=32) | 23 (n=32) | 3147 (n=32) | 7 (n=13) | 6 (n=13) | 1743 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 7 (n=32) | 25 (n=32) | 1629 (n=32) | 3 (n=13) | 10 (n=13) | 903 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 5 (n=32) | 27 (n=32) | 664 (n=32) | 1 (n=13) | 12 (n=13) | 330 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 2 (n=32) | 30 (n=32) | 308 (n=32) | 0 (n=13) | 13 (n=13) | 162 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 12 (n=32) | 20 (n=32) | 6165 (n=32) | 8 (n=13) | 5 (n=13) | 3342 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 11 (n=32) | 21 (n=32) | 3219 (n=32) | 8 (n=13) | 5 (n=13) | 1760 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 7 (n=32) | 25 (n=32) | 1647 (n=32) | 4 (n=13) | 9 (n=13) | 872 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 3 (n=32) | 29 (n=32) | 667 (n=32) | 1 (n=13) | 12 (n=13) | 293 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 2 (n=32) | 30 (n=32) | 316 (n=32) | 0 (n=13) | 13 (n=13) | 133 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 14 (n=32) | 18 (n=32) | 6436 (n=32) | 8 (n=13) | 5 (n=13) | 3540 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 10 (n=32) | 22 (n=32) | 3288 (n=32) | 8 (n=13) | 5 (n=13) | 1754 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 5 (n=32) | 27 (n=32) | 1652 (n=32) | 3 (n=13) | 10 (n=13) | 821 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 4 (n=32) | 28 (n=32) | 656 (n=32) | 1 (n=13) | 12 (n=13) | 296 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 3 (n=32) | 29 (n=32) | 304 (n=32) | 1 (n=13) | 12 (n=13) | 138 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 20 (n=32) | 12 (n=32) | 5790 (n=32) | 10 (n=13) | 3 (n=13) | 3226 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 14 (n=32) | 18 (n=32) | 3015 (n=32) | 6 (n=13) | 7 (n=13) | 1621 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 7 (n=32) | 25 (n=32) | 1585 (n=32) | 3 (n=13) | 10 (n=13) | 870 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 6 (n=32) | 26 (n=32) | 650 (n=32) | 2 (n=13) | 11 (n=13) | 311 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=32) | 29 (n=32) | 314 (n=32) | 0 (n=13) | 13 (n=13) | 149 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 13 (n=32) | 19 (n=32) | 6086 (n=32) | 7 (n=13) | 6 (n=13) | 3199 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 10 (n=32) | 22 (n=32) | 3195 (n=32) | 5 (n=13) | 8 (n=13) | 1732 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 9 (n=32) | 23 (n=32) | 1615 (n=32) | 3 (n=13) | 10 (n=13) | 794 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 4 (n=32) | 28 (n=32) | 648 (n=32) | 0 (n=13) | 13 (n=13) | 291 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 4 (n=32) | 28 (n=32) | 300 (n=32) | 0 (n=13) | 13 (n=13) | 158 (n=13) |
| nieve | `nieve_24h_cm_pct` | p80 | 10 (n=13) | 3 (n=13) | 325 (n=13) | 9 (n=20) | 11 (n=20) | 141 (n=20) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=13) | 3 (n=13) | 298 (n=13) | 9 (n=20) | 11 (n=20) | 132 (n=20) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=13) | 3 (n=13) | 265 (n=13) | 9 (n=20) | 11 (n=20) | 113 (n=20) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=13) | 9 (n=13) | 186 (n=13) | 4 (n=20) | 16 (n=20) | 71 (n=20) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=13) | 11 (n=13) | 117 (n=13) | 3 (n=20) | 17 (n=20) | 41 (n=20) |
| nieve | `nieve_72h_cm_pct` | p80 | 12 (n=13) | 1 (n=13) | 702 (n=13) | 12 (n=20) | 8 (n=20) | 276 (n=20) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=13) | 2 (n=13) | 608 (n=13) | 11 (n=20) | 9 (n=20) | 236 (n=20) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=13) | 6 (n=13) | 450 (n=13) | 8 (n=20) | 12 (n=20) | 170 (n=20) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=13) | 10 (n=13) | 265 (n=13) | 4 (n=20) | 16 (n=20) | 84 (n=20) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=13) | 11 (n=13) | 162 (n=13) | 2 (n=20) | 18 (n=20) | 50 (n=20) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=13) | 2 (n=13) | 1271 (n=13) | 12 (n=20) | 8 (n=20) | 490 (n=20) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=13) | 7 (n=13) | 971 (n=13) | 9 (n=20) | 11 (n=20) | 359 (n=20) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=13) | 8 (n=13) | 658 (n=13) | 6 (n=20) | 14 (n=20) | 211 (n=20) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=13) | 11 (n=13) | 359 (n=13) | 3 (n=20) | 17 (n=20) | 100 (n=20) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=13) | 12 (n=13) | 181 (n=13) | 1 (n=20) | 19 (n=20) | 68 (n=20) |

## Solo fuentes estables

Eventos con punto crítico usados: aluvión 32, crecida 13 (lluvia 45), nieve 29.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 20 | 17.9 | 4.0 | 83 |
| aluvion | `lluvia_48h_mm` | 20 | 22.0 | 9.2 | 81 |
| aluvion | `lluvia_72h_mm` | 20 | 28.4 | 15.3 | 75 |
| aluvion | `lluvia_7d_mm` | 20 | 79.4 | 43.9 | 80 |
| aluvion | `lluvia_max_horaria_24h_mm` | 20 | 2.7 | 0.8 | 86 |
| aluvion | `lluvia_max_horaria_72h_mm` | 20 | 3.4 | 1.7 | 79 |
| crecida | `lluvia_24h_mm` | 8 | 12.3 | 4.0 | 82 |
| crecida | `lluvia_48h_mm` | 8 | 18.6 | 9.5 | 77 |
| crecida | `lluvia_72h_mm` | 8 | 24.6 | 15.8 | 71 |
| crecida | `lluvia_7d_mm` | 8 | 59.4 | 42.9 | 77 |
| crecida | `lluvia_max_horaria_24h_mm` | 8 | 2.5 | 0.9 | 78 |
| crecida | `lluvia_max_horaria_72h_mm` | 8 | 3.0 | 1.8 | 75 |
| nieve | `nieve_24h_cm` | 13 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 13 | 1.3 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 13 | 2.2 | 0.0 | 89 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 3.9 mm | 18 (n=23) | 5 (n=23) | 8482 (n=23) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 4459 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 6 mm | 18 (n=23) | 5 (n=23) | 6167 (n=23) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 3186 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 17.9 mm | 12 (n=23) | 11 (n=23) | 1419 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 695 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 34.2 mm | 5 (n=23) | 18 (n=23) | 350 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 159 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 14.8 mm | 18 (n=23) | 5 (n=23) | 5285 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2645 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 16.7 mm | 18 (n=23) | 5 (n=23) | 4617 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2283 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 22 mm | 11 (n=23) | 12 (n=23) | 3177 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1510 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 50.1 mm | 5 (n=23) | 18 (n=23) | 528 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 219 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 20.5 mm | 18 (n=23) | 5 (n=23) | 5995 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3022 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 24.9 mm | 16 (n=23) | 7 (n=23) | 4699 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2356 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 28.4 mm | 14 (n=23) | 9 (n=23) | 3886 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1953 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 54.5 mm | 5 (n=23) | 18 (n=23) | 1074 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 437 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 32.4 mm | 18 (n=23) | 5 (n=23) | 9131 (n=23) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 4868 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 48.6 mm | 15 (n=23) | 8 (n=23) | 6155 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3028 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 79.4 mm | 10 (n=23) | 13 (n=23) | 2744 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1212 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 116 mm | 6 (n=23) | 17 (n=23) | 870 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 381 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.8 mm | 19 (n=23) | 4 (n=23) | 9209 (n=23) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 4717 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.4 mm | 18 (n=23) | 5 (n=23) | 5424 (n=23) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 2710 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 2.7 mm | 13 (n=23) | 10 (n=23) | 2008 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 968 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 5.8 mm | 5 (n=23) | 18 (n=23) | 347 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 177 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.9 mm | 18 (n=23) | 5 (n=23) | 7571 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3866 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 17 (n=23) | 6 (n=23) | 7122 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3583 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.4 mm | 13 (n=23) | 10 (n=23) | 3088 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 1530 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.7 mm | 5 (n=23) | 18 (n=23) | 962 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 501 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 4.5 mm | 8 (n=9) | 1 (n=9) | 7708 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 4061 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 6.5 mm | 6 (n=9) | 3 (n=9) | 5741 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 2966 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 12.3 mm | 4 (n=9) | 5 (n=9) | 2696 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1297 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 24.2 mm | 2 (n=9) | 7 (n=9) | 787 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 380 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 9.7 mm | 8 (n=9) | 1 (n=9) | 7828 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 4114 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 10.1 mm | 8 (n=9) | 1 (n=9) | 7580 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3975 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 18.6 mm | 4 (n=9) | 5 (n=9) | 4025 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 1979 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 40.2 mm | 2 (n=9) | 7 (n=9) | 1020 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 431 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 16.3 mm | 7 (n=9) | 2 (n=9) | 7459 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3872 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 17.7 mm | 7 (n=9) | 2 (n=9) | 6928 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3531 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 24.6 mm | 6 (n=9) | 3 (n=9) | 4808 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2389 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 42.6 mm | 4 (n=9) | 5 (n=9) | 1965 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 869 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 40.5 mm | 7 (n=9) | 2 (n=9) | 7514 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3812 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 48.2 mm | 6 (n=9) | 3 (n=9) | 6243 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3059 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 59.4 mm | 4 (n=9) | 5 (n=9) | 4616 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2242 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 88.8 mm | 2 (n=9) | 7 (n=9) | 2113 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 900 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.8 mm | 8 (n=9) | 1 (n=9) | 9228 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 4723 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.1 mm | 8 (n=9) | 1 (n=9) | 7095 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3574 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.5 mm | 5 (n=9) | 4 (n=9) | 2350 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1141 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 3.1 mm | 3 (n=9) | 6 (n=9) | 1569 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 721 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 1.9 mm | 7 (n=9) | 2 (n=9) | 7591 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3875 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 2.2 mm | 7 (n=9) | 2 (n=9) | 6285 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3227 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 6 (n=9) | 3 (n=9) | 3944 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1923 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.4 mm | 5 (n=9) | 4 (n=9) | 1875 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 902 (n=4 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 9 (n=13) | 4 (n=13) | 272 (n=13) | 5 (n=16) | 11 (n=16) | 114 (n=16) |
| nieve | `nieve_24h_cm` | 0.2 cm | 8 (n=13) | 5 (n=13) | 233 (n=13) | 5 (n=16) | 11 (n=16) | 102 (n=16) |
| nieve | `nieve_24h_cm` | 1.1 cm | 5 (n=13) | 8 (n=13) | 80 (n=13) | 2 (n=16) | 14 (n=16) | 33 (n=16) |
| nieve | `nieve_72h_cm` | 0.1 cm | 11 (n=13) | 2 (n=13) | 643 (n=13) | 9 (n=16) | 7 (n=16) | 239 (n=16) |
| nieve | `nieve_72h_cm` | 0.8 cm | 8 (n=13) | 5 (n=13) | 312 (n=13) | 4 (n=16) | 12 (n=16) | 116 (n=16) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=13) | 7 (n=13) | 202 (n=13) | 2 (n=16) | 14 (n=16) | 80 (n=16) |
| nieve | `nieve_72h_cm` | 2.6 cm | 3 (n=13) | 10 (n=13) | 78 (n=13) | 1 (n=16) | 15 (n=16) | 36 (n=16) |
| nieve | `nieve_7d_cm` | 0.2 cm | 10 (n=13) | 3 (n=13) | 1140 (n=13) | 9 (n=16) | 7 (n=16) | 448 (n=16) |
| nieve | `nieve_7d_cm` | 0.9 cm | 9 (n=13) | 4 (n=13) | 636 (n=13) | 4 (n=16) | 12 (n=16) | 235 (n=16) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=13) | 7 (n=13) | 269 (n=13) | 2 (n=16) | 14 (n=16) | 88 (n=16) |
| nieve | `nieve_7d_cm` | 3.2 cm | 3 (n=13) | 10 (n=13) | 178 (n=13) | 0 (n=16) | 16 (n=16) | 66 (n=16) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 15 (n=23) | 8 (n=23) | 5799 (n=23) | 8 (n=9 muestra chica) | 1 (n=9 muestra chica) | 3342 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 11 (n=23) | 12 (n=23) | 3058 (n=23) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1713 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 7 (n=23) | 16 (n=23) | 1594 (n=23) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 910 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 5 (n=23) | 18 (n=23) | 666 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 386 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 4 (n=23) | 19 (n=23) | 310 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 171 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 11 (n=23) | 12 (n=23) | 6080 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3341 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 8 (n=23) | 15 (n=23) | 3148 (n=23) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 1745 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 6 (n=23) | 17 (n=23) | 1630 (n=23) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 904 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 5 (n=23) | 18 (n=23) | 664 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 330 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 2 (n=23) | 21 (n=23) | 308 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 162 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 8 (n=23) | 15 (n=23) | 6171 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3344 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 8 (n=23) | 15 (n=23) | 3222 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 1761 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 6 (n=23) | 17 (n=23) | 1648 (n=23) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 872 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 3 (n=23) | 20 (n=23) | 667 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 293 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 2 (n=23) | 21 (n=23) | 316 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 133 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 11 (n=23) | 12 (n=23) | 6440 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3542 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 8 (n=23) | 15 (n=23) | 3290 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 1756 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 3 (n=23) | 20 (n=23) | 1654 (n=23) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 823 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 3 (n=23) | 20 (n=23) | 657 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 296 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 3 (n=23) | 20 (n=23) | 304 (n=23) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 138 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 14 (n=23) | 9 (n=23) | 5797 (n=23) | 8 (n=9 muestra chica) | 1 (n=9 muestra chica) | 3228 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 12 (n=23) | 11 (n=23) | 3017 (n=23) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 1621 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 6 (n=23) | 17 (n=23) | 1586 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 870 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 5 (n=23) | 18 (n=23) | 651 (n=23) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 311 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=23) | 20 (n=23) | 314 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 149 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 10 (n=23) | 13 (n=23) | 6091 (n=23) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3199 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 7 (n=23) | 16 (n=23) | 3198 (n=23) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1732 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 6 (n=23) | 17 (n=23) | 1618 (n=23) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 794 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 3 (n=23) | 20 (n=23) | 649 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 291 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 3 (n=23) | 20 (n=23) | 301 (n=23) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 158 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p80 | 5 (n=9) | 4 (n=9) | 5814 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3352 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 1 (n=9) | 8 (n=9) | 3070 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1717 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 1 (n=9) | 8 (n=9) | 1602 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 911 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 1 (n=9) | 8 (n=9) | 672 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 386 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 314 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 171 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 4 (n=9) | 5 (n=9) | 6091 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3349 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 1 (n=9) | 8 (n=9) | 3159 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1751 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 1 (n=9) | 8 (n=9) | 1638 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 905 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 0 (n=9) | 9 (n=9) | 672 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 331 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 312 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 162 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 4 (n=9) | 5 (n=9) | 6179 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3355 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 3 (n=9) | 6 (n=9) | 3231 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1772 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 1 (n=9) | 8 (n=9) | 1656 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 878 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 0 (n=9) | 9 (n=9) | 672 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 294 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 318 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 133 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 3 (n=9) | 6 (n=9) | 6456 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3554 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 2 (n=9) | 7 (n=9) | 3300 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1766 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 2 (n=9) | 7 (n=9) | 1658 (n=9) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 825 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 1 (n=9) | 8 (n=9) | 662 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 298 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 308 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 140 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 6 (n=9) | 3 (n=9) | 5812 (n=9) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3238 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 2 (n=9) | 7 (n=9) | 3032 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1630 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 1 (n=9) | 8 (n=9) | 1595 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 873 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 1 (n=9) | 8 (n=9) | 657 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 313 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 0 (n=9) | 9 (n=9) | 319 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 149 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 3 (n=9) | 6 (n=9) | 6104 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 3212 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 3 (n=9) | 6 (n=9) | 3205 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1739 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 3 (n=9) | 6 (n=9) | 1624 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 797 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=9) | 8 (n=9) | 654 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 291 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=9) | 8 (n=9) | 306 (n=9) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 158 (n=4 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 10 (n=13) | 3 (n=13) | 325 (n=13) | 7 (n=16) | 9 (n=16) | 143 (n=16) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=13) | 3 (n=13) | 298 (n=13) | 7 (n=16) | 9 (n=16) | 134 (n=16) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=13) | 3 (n=13) | 265 (n=13) | 7 (n=16) | 9 (n=16) | 115 (n=16) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=13) | 9 (n=13) | 186 (n=13) | 3 (n=16) | 13 (n=16) | 72 (n=16) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=13) | 11 (n=13) | 117 (n=13) | 3 (n=16) | 13 (n=16) | 41 (n=16) |
| nieve | `nieve_72h_cm_pct` | p80 | 12 (n=13) | 1 (n=13) | 702 (n=13) | 10 (n=16) | 6 (n=16) | 279 (n=16) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=13) | 2 (n=13) | 608 (n=13) | 9 (n=16) | 7 (n=16) | 239 (n=16) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=13) | 6 (n=13) | 450 (n=13) | 6 (n=16) | 10 (n=16) | 173 (n=16) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=13) | 10 (n=13) | 265 (n=13) | 4 (n=16) | 12 (n=16) | 84 (n=16) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=13) | 11 (n=13) | 162 (n=13) | 2 (n=16) | 14 (n=16) | 50 (n=16) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=13) | 2 (n=13) | 1271 (n=13) | 9 (n=16) | 7 (n=16) | 495 (n=16) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=13) | 7 (n=13) | 971 (n=13) | 6 (n=16) | 10 (n=16) | 364 (n=16) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=13) | 8 (n=13) | 658 (n=13) | 5 (n=16) | 11 (n=16) | 213 (n=16) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=13) | 11 (n=13) | 359 (n=13) | 2 (n=16) | 14 (n=16) | 102 (n=16) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=13) | 12 (n=13) | 181 (n=13) | 1 (n=16) | 15 (n=16) | 68 (n=16) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 28 | 15.4 | 3.9 | 83 |
| lluvia | `lluvia_48h_mm` | 28 | 21.6 | 9.0 | 80 |
| lluvia | `lluvia_72h_mm` | 28 | 27.3 | 15.0 | 75 |
| lluvia | `lluvia_7d_mm` | 28 | 69.9 | 41.8 | 79 |
| lluvia | `lluvia_max_horaria_24h_mm` | 28 | 2.6 | 0.8 | 82 |
| lluvia | `lluvia_max_horaria_72h_mm` | 28 | 3.0 | 1.7 | 78 |
| nieve | `nieve_24h_cm` | 13 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 13 | 1.3 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 13 | 2.2 | 0.0 | 89 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 4 mm | 26 (n=32) | 6 (n=32) | 8343 (n=32) | 7 (n=13) | 6 (n=13) | 4390 (n=13) |
| lluvia | `lluvia_24h_mm` | 6 mm | 25 (n=32) | 7 (n=32) | 6157 (n=32) | 6 (n=13) | 7 (n=13) | 3182 (n=13) |
| lluvia | `lluvia_24h_mm` | 17.9 mm | 15 (n=32) | 17 (n=32) | 1415 (n=32) | 2 (n=13) | 11 (n=13) | 694 (n=13) |
| lluvia | `lluvia_24h_mm` | 30.9 mm | 8 (n=32) | 24 (n=32) | 472 (n=32) | 0 (n=13) | 13 (n=13) | 199 (n=13) |
| lluvia | `lluvia_48h_mm` | 9.7 mm | 27 (n=32) | 5 (n=32) | 7794 (n=32) | 7 (n=13) | 6 (n=13) | 4106 (n=13) |
| lluvia | `lluvia_48h_mm` | 16.2 mm | 22 (n=32) | 10 (n=32) | 4800 (n=32) | 5 (n=13) | 8 (n=13) | 2371 (n=13) |
| lluvia | `lluvia_48h_mm` | 21.6 mm | 15 (n=32) | 17 (n=32) | 3266 (n=32) | 2 (n=13) | 11 (n=13) | 1548 (n=13) |
| lluvia | `lluvia_48h_mm` | 47.6 mm | 7 (n=32) | 25 (n=32) | 624 (n=32) | 0 (n=13) | 13 (n=13) | 272 (n=13) |
| lluvia | `lluvia_72h_mm` | 16.3 mm | 25 (n=32) | 7 (n=32) | 7426 (n=32) | 5 (n=13) | 8 (n=13) | 3866 (n=13) |
| lluvia | `lluvia_72h_mm` | 23.4 mm | 22 (n=32) | 10 (n=32) | 5131 (n=32) | 5 (n=13) | 8 (n=13) | 2564 (n=13) |
| lluvia | `lluvia_72h_mm` | 27.3 mm | 20 (n=32) | 12 (n=32) | 4141 (n=32) | 2 (n=13) | 11 (n=13) | 2059 (n=13) |
| lluvia | `lluvia_72h_mm` | 53.1 mm | 9 (n=32) | 23 (n=32) | 1149 (n=32) | 0 (n=13) | 13 (n=13) | 482 (n=13) |
| lluvia | `lluvia_7d_mm` | 31.1 mm | 25 (n=32) | 7 (n=32) | 9428 (n=32) | 5 (n=13) | 8 (n=13) | 5068 (n=13) |
| lluvia | `lluvia_7d_mm` | 48.2 mm | 21 (n=32) | 11 (n=32) | 6215 (n=32) | 4 (n=13) | 9 (n=13) | 3054 (n=13) |
| lluvia | `lluvia_7d_mm` | 69.9 mm | 14 (n=32) | 18 (n=32) | 3523 (n=32) | 2 (n=13) | 11 (n=13) | 1635 (n=13) |
| lluvia | `lluvia_7d_mm` | 116 mm | 8 (n=32) | 24 (n=32) | 867 (n=32) | 1 (n=13) | 12 (n=13) | 379 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.8 mm | 27 (n=32) | 5 (n=32) | 9195 (n=32) | 8 (n=13) | 5 (n=13) | 4713 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.2 mm | 26 (n=32) | 6 (n=32) | 6478 (n=32) | 8 (n=13) | 5 (n=13) | 3226 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 2.7 mm | 17 (n=32) | 15 (n=32) | 2002 (n=32) | 1 (n=13) | 12 (n=13) | 967 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 5.2 mm | 7 (n=32) | 25 (n=32) | 487 (n=32) | 0 (n=13) | 13 (n=13) | 232 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.8 mm | 25 (n=32) | 7 (n=32) | 8014 (n=32) | 9 (n=13) | 4 (n=13) | 4099 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 2.1 mm | 23 (n=32) | 9 (n=32) | 6646 (n=32) | 7 (n=13) | 6 (n=13) | 3431 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 3 mm | 19 (n=32) | 13 (n=32) | 3924 (n=32) | 1 (n=13) | 12 (n=13) | 1923 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 5.2 mm | 10 (n=32) | 22 (n=32) | 1255 (n=32) | 0 (n=13) | 13 (n=13) | 618 (n=13) |
| nieve | `nieve_24h_cm` | 0.1 cm | 9 (n=13) | 4 (n=13) | 272 (n=13) | 5 (n=16) | 11 (n=16) | 114 (n=16) |
| nieve | `nieve_24h_cm` | 0.2 cm | 8 (n=13) | 5 (n=13) | 233 (n=13) | 5 (n=16) | 11 (n=16) | 102 (n=16) |
| nieve | `nieve_24h_cm` | 1.1 cm | 5 (n=13) | 8 (n=13) | 80 (n=13) | 2 (n=16) | 14 (n=16) | 33 (n=16) |
| nieve | `nieve_72h_cm` | 0.1 cm | 11 (n=13) | 2 (n=13) | 643 (n=13) | 9 (n=16) | 7 (n=16) | 239 (n=16) |
| nieve | `nieve_72h_cm` | 0.8 cm | 8 (n=13) | 5 (n=13) | 312 (n=13) | 4 (n=16) | 12 (n=16) | 116 (n=16) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=13) | 7 (n=13) | 202 (n=13) | 2 (n=16) | 14 (n=16) | 80 (n=16) |
| nieve | `nieve_72h_cm` | 2.6 cm | 3 (n=13) | 10 (n=13) | 78 (n=13) | 1 (n=16) | 15 (n=16) | 36 (n=16) |
| nieve | `nieve_7d_cm` | 0.2 cm | 10 (n=13) | 3 (n=13) | 1140 (n=13) | 9 (n=16) | 7 (n=16) | 448 (n=16) |
| nieve | `nieve_7d_cm` | 0.9 cm | 9 (n=13) | 4 (n=13) | 636 (n=13) | 4 (n=16) | 12 (n=16) | 235 (n=16) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=13) | 7 (n=13) | 269 (n=13) | 2 (n=16) | 14 (n=16) | 88 (n=16) |
| nieve | `nieve_7d_cm` | 3.2 cm | 3 (n=13) | 10 (n=13) | 178 (n=13) | 0 (n=16) | 16 (n=16) | 66 (n=16) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 20 (n=32) | 12 (n=32) | 5793 (n=32) | 10 (n=13) | 3 (n=13) | 3339 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 12 (n=32) | 20 (n=32) | 3057 (n=32) | 6 (n=13) | 7 (n=13) | 1711 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 8 (n=32) | 24 (n=32) | 1593 (n=32) | 3 (n=13) | 10 (n=13) | 909 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 6 (n=32) | 26 (n=32) | 665 (n=32) | 0 (n=13) | 13 (n=13) | 386 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 4 (n=32) | 28 (n=32) | 310 (n=32) | 0 (n=13) | 13 (n=13) | 171 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 15 (n=32) | 17 (n=32) | 6075 (n=32) | 9 (n=13) | 4 (n=13) | 3337 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 9 (n=32) | 23 (n=32) | 3147 (n=32) | 7 (n=13) | 6 (n=13) | 1743 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 7 (n=32) | 25 (n=32) | 1629 (n=32) | 3 (n=13) | 10 (n=13) | 903 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 5 (n=32) | 27 (n=32) | 664 (n=32) | 1 (n=13) | 12 (n=13) | 330 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 2 (n=32) | 30 (n=32) | 308 (n=32) | 0 (n=13) | 13 (n=13) | 162 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 12 (n=32) | 20 (n=32) | 6165 (n=32) | 8 (n=13) | 5 (n=13) | 3342 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 11 (n=32) | 21 (n=32) | 3219 (n=32) | 8 (n=13) | 5 (n=13) | 1760 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 7 (n=32) | 25 (n=32) | 1647 (n=32) | 4 (n=13) | 9 (n=13) | 872 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 3 (n=32) | 29 (n=32) | 667 (n=32) | 1 (n=13) | 12 (n=13) | 293 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 2 (n=32) | 30 (n=32) | 316 (n=32) | 0 (n=13) | 13 (n=13) | 133 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 14 (n=32) | 18 (n=32) | 6436 (n=32) | 8 (n=13) | 5 (n=13) | 3540 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 10 (n=32) | 22 (n=32) | 3288 (n=32) | 8 (n=13) | 5 (n=13) | 1754 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 5 (n=32) | 27 (n=32) | 1652 (n=32) | 3 (n=13) | 10 (n=13) | 821 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 4 (n=32) | 28 (n=32) | 656 (n=32) | 1 (n=13) | 12 (n=13) | 296 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 3 (n=32) | 29 (n=32) | 304 (n=32) | 1 (n=13) | 12 (n=13) | 138 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 20 (n=32) | 12 (n=32) | 5790 (n=32) | 10 (n=13) | 3 (n=13) | 3226 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 14 (n=32) | 18 (n=32) | 3015 (n=32) | 6 (n=13) | 7 (n=13) | 1621 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 7 (n=32) | 25 (n=32) | 1585 (n=32) | 3 (n=13) | 10 (n=13) | 870 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 6 (n=32) | 26 (n=32) | 650 (n=32) | 2 (n=13) | 11 (n=13) | 311 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=32) | 29 (n=32) | 314 (n=32) | 0 (n=13) | 13 (n=13) | 149 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 13 (n=32) | 19 (n=32) | 6086 (n=32) | 7 (n=13) | 6 (n=13) | 3199 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 10 (n=32) | 22 (n=32) | 3195 (n=32) | 5 (n=13) | 8 (n=13) | 1732 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 9 (n=32) | 23 (n=32) | 1615 (n=32) | 3 (n=13) | 10 (n=13) | 794 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 4 (n=32) | 28 (n=32) | 648 (n=32) | 0 (n=13) | 13 (n=13) | 291 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 4 (n=32) | 28 (n=32) | 300 (n=32) | 0 (n=13) | 13 (n=13) | 158 (n=13) |
| nieve | `nieve_24h_cm_pct` | p80 | 10 (n=13) | 3 (n=13) | 325 (n=13) | 7 (n=16) | 9 (n=16) | 143 (n=16) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=13) | 3 (n=13) | 298 (n=13) | 7 (n=16) | 9 (n=16) | 134 (n=16) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=13) | 3 (n=13) | 265 (n=13) | 7 (n=16) | 9 (n=16) | 115 (n=16) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=13) | 9 (n=13) | 186 (n=13) | 3 (n=16) | 13 (n=16) | 72 (n=16) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=13) | 11 (n=13) | 117 (n=13) | 3 (n=16) | 13 (n=16) | 41 (n=16) |
| nieve | `nieve_72h_cm_pct` | p80 | 12 (n=13) | 1 (n=13) | 702 (n=13) | 10 (n=16) | 6 (n=16) | 279 (n=16) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=13) | 2 (n=13) | 608 (n=13) | 9 (n=16) | 7 (n=16) | 239 (n=16) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=13) | 6 (n=13) | 450 (n=13) | 6 (n=16) | 10 (n=16) | 173 (n=16) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=13) | 10 (n=13) | 265 (n=13) | 4 (n=16) | 12 (n=16) | 84 (n=16) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=13) | 11 (n=13) | 162 (n=13) | 2 (n=16) | 14 (n=16) | 50 (n=16) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=13) | 2 (n=13) | 1271 (n=13) | 9 (n=16) | 7 (n=16) | 495 (n=16) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=13) | 7 (n=13) | 971 (n=13) | 6 (n=16) | 10 (n=16) | 364 (n=16) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=13) | 8 (n=13) | 658 (n=13) | 5 (n=16) | 11 (n=16) | 213 (n=16) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=13) | 11 (n=13) | 359 (n=13) | 2 (n=16) | 14 (n=16) | 102 (n=16) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=13) | 12 (n=13) | 181 (n=13) | 1 (n=16) | 15 (n=16) | 68 (n=16) |

## Todas las fuentes: nieve en Paso de Jama por lado

Eventos de nieve en `rn52_paso_jama`: 29 (AR 1, ambos 3, CL 19, lado desconocido 6, que quedan fuera de esta sección).

Falta el clima de `ch27_alto`: CL y combinado quedan sin datos.

### Nieve AR o ambos (clima de rn52_paso_jama)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 1 | 0.1 | 0.0 | 97 |
| nieve | `nieve_72h_cm` | 1 | 0.1 | 0.0 | 92 |
| nieve | `nieve_7d_cm` | 1 | 0.1 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=1) | 0 (n=1) | 142 (n=1) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 81 (n=3 muestra chica) |
| nieve | `nieve_72h_cm` | 0.1 cm | 1 (n=1) | 0 (n=1) | 308 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 156 (n=3 muestra chica) |
| nieve | `nieve_7d_cm` | 0.1 cm | 1 (n=1) | 0 (n=1) | 556 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 284 (n=3 muestra chica) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=1) | 0 (n=1) | 168 (n=1) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 93 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=1) | 0 (n=1) | 141 (n=1) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 84 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=1) | 0 (n=1) | 106 (n=1) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 65 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=1) | 1 (n=1) | 53 (n=1) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 34 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=1) | 1 (n=1) | 24 (n=1) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 21 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p80 | 1 (n=1) | 0 (n=1) | 311 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 153 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p90 | 1 (n=1) | 0 (n=1) | 225 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 115 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=1) | 1 (n=1) | 126 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 77 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=1) | 1 (n=1) | 52 (n=1) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 33 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=1) | 1 (n=1) | 26 (n=1) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 19 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p80 | 1 (n=1) | 0 (n=1) | 441 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 220 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=1) | 1 (n=1) | 262 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 150 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=1) | 1 (n=1) | 129 (n=1) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 90 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=1) | 1 (n=1) | 53 (n=1) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 42 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=1) | 1 (n=1) | 27 (n=1) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 29 (n=3 muestra chica) |

### Nieve CL (clima de ch27_alto)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0 | — | — | — |
| nieve | `nieve_72h_cm` | 0 | — | — | — |
| nieve | `nieve_7d_cm` | 0 | — | — | — |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

Sin candidatos (no hay eventos de esta causa con punto en el período de ajuste).

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_24h_cm_pct` | p90 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_24h_cm_pct` | p95 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_72h_cm_pct` | p80 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_72h_cm_pct` | p90 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_7d_cm_pct` | p80 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=10) | 10 (n=10) | 0 (n=10) |

### Nieve combinado (AR + ambos + CL)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 1 | 0.1 | 0.0 | 97 |
| nieve | `nieve_72h_cm` | 1 | 0.1 | 0.0 | 92 |
| nieve | `nieve_7d_cm` | 1 | 0.1 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=10) | 9 (n=10) | 142 (n=10) | 1 (n=13) | 12 (n=13) | 81 (n=13) |
| nieve | `nieve_72h_cm` | 0.1 cm | 1 (n=10) | 9 (n=10) | 308 (n=10) | 3 (n=13) | 10 (n=13) | 156 (n=13) |
| nieve | `nieve_7d_cm` | 0.1 cm | 1 (n=10) | 9 (n=10) | 556 (n=10) | 3 (n=13) | 10 (n=13) | 284 (n=13) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=10) | 9 (n=10) | 168 (n=10) | 2 (n=13) | 11 (n=13) | 93 (n=13) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=10) | 9 (n=10) | 141 (n=10) | 2 (n=13) | 11 (n=13) | 84 (n=13) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=10) | 9 (n=10) | 106 (n=10) | 2 (n=13) | 11 (n=13) | 65 (n=13) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=10) | 10 (n=10) | 53 (n=10) | 1 (n=13) | 12 (n=13) | 34 (n=13) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=10) | 10 (n=10) | 24 (n=10) | 1 (n=13) | 12 (n=13) | 21 (n=13) |
| nieve | `nieve_72h_cm_pct` | p80 | 1 (n=10) | 9 (n=10) | 311 (n=10) | 3 (n=13) | 10 (n=13) | 153 (n=13) |
| nieve | `nieve_72h_cm_pct` | p90 | 1 (n=10) | 9 (n=10) | 225 (n=10) | 3 (n=13) | 10 (n=13) | 115 (n=13) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=10) | 10 (n=10) | 126 (n=10) | 3 (n=13) | 10 (n=13) | 77 (n=13) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=10) | 10 (n=10) | 52 (n=10) | 1 (n=13) | 12 (n=13) | 33 (n=13) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=10) | 10 (n=10) | 26 (n=10) | 0 (n=13) | 13 (n=13) | 19 (n=13) |
| nieve | `nieve_7d_cm_pct` | p80 | 1 (n=10) | 9 (n=10) | 441 (n=10) | 3 (n=13) | 10 (n=13) | 220 (n=13) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=10) | 10 (n=10) | 262 (n=10) | 3 (n=13) | 10 (n=13) | 150 (n=13) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=10) | 10 (n=10) | 129 (n=10) | 2 (n=13) | 11 (n=13) | 90 (n=13) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=10) | 10 (n=10) | 53 (n=10) | 0 (n=13) | 13 (n=13) | 42 (n=13) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=10) | 10 (n=10) | 27 (n=10) | 0 (n=13) | 13 (n=13) | 29 (n=13) |


## Solo fuentes estables: nieve en Paso de Jama por lado

Eventos de nieve en `rn52_paso_jama`: 26 (AR 1, ambos 3, CL 17, lado desconocido 5, que quedan fuera de esta sección).

Falta el clima de `ch27_alto`: CL y combinado quedan sin datos.

### Nieve AR o ambos (clima de rn52_paso_jama)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 1 | 0.1 | 0.0 | 97 |
| nieve | `nieve_72h_cm` | 1 | 0.1 | 0.0 | 92 |
| nieve | `nieve_7d_cm` | 1 | 0.1 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=1) | 0 (n=1) | 142 (n=1) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 81 (n=3 muestra chica) |
| nieve | `nieve_72h_cm` | 0.1 cm | 1 (n=1) | 0 (n=1) | 308 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 156 (n=3 muestra chica) |
| nieve | `nieve_7d_cm` | 0.1 cm | 1 (n=1) | 0 (n=1) | 556 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 284 (n=3 muestra chica) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=1) | 0 (n=1) | 168 (n=1) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 93 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=1) | 0 (n=1) | 141 (n=1) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 84 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=1) | 0 (n=1) | 106 (n=1) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 65 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=1) | 1 (n=1) | 53 (n=1) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 34 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=1) | 1 (n=1) | 24 (n=1) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 21 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p80 | 1 (n=1) | 0 (n=1) | 311 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 153 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p90 | 1 (n=1) | 0 (n=1) | 225 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 115 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=1) | 1 (n=1) | 126 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 77 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=1) | 1 (n=1) | 52 (n=1) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 33 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=1) | 1 (n=1) | 26 (n=1) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 19 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p80 | 1 (n=1) | 0 (n=1) | 441 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 220 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=1) | 1 (n=1) | 262 (n=1) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 150 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=1) | 1 (n=1) | 129 (n=1) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 90 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=1) | 1 (n=1) | 53 (n=1) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 42 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=1) | 1 (n=1) | 27 (n=1) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 29 (n=3 muestra chica) |

### Nieve CL (clima de ch27_alto)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0 | — | — | — |
| nieve | `nieve_72h_cm` | 0 | — | — | — |
| nieve | `nieve_7d_cm` | 0 | — | — | — |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

Sin candidatos (no hay eventos de esta causa con punto en el período de ajuste).

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p90 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p95 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p80 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p90 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p80 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=9) | 9 (n=9) | 0 (n=9) | 0 (n=8 muestra chica) | 8 (n=8 muestra chica) | 0 (n=8 muestra chica) |

### Nieve combinado (AR + ambos + CL)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 1 | 0.1 | 0.0 | 97 |
| nieve | `nieve_72h_cm` | 1 | 0.1 | 0.0 | 92 |
| nieve | `nieve_7d_cm` | 1 | 0.1 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=10) | 9 (n=10) | 142 (n=10) | 1 (n=11) | 10 (n=11) | 81 (n=11) |
| nieve | `nieve_72h_cm` | 0.1 cm | 1 (n=10) | 9 (n=10) | 308 (n=10) | 3 (n=11) | 8 (n=11) | 156 (n=11) |
| nieve | `nieve_7d_cm` | 0.1 cm | 1 (n=10) | 9 (n=10) | 556 (n=10) | 3 (n=11) | 8 (n=11) | 284 (n=11) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=10) | 9 (n=10) | 168 (n=10) | 2 (n=11) | 9 (n=11) | 93 (n=11) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=10) | 9 (n=10) | 141 (n=10) | 2 (n=11) | 9 (n=11) | 84 (n=11) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=10) | 9 (n=10) | 106 (n=10) | 2 (n=11) | 9 (n=11) | 65 (n=11) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=10) | 10 (n=10) | 53 (n=10) | 1 (n=11) | 10 (n=11) | 34 (n=11) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=10) | 10 (n=10) | 24 (n=10) | 1 (n=11) | 10 (n=11) | 21 (n=11) |
| nieve | `nieve_72h_cm_pct` | p80 | 1 (n=10) | 9 (n=10) | 311 (n=10) | 3 (n=11) | 8 (n=11) | 153 (n=11) |
| nieve | `nieve_72h_cm_pct` | p90 | 1 (n=10) | 9 (n=10) | 225 (n=10) | 3 (n=11) | 8 (n=11) | 115 (n=11) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=10) | 10 (n=10) | 126 (n=10) | 3 (n=11) | 8 (n=11) | 77 (n=11) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=10) | 10 (n=10) | 52 (n=10) | 1 (n=11) | 10 (n=11) | 33 (n=11) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=10) | 10 (n=10) | 26 (n=10) | 0 (n=11) | 11 (n=11) | 19 (n=11) |
| nieve | `nieve_7d_cm_pct` | p80 | 1 (n=10) | 9 (n=10) | 441 (n=10) | 3 (n=11) | 8 (n=11) | 220 (n=11) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=10) | 10 (n=10) | 262 (n=10) | 3 (n=11) | 8 (n=11) | 150 (n=11) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=10) | 10 (n=10) | 129 (n=10) | 2 (n=11) | 9 (n=11) | 90 (n=11) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=10) | 10 (n=10) | 53 (n=10) | 0 (n=11) | 11 (n=11) | 42 (n=11) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=10) | 10 (n=10) | 27 (n=10) | 0 (n=11) | 11 (n=11) | 29 (n=11) |
