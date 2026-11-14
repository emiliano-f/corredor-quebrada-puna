# Validación de umbrales

> Generado: 2026-11-14 15:34 UTC · versión `0.1.0.dev0` · commit `7b22818` · SCHEMA_VERSION 3 · fuentes `b3dab32ad1adf821`

Causas meteorológicas: aluvión y crecida contra lluvia, nieve contra nieve. Una regla por causa, igual para todos los puntos; ajuste 2016–2022, prueba 2023→hoy. Acierto = evento con alarma ese día o el anterior; falsa alarma = día con alarma sin evento ese día o el siguiente. Los mm de ERA5 no son lluvia local (ver docs/DATOS.md): por eso cada variable va también como percentil de su celda en la misma estación. Cada sección trae también la variante con aluvión y crecida juntos como una sola causa "lluvia". Junto a cada número va n = días-evento (punto, fecha) del período en que se basa; en prueba, n < 10 se marca "muestra chica". Vos elegís la regla final.

Fuentes estables (archivo desde ≤ 2016-01-01): elsubmarino, eltribunojujuy, jujuyaldia, jujuyalmomento, todojujuy.

## Todas las fuentes

Eventos con punto crítico usados: aluvión 33, crecida 11 (lluvia 44), nieve 34.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 20 | 17.9 | 4.0 | 83 |
| aluvion | `lluvia_48h_mm` | 20 | 22.0 | 9.2 | 81 |
| aluvion | `lluvia_72h_mm` | 20 | 28.4 | 15.3 | 75 |
| aluvion | `lluvia_7d_mm` | 20 | 79.4 | 43.9 | 80 |
| aluvion | `lluvia_max_horaria_24h_mm` | 20 | 2.7 | 0.8 | 86 |
| aluvion | `lluvia_max_horaria_72h_mm` | 20 | 3.4 | 1.7 | 79 |
| crecida | `lluvia_24h_mm` | 7 | 13.0 | 4.9 | 86 |
| crecida | `lluvia_48h_mm` | 7 | 23.2 | 11.7 | 72 |
| crecida | `lluvia_72h_mm` | 7 | 24.9 | 19.4 | 67 |
| crecida | `lluvia_7d_mm` | 7 | 69.2 | 50.0 | 78 |
| crecida | `lluvia_max_horaria_24h_mm` | 7 | 2.5 | 1.0 | 79 |
| crecida | `lluvia_max_horaria_72h_mm` | 7 | 3.1 | 1.9 | 74 |
| nieve | `nieve_24h_cm` | 14 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 14 | 1.2 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 14 | 1.7 | 0.0 | 89 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 3.9 mm | 18 (n=24) | 6 (n=24) | 8482 (n=24) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 4459 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 6 mm | 18 (n=24) | 6 (n=24) | 6167 (n=24) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 3186 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 17.9 mm | 12 (n=24) | 12 (n=24) | 1419 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 695 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 34.2 mm | 5 (n=24) | 19 (n=24) | 350 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 159 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 14.8 mm | 18 (n=24) | 6 (n=24) | 5285 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2645 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 16.7 mm | 18 (n=24) | 6 (n=24) | 4617 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2283 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 22 mm | 11 (n=24) | 13 (n=24) | 3177 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1510 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 50.1 mm | 5 (n=24) | 19 (n=24) | 528 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 219 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 20.5 mm | 18 (n=24) | 6 (n=24) | 5995 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3022 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 24.9 mm | 16 (n=24) | 8 (n=24) | 4699 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2356 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 28.4 mm | 14 (n=24) | 10 (n=24) | 3886 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1953 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 54.5 mm | 5 (n=24) | 19 (n=24) | 1074 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 437 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 32.4 mm | 18 (n=24) | 6 (n=24) | 9131 (n=24) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 4868 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 48.6 mm | 15 (n=24) | 9 (n=24) | 6155 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3028 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 79.4 mm | 10 (n=24) | 14 (n=24) | 2744 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1212 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 116 mm | 6 (n=24) | 18 (n=24) | 870 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 381 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.8 mm | 19 (n=24) | 5 (n=24) | 9209 (n=24) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 4717 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.4 mm | 18 (n=24) | 6 (n=24) | 5424 (n=24) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 2710 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 2.7 mm | 13 (n=24) | 11 (n=24) | 2008 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 968 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 5.8 mm | 5 (n=24) | 19 (n=24) | 347 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 177 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.9 mm | 18 (n=24) | 6 (n=24) | 7571 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3866 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 17 (n=24) | 7 (n=24) | 7122 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3583 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.4 mm | 13 (n=24) | 11 (n=24) | 3088 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 1530 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.7 mm | 5 (n=24) | 19 (n=24) | 962 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 501 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 6.1 mm | 6 (n=7) | 1 (n=7) | 6093 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3131 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 9.4 mm | 5 (n=7) | 2 (n=7) | 3873 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 1854 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 13 mm | 3 (n=7) | 4 (n=7) | 2484 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1205 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 24.3 mm | 2 (n=7) | 5 (n=7) | 777 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 376 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 9.6 mm | 7 (n=7) | 0 (n=7) | 7897 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 4150 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 12 mm | 6 (n=7) | 1 (n=7) | 6557 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3335 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 23.2 mm | 4 (n=7) | 3 (n=7) | 2916 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1390 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 42.4 mm | 2 (n=7) | 5 (n=7) | 906 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 369 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 17.6 mm | 7 (n=7) | 0 (n=7) | 6952 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3549 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 21.2 mm | 7 (n=7) | 0 (n=7) | 5787 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 2899 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 24.9 mm | 5 (n=7) | 2 (n=7) | 4718 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2359 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 46.1 mm | 4 (n=7) | 3 (n=7) | 1673 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 725 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 48 mm | 6 (n=7) | 1 (n=7) | 6275 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3072 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 49 mm | 6 (n=7) | 1 (n=7) | 6123 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3009 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 69.2 mm | 4 (n=7) | 3 (n=7) | 3611 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1665 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 106.9 mm | 2 (n=7) | 5 (n=7) | 1208 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 506 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1 mm | 7 (n=7) | 0 (n=7) | 7778 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3941 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.9 mm | 5 (n=7) | 2 (n=7) | 3659 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1819 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.5 mm | 5 (n=7) | 2 (n=7) | 2350 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1141 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 3.6 mm | 3 (n=7) | 4 (n=7) | 1138 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 551 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 1.9 mm | 6 (n=7) | 1 (n=7) | 7593 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3875 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 2.5 mm | 6 (n=7) | 1 (n=7) | 5269 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2632 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3.1 mm | 5 (n=7) | 2 (n=7) | 3687 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1771 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.5 mm | 4 (n=7) | 3 (n=7) | 1815 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 854 (n=4 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 9 (n=14) | 5 (n=14) | 272 (n=14) | 7 (n=20) | 13 (n=20) | 112 (n=20) |
| nieve | `nieve_24h_cm` | 0.2 cm | 8 (n=14) | 6 (n=14) | 233 (n=14) | 7 (n=20) | 13 (n=20) | 100 (n=20) |
| nieve | `nieve_24h_cm` | 1.1 cm | 5 (n=14) | 9 (n=14) | 80 (n=14) | 3 (n=20) | 17 (n=20) | 32 (n=20) |
| nieve | `nieve_72h_cm` | 0.1 cm | 11 (n=14) | 3 (n=14) | 643 (n=14) | 11 (n=20) | 9 (n=20) | 236 (n=20) |
| nieve | `nieve_72h_cm` | 0.8 cm | 8 (n=14) | 6 (n=14) | 312 (n=14) | 6 (n=20) | 14 (n=20) | 113 (n=20) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=14) | 8 (n=14) | 202 (n=14) | 3 (n=20) | 17 (n=20) | 78 (n=20) |
| nieve | `nieve_72h_cm` | 2.6 cm | 3 (n=14) | 11 (n=14) | 78 (n=14) | 1 (n=20) | 19 (n=20) | 36 (n=20) |
| nieve | `nieve_7d_cm` | 0.2 cm | 10 (n=14) | 4 (n=14) | 1140 (n=14) | 12 (n=20) | 8 (n=20) | 443 (n=20) |
| nieve | `nieve_7d_cm` | 0.9 cm | 9 (n=14) | 5 (n=14) | 636 (n=14) | 6 (n=20) | 14 (n=20) | 232 (n=20) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=14) | 8 (n=14) | 269 (n=14) | 2 (n=20) | 18 (n=20) | 88 (n=20) |
| nieve | `nieve_7d_cm` | 3.2 cm | 3 (n=14) | 11 (n=14) | 178 (n=14) | 0 (n=20) | 20 (n=20) | 66 (n=20) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 15 (n=24) | 9 (n=24) | 5799 (n=24) | 8 (n=9 muestra chica) | 1 (n=9 muestra chica) | 3342 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 11 (n=24) | 13 (n=24) | 3058 (n=24) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1713 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 7 (n=24) | 17 (n=24) | 1594 (n=24) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 910 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 5 (n=24) | 19 (n=24) | 666 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 386 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 4 (n=24) | 20 (n=24) | 310 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 171 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 11 (n=24) | 13 (n=24) | 6080 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3341 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3148 (n=24) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 1745 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1630 (n=24) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 904 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 5 (n=24) | 19 (n=24) | 664 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 330 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 308 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 162 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 8 (n=24) | 16 (n=24) | 6171 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3344 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3222 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 1761 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1648 (n=24) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 872 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 667 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 293 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 316 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 133 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 11 (n=24) | 13 (n=24) | 6440 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3542 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3290 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 1756 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 3 (n=24) | 21 (n=24) | 1654 (n=24) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 823 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 657 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 296 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 304 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 138 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 14 (n=24) | 10 (n=24) | 5797 (n=24) | 8 (n=9 muestra chica) | 1 (n=9 muestra chica) | 3228 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 12 (n=24) | 12 (n=24) | 3017 (n=24) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 1621 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1586 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 870 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 5 (n=24) | 19 (n=24) | 651 (n=24) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 311 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 314 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 149 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 10 (n=24) | 14 (n=24) | 6091 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3199 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 7 (n=24) | 17 (n=24) | 3198 (n=24) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1732 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1618 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 794 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 649 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 291 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 301 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 158 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p80 | 4 (n=7) | 3 (n=7) | 5815 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3352 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 1 (n=7) | 6 (n=7) | 3070 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1717 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 1 (n=7) | 6 (n=7) | 1602 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 911 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 1 (n=7) | 6 (n=7) | 672 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 386 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 314 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 171 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 3 (n=7) | 4 (n=7) | 6093 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3349 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 1 (n=7) | 6 (n=7) | 3159 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1751 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 1 (n=7) | 6 (n=7) | 1638 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 905 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 0 (n=7) | 7 (n=7) | 672 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 331 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 312 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 162 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 3 (n=7) | 4 (n=7) | 6181 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3355 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 3 (n=7) | 4 (n=7) | 3231 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1772 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 1 (n=7) | 6 (n=7) | 1656 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 878 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 0 (n=7) | 7 (n=7) | 672 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 294 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 318 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 133 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 3 (n=7) | 4 (n=7) | 6456 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3554 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 2 (n=7) | 5 (n=7) | 3300 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1766 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 2 (n=7) | 5 (n=7) | 1658 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 825 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 1 (n=7) | 6 (n=7) | 662 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 298 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 308 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 140 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 5 (n=7) | 2 (n=7) | 5813 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3238 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 1 (n=7) | 6 (n=7) | 3033 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1630 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 1 (n=7) | 6 (n=7) | 1595 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 873 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 1 (n=7) | 6 (n=7) | 657 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 313 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 319 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 149 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 3 (n=7) | 4 (n=7) | 6104 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 3212 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 3 (n=7) | 4 (n=7) | 3205 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1739 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 3 (n=7) | 4 (n=7) | 1624 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 797 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=7) | 6 (n=7) | 654 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 291 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=7) | 6 (n=7) | 306 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 158 (n=4 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 10 (n=14) | 4 (n=14) | 325 (n=14) | 9 (n=20) | 11 (n=20) | 141 (n=20) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=14) | 4 (n=14) | 298 (n=14) | 9 (n=20) | 11 (n=20) | 132 (n=20) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=14) | 4 (n=14) | 265 (n=14) | 9 (n=20) | 11 (n=20) | 113 (n=20) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=14) | 10 (n=14) | 186 (n=14) | 4 (n=20) | 16 (n=20) | 71 (n=20) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 117 (n=14) | 3 (n=20) | 17 (n=20) | 41 (n=20) |
| nieve | `nieve_72h_cm_pct` | p80 | 12 (n=14) | 2 (n=14) | 702 (n=14) | 12 (n=20) | 8 (n=20) | 276 (n=20) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=14) | 3 (n=14) | 608 (n=14) | 11 (n=20) | 9 (n=20) | 236 (n=20) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=14) | 7 (n=14) | 450 (n=14) | 8 (n=20) | 12 (n=20) | 170 (n=20) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=14) | 11 (n=14) | 265 (n=14) | 4 (n=20) | 16 (n=20) | 84 (n=20) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 162 (n=14) | 2 (n=20) | 18 (n=20) | 50 (n=20) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 1271 (n=14) | 12 (n=20) | 8 (n=20) | 490 (n=20) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=14) | 8 (n=14) | 971 (n=14) | 9 (n=20) | 11 (n=20) | 359 (n=20) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=14) | 9 (n=14) | 658 (n=14) | 6 (n=20) | 14 (n=20) | 211 (n=20) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=14) | 12 (n=14) | 359 (n=14) | 3 (n=20) | 17 (n=20) | 100 (n=20) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=14) | 13 (n=14) | 181 (n=14) | 1 (n=20) | 19 (n=20) | 68 (n=20) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 27 | 17.9 | 3.9 | 85 |
| lluvia | `lluvia_48h_mm` | 27 | 23.2 | 9.0 | 78 |
| lluvia | `lluvia_72h_mm` | 27 | 27.3 | 15.0 | 74 |
| lluvia | `lluvia_7d_mm` | 27 | 70.6 | 41.8 | 79 |
| lluvia | `lluvia_max_horaria_24h_mm` | 27 | 2.7 | 0.8 | 85 |
| lluvia | `lluvia_max_horaria_72h_mm` | 27 | 3.1 | 1.7 | 78 |
| nieve | `nieve_24h_cm` | 14 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 14 | 1.2 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 14 | 1.7 | 0.0 | 89 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 4.4 mm | 25 (n=31) | 6 (n=31) | 7816 (n=31) | 6 (n=13) | 7 (n=13) | 4129 (n=13) |
| lluvia | `lluvia_24h_mm` | 6.5 mm | 24 (n=31) | 7 (n=31) | 5713 (n=31) | 6 (n=13) | 7 (n=13) | 2962 (n=13) |
| lluvia | `lluvia_24h_mm` | 17.9 mm | 15 (n=31) | 16 (n=31) | 1415 (n=31) | 2 (n=13) | 11 (n=13) | 694 (n=13) |
| lluvia | `lluvia_24h_mm` | 32.4 mm | 7 (n=31) | 24 (n=31) | 407 (n=31) | 0 (n=13) | 13 (n=13) | 176 (n=13) |
| lluvia | `lluvia_48h_mm` | 9.6 mm | 26 (n=31) | 5 (n=31) | 7863 (n=31) | 7 (n=13) | 6 (n=13) | 4142 (n=13) |
| lluvia | `lluvia_48h_mm` | 16.4 mm | 22 (n=31) | 9 (n=31) | 4724 (n=31) | 5 (n=13) | 8 (n=13) | 2345 (n=13) |
| lluvia | `lluvia_48h_mm` | 23.2 mm | 15 (n=31) | 16 (n=31) | 2899 (n=31) | 2 (n=13) | 11 (n=13) | 1389 (n=13) |
| lluvia | `lluvia_48h_mm` | 48.4 mm | 7 (n=31) | 24 (n=31) | 594 (n=31) | 0 (n=13) | 13 (n=13) | 253 (n=13) |
| lluvia | `lluvia_72h_mm` | 17.6 mm | 25 (n=31) | 6 (n=31) | 6919 (n=31) | 5 (n=13) | 8 (n=13) | 3543 (n=13) |
| lluvia | `lluvia_72h_mm` | 24.1 mm | 22 (n=31) | 9 (n=31) | 4902 (n=31) | 4 (n=13) | 9 (n=13) | 2454 (n=13) |
| lluvia | `lluvia_72h_mm` | 27.3 mm | 20 (n=31) | 11 (n=31) | 4141 (n=31) | 2 (n=13) | 11 (n=13) | 2059 (n=13) |
| lluvia | `lluvia_72h_mm` | 53.2 mm | 9 (n=31) | 22 (n=31) | 1147 (n=31) | 0 (n=13) | 13 (n=13) | 477 (n=13) |
| lluvia | `lluvia_7d_mm` | 33.4 mm | 24 (n=31) | 7 (n=31) | 8909 (n=31) | 5 (n=13) | 8 (n=13) | 4735 (n=13) |
| lluvia | `lluvia_7d_mm` | 49 mm | 21 (n=31) | 10 (n=31) | 6095 (n=31) | 4 (n=13) | 9 (n=13) | 3004 (n=13) |
| lluvia | `lluvia_7d_mm` | 70.6 mm | 14 (n=31) | 17 (n=31) | 3470 (n=31) | 2 (n=13) | 11 (n=13) | 1606 (n=13) |
| lluvia | `lluvia_7d_mm` | 116 mm | 8 (n=31) | 23 (n=31) | 867 (n=31) | 1 (n=13) | 12 (n=13) | 379 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.8 mm | 26 (n=31) | 5 (n=31) | 9197 (n=31) | 8 (n=13) | 5 (n=13) | 4713 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.3 mm | 24 (n=31) | 7 (n=31) | 5919 (n=31) | 8 (n=13) | 5 (n=13) | 2944 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 2.7 mm | 17 (n=31) | 14 (n=31) | 2002 (n=31) | 1 (n=13) | 12 (n=13) | 967 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 5.4 mm | 7 (n=31) | 24 (n=31) | 446 (n=31) | 0 (n=13) | 13 (n=13) | 206 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.7 mm | 24 (n=31) | 7 (n=31) | 8462 (n=31) | 9 (n=13) | 4 (n=13) | 4331 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 2 mm | 23 (n=31) | 8 (n=31) | 7110 (n=31) | 8 (n=13) | 5 (n=13) | 3581 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 3.1 mm | 18 (n=31) | 13 (n=31) | 3667 (n=31) | 1 (n=13) | 12 (n=13) | 1771 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 5.3 mm | 10 (n=31) | 21 (n=31) | 1210 (n=31) | 0 (n=13) | 13 (n=13) | 609 (n=13) |
| nieve | `nieve_24h_cm` | 0.1 cm | 9 (n=14) | 5 (n=14) | 272 (n=14) | 7 (n=20) | 13 (n=20) | 112 (n=20) |
| nieve | `nieve_24h_cm` | 0.2 cm | 8 (n=14) | 6 (n=14) | 233 (n=14) | 7 (n=20) | 13 (n=20) | 100 (n=20) |
| nieve | `nieve_24h_cm` | 1.1 cm | 5 (n=14) | 9 (n=14) | 80 (n=14) | 3 (n=20) | 17 (n=20) | 32 (n=20) |
| nieve | `nieve_72h_cm` | 0.1 cm | 11 (n=14) | 3 (n=14) | 643 (n=14) | 11 (n=20) | 9 (n=20) | 236 (n=20) |
| nieve | `nieve_72h_cm` | 0.8 cm | 8 (n=14) | 6 (n=14) | 312 (n=14) | 6 (n=20) | 14 (n=20) | 113 (n=20) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=14) | 8 (n=14) | 202 (n=14) | 3 (n=20) | 17 (n=20) | 78 (n=20) |
| nieve | `nieve_72h_cm` | 2.6 cm | 3 (n=14) | 11 (n=14) | 78 (n=14) | 1 (n=20) | 19 (n=20) | 36 (n=20) |
| nieve | `nieve_7d_cm` | 0.2 cm | 10 (n=14) | 4 (n=14) | 1140 (n=14) | 12 (n=20) | 8 (n=20) | 443 (n=20) |
| nieve | `nieve_7d_cm` | 0.9 cm | 9 (n=14) | 5 (n=14) | 636 (n=14) | 6 (n=20) | 14 (n=20) | 232 (n=20) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=14) | 8 (n=14) | 269 (n=14) | 2 (n=20) | 18 (n=20) | 88 (n=20) |
| nieve | `nieve_7d_cm` | 3.2 cm | 3 (n=14) | 11 (n=14) | 178 (n=14) | 0 (n=20) | 20 (n=20) | 66 (n=20) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 19 (n=31) | 12 (n=31) | 5794 (n=31) | 10 (n=13) | 3 (n=13) | 3339 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 12 (n=31) | 19 (n=31) | 3057 (n=31) | 6 (n=13) | 7 (n=13) | 1711 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 8 (n=31) | 23 (n=31) | 1593 (n=31) | 3 (n=13) | 10 (n=13) | 909 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 6 (n=31) | 25 (n=31) | 665 (n=31) | 0 (n=13) | 13 (n=13) | 386 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 4 (n=31) | 27 (n=31) | 310 (n=31) | 0 (n=13) | 13 (n=13) | 171 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 14 (n=31) | 17 (n=31) | 6077 (n=31) | 9 (n=13) | 4 (n=13) | 3337 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 9 (n=31) | 22 (n=31) | 3147 (n=31) | 7 (n=13) | 6 (n=13) | 1743 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 7 (n=31) | 24 (n=31) | 1629 (n=31) | 3 (n=13) | 10 (n=13) | 903 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 5 (n=31) | 26 (n=31) | 664 (n=31) | 1 (n=13) | 12 (n=13) | 330 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 2 (n=31) | 29 (n=31) | 308 (n=31) | 0 (n=13) | 13 (n=13) | 162 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 11 (n=31) | 20 (n=31) | 6167 (n=31) | 8 (n=13) | 5 (n=13) | 3342 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 11 (n=31) | 20 (n=31) | 3219 (n=31) | 8 (n=13) | 5 (n=13) | 1760 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 7 (n=31) | 24 (n=31) | 1647 (n=31) | 4 (n=13) | 9 (n=13) | 872 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 3 (n=31) | 28 (n=31) | 667 (n=31) | 1 (n=13) | 12 (n=13) | 293 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 2 (n=31) | 29 (n=31) | 316 (n=31) | 0 (n=13) | 13 (n=13) | 133 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 14 (n=31) | 17 (n=31) | 6436 (n=31) | 8 (n=13) | 5 (n=13) | 3540 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 10 (n=31) | 21 (n=31) | 3288 (n=31) | 8 (n=13) | 5 (n=13) | 1754 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 5 (n=31) | 26 (n=31) | 1652 (n=31) | 3 (n=13) | 10 (n=13) | 821 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 4 (n=31) | 27 (n=31) | 656 (n=31) | 1 (n=13) | 12 (n=13) | 296 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 3 (n=31) | 28 (n=31) | 304 (n=31) | 1 (n=13) | 12 (n=13) | 138 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 19 (n=31) | 12 (n=31) | 5791 (n=31) | 10 (n=13) | 3 (n=13) | 3226 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 13 (n=31) | 18 (n=31) | 3016 (n=31) | 6 (n=13) | 7 (n=13) | 1621 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 7 (n=31) | 24 (n=31) | 1585 (n=31) | 3 (n=13) | 10 (n=13) | 870 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 6 (n=31) | 25 (n=31) | 650 (n=31) | 2 (n=13) | 11 (n=13) | 311 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=31) | 28 (n=31) | 314 (n=31) | 0 (n=13) | 13 (n=13) | 149 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 13 (n=31) | 18 (n=31) | 6086 (n=31) | 7 (n=13) | 6 (n=13) | 3199 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 10 (n=31) | 21 (n=31) | 3195 (n=31) | 5 (n=13) | 8 (n=13) | 1732 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 9 (n=31) | 22 (n=31) | 1615 (n=31) | 3 (n=13) | 10 (n=13) | 794 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 4 (n=31) | 27 (n=31) | 648 (n=31) | 0 (n=13) | 13 (n=13) | 291 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 4 (n=31) | 27 (n=31) | 300 (n=31) | 0 (n=13) | 13 (n=13) | 158 (n=13) |
| nieve | `nieve_24h_cm_pct` | p80 | 10 (n=14) | 4 (n=14) | 325 (n=14) | 9 (n=20) | 11 (n=20) | 141 (n=20) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=14) | 4 (n=14) | 298 (n=14) | 9 (n=20) | 11 (n=20) | 132 (n=20) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=14) | 4 (n=14) | 265 (n=14) | 9 (n=20) | 11 (n=20) | 113 (n=20) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=14) | 10 (n=14) | 186 (n=14) | 4 (n=20) | 16 (n=20) | 71 (n=20) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 117 (n=14) | 3 (n=20) | 17 (n=20) | 41 (n=20) |
| nieve | `nieve_72h_cm_pct` | p80 | 12 (n=14) | 2 (n=14) | 702 (n=14) | 12 (n=20) | 8 (n=20) | 276 (n=20) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=14) | 3 (n=14) | 608 (n=14) | 11 (n=20) | 9 (n=20) | 236 (n=20) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=14) | 7 (n=14) | 450 (n=14) | 8 (n=20) | 12 (n=20) | 170 (n=20) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=14) | 11 (n=14) | 265 (n=14) | 4 (n=20) | 16 (n=20) | 84 (n=20) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 162 (n=14) | 2 (n=20) | 18 (n=20) | 50 (n=20) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 1271 (n=14) | 12 (n=20) | 8 (n=20) | 490 (n=20) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=14) | 8 (n=14) | 971 (n=14) | 9 (n=20) | 11 (n=20) | 359 (n=20) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=14) | 9 (n=14) | 658 (n=14) | 6 (n=20) | 14 (n=20) | 211 (n=20) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=14) | 12 (n=14) | 359 (n=14) | 3 (n=20) | 17 (n=20) | 100 (n=20) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=14) | 13 (n=14) | 181 (n=14) | 1 (n=20) | 19 (n=20) | 68 (n=20) |

