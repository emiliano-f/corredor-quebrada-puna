# Validación de umbrales

> Generado: 2026-11-14 00:51 UTC · versión `0.1.0.dev0` · commit `f8c4a4c` · SCHEMA_VERSION 2 · fuentes `b3dab32ad1adf821`

Causas meteorológicas: aluvión y crecida contra lluvia, nieve contra nieve. Una regla por causa, igual para todos los puntos; ajuste 2016–2022, prueba 2023→hoy. Acierto = evento con alarma ese día o el anterior; falsa alarma = día con alarma sin evento ese día o el siguiente. Los mm de ERA5 no son lluvia local (ver docs/DATOS.md): por eso cada variable va también como percentil de su celda en la misma estación. Vos elegís la regla final.

Fuentes estables (archivo desde ≤ 2016-01-01): elsubmarino, eltribunojujuy, jujuyaldia, jujuyalmomento, todojujuy.

## Todas las fuentes

Eventos con punto crítico usados: aluvión 23, crecida 12, nieve 35.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 16 | 12.8 | 4.9 | 79 |
| aluvion | `lluvia_48h_mm` | 16 | 20.5 | 11.5 | 80 |
| aluvion | `lluvia_72h_mm` | 16 | 28.4 | 19.3 | 74 |
| aluvion | `lluvia_7d_mm` | 16 | 66.9 | 50.9 | 73 |
| aluvion | `lluvia_max_horaria_24h_mm` | 16 | 2.1 | 1.0 | 79 |
| aluvion | `lluvia_max_horaria_72h_mm` | 16 | 3.3 | 1.9 | 77 |
| crecida | `lluvia_24h_mm` | 8 | 24.3 | 6.0 | 89 |
| crecida | `lluvia_48h_mm` | 8 | 43.1 | 14.3 | 89 |
| crecida | `lluvia_72h_mm` | 8 | 49.2 | 24.0 | 80 |
| crecida | `lluvia_7d_mm` | 8 | 93.3 | 61.3 | 86 |
| crecida | `lluvia_max_horaria_24h_mm` | 8 | 3.6 | 1.1 | 84 |
| crecida | `lluvia_max_horaria_72h_mm` | 8 | 4.5 | 2.2 | 75 |
| nieve | `nieve_24h_cm` | 14 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 14 | 1.2 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 14 | 1.7 | 0.0 | 89 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 4.5 mm | 16 | 0 | 7692 | 2 | 5 | 4062 |
| aluvion | `lluvia_24h_mm` | 5.3 mm | 15 | 1 | 6809 | 2 | 5 | 3594 |
| aluvion | `lluvia_24h_mm` | 12.8 mm | 10 | 6 | 2531 | 1 | 6 | 1230 |
| aluvion | `lluvia_24h_mm` | 29.5 mm | 5 | 11 | 534 | 0 | 7 | 217 |
| aluvion | `lluvia_48h_mm` | 12.5 mm | 14 | 2 | 6324 | 2 | 5 | 3225 |
| aluvion | `lluvia_48h_mm` | 16.4 mm | 14 | 2 | 4737 | 1 | 6 | 2351 |
| aluvion | `lluvia_48h_mm` | 20.5 mm | 9 | 7 | 3514 | 1 | 6 | 1715 |
| aluvion | `lluvia_48h_mm` | 44.8 mm | 4 | 12 | 755 | 0 | 7 | 321 |
| aluvion | `lluvia_72h_mm` | 18.3 mm | 14 | 2 | 6678 | 1 | 6 | 3446 |
| aluvion | `lluvia_72h_mm` | 24.6 mm | 12 | 4 | 4796 | 1 | 6 | 2389 |
| aluvion | `lluvia_72h_mm` | 28.4 mm | 11 | 5 | 3891 | 1 | 6 | 1953 |
| aluvion | `lluvia_72h_mm` | 48.6 mm | 4 | 12 | 1477 | 0 | 7 | 623 |
| aluvion | `lluvia_7d_mm` | 45 mm | 14 | 2 | 6752 | 2 | 5 | 3327 |
| aluvion | `lluvia_7d_mm` | 50.2 mm | 12 | 4 | 5898 | 2 | 5 | 2903 |
| aluvion | `lluvia_7d_mm` | 66.9 mm | 8 | 8 | 3840 | 2 | 5 | 1782 |
| aluvion | `lluvia_7d_mm` | 97 mm | 4 | 12 | 1653 | 0 | 7 | 691 |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.8 mm | 16 | 0 | 9216 | 4 | 3 | 4722 |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.1 mm | 15 | 1 | 7083 | 4 | 3 | 3573 |
| aluvion | `lluvia_max_horaria_24h_mm` | 2.1 mm | 11 | 5 | 3098 | 2 | 5 | 1576 |
| aluvion | `lluvia_max_horaria_24h_mm` | 4.9 mm | 5 | 11 | 585 | 0 | 7 | 265 |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.6 mm | 14 | 2 | 8986 | 6 | 1 | 4624 |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 12 | 4 | 7132 | 5 | 2 | 3586 |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.3 mm | 10 | 6 | 3257 | 0 | 7 | 1602 |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.2 mm | 5 | 11 | 1262 | 0 | 7 | 618 |
| crecida | `lluvia_24h_mm` | 10.3 mm | 7 | 1 | 3431 | 2 | 2 | 1668 |
| crecida | `lluvia_24h_mm` | 19 mm | 6 | 2 | 1272 | 1 | 3 | 626 |
| crecida | `lluvia_24h_mm` | 24.3 mm | 4 | 4 | 774 | 1 | 3 | 376 |
| crecida | `lluvia_24h_mm` | 50.4 mm | 3 | 5 | 74 | 0 | 4 | 35 |
| crecida | `lluvia_48h_mm` | 19.2 mm | 7 | 1 | 3849 | 1 | 3 | 1907 |
| crecida | `lluvia_48h_mm` | 34.3 mm | 6 | 2 | 1454 | 1 | 3 | 645 |
| crecida | `lluvia_48h_mm` | 43.1 mm | 4 | 4 | 856 | 0 | 4 | 356 |
| crecida | `lluvia_48h_mm` | 62.8 mm | 2 | 6 | 208 | 0 | 4 | 97 |
| crecida | `lluvia_72h_mm` | 22.8 mm | 8 | 0 | 5312 | 2 | 2 | 2642 |
| crecida | `lluvia_72h_mm` | 35.6 mm | 7 | 1 | 2765 | 1 | 3 | 1293 |
| crecida | `lluvia_72h_mm` | 49.2 mm | 5 | 3 | 1420 | 1 | 3 | 594 |
| crecida | `lluvia_72h_mm` | 81.1 mm | 2 | 6 | 218 | 0 | 4 | 105 |
| crecida | `lluvia_7d_mm` | 48.8 mm | 7 | 1 | 6148 | 1 | 3 | 3020 |
| crecida | `lluvia_7d_mm` | 52.6 mm | 6 | 2 | 5522 | 1 | 3 | 2700 |
| crecida | `lluvia_7d_mm` | 93.3 mm | 4 | 4 | 1860 | 1 | 3 | 789 |
| crecida | `lluvia_7d_mm` | 148.4 mm | 2 | 6 | 207 | 1 | 3 | 56 |
| crecida | `lluvia_max_horaria_24h_mm` | 1.6 mm | 7 | 1 | 4629 | 2 | 2 | 2268 |
| crecida | `lluvia_max_horaria_24h_mm` | 2.3 mm | 7 | 1 | 2673 | 1 | 3 | 1344 |
| crecida | `lluvia_max_horaria_24h_mm` | 3.6 mm | 5 | 3 | 1134 | 0 | 4 | 551 |
| crecida | `lluvia_max_horaria_24h_mm` | 9.2 mm | 2 | 6 | 89 | 0 | 4 | 40 |
| crecida | `lluvia_max_horaria_72h_mm` | 2.7 mm | 8 | 0 | 4609 | 1 | 3 | 2295 |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 7 | 1 | 3942 | 1 | 3 | 1923 |
| crecida | `lluvia_max_horaria_72h_mm` | 4.5 mm | 5 | 3 | 1813 | 0 | 4 | 854 |
| crecida | `lluvia_max_horaria_72h_mm` | 9.2 mm | 2 | 6 | 233 | 0 | 4 | 110 |
| nieve | `nieve_24h_cm` | 0.1 cm | 10 | 4 | 270 | 8 | 13 | 110 |
| nieve | `nieve_24h_cm` | 0.2 cm | 9 | 5 | 231 | 8 | 13 | 99 |
| nieve | `nieve_24h_cm` | 0.8 cm | 6 | 8 | 114 | 4 | 17 | 43 |
| nieve | `nieve_72h_cm` | 0.2 cm | 11 | 3 | 557 | 13 | 8 | 217 |
| nieve | `nieve_72h_cm` | 0.6 cm | 9 | 5 | 362 | 6 | 15 | 145 |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 | 8 | 202 | 3 | 18 | 78 |
| nieve | `nieve_72h_cm` | 2.5 cm | 3 | 11 | 84 | 1 | 20 | 36 |
| nieve | `nieve_7d_cm` | 0.2 cm | 11 | 3 | 1138 | 13 | 8 | 442 |
| nieve | `nieve_7d_cm` | 0.6 cm | 10 | 4 | 768 | 7 | 14 | 313 |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 | 8 | 269 | 2 | 19 | 88 |
| nieve | `nieve_7d_cm` | 2.9 cm | 5 | 9 | 189 | 0 | 21 | 72 |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 11 | 5 | 5806 | 5 | 2 | 3348 |
| aluvion | `lluvia_24h_mm_pct` | p90 | 9 | 7 | 3061 | 3 | 4 | 1715 |
| aluvion | `lluvia_24h_mm_pct` | p95 | 4 | 12 | 1598 | 1 | 6 | 911 |
| aluvion | `lluvia_24h_mm_pct` | p98 | 2 | 14 | 670 | 0 | 7 | 386 |
| aluvion | `lluvia_24h_mm_pct` | p99 | 2 | 14 | 312 | 0 | 7 | 171 |
| aluvion | `lluvia_48h_mm_pct` | p80 | 9 | 7 | 6084 | 4 | 3 | 3347 |
| aluvion | `lluvia_48h_mm_pct` | p90 | 5 | 11 | 3153 | 3 | 4 | 1748 |
| aluvion | `lluvia_48h_mm_pct` | p95 | 3 | 13 | 1635 | 2 | 5 | 904 |
| aluvion | `lluvia_48h_mm_pct` | p98 | 2 | 14 | 669 | 1 | 6 | 330 |
| aluvion | `lluvia_48h_mm_pct` | p99 | 1 | 15 | 310 | 0 | 7 | 162 |
| aluvion | `lluvia_72h_mm_pct` | p80 | 5 | 11 | 6177 | 4 | 3 | 3350 |
| aluvion | `lluvia_72h_mm_pct` | p90 | 5 | 11 | 3227 | 4 | 3 | 1766 |
| aluvion | `lluvia_72h_mm_pct` | p95 | 3 | 13 | 1653 | 3 | 4 | 873 |
| aluvion | `lluvia_72h_mm_pct` | p98 | 1 | 15 | 670 | 1 | 6 | 293 |
| aluvion | `lluvia_72h_mm_pct` | p99 | 1 | 15 | 317 | 0 | 7 | 133 |
| aluvion | `lluvia_7d_mm_pct` | p80 | 7 | 9 | 6448 | 5 | 2 | 3546 |
| aluvion | `lluvia_7d_mm_pct` | p90 | 4 | 12 | 3296 | 4 | 3 | 1761 |
| aluvion | `lluvia_7d_mm_pct` | p95 | 1 | 15 | 1658 | 2 | 5 | 823 |
| aluvion | `lluvia_7d_mm_pct` | p98 | 1 | 15 | 661 | 1 | 6 | 296 |
| aluvion | `lluvia_7d_mm_pct` | p99 | 1 | 15 | 307 | 1 | 6 | 138 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 11 | 5 | 5803 | 5 | 2 | 3233 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 9 | 7 | 3023 | 3 | 4 | 1626 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 4 | 12 | 1590 | 1 | 6 | 872 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 3 | 13 | 654 | 1 | 6 | 312 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 | 14 | 316 | 0 | 7 | 149 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 7 | 9 | 6097 | 5 | 2 | 3203 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 5 | 11 | 3201 | 3 | 4 | 1734 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 4 | 12 | 1621 | 2 | 5 | 795 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 2 | 14 | 651 | 0 | 7 | 291 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 2 | 14 | 303 | 0 | 7 | 158 |
| crecida | `lluvia_24h_mm_pct` | p80 | 6 | 2 | 5810 | 2 | 2 | 3352 |
| crecida | `lluvia_24h_mm_pct` | p90 | 3 | 5 | 3067 | 1 | 3 | 1717 |
| crecida | `lluvia_24h_mm_pct` | p95 | 3 | 5 | 1599 | 1 | 3 | 911 |
| crecida | `lluvia_24h_mm_pct` | p98 | 3 | 5 | 669 | 0 | 4 | 386 |
| crecida | `lluvia_24h_mm_pct` | p99 | 2 | 6 | 312 | 0 | 4 | 171 |
| crecida | `lluvia_48h_mm_pct` | p80 | 6 | 2 | 6089 | 2 | 2 | 3349 |
| crecida | `lluvia_48h_mm_pct` | p90 | 3 | 5 | 3156 | 1 | 3 | 1751 |
| crecida | `lluvia_48h_mm_pct` | p95 | 3 | 5 | 1635 | 1 | 3 | 905 |
| crecida | `lluvia_48h_mm_pct` | p98 | 2 | 6 | 669 | 0 | 4 | 331 |
| crecida | `lluvia_48h_mm_pct` | p99 | 1 | 7 | 310 | 0 | 4 | 162 |
| crecida | `lluvia_72h_mm_pct` | p80 | 5 | 3 | 6177 | 1 | 3 | 3355 |
| crecida | `lluvia_72h_mm_pct` | p90 | 4 | 4 | 3229 | 1 | 3 | 1772 |
| crecida | `lluvia_72h_mm_pct` | p95 | 3 | 5 | 1653 | 0 | 4 | 878 |
| crecida | `lluvia_72h_mm_pct` | p98 | 1 | 7 | 670 | 0 | 4 | 294 |
| crecida | `lluvia_72h_mm_pct` | p99 | 1 | 7 | 317 | 0 | 4 | 133 |
| crecida | `lluvia_7d_mm_pct` | p80 | 4 | 4 | 6453 | 1 | 3 | 3554 |
| crecida | `lluvia_7d_mm_pct` | p90 | 4 | 4 | 3297 | 1 | 3 | 1766 |
| crecida | `lluvia_7d_mm_pct` | p95 | 3 | 5 | 1656 | 1 | 3 | 825 |
| crecida | `lluvia_7d_mm_pct` | p98 | 2 | 6 | 660 | 0 | 4 | 298 |
| crecida | `lluvia_7d_mm_pct` | p99 | 1 | 7 | 307 | 0 | 4 | 140 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 7 | 1 | 5809 | 2 | 2 | 3238 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 3 | 5 | 3029 | 0 | 4 | 1630 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 3 | 5 | 1591 | 0 | 4 | 873 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 3 | 5 | 654 | 0 | 4 | 313 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 1 | 7 | 317 | 0 | 4 | 149 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 4 | 4 | 6102 | 0 | 4 | 3212 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 4 | 4 | 3203 | 0 | 4 | 1739 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 4 | 4 | 1622 | 0 | 4 | 797 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 | 7 | 653 | 0 | 4 | 291 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 | 7 | 305 | 0 | 4 | 158 |
| nieve | `nieve_24h_cm_pct` | p80 | 11 | 3 | 323 | 10 | 11 | 139 |
| nieve | `nieve_24h_cm_pct` | p90 | 10 | 4 | 298 | 10 | 11 | 130 |
| nieve | `nieve_24h_cm_pct` | p95 | 10 | 4 | 265 | 10 | 11 | 111 |
| nieve | `nieve_24h_cm_pct` | p98 | 4 | 10 | 186 | 5 | 16 | 69 |
| nieve | `nieve_24h_cm_pct` | p99 | 2 | 12 | 117 | 4 | 17 | 40 |
| nieve | `nieve_72h_cm_pct` | p80 | 13 | 1 | 700 | 14 | 7 | 273 |
| nieve | `nieve_72h_cm_pct` | p90 | 11 | 3 | 608 | 13 | 8 | 233 |
| nieve | `nieve_72h_cm_pct` | p95 | 7 | 7 | 450 | 9 | 12 | 168 |
| nieve | `nieve_72h_cm_pct` | p98 | 3 | 11 | 265 | 5 | 16 | 83 |
| nieve | `nieve_72h_cm_pct` | p99 | 2 | 12 | 162 | 2 | 19 | 50 |
| nieve | `nieve_7d_cm_pct` | p80 | 11 | 3 | 1271 | 13 | 8 | 488 |
| nieve | `nieve_7d_cm_pct` | p90 | 6 | 8 | 971 | 10 | 11 | 357 |
| nieve | `nieve_7d_cm_pct` | p95 | 5 | 9 | 658 | 6 | 15 | 212 |
| nieve | `nieve_7d_cm_pct` | p98 | 2 | 12 | 359 | 2 | 19 | 102 |
| nieve | `nieve_7d_cm_pct` | p99 | 1 | 13 | 181 | 1 | 20 | 68 |