## Solo fuentes estables

Eventos con punto crítico usados: aluvión 33, crecida 11 (lluvia 44), nieve 30.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 20 | 17.9 | 4.0 | 83 |
| aluvion | `lluvia_48h_mm` | 20 | 22.0 | 9.2 | 81 |
| aluvion | `lluvia_72h_mm` | 20 | 28.4 | 15.3 | 75 |
| aluvion | `lluvia_7d_mm` | 20 | 79.4 | 43.9 | 80 |
| aluvion | `lluvia_max_horaria_24h_mm` | 20 | 2.7 | 0.8 | 86 |
| aluvion | `lluvia_max_horaria_72h_mm` | 20 | 3.4 | 1.7 | 79 |
| crecida | `lluvia_24h_mm` | 7 | 13.0 | 4.9 | 86 |
| crecida | `lluvia_48h_mm` | 7 | 23.2 | 11.7 | 72 |
| crecida | `lluvia_72h_mm` | 7 | 24.9 | 19.4 | 67 |
| crecida | `lluvia_7d_mm` | 7 | 69.2 | 50.0 | 78 |
| crecida | `lluvia_max_horaria_24h_mm` | 7 | 2.5 | 1.0 | 79 |
| crecida | `lluvia_max_horaria_72h_mm` | 7 | 3.1 | 1.9 | 74 |
| nieve | `nieve_24h_cm` | 14 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 14 | 1.2 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 14 | 1.7 | 0.0 | 89 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 3.9 mm | 18 (n=24) | 6 (n=24) | 8482 (n=24) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 4459 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 6 mm | 18 (n=24) | 6 (n=24) | 6167 (n=24) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 3186 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 17.9 mm | 12 (n=24) | 12 (n=24) | 1419 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 695 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm` | 34.2 mm | 5 (n=24) | 19 (n=24) | 350 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 159 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 14.8 mm | 18 (n=24) | 6 (n=24) | 5285 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2645 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 16.7 mm | 18 (n=24) | 6 (n=24) | 4617 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2283 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 22 mm | 11 (n=24) | 13 (n=24) | 3177 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1510 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm` | 50.1 mm | 5 (n=24) | 19 (n=24) | 528 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 219 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 20.5 mm | 18 (n=24) | 6 (n=24) | 5995 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3022 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 24.9 mm | 16 (n=24) | 8 (n=24) | 4699 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 2356 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 28.4 mm | 14 (n=24) | 10 (n=24) | 3886 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1953 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm` | 54.5 mm | 5 (n=24) | 19 (n=24) | 1074 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 437 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 32.4 mm | 18 (n=24) | 6 (n=24) | 9131 (n=24) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 4868 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 48.6 mm | 15 (n=24) | 9 (n=24) | 6155 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3028 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 79.4 mm | 10 (n=24) | 14 (n=24) | 2744 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1212 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm` | 116 mm | 6 (n=24) | 18 (n=24) | 870 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 381 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.8 mm | 19 (n=24) | 5 (n=24) | 9209 (n=24) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 4717 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.4 mm | 18 (n=24) | 6 (n=24) | 5424 (n=24) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 2710 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 2.7 mm | 13 (n=24) | 11 (n=24) | 2008 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 968 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 5.8 mm | 5 (n=24) | 19 (n=24) | 347 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 177 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.9 mm | 18 (n=24) | 6 (n=24) | 7571 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3866 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 17 (n=24) | 7 (n=24) | 7122 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3583 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.4 mm | 13 (n=24) | 11 (n=24) | 3088 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 1530 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.7 mm | 5 (n=24) | 19 (n=24) | 962 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 501 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 6.1 mm | 6 (n=7) | 1 (n=7) | 6093 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3131 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 9.4 mm | 5 (n=7) | 2 (n=7) | 3873 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 1854 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 13 mm | 3 (n=7) | 4 (n=7) | 2484 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1205 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 24.3 mm | 2 (n=7) | 5 (n=7) | 777 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 376 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 9.6 mm | 7 (n=7) | 0 (n=7) | 7897 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 4150 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 12 mm | 6 (n=7) | 1 (n=7) | 6557 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3335 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 23.2 mm | 4 (n=7) | 3 (n=7) | 2916 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1390 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 42.4 mm | 2 (n=7) | 5 (n=7) | 906 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 369 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 17.6 mm | 7 (n=7) | 0 (n=7) | 6952 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3549 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 21.2 mm | 7 (n=7) | 0 (n=7) | 5787 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 2899 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 24.9 mm | 5 (n=7) | 2 (n=7) | 4718 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2359 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 46.1 mm | 4 (n=7) | 3 (n=7) | 1673 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 725 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 48 mm | 6 (n=7) | 1 (n=7) | 6275 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3072 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 49 mm | 6 (n=7) | 1 (n=7) | 6123 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3009 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 69.2 mm | 4 (n=7) | 3 (n=7) | 3611 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1665 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 106.9 mm | 2 (n=7) | 5 (n=7) | 1208 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 506 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1 mm | 7 (n=7) | 0 (n=7) | 7778 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3941 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.9 mm | 5 (n=7) | 2 (n=7) | 3659 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1819 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.5 mm | 5 (n=7) | 2 (n=7) | 2350 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1141 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 3.6 mm | 3 (n=7) | 4 (n=7) | 1138 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 551 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 1.9 mm | 6 (n=7) | 1 (n=7) | 7593 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3875 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 2.5 mm | 6 (n=7) | 1 (n=7) | 5269 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2632 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3.1 mm | 5 (n=7) | 2 (n=7) | 3687 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1771 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.5 mm | 4 (n=7) | 3 (n=7) | 1815 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 854 (n=4 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 9 (n=14) | 5 (n=14) | 272 (n=14) | 5 (n=16) | 11 (n=16) | 114 (n=16) |
| nieve | `nieve_24h_cm` | 0.2 cm | 8 (n=14) | 6 (n=14) | 233 (n=14) | 5 (n=16) | 11 (n=16) | 102 (n=16) |
| nieve | `nieve_24h_cm` | 1.1 cm | 5 (n=14) | 9 (n=14) | 80 (n=14) | 2 (n=16) | 14 (n=16) | 33 (n=16) |
| nieve | `nieve_72h_cm` | 0.1 cm | 11 (n=14) | 3 (n=14) | 643 (n=14) | 9 (n=16) | 7 (n=16) | 239 (n=16) |
| nieve | `nieve_72h_cm` | 0.8 cm | 8 (n=14) | 6 (n=14) | 312 (n=14) | 4 (n=16) | 12 (n=16) | 116 (n=16) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=14) | 8 (n=14) | 202 (n=14) | 2 (n=16) | 14 (n=16) | 80 (n=16) |
| nieve | `nieve_72h_cm` | 2.6 cm | 3 (n=14) | 11 (n=14) | 78 (n=14) | 1 (n=16) | 15 (n=16) | 36 (n=16) |
| nieve | `nieve_7d_cm` | 0.2 cm | 10 (n=14) | 4 (n=14) | 1140 (n=14) | 9 (n=16) | 7 (n=16) | 448 (n=16) |
| nieve | `nieve_7d_cm` | 0.9 cm | 9 (n=14) | 5 (n=14) | 636 (n=14) | 4 (n=16) | 12 (n=16) | 235 (n=16) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=14) | 8 (n=14) | 269 (n=14) | 2 (n=16) | 14 (n=16) | 88 (n=16) |
| nieve | `nieve_7d_cm` | 3.2 cm | 3 (n=14) | 11 (n=14) | 178 (n=14) | 0 (n=16) | 16 (n=16) | 66 (n=16) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 15 (n=24) | 9 (n=24) | 5799 (n=24) | 8 (n=9 muestra chica) | 1 (n=9 muestra chica) | 3342 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 11 (n=24) | 13 (n=24) | 3058 (n=24) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1713 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 7 (n=24) | 17 (n=24) | 1594 (n=24) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 910 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 5 (n=24) | 19 (n=24) | 666 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 386 (n=9 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 4 (n=24) | 20 (n=24) | 310 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 171 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 11 (n=24) | 13 (n=24) | 6080 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3341 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3148 (n=24) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 1745 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1630 (n=24) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 904 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 5 (n=24) | 19 (n=24) | 664 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 330 (n=9 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 308 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 162 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 8 (n=24) | 16 (n=24) | 6171 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3344 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3222 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 1761 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1648 (n=24) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 872 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 667 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 293 (n=9 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 316 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 133 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 11 (n=24) | 13 (n=24) | 6440 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3542 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3290 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 1756 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 3 (n=24) | 21 (n=24) | 1654 (n=24) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 823 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 657 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 296 (n=9 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 304 (n=24) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 138 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 14 (n=24) | 10 (n=24) | 5797 (n=24) | 8 (n=9 muestra chica) | 1 (n=9 muestra chica) | 3228 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 12 (n=24) | 12 (n=24) | 3017 (n=24) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 1621 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1586 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 870 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 5 (n=24) | 19 (n=24) | 651 (n=24) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 311 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 314 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 149 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 10 (n=24) | 14 (n=24) | 6091 (n=24) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3199 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 7 (n=24) | 17 (n=24) | 3198 (n=24) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1732 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1618 (n=24) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 794 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 649 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 291 (n=9 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 301 (n=24) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 158 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p80 | 4 (n=7) | 3 (n=7) | 5815 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3352 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 1 (n=7) | 6 (n=7) | 3070 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1717 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 1 (n=7) | 6 (n=7) | 1602 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 911 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 1 (n=7) | 6 (n=7) | 672 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 386 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 314 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 171 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 3 (n=7) | 4 (n=7) | 6093 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3349 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 1 (n=7) | 6 (n=7) | 3159 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1751 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 1 (n=7) | 6 (n=7) | 1638 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 905 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 0 (n=7) | 7 (n=7) | 672 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 331 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 312 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 162 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 3 (n=7) | 4 (n=7) | 6181 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3355 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 3 (n=7) | 4 (n=7) | 3231 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1772 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 1 (n=7) | 6 (n=7) | 1656 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 878 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 0 (n=7) | 7 (n=7) | 672 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 294 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 318 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 133 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 3 (n=7) | 4 (n=7) | 6456 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3554 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 2 (n=7) | 5 (n=7) | 3300 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1766 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 2 (n=7) | 5 (n=7) | 1658 (n=7) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 825 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 1 (n=7) | 6 (n=7) | 662 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 298 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 308 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 140 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 5 (n=7) | 2 (n=7) | 5813 (n=7) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3238 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 1 (n=7) | 6 (n=7) | 3033 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1630 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 1 (n=7) | 6 (n=7) | 1595 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 873 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 1 (n=7) | 6 (n=7) | 657 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 313 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 0 (n=7) | 7 (n=7) | 319 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 149 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 3 (n=7) | 4 (n=7) | 6104 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 3212 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 3 (n=7) | 4 (n=7) | 3205 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1739 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 3 (n=7) | 4 (n=7) | 1624 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 797 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=7) | 6 (n=7) | 654 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 291 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=7) | 6 (n=7) | 306 (n=7) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 158 (n=4 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 10 (n=14) | 4 (n=14) | 325 (n=14) | 7 (n=16) | 9 (n=16) | 143 (n=16) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=14) | 4 (n=14) | 298 (n=14) | 7 (n=16) | 9 (n=16) | 134 (n=16) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=14) | 4 (n=14) | 265 (n=14) | 7 (n=16) | 9 (n=16) | 115 (n=16) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=14) | 10 (n=14) | 186 (n=14) | 3 (n=16) | 13 (n=16) | 72 (n=16) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 117 (n=14) | 3 (n=16) | 13 (n=16) | 41 (n=16) |
| nieve | `nieve_72h_cm_pct` | p80 | 12 (n=14) | 2 (n=14) | 702 (n=14) | 10 (n=16) | 6 (n=16) | 279 (n=16) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=14) | 3 (n=14) | 608 (n=14) | 9 (n=16) | 7 (n=16) | 239 (n=16) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=14) | 7 (n=14) | 450 (n=14) | 6 (n=16) | 10 (n=16) | 173 (n=16) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=14) | 11 (n=14) | 265 (n=14) | 4 (n=16) | 12 (n=16) | 84 (n=16) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 162 (n=14) | 2 (n=16) | 14 (n=16) | 50 (n=16) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 1271 (n=14) | 9 (n=16) | 7 (n=16) | 495 (n=16) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=14) | 8 (n=14) | 971 (n=14) | 6 (n=16) | 10 (n=16) | 364 (n=16) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=14) | 9 (n=14) | 658 (n=14) | 5 (n=16) | 11 (n=16) | 213 (n=16) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=14) | 12 (n=14) | 359 (n=14) | 2 (n=16) | 14 (n=16) | 102 (n=16) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=14) | 13 (n=14) | 181 (n=14) | 1 (n=16) | 15 (n=16) | 68 (n=16) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 27 | 17.9 | 3.9 | 85 |
| lluvia | `lluvia_48h_mm` | 27 | 23.2 | 9.0 | 78 |
| lluvia | `lluvia_72h_mm` | 27 | 27.3 | 15.0 | 74 |
| lluvia | `lluvia_7d_mm` | 27 | 70.6 | 41.8 | 79 |
| lluvia | `lluvia_max_horaria_24h_mm` | 27 | 2.7 | 0.8 | 85 |
| lluvia | `lluvia_max_horaria_72h_mm` | 27 | 3.1 | 1.7 | 78 |
| nieve | `nieve_24h_cm` | 14 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 14 | 1.2 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 14 | 1.7 | 0.0 | 89 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 4.4 mm | 25 (n=31) | 6 (n=31) | 7816 (n=31) | 6 (n=13) | 7 (n=13) | 4129 (n=13) |
| lluvia | `lluvia_24h_mm` | 6.5 mm | 24 (n=31) | 7 (n=31) | 5713 (n=31) | 6 (n=13) | 7 (n=13) | 2962 (n=13) |
| lluvia | `lluvia_24h_mm` | 17.9 mm | 15 (n=31) | 16 (n=31) | 1415 (n=31) | 2 (n=13) | 11 (n=13) | 694 (n=13) |
| lluvia | `lluvia_24h_mm` | 32.4 mm | 7 (n=31) | 24 (n=31) | 407 (n=31) | 0 (n=13) | 13 (n=13) | 176 (n=13) |
| lluvia | `lluvia_48h_mm` | 9.6 mm | 26 (n=31) | 5 (n=31) | 7863 (n=31) | 7 (n=13) | 6 (n=13) | 4142 (n=13) |
| lluvia | `lluvia_48h_mm` | 16.4 mm | 22 (n=31) | 9 (n=31) | 4724 (n=31) | 5 (n=13) | 8 (n=13) | 2345 (n=13) |
| lluvia | `lluvia_48h_mm` | 23.2 mm | 15 (n=31) | 16 (n=31) | 2899 (n=31) | 2 (n=13) | 11 (n=13) | 1389 (n=13) |
| lluvia | `lluvia_48h_mm` | 48.4 mm | 7 (n=31) | 24 (n=31) | 594 (n=31) | 0 (n=13) | 13 (n=13) | 253 (n=13) |
| lluvia | `lluvia_72h_mm` | 17.6 mm | 25 (n=31) | 6 (n=31) | 6919 (n=31) | 5 (n=13) | 8 (n=13) | 3543 (n=13) |
| lluvia | `lluvia_72h_mm` | 24.1 mm | 22 (n=31) | 9 (n=31) | 4902 (n=31) | 4 (n=13) | 9 (n=13) | 2454 (n=13) |
| lluvia | `lluvia_72h_mm` | 27.3 mm | 20 (n=31) | 11 (n=31) | 4141 (n=31) | 2 (n=13) | 11 (n=13) | 2059 (n=13) |
| lluvia | `lluvia_72h_mm` | 53.2 mm | 9 (n=31) | 22 (n=31) | 1147 (n=31) | 0 (n=13) | 13 (n=13) | 477 (n=13) |
| lluvia | `lluvia_7d_mm` | 33.4 mm | 24 (n=31) | 7 (n=31) | 8909 (n=31) | 5 (n=13) | 8 (n=13) | 4735 (n=13) |
| lluvia | `lluvia_7d_mm` | 49 mm | 21 (n=31) | 10 (n=31) | 6095 (n=31) | 4 (n=13) | 9 (n=13) | 3004 (n=13) |
| lluvia | `lluvia_7d_mm` | 70.6 mm | 14 (n=31) | 17 (n=31) | 3470 (n=31) | 2 (n=13) | 11 (n=13) | 1606 (n=13) |
| lluvia | `lluvia_7d_mm` | 116 mm | 8 (n=31) | 23 (n=31) | 867 (n=31) | 1 (n=13) | 12 (n=13) | 379 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.8 mm | 26 (n=31) | 5 (n=31) | 9197 (n=31) | 8 (n=13) | 5 (n=13) | 4713 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.3 mm | 24 (n=31) | 7 (n=31) | 5919 (n=31) | 8 (n=13) | 5 (n=13) | 2944 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 2.7 mm | 17 (n=31) | 14 (n=31) | 2002 (n=31) | 1 (n=13) | 12 (n=13) | 967 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm` | 5.4 mm | 7 (n=31) | 24 (n=31) | 446 (n=31) | 0 (n=13) | 13 (n=13) | 206 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.7 mm | 24 (n=31) | 7 (n=31) | 8462 (n=31) | 9 (n=13) | 4 (n=13) | 4331 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 2 mm | 23 (n=31) | 8 (n=31) | 7110 (n=31) | 8 (n=13) | 5 (n=13) | 3581 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 3.1 mm | 18 (n=31) | 13 (n=31) | 3667 (n=31) | 1 (n=13) | 12 (n=13) | 1771 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm` | 5.3 mm | 10 (n=31) | 21 (n=31) | 1210 (n=31) | 0 (n=13) | 13 (n=13) | 609 (n=13) |
| nieve | `nieve_24h_cm` | 0.1 cm | 9 (n=14) | 5 (n=14) | 272 (n=14) | 5 (n=16) | 11 (n=16) | 114 (n=16) |
| nieve | `nieve_24h_cm` | 0.2 cm | 8 (n=14) | 6 (n=14) | 233 (n=14) | 5 (n=16) | 11 (n=16) | 102 (n=16) |
| nieve | `nieve_24h_cm` | 1.1 cm | 5 (n=14) | 9 (n=14) | 80 (n=14) | 2 (n=16) | 14 (n=16) | 33 (n=16) |
| nieve | `nieve_72h_cm` | 0.1 cm | 11 (n=14) | 3 (n=14) | 643 (n=14) | 9 (n=16) | 7 (n=16) | 239 (n=16) |
| nieve | `nieve_72h_cm` | 0.8 cm | 8 (n=14) | 6 (n=14) | 312 (n=14) | 4 (n=16) | 12 (n=16) | 116 (n=16) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=14) | 8 (n=14) | 202 (n=14) | 2 (n=16) | 14 (n=16) | 80 (n=16) |
| nieve | `nieve_72h_cm` | 2.6 cm | 3 (n=14) | 11 (n=14) | 78 (n=14) | 1 (n=16) | 15 (n=16) | 36 (n=16) |
| nieve | `nieve_7d_cm` | 0.2 cm | 10 (n=14) | 4 (n=14) | 1140 (n=14) | 9 (n=16) | 7 (n=16) | 448 (n=16) |
| nieve | `nieve_7d_cm` | 0.9 cm | 9 (n=14) | 5 (n=14) | 636 (n=14) | 4 (n=16) | 12 (n=16) | 235 (n=16) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=14) | 8 (n=14) | 269 (n=14) | 2 (n=16) | 14 (n=16) | 88 (n=16) |
| nieve | `nieve_7d_cm` | 3.2 cm | 3 (n=14) | 11 (n=14) | 178 (n=14) | 0 (n=16) | 16 (n=16) | 66 (n=16) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 19 (n=31) | 12 (n=31) | 5794 (n=31) | 10 (n=13) | 3 (n=13) | 3339 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 12 (n=31) | 19 (n=31) | 3057 (n=31) | 6 (n=13) | 7 (n=13) | 1711 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 8 (n=31) | 23 (n=31) | 1593 (n=31) | 3 (n=13) | 10 (n=13) | 909 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 6 (n=31) | 25 (n=31) | 665 (n=31) | 0 (n=13) | 13 (n=13) | 386 (n=13) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 4 (n=31) | 27 (n=31) | 310 (n=31) | 0 (n=13) | 13 (n=13) | 171 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 14 (n=31) | 17 (n=31) | 6077 (n=31) | 9 (n=13) | 4 (n=13) | 3337 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 9 (n=31) | 22 (n=31) | 3147 (n=31) | 7 (n=13) | 6 (n=13) | 1743 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 7 (n=31) | 24 (n=31) | 1629 (n=31) | 3 (n=13) | 10 (n=13) | 903 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 5 (n=31) | 26 (n=31) | 664 (n=31) | 1 (n=13) | 12 (n=13) | 330 (n=13) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 2 (n=31) | 29 (n=31) | 308 (n=31) | 0 (n=13) | 13 (n=13) | 162 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 11 (n=31) | 20 (n=31) | 6167 (n=31) | 8 (n=13) | 5 (n=13) | 3342 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 11 (n=31) | 20 (n=31) | 3219 (n=31) | 8 (n=13) | 5 (n=13) | 1760 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 7 (n=31) | 24 (n=31) | 1647 (n=31) | 4 (n=13) | 9 (n=13) | 872 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 3 (n=31) | 28 (n=31) | 667 (n=31) | 1 (n=13) | 12 (n=13) | 293 (n=13) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 2 (n=31) | 29 (n=31) | 316 (n=31) | 0 (n=13) | 13 (n=13) | 133 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 14 (n=31) | 17 (n=31) | 6436 (n=31) | 8 (n=13) | 5 (n=13) | 3540 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 10 (n=31) | 21 (n=31) | 3288 (n=31) | 8 (n=13) | 5 (n=13) | 1754 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 5 (n=31) | 26 (n=31) | 1652 (n=31) | 3 (n=13) | 10 (n=13) | 821 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 4 (n=31) | 27 (n=31) | 656 (n=31) | 1 (n=13) | 12 (n=13) | 296 (n=13) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 3 (n=31) | 28 (n=31) | 304 (n=31) | 1 (n=13) | 12 (n=13) | 138 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 19 (n=31) | 12 (n=31) | 5791 (n=31) | 10 (n=13) | 3 (n=13) | 3226 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 13 (n=31) | 18 (n=31) | 3016 (n=31) | 6 (n=13) | 7 (n=13) | 1621 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 7 (n=31) | 24 (n=31) | 1585 (n=31) | 3 (n=13) | 10 (n=13) | 870 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 6 (n=31) | 25 (n=31) | 650 (n=31) | 2 (n=13) | 11 (n=13) | 311 (n=13) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=31) | 28 (n=31) | 314 (n=31) | 0 (n=13) | 13 (n=13) | 149 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 13 (n=31) | 18 (n=31) | 6086 (n=31) | 7 (n=13) | 6 (n=13) | 3199 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 10 (n=31) | 21 (n=31) | 3195 (n=31) | 5 (n=13) | 8 (n=13) | 1732 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 9 (n=31) | 22 (n=31) | 1615 (n=31) | 3 (n=13) | 10 (n=13) | 794 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 4 (n=31) | 27 (n=31) | 648 (n=31) | 0 (n=13) | 13 (n=13) | 291 (n=13) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 4 (n=31) | 27 (n=31) | 300 (n=31) | 0 (n=13) | 13 (n=13) | 158 (n=13) |
| nieve | `nieve_24h_cm_pct` | p80 | 10 (n=14) | 4 (n=14) | 325 (n=14) | 7 (n=16) | 9 (n=16) | 143 (n=16) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=14) | 4 (n=14) | 298 (n=14) | 7 (n=16) | 9 (n=16) | 134 (n=16) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=14) | 4 (n=14) | 265 (n=14) | 7 (n=16) | 9 (n=16) | 115 (n=16) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=14) | 10 (n=14) | 186 (n=14) | 3 (n=16) | 13 (n=16) | 72 (n=16) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 117 (n=14) | 3 (n=16) | 13 (n=16) | 41 (n=16) |
| nieve | `nieve_72h_cm_pct` | p80 | 12 (n=14) | 2 (n=14) | 702 (n=14) | 10 (n=16) | 6 (n=16) | 279 (n=16) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=14) | 3 (n=14) | 608 (n=14) | 9 (n=16) | 7 (n=16) | 239 (n=16) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=14) | 7 (n=14) | 450 (n=14) | 6 (n=16) | 10 (n=16) | 173 (n=16) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=14) | 11 (n=14) | 265 (n=14) | 4 (n=16) | 12 (n=16) | 84 (n=16) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 162 (n=14) | 2 (n=16) | 14 (n=16) | 50 (n=16) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 1271 (n=14) | 9 (n=16) | 7 (n=16) | 495 (n=16) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=14) | 8 (n=14) | 971 (n=14) | 6 (n=16) | 10 (n=16) | 364 (n=16) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=14) | 9 (n=14) | 658 (n=14) | 5 (n=16) | 11 (n=16) | 213 (n=16) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=14) | 12 (n=14) | 359 (n=14) | 2 (n=16) | 14 (n=16) | 102 (n=16) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=14) | 13 (n=14) | 181 (n=14) | 1 (n=16) | 15 (n=16) | 68 (n=16) |

## Todas las fuentes: nieve en Paso de Jama por lado

Eventos de nieve en `rn52_paso_jama`: 30 (AR 1, ambos 4, CL 19, lado desconocido 6, que quedan fuera de esta sección).

Falta el clima de `ch27_alto`: CL y combinado quedan sin datos.

### Nieve AR o ambos (clima de rn52_paso_jama)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 2 | 0.1 | 0.0 | 70 |
| nieve | `nieve_72h_cm` | 2 | 0.1 | 0.0 | 65 |
| nieve | `nieve_7d_cm` | 2 | 0.1 | 0.0 | 57 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=2) | 1 (n=2) | 142 (n=2) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 81 (n=3 muestra chica) |
| nieve | `nieve_72h_cm` | 0.1 cm | 1 (n=2) | 1 (n=2) | 308 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 156 (n=3 muestra chica) |
| nieve | `nieve_7d_cm` | 0.1 cm | 1 (n=2) | 1 (n=2) | 556 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 284 (n=3 muestra chica) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=2) | 1 (n=2) | 168 (n=2) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 93 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=2) | 1 (n=2) | 141 (n=2) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 84 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=2) | 1 (n=2) | 106 (n=2) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 65 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=2) | 2 (n=2) | 53 (n=2) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 34 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=2) | 2 (n=2) | 24 (n=2) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 21 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p80 | 1 (n=2) | 1 (n=2) | 311 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 153 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p90 | 1 (n=2) | 1 (n=2) | 225 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 115 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=2) | 2 (n=2) | 126 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 77 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=2) | 2 (n=2) | 52 (n=2) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 33 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=2) | 2 (n=2) | 26 (n=2) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 19 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p80 | 1 (n=2) | 1 (n=2) | 441 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 220 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=2) | 2 (n=2) | 262 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 150 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=2) | 2 (n=2) | 129 (n=2) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 90 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=2) | 2 (n=2) | 53 (n=2) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 42 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=2) | 2 (n=2) | 27 (n=2) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 29 (n=3 muestra chica) |

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
| nieve | `nieve_24h_cm` | 2 | 0.1 | 0.0 | 70 |
| nieve | `nieve_72h_cm` | 2 | 0.1 | 0.0 | 65 |
| nieve | `nieve_7d_cm` | 2 | 0.1 | 0.0 | 57 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=11) | 10 (n=11) | 142 (n=11) | 1 (n=13) | 12 (n=13) | 81 (n=13) |
| nieve | `nieve_72h_cm` | 0.1 cm | 1 (n=11) | 10 (n=11) | 308 (n=11) | 3 (n=13) | 10 (n=13) | 156 (n=13) |
| nieve | `nieve_7d_cm` | 0.1 cm | 1 (n=11) | 10 (n=11) | 556 (n=11) | 3 (n=13) | 10 (n=13) | 284 (n=13) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=11) | 10 (n=11) | 168 (n=11) | 2 (n=13) | 11 (n=13) | 93 (n=13) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=11) | 10 (n=11) | 141 (n=11) | 2 (n=13) | 11 (n=13) | 84 (n=13) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=11) | 10 (n=11) | 106 (n=11) | 2 (n=13) | 11 (n=13) | 65 (n=13) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=11) | 11 (n=11) | 53 (n=11) | 1 (n=13) | 12 (n=13) | 34 (n=13) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=11) | 11 (n=11) | 24 (n=11) | 1 (n=13) | 12 (n=13) | 21 (n=13) |
| nieve | `nieve_72h_cm_pct` | p80 | 1 (n=11) | 10 (n=11) | 311 (n=11) | 3 (n=13) | 10 (n=13) | 153 (n=13) |
| nieve | `nieve_72h_cm_pct` | p90 | 1 (n=11) | 10 (n=11) | 225 (n=11) | 3 (n=13) | 10 (n=13) | 115 (n=13) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=11) | 11 (n=11) | 126 (n=11) | 3 (n=13) | 10 (n=13) | 77 (n=13) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=11) | 11 (n=11) | 52 (n=11) | 1 (n=13) | 12 (n=13) | 33 (n=13) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=11) | 11 (n=11) | 26 (n=11) | 0 (n=13) | 13 (n=13) | 19 (n=13) |
| nieve | `nieve_7d_cm_pct` | p80 | 1 (n=11) | 10 (n=11) | 441 (n=11) | 3 (n=13) | 10 (n=13) | 220 (n=13) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=11) | 11 (n=11) | 262 (n=11) | 3 (n=13) | 10 (n=13) | 150 (n=13) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=11) | 11 (n=11) | 129 (n=11) | 2 (n=13) | 11 (n=13) | 90 (n=13) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=11) | 11 (n=11) | 53 (n=11) | 0 (n=13) | 13 (n=13) | 42 (n=13) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=11) | 11 (n=11) | 27 (n=11) | 0 (n=13) | 13 (n=13) | 29 (n=13) |