## Solo fuentes estables

Eventos con punto crítico usados: aluvión 23, crecida 12, nieve 31.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 16 | 12.8 | 4.9 | 79 |
| aluvion | `lluvia_48h_mm` | 16 | 20.5 | 11.5 | 80 |
| aluvion | `lluvia_72h_mm` | 16 | 28.4 | 19.3 | 74 |
| aluvion | `lluvia_7d_mm` | 16 | 66.9 | 50.9 | 73 |
| aluvion | `lluvia_max_horaria_24h_mm` | 16 | 2.1 | 1.0 | 79 |
| aluvion | `lluvia_max_horaria_72h_mm` | 16 | 3.3 | 1.9 | 77 |
| crecida | `lluvia_24h_mm` | 8 | 24.3 | 6.0 | 89 |
| crecida | `lluvia_48h_mm` | 8 | 43.1 | 14.3 | 89 |
| crecida | `lluvia_72h_mm` | 8 | 49.2 | 24.0 | 80 |
| crecida | `lluvia_7d_mm` | 8 | 93.3 | 61.3 | 86 |
| crecida | `lluvia_max_horaria_24h_mm` | 8 | 3.6 | 1.1 | 84 |
| crecida | `lluvia_max_horaria_72h_mm` | 8 | 4.5 | 2.2 | 75 |
| nieve | `nieve_24h_cm` | 14 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 14 | 1.2 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 14 | 1.7 | 0.0 | 89 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 4.5 mm | 16 | 0 | 7692 | 2 | 5 | 4062 |
| aluvion | `lluvia_24h_mm` | 5.3 mm | 15 | 1 | 6809 | 2 | 5 | 3594 |
| aluvion | `lluvia_24h_mm` | 12.8 mm | 10 | 6 | 2531 | 1 | 6 | 1230 |
| aluvion | `lluvia_24h_mm` | 29.5 mm | 5 | 11 | 534 | 0 | 7 | 217 |
| aluvion | `lluvia_48h_mm` | 12.5 mm | 14 | 2 | 6324 | 2 | 5 | 3225 |
| aluvion | `lluvia_48h_mm` | 16.4 mm | 14 | 2 | 4737 | 1 | 6 | 2351 |
| aluvion | `lluvia_48h_mm` | 20.5 mm | 9 | 7 | 3514 | 1 | 6 | 1715 |
| aluvion | `lluvia_48h_mm` | 44.8 mm | 4 | 12 | 755 | 0 | 7 | 321 |
| aluvion | `lluvia_72h_mm` | 18.3 mm | 14 | 2 | 6678 | 1 | 6 | 3446 |
| aluvion | `lluvia_72h_mm` | 24.6 mm | 12 | 4 | 4796 | 1 | 6 | 2389 |
| aluvion | `lluvia_72h_mm` | 28.4 mm | 11 | 5 | 3891 | 1 | 6 | 1953 |
| aluvion | `lluvia_72h_mm` | 48.6 mm | 4 | 12 | 1477 | 0 | 7 | 623 |
| aluvion | `lluvia_7d_mm` | 45 mm | 14 | 2 | 6752 | 2 | 5 | 3327 |
| aluvion | `lluvia_7d_mm` | 50.2 mm | 12 | 4 | 5898 | 2 | 5 | 2903 |
| aluvion | `lluvia_7d_mm` | 66.9 mm | 8 | 8 | 3840 | 2 | 5 | 1782 |
| aluvion | `lluvia_7d_mm` | 97 mm | 4 | 12 | 1653 | 0 | 7 | 691 |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.8 mm | 16 | 0 | 9216 | 4 | 3 | 4722 |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.1 mm | 15 | 1 | 7083 | 4 | 3 | 3573 |
| aluvion | `lluvia_max_horaria_24h_mm` | 2.1 mm | 11 | 5 | 3098 | 2 | 5 | 1576 |
| aluvion | `lluvia_max_horaria_24h_mm` | 4.9 mm | 5 | 11 | 585 | 0 | 7 | 265 |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.6 mm | 14 | 2 | 8986 | 6 | 1 | 4624 |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 12 | 4 | 7132 | 5 | 2 | 3586 |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.3 mm | 10 | 6 | 3257 | 0 | 7 | 1602 |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.2 mm | 5 | 11 | 1262 | 0 | 7 | 618 |
| crecida | `lluvia_24h_mm` | 10.3 mm | 7 | 1 | 3431 | 2 | 2 | 1668 |
| crecida | `lluvia_24h_mm` | 19 mm | 6 | 2 | 1272 | 1 | 3 | 626 |
| crecida | `lluvia_24h_mm` | 24.3 mm | 4 | 4 | 774 | 1 | 3 | 376 |
| crecida | `lluvia_24h_mm` | 50.4 mm | 3 | 5 | 74 | 0 | 4 | 35 |
| crecida | `lluvia_48h_mm` | 19.2 mm | 7 | 1 | 3849 | 1 | 3 | 1907 |
| crecida | `lluvia_48h_mm` | 34.3 mm | 6 | 2 | 1454 | 1 | 3 | 645 |
| crecida | `lluvia_48h_mm` | 43.1 mm | 4 | 4 | 856 | 0 | 4 | 356 |
| crecida | `lluvia_48h_mm` | 62.8 mm | 2 | 6 | 208 | 0 | 4 | 97 |
| crecida | `lluvia_72h_mm` | 22.8 mm | 8 | 0 | 5312 | 2 | 2 | 2642 |
| crecida | `lluvia_72h_mm` | 35.6 mm | 7 | 1 | 2765 | 1 | 3 | 1293 |
| crecida | `lluvia_72h_mm` | 49.2 mm | 5 | 3 | 1420 | 1 | 3 | 594 |
| crecida | `lluvia_72h_mm` | 81.1 mm | 2 | 6 | 218 | 0 | 4 | 105 |
| crecida | `lluvia_7d_mm` | 48.8 mm | 7 | 1 | 6148 | 1 | 3 | 3020 |
| crecida | `lluvia_7d_mm` | 52.6 mm | 6 | 2 | 5522 | 1 | 3 | 2700 |
| crecida | `lluvia_7d_mm` | 93.3 mm | 4 | 4 | 1860 | 1 | 3 | 789 |
| crecida | `lluvia_7d_mm` | 148.4 mm | 2 | 6 | 207 | 1 | 3 | 56 |
| crecida | `lluvia_max_horaria_24h_mm` | 1.6 mm | 7 | 1 | 4629 | 2 | 2 | 2268 |
| crecida | `lluvia_max_horaria_24h_mm` | 2.3 mm | 7 | 1 | 2673 | 1 | 3 | 1344 |
| crecida | `lluvia_max_horaria_24h_mm` | 3.6 mm | 5 | 3 | 1134 | 0 | 4 | 551 |
| crecida | `lluvia_max_horaria_24h_mm` | 9.2 mm | 2 | 6 | 89 | 0 | 4 | 40 |
| crecida | `lluvia_max_horaria_72h_mm` | 2.7 mm | 8 | 0 | 4609 | 1 | 3 | 2295 |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 7 | 1 | 3942 | 1 | 3 | 1923 |
| crecida | `lluvia_max_horaria_72h_mm` | 4.5 mm | 5 | 3 | 1813 | 0 | 4 | 854 |
| crecida | `lluvia_max_horaria_72h_mm` | 9.2 mm | 2 | 6 | 233 | 0 | 4 | 110 |
| nieve | `nieve_24h_cm` | 0.1 cm | 10 | 4 | 270 | 6 | 11 | 112 |
| nieve | `nieve_24h_cm` | 0.2 cm | 9 | 5 | 231 | 6 | 11 | 101 |
| nieve | `nieve_24h_cm` | 0.8 cm | 6 | 8 | 114 | 3 | 14 | 44 |
| nieve | `nieve_72h_cm` | 0.2 cm | 11 | 3 | 557 | 10 | 7 | 221 |
| nieve | `nieve_72h_cm` | 0.6 cm | 9 | 5 | 362 | 4 | 13 | 148 |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 | 8 | 202 | 2 | 15 | 80 |
| nieve | `nieve_72h_cm` | 2.5 cm | 3 | 11 | 84 | 1 | 16 | 36 |
| nieve | `nieve_7d_cm` | 0.2 cm | 11 | 3 | 1138 | 10 | 7 | 447 |
| nieve | `nieve_7d_cm` | 0.6 cm | 10 | 4 | 768 | 4 | 13 | 318 |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 | 8 | 269 | 2 | 15 | 88 |
| nieve | `nieve_7d_cm` | 2.9 cm | 5 | 9 | 189 | 0 | 17 | 72 |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 11 | 5 | 5806 | 5 | 2 | 3348 |
| aluvion | `lluvia_24h_mm_pct` | p90 | 9 | 7 | 3061 | 3 | 4 | 1715 |
| aluvion | `lluvia_24h_mm_pct` | p95 | 4 | 12 | 1598 | 1 | 6 | 911 |
| aluvion | `lluvia_24h_mm_pct` | p98 | 2 | 14 | 670 | 0 | 7 | 386 |
| aluvion | `lluvia_24h_mm_pct` | p99 | 2 | 14 | 312 | 0 | 7 | 171 |
| aluvion | `lluvia_48h_mm_pct` | p80 | 9 | 7 | 6084 | 4 | 3 | 3347 |
| aluvion | `lluvia_48h_mm_pct` | p90 | 5 | 11 | 3153 | 3 | 4 | 1748 |
| aluvion | `lluvia_48h_mm_pct` | p95 | 3 | 13 | 1635 | 2 | 5 | 904 |
| aluvion | `lluvia_48h_mm_pct` | p98 | 2 | 14 | 669 | 1 | 6 | 330 |
| aluvion | `lluvia_48h_mm_pct` | p99 | 1 | 15 | 310 | 0 | 7 | 162 |
| aluvion | `lluvia_72h_mm_pct` | p80 | 5 | 11 | 6177 | 4 | 3 | 3350 |
| aluvion | `lluvia_72h_mm_pct` | p90 | 5 | 11 | 3227 | 4 | 3 | 1766 |
| aluvion | `lluvia_72h_mm_pct` | p95 | 3 | 13 | 1653 | 3 | 4 | 873 |
| aluvion | `lluvia_72h_mm_pct` | p98 | 1 | 15 | 670 | 1 | 6 | 293 |
| aluvion | `lluvia_72h_mm_pct` | p99 | 1 | 15 | 317 | 0 | 7 | 133 |
| aluvion | `lluvia_7d_mm_pct` | p80 | 7 | 9 | 6448 | 5 | 2 | 3546 |
| aluvion | `lluvia_7d_mm_pct` | p90 | 4 | 12 | 3296 | 4 | 3 | 1761 |
| aluvion | `lluvia_7d_mm_pct` | p95 | 1 | 15 | 1658 | 2 | 5 | 823 |
| aluvion | `lluvia_7d_mm_pct` | p98 | 1 | 15 | 661 | 1 | 6 | 296 |
| aluvion | `lluvia_7d_mm_pct` | p99 | 1 | 15 | 307 | 1 | 6 | 138 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 11 | 5 | 5803 | 5 | 2 | 3233 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 9 | 7 | 3023 | 3 | 4 | 1626 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 4 | 12 | 1590 | 1 | 6 | 872 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 3 | 13 | 654 | 1 | 6 | 312 |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 | 14 | 316 | 0 | 7 | 149 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 7 | 9 | 6097 | 5 | 2 | 3203 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 5 | 11 | 3201 | 3 | 4 | 1734 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 4 | 12 | 1621 | 2 | 5 | 795 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 2 | 14 | 651 | 0 | 7 | 291 |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 2 | 14 | 303 | 0 | 7 | 158 |
| crecida | `lluvia_24h_mm_pct` | p80 | 6 | 2 | 5810 | 2 | 2 | 3352 |
| crecida | `lluvia_24h_mm_pct` | p90 | 3 | 5 | 3067 | 1 | 3 | 1717 |
| crecida | `lluvia_24h_mm_pct` | p95 | 3 | 5 | 1599 | 1 | 3 | 911 |
| crecida | `lluvia_24h_mm_pct` | p98 | 3 | 5 | 669 | 0 | 4 | 386 |
| crecida | `lluvia_24h_mm_pct` | p99 | 2 | 6 | 312 | 0 | 4 | 171 |
| crecida | `lluvia_48h_mm_pct` | p80 | 6 | 2 | 6089 | 2 | 2 | 3349 |
| crecida | `lluvia_48h_mm_pct` | p90 | 3 | 5 | 3156 | 1 | 3 | 1751 |
| crecida | `lluvia_48h_mm_pct` | p95 | 3 | 5 | 1635 | 1 | 3 | 905 |
| crecida | `lluvia_48h_mm_pct` | p98 | 2 | 6 | 669 | 0 | 4 | 331 |
| crecida | `lluvia_48h_mm_pct` | p99 | 1 | 7 | 310 | 0 | 4 | 162 |
| crecida | `lluvia_72h_mm_pct` | p80 | 5 | 3 | 6177 | 1 | 3 | 3355 |
| crecida | `lluvia_72h_mm_pct` | p90 | 4 | 4 | 3229 | 1 | 3 | 1772 |
| crecida | `lluvia_72h_mm_pct` | p95 | 3 | 5 | 1653 | 0 | 4 | 878 |
| crecida | `lluvia_72h_mm_pct` | p98 | 1 | 7 | 670 | 0 | 4 | 294 |
| crecida | `lluvia_72h_mm_pct` | p99 | 1 | 7 | 317 | 0 | 4 | 133 |
| crecida | `lluvia_7d_mm_pct` | p80 | 4 | 4 | 6453 | 1 | 3 | 3554 |
| crecida | `lluvia_7d_mm_pct` | p90 | 4 | 4 | 3297 | 1 | 3 | 1766 |
| crecida | `lluvia_7d_mm_pct` | p95 | 3 | 5 | 1656 | 1 | 3 | 825 |
| crecida | `lluvia_7d_mm_pct` | p98 | 2 | 6 | 660 | 0 | 4 | 298 |
| crecida | `lluvia_7d_mm_pct` | p99 | 1 | 7 | 307 | 0 | 4 | 140 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 7 | 1 | 5809 | 2 | 2 | 3238 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 3 | 5 | 3029 | 0 | 4 | 1630 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 3 | 5 | 1591 | 0 | 4 | 873 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 3 | 5 | 654 | 0 | 4 | 313 |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 1 | 7 | 317 | 0 | 4 | 149 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 4 | 4 | 6102 | 0 | 4 | 3212 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 4 | 4 | 3203 | 0 | 4 | 1739 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 4 | 4 | 1622 | 0 | 4 | 797 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 | 7 | 653 | 0 | 4 | 291 |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 | 7 | 305 | 0 | 4 | 158 |
| nieve | `nieve_24h_cm_pct` | p80 | 11 | 3 | 323 | 8 | 9 | 141 |
| nieve | `nieve_24h_cm_pct` | p90 | 10 | 4 | 298 | 8 | 9 | 132 |
| nieve | `nieve_24h_cm_pct` | p95 | 10 | 4 | 265 | 8 | 9 | 113 |
| nieve | `nieve_24h_cm_pct` | p98 | 4 | 10 | 186 | 4 | 13 | 70 |
| nieve | `nieve_24h_cm_pct` | p99 | 2 | 12 | 117 | 4 | 13 | 40 |
| nieve | `nieve_72h_cm_pct` | p80 | 13 | 1 | 700 | 11 | 6 | 277 |
| nieve | `nieve_72h_cm_pct` | p90 | 11 | 3 | 608 | 10 | 7 | 237 |
| nieve | `nieve_72h_cm_pct` | p95 | 7 | 7 | 450 | 7 | 10 | 171 |
| nieve | `nieve_72h_cm_pct` | p98 | 3 | 11 | 265 | 5 | 12 | 83 |
| nieve | `nieve_72h_cm_pct` | p99 | 2 | 12 | 162 | 2 | 15 | 50 |
| nieve | `nieve_7d_cm_pct` | p80 | 11 | 3 | 1271 | 10 | 7 | 493 |
| nieve | `nieve_7d_cm_pct` | p90 | 6 | 8 | 971 | 7 | 10 | 362 |
| nieve | `nieve_7d_cm_pct` | p95 | 5 | 9 | 658 | 6 | 11 | 212 |
| nieve | `nieve_7d_cm_pct` | p98 | 2 | 12 | 359 | 2 | 15 | 102 |
| nieve | `nieve_7d_cm_pct` | p99 | 1 | 13 | 181 | 1 | 16 | 68 |