## Solo fuentes estables: nieve en Paso de Jama por lado

Eventos de nieve en `rn52_paso_jama`: 27 (AR 1, ambos 4, CL 17, lado desconocido 5, que quedan fuera de esta sección).

Falta el clima de `ch27_alto`: CL y combinado quedan sin datos.

### Nieve AR o ambos (clima de rn52_paso_jama)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 2 | 0.1 | 0.0 | 70 |
| nieve | `nieve_72h_cm` | 2 | 0.1 | 0.0 | 65 |
| nieve | `nieve_7d_cm` | 2 | 0.1 | 0.0 | 57 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=2) | 1 (n=2) | 142 (n=2) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 81 (n=3 muestra chica) |
| nieve | `nieve_72h_cm` | 0.1 cm | 1 (n=2) | 1 (n=2) | 308 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 156 (n=3 muestra chica) |
| nieve | `nieve_7d_cm` | 0.1 cm | 1 (n=2) | 1 (n=2) | 556 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 284 (n=3 muestra chica) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=2) | 1 (n=2) | 168 (n=2) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 93 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=2) | 1 (n=2) | 141 (n=2) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 84 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=2) | 1 (n=2) | 106 (n=2) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 65 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=2) | 2 (n=2) | 53 (n=2) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 34 (n=3 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=2) | 2 (n=2) | 24 (n=2) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 21 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p80 | 1 (n=2) | 1 (n=2) | 311 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 153 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p90 | 1 (n=2) | 1 (n=2) | 225 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 115 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=2) | 2 (n=2) | 126 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 77 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=2) | 2 (n=2) | 52 (n=2) | 1 (n=3 muestra chica) | 2 (n=3 muestra chica) | 33 (n=3 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=2) | 2 (n=2) | 26 (n=2) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 19 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p80 | 1 (n=2) | 1 (n=2) | 441 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 220 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=2) | 2 (n=2) | 262 (n=2) | 3 (n=3 muestra chica) | 0 (n=3 muestra chica) | 150 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=2) | 2 (n=2) | 129 (n=2) | 2 (n=3 muestra chica) | 1 (n=3 muestra chica) | 90 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=2) | 2 (n=2) | 53 (n=2) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 42 (n=3 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=2) | 2 (n=2) | 27 (n=2) | 0 (n=3 muestra chica) | 3 (n=3 muestra chica) | 29 (n=3 muestra chica) |

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
| nieve | `nieve_24h_cm` | 2 | 0.1 | 0.0 | 70 |
| nieve | `nieve_72h_cm` | 2 | 0.1 | 0.0 | 65 |
| nieve | `nieve_7d_cm` | 2 | 0.1 | 0.0 | 57 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=11) | 10 (n=11) | 142 (n=11) | 1 (n=11) | 10 (n=11) | 81 (n=11) |
| nieve | `nieve_72h_cm` | 0.1 cm | 1 (n=11) | 10 (n=11) | 308 (n=11) | 3 (n=11) | 8 (n=11) | 156 (n=11) |
| nieve | `nieve_7d_cm` | 0.1 cm | 1 (n=11) | 10 (n=11) | 556 (n=11) | 3 (n=11) | 8 (n=11) | 284 (n=11) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=11) | 10 (n=11) | 168 (n=11) | 2 (n=11) | 9 (n=11) | 93 (n=11) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=11) | 10 (n=11) | 141 (n=11) | 2 (n=11) | 9 (n=11) | 84 (n=11) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=11) | 10 (n=11) | 106 (n=11) | 2 (n=11) | 9 (n=11) | 65 (n=11) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=11) | 11 (n=11) | 53 (n=11) | 1 (n=11) | 10 (n=11) | 34 (n=11) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=11) | 11 (n=11) | 24 (n=11) | 1 (n=11) | 10 (n=11) | 21 (n=11) |
| nieve | `nieve_72h_cm_pct` | p80 | 1 (n=11) | 10 (n=11) | 311 (n=11) | 3 (n=11) | 8 (n=11) | 153 (n=11) |
| nieve | `nieve_72h_cm_pct` | p90 | 1 (n=11) | 10 (n=11) | 225 (n=11) | 3 (n=11) | 8 (n=11) | 115 (n=11) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=11) | 11 (n=11) | 126 (n=11) | 3 (n=11) | 8 (n=11) | 77 (n=11) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=11) | 11 (n=11) | 52 (n=11) | 1 (n=11) | 10 (n=11) | 33 (n=11) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=11) | 11 (n=11) | 26 (n=11) | 0 (n=11) | 11 (n=11) | 19 (n=11) |
| nieve | `nieve_7d_cm_pct` | p80 | 1 (n=11) | 10 (n=11) | 441 (n=11) | 3 (n=11) | 8 (n=11) | 220 (n=11) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=11) | 11 (n=11) | 262 (n=11) | 3 (n=11) | 8 (n=11) | 150 (n=11) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=11) | 11 (n=11) | 129 (n=11) | 2 (n=11) | 9 (n=11) | 90 (n=11) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=11) | 11 (n=11) | 53 (n=11) | 0 (n=11) | 11 (n=11) | 42 (n=11) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=11) | 11 (n=11) | 27 (n=11) | 0 (n=11) | 11 (n=11) | 29 (n=11) |
