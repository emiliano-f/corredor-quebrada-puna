# Validación de umbrales

> Generado: 2026-11-14 01:09 UTC · versión `0.1.0.dev0` · commit `e86aa5e` · SCHEMA_VERSION 2 · fuentes `b3dab32ad1adf821`

Causas meteorológicas: aluvión y crecida contra lluvia, nieve contra nieve. Una regla por causa, igual para todos los puntos; ajuste 2016–2022, prueba 2023→hoy. Acierto = evento con alarma ese día o el anterior; falsa alarma = día con alarma sin evento ese día o el siguiente. Los mm de ERA5 no son lluvia local (ver docs/DATOS.md): por eso cada variable va también como percentil de su celda en la misma estación. Cada sección trae también la variante con aluvión y crecida juntos como una sola causa "lluvia". Junto a cada número va n = días-evento (punto, fecha) del período en que se basa; en prueba, n < 10 se marca "muestra chica". Vos elegís la regla final.

Fuentes estables (archivo desde ≤ 2016-01-01): elsubmarino, eltribunojujuy, jujuyaldia, jujuyalmomento, todojujuy.

## Todas las fuentes

Eventos con punto crítico usados: aluvión 23, crecida 12 (lluvia 35), nieve 35.

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
| aluvion | `lluvia_24h_mm` | 4.5 mm | 16 (n=16) | 0 (n=16) | 7692 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 4062 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm` | 5.3 mm | 15 (n=16) | 1 (n=16) | 6809 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 3594 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm` | 12.8 mm | 10 (n=16) | 6 (n=16) | 2531 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 1230 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm` | 29.5 mm | 5 (n=16) | 11 (n=16) | 534 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 217 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm` | 12.5 mm | 14 (n=16) | 2 (n=16) | 6324 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 3225 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm` | 16.4 mm | 14 (n=16) | 2 (n=16) | 4737 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 2351 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm` | 20.5 mm | 9 (n=16) | 7 (n=16) | 3514 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 1715 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm` | 44.8 mm | 4 (n=16) | 12 (n=16) | 755 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 321 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm` | 18.3 mm | 14 (n=16) | 2 (n=16) | 6678 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 3446 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm` | 24.6 mm | 12 (n=16) | 4 (n=16) | 4796 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 2389 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm` | 28.4 mm | 11 (n=16) | 5 (n=16) | 3891 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 1953 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm` | 48.6 mm | 4 (n=16) | 12 (n=16) | 1477 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 623 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm` | 45 mm | 14 (n=16) | 2 (n=16) | 6752 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 3327 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm` | 50.2 mm | 12 (n=16) | 4 (n=16) | 5898 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 2903 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm` | 66.9 mm | 8 (n=16) | 8 (n=16) | 3840 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 1782 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm` | 97 mm | 4 (n=16) | 12 (n=16) | 1653 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 691 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.8 mm | 16 (n=16) | 0 (n=16) | 9216 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 4722 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.1 mm | 15 (n=16) | 1 (n=16) | 7083 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 3573 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 2.1 mm | 11 (n=16) | 5 (n=16) | 3098 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 1576 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 4.9 mm | 5 (n=16) | 11 (n=16) | 585 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 265 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.6 mm | 14 (n=16) | 2 (n=16) | 8986 (n=16) | 6 (n=7 muestra chica) | 1 (n=7 muestra chica) | 4624 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 12 (n=16) | 4 (n=16) | 7132 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3586 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.3 mm | 10 (n=16) | 6 (n=16) | 3257 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 1602 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.2 mm | 5 (n=16) | 11 (n=16) | 1262 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 618 (n=7 muestra chica) |
| crecida | `lluvia_24h_mm` | 10.3 mm | 7 (n=8) | 1 (n=8) | 3431 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 1668 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 19 mm | 6 (n=8) | 2 (n=8) | 1272 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 626 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 24.3 mm | 4 (n=8) | 4 (n=8) | 774 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 376 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 50.4 mm | 3 (n=8) | 5 (n=8) | 74 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 35 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 19.2 mm | 7 (n=8) | 1 (n=8) | 3849 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1907 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 34.3 mm | 6 (n=8) | 2 (n=8) | 1454 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 645 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 43.1 mm | 4 (n=8) | 4 (n=8) | 856 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 356 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 62.8 mm | 2 (n=8) | 6 (n=8) | 208 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 97 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 22.8 mm | 8 (n=8) | 0 (n=8) | 5312 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 2642 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 35.6 mm | 7 (n=8) | 1 (n=8) | 2765 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1293 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 49.2 mm | 5 (n=8) | 3 (n=8) | 1420 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 594 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 81.1 mm | 2 (n=8) | 6 (n=8) | 218 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 105 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 48.8 mm | 7 (n=8) | 1 (n=8) | 6148 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3020 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 52.6 mm | 6 (n=8) | 2 (n=8) | 5522 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2700 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 93.3 mm | 4 (n=8) | 4 (n=8) | 1860 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 789 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 148.4 mm | 2 (n=8) | 6 (n=8) | 207 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 56 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.6 mm | 7 (n=8) | 1 (n=8) | 4629 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 2268 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.3 mm | 7 (n=8) | 1 (n=8) | 2673 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1344 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 3.6 mm | 5 (n=8) | 3 (n=8) | 1134 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 551 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 9.2 mm | 2 (n=8) | 6 (n=8) | 89 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 40 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 2.7 mm | 8 (n=8) | 0 (n=8) | 4609 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2295 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 7 (n=8) | 1 (n=8) | 3942 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1923 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.5 mm | 5 (n=8) | 3 (n=8) | 1813 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 854 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 9.2 mm | 2 (n=8) | 6 (n=8) | 233 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 110 (n=4 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 10 (n=14) | 4 (n=14) | 270 (n=14) | 8 (n=21) | 13 (n=21) | 110 (n=21) |
| nieve | `nieve_24h_cm` | 0.2 cm | 9 (n=14) | 5 (n=14) | 231 (n=14) | 8 (n=21) | 13 (n=21) | 99 (n=21) |
| nieve | `nieve_24h_cm` | 0.8 cm | 6 (n=14) | 8 (n=14) | 114 (n=14) | 4 (n=21) | 17 (n=21) | 43 (n=21) |
| nieve | `nieve_72h_cm` | 0.2 cm | 11 (n=14) | 3 (n=14) | 557 (n=14) | 13 (n=21) | 8 (n=21) | 217 (n=21) |
| nieve | `nieve_72h_cm` | 0.6 cm | 9 (n=14) | 5 (n=14) | 362 (n=14) | 6 (n=21) | 15 (n=21) | 145 (n=21) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=14) | 8 (n=14) | 202 (n=14) | 3 (n=21) | 18 (n=21) | 78 (n=21) |
| nieve | `nieve_72h_cm` | 2.5 cm | 3 (n=14) | 11 (n=14) | 84 (n=14) | 1 (n=21) | 20 (n=21) | 36 (n=21) |
| nieve | `nieve_7d_cm` | 0.2 cm | 11 (n=14) | 3 (n=14) | 1138 (n=14) | 13 (n=21) | 8 (n=21) | 442 (n=21) |
| nieve | `nieve_7d_cm` | 0.6 cm | 10 (n=14) | 4 (n=14) | 768 (n=14) | 7 (n=21) | 14 (n=21) | 313 (n=21) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=14) | 8 (n=14) | 269 (n=14) | 2 (n=21) | 19 (n=21) | 88 (n=21) |
| nieve | `nieve_7d_cm` | 2.9 cm | 5 (n=14) | 9 (n=14) | 189 (n=14) | 0 (n=21) | 21 (n=21) | 72 (n=21) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 11 (n=16) | 5 (n=16) | 5806 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3348 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 9 (n=16) | 7 (n=16) | 3061 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 1715 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 4 (n=16) | 12 (n=16) | 1598 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 911 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 2 (n=16) | 14 (n=16) | 670 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 386 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 2 (n=16) | 14 (n=16) | 312 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 171 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 9 (n=16) | 7 (n=16) | 6084 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 3347 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 5 (n=16) | 11 (n=16) | 3153 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 1748 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 3 (n=16) | 13 (n=16) | 1635 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 904 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 2 (n=16) | 14 (n=16) | 669 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 330 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 1 (n=16) | 15 (n=16) | 310 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 162 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 5 (n=16) | 11 (n=16) | 6177 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 3350 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 5 (n=16) | 11 (n=16) | 3227 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 1766 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 3 (n=16) | 13 (n=16) | 1653 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 873 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 1 (n=16) | 15 (n=16) | 670 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 293 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 1 (n=16) | 15 (n=16) | 317 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 133 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 7 (n=16) | 9 (n=16) | 6448 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3546 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 4 (n=16) | 12 (n=16) | 3296 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 1761 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 1 (n=16) | 15 (n=16) | 1658 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 823 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 1 (n=16) | 15 (n=16) | 661 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 296 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 1 (n=16) | 15 (n=16) | 307 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 138 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 11 (n=16) | 5 (n=16) | 5803 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3233 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 9 (n=16) | 7 (n=16) | 3023 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 1626 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 4 (n=16) | 12 (n=16) | 1590 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 872 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 3 (n=16) | 13 (n=16) | 654 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 312 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 (n=16) | 14 (n=16) | 316 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 149 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 7 (n=16) | 9 (n=16) | 6097 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3203 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 5 (n=16) | 11 (n=16) | 3201 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 1734 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 4 (n=16) | 12 (n=16) | 1621 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 795 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 2 (n=16) | 14 (n=16) | 651 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 291 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 2 (n=16) | 14 (n=16) | 303 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 158 (n=7 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p80 | 6 (n=8) | 2 (n=8) | 5810 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3352 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 3 (n=8) | 5 (n=8) | 3067 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1717 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1599 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 911 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 3 (n=8) | 5 (n=8) | 669 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 386 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 2 (n=8) | 6 (n=8) | 312 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 171 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 6 (n=8) | 2 (n=8) | 6089 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3349 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 3 (n=8) | 5 (n=8) | 3156 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1751 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1635 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 905 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 2 (n=8) | 6 (n=8) | 669 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 331 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 310 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 162 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 5 (n=8) | 3 (n=8) | 6177 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3355 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 4 (n=8) | 4 (n=8) | 3229 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1772 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1653 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 878 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 1 (n=8) | 7 (n=8) | 670 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 294 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 317 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 133 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 4 (n=8) | 4 (n=8) | 6453 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3554 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 4 (n=8) | 4 (n=8) | 3297 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1766 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1656 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 825 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 2 (n=8) | 6 (n=8) | 660 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 298 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 307 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 140 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 7 (n=8) | 1 (n=8) | 5809 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3238 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 3 (n=8) | 5 (n=8) | 3029 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1630 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1591 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 873 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 3 (n=8) | 5 (n=8) | 654 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 313 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 317 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 149 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 4 (n=8) | 4 (n=8) | 6102 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 3212 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 4 (n=8) | 4 (n=8) | 3203 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1739 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 4 (n=8) | 4 (n=8) | 1622 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 797 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=8) | 7 (n=8) | 653 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 291 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 305 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 158 (n=4 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 323 (n=14) | 10 (n=21) | 11 (n=21) | 139 (n=21) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=14) | 4 (n=14) | 298 (n=14) | 10 (n=21) | 11 (n=21) | 130 (n=21) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=14) | 4 (n=14) | 265 (n=14) | 10 (n=21) | 11 (n=21) | 111 (n=21) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=14) | 10 (n=14) | 186 (n=14) | 5 (n=21) | 16 (n=21) | 69 (n=21) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 117 (n=14) | 4 (n=21) | 17 (n=21) | 40 (n=21) |
| nieve | `nieve_72h_cm_pct` | p80 | 13 (n=14) | 1 (n=14) | 700 (n=14) | 14 (n=21) | 7 (n=21) | 273 (n=21) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=14) | 3 (n=14) | 608 (n=14) | 13 (n=21) | 8 (n=21) | 233 (n=21) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=14) | 7 (n=14) | 450 (n=14) | 9 (n=21) | 12 (n=21) | 168 (n=21) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=14) | 11 (n=14) | 265 (n=14) | 5 (n=21) | 16 (n=21) | 83 (n=21) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 162 (n=14) | 2 (n=21) | 19 (n=21) | 50 (n=21) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 1271 (n=14) | 13 (n=21) | 8 (n=21) | 488 (n=21) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=14) | 8 (n=14) | 971 (n=14) | 10 (n=21) | 11 (n=21) | 357 (n=21) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=14) | 9 (n=14) | 658 (n=14) | 6 (n=21) | 15 (n=21) | 212 (n=21) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=14) | 12 (n=14) | 359 (n=14) | 2 (n=21) | 19 (n=21) | 102 (n=21) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=14) | 13 (n=14) | 181 (n=14) | 1 (n=21) | 20 (n=21) | 68 (n=21) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 24 | 18.3 | 4.7 | 87 |
| lluvia | `lluvia_48h_mm` | 24 | 33.6 | 11.0 | 83 |
| lluvia | `lluvia_72h_mm` | 24 | 39.0 | 18.2 | 75 |
| lluvia | `lluvia_7d_mm` | 24 | 71.5 | 49.4 | 76 |
| lluvia | `lluvia_max_horaria_24h_mm` | 24 | 2.6 | 0.9 | 82 |
| lluvia | `lluvia_max_horaria_72h_mm` | 24 | 4.1 | 1.8 | 76 |
| nieve | `nieve_24h_cm` | 14 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 14 | 1.2 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 14 | 1.7 | 0.0 | 89 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 4.9 mm | 24 (n=24) | 0 (n=24) | 7198 (n=24) | 4 (n=11) | 7 (n=11) | 3791 (n=11) |
| lluvia | `lluvia_24h_mm` | 6.9 mm | 22 (n=24) | 2 (n=24) | 5372 (n=24) | 4 (n=11) | 7 (n=11) | 2754 (n=11) |
| lluvia | `lluvia_24h_mm` | 18.3 mm | 13 (n=24) | 11 (n=24) | 1369 (n=24) | 1 (n=11) | 10 (n=11) | 660 (n=11) |
| lluvia | `lluvia_24h_mm` | 34 mm | 6 (n=24) | 18 (n=24) | 353 (n=24) | 0 (n=11) | 11 (n=11) | 159 (n=11) |
| lluvia | `lluvia_48h_mm` | 11.7 mm | 21 (n=24) | 3 (n=24) | 6672 (n=24) | 4 (n=11) | 7 (n=11) | 3432 (n=11) |
| lluvia | `lluvia_48h_mm` | 16.7 mm | 21 (n=24) | 3 (n=24) | 4612 (n=24) | 3 (n=11) | 8 (n=11) | 2282 (n=11) |
| lluvia | `lluvia_48h_mm` | 33.6 mm | 13 (n=24) | 11 (n=24) | 1495 (n=24) | 1 (n=11) | 10 (n=11) | 678 (n=11) |
| lluvia | `lluvia_48h_mm` | 50.1 mm | 6 (n=24) | 18 (n=24) | 527 (n=24) | 0 (n=11) | 11 (n=11) | 219 (n=11) |
| lluvia | `lluvia_72h_mm` | 19 mm | 22 (n=24) | 2 (n=24) | 6451 (n=24) | 3 (n=11) | 8 (n=11) | 3324 (n=11) |
| lluvia | `lluvia_72h_mm` | 25.2 mm | 19 (n=24) | 5 (n=24) | 4608 (n=24) | 2 (n=11) | 9 (n=11) | 2306 (n=11) |
| lluvia | `lluvia_72h_mm` | 39 mm | 14 (n=24) | 10 (n=24) | 2318 (n=24) | 1 (n=11) | 10 (n=11) | 1063 (n=11) |
| lluvia | `lluvia_72h_mm` | 54.5 mm | 6 (n=24) | 18 (n=24) | 1072 (n=24) | 0 (n=11) | 11 (n=11) | 437 (n=11) |
| lluvia | `lluvia_7d_mm` | 47.3 mm | 21 (n=24) | 3 (n=24) | 6367 (n=24) | 3 (n=11) | 8 (n=11) | 3122 (n=11) |
| lluvia | `lluvia_7d_mm` | 50.3 mm | 18 (n=24) | 6 (n=24) | 5872 (n=24) | 3 (n=11) | 8 (n=11) | 2897 (n=11) |
| lluvia | `lluvia_7d_mm` | 71.5 mm | 12 (n=24) | 12 (n=24) | 3393 (n=24) | 2 (n=11) | 9 (n=11) | 1561 (n=11) |
| lluvia | `lluvia_7d_mm` | 116 mm | 7 (n=24) | 17 (n=24) | 869 (n=24) | 1 (n=11) | 10 (n=11) | 379 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1 mm | 24 (n=24) | 0 (n=24) | 7748 (n=24) | 6 (n=11) | 5 (n=11) | 3936 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.5 mm | 21 (n=24) | 3 (n=24) | 4992 (n=24) | 5 (n=11) | 6 (n=11) | 2495 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm` | 2.6 mm | 16 (n=24) | 8 (n=24) | 2151 (n=24) | 1 (n=11) | 10 (n=11) | 1068 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm` | 5.7 mm | 6 (n=24) | 18 (n=24) | 373 (n=24) | 0 (n=11) | 11 (n=11) | 187 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.8 mm | 22 (n=24) | 2 (n=24) | 8021 (n=24) | 7 (n=11) | 4 (n=11) | 4102 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm` | 2.2 mm | 20 (n=24) | 4 (n=24) | 6262 (n=24) | 5 (n=11) | 6 (n=11) | 3221 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm` | 4.1 mm | 14 (n=24) | 10 (n=24) | 2148 (n=24) | 0 (n=11) | 11 (n=11) | 1037 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm` | 5.7 mm | 7 (n=24) | 17 (n=24) | 960 (n=24) | 0 (n=11) | 11 (n=11) | 501 (n=11) |
| nieve | `nieve_24h_cm` | 0.1 cm | 10 (n=14) | 4 (n=14) | 270 (n=14) | 8 (n=21) | 13 (n=21) | 110 (n=21) |
| nieve | `nieve_24h_cm` | 0.2 cm | 9 (n=14) | 5 (n=14) | 231 (n=14) | 8 (n=21) | 13 (n=21) | 99 (n=21) |
| nieve | `nieve_24h_cm` | 0.8 cm | 6 (n=14) | 8 (n=14) | 114 (n=14) | 4 (n=21) | 17 (n=21) | 43 (n=21) |
| nieve | `nieve_72h_cm` | 0.2 cm | 11 (n=14) | 3 (n=14) | 557 (n=14) | 13 (n=21) | 8 (n=21) | 217 (n=21) |
| nieve | `nieve_72h_cm` | 0.6 cm | 9 (n=14) | 5 (n=14) | 362 (n=14) | 6 (n=21) | 15 (n=21) | 145 (n=21) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=14) | 8 (n=14) | 202 (n=14) | 3 (n=21) | 18 (n=21) | 78 (n=21) |
| nieve | `nieve_72h_cm` | 2.5 cm | 3 (n=14) | 11 (n=14) | 84 (n=14) | 1 (n=21) | 20 (n=21) | 36 (n=21) |
| nieve | `nieve_7d_cm` | 0.2 cm | 11 (n=14) | 3 (n=14) | 1138 (n=14) | 13 (n=21) | 8 (n=21) | 442 (n=21) |
| nieve | `nieve_7d_cm` | 0.6 cm | 10 (n=14) | 4 (n=14) | 768 (n=14) | 7 (n=21) | 14 (n=21) | 313 (n=21) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=14) | 8 (n=14) | 269 (n=14) | 2 (n=21) | 19 (n=21) | 88 (n=21) |
| nieve | `nieve_7d_cm` | 2.9 cm | 5 (n=14) | 9 (n=14) | 189 (n=14) | 0 (n=21) | 21 (n=21) | 72 (n=21) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 17 (n=24) | 7 (n=24) | 5796 (n=24) | 7 (n=11) | 4 (n=11) | 3345 (n=11) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 12 (n=24) | 12 (n=24) | 3057 (n=24) | 4 (n=11) | 7 (n=11) | 1713 (n=11) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 7 (n=24) | 17 (n=24) | 1594 (n=24) | 2 (n=11) | 9 (n=11) | 910 (n=11) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 5 (n=24) | 19 (n=24) | 666 (n=24) | 0 (n=11) | 11 (n=11) | 386 (n=11) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 4 (n=24) | 20 (n=24) | 310 (n=24) | 0 (n=11) | 11 (n=11) | 171 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 15 (n=24) | 9 (n=24) | 6077 (n=24) | 6 (n=11) | 5 (n=11) | 3343 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3149 (n=24) | 4 (n=11) | 7 (n=11) | 1746 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1631 (n=24) | 3 (n=11) | 8 (n=11) | 903 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 4 (n=24) | 20 (n=24) | 666 (n=24) | 1 (n=11) | 10 (n=11) | 330 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 308 (n=24) | 0 (n=11) | 11 (n=11) | 162 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 10 (n=24) | 14 (n=24) | 6169 (n=24) | 5 (n=11) | 6 (n=11) | 3348 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 9 (n=24) | 15 (n=24) | 3222 (n=24) | 5 (n=11) | 6 (n=11) | 1765 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1649 (n=24) | 3 (n=11) | 8 (n=11) | 873 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 2 (n=24) | 22 (n=24) | 668 (n=24) | 1 (n=11) | 10 (n=11) | 293 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 316 (n=24) | 0 (n=11) | 11 (n=11) | 133 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 11 (n=24) | 13 (n=24) | 6441 (n=24) | 6 (n=11) | 5 (n=11) | 3544 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3291 (n=24) | 5 (n=11) | 6 (n=11) | 1759 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 4 (n=24) | 20 (n=24) | 1654 (n=24) | 3 (n=11) | 8 (n=11) | 821 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 658 (n=24) | 1 (n=11) | 10 (n=11) | 296 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 306 (n=24) | 1 (n=11) | 10 (n=11) | 138 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 18 (n=24) | 6 (n=24) | 5793 (n=24) | 7 (n=11) | 4 (n=11) | 3231 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 12 (n=24) | 12 (n=24) | 3018 (n=24) | 3 (n=11) | 8 (n=11) | 1626 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 7 (n=24) | 17 (n=24) | 1585 (n=24) | 1 (n=11) | 10 (n=11) | 872 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 6 (n=24) | 18 (n=24) | 650 (n=24) | 1 (n=11) | 10 (n=11) | 312 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 314 (n=24) | 0 (n=11) | 11 (n=11) | 149 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 11 (n=24) | 13 (n=24) | 6090 (n=24) | 5 (n=11) | 6 (n=11) | 3203 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 9 (n=24) | 15 (n=24) | 3196 (n=24) | 3 (n=11) | 8 (n=11) | 1734 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 8 (n=24) | 16 (n=24) | 1616 (n=24) | 2 (n=11) | 9 (n=11) | 795 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 649 (n=24) | 0 (n=11) | 11 (n=11) | 291 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 301 (n=24) | 0 (n=11) | 11 (n=11) | 158 (n=11) |
| nieve | `nieve_24h_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 323 (n=14) | 10 (n=21) | 11 (n=21) | 139 (n=21) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=14) | 4 (n=14) | 298 (n=14) | 10 (n=21) | 11 (n=21) | 130 (n=21) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=14) | 4 (n=14) | 265 (n=14) | 10 (n=21) | 11 (n=21) | 111 (n=21) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=14) | 10 (n=14) | 186 (n=14) | 5 (n=21) | 16 (n=21) | 69 (n=21) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 117 (n=14) | 4 (n=21) | 17 (n=21) | 40 (n=21) |
| nieve | `nieve_72h_cm_pct` | p80 | 13 (n=14) | 1 (n=14) | 700 (n=14) | 14 (n=21) | 7 (n=21) | 273 (n=21) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=14) | 3 (n=14) | 608 (n=14) | 13 (n=21) | 8 (n=21) | 233 (n=21) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=14) | 7 (n=14) | 450 (n=14) | 9 (n=21) | 12 (n=21) | 168 (n=21) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=14) | 11 (n=14) | 265 (n=14) | 5 (n=21) | 16 (n=21) | 83 (n=21) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 162 (n=14) | 2 (n=21) | 19 (n=21) | 50 (n=21) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 1271 (n=14) | 13 (n=21) | 8 (n=21) | 488 (n=21) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=14) | 8 (n=14) | 971 (n=14) | 10 (n=21) | 11 (n=21) | 357 (n=21) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=14) | 9 (n=14) | 658 (n=14) | 6 (n=21) | 15 (n=21) | 212 (n=21) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=14) | 12 (n=14) | 359 (n=14) | 2 (n=21) | 19 (n=21) | 102 (n=21) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=14) | 13 (n=14) | 181 (n=14) | 1 (n=21) | 20 (n=21) | 68 (n=21) |

## Solo fuentes estables

Eventos con punto crítico usados: aluvión 23, crecida 12 (lluvia 35), nieve 31.

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
| aluvion | `lluvia_24h_mm` | 4.5 mm | 16 (n=16) | 0 (n=16) | 7692 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 4062 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm` | 5.3 mm | 15 (n=16) | 1 (n=16) | 6809 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 3594 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm` | 12.8 mm | 10 (n=16) | 6 (n=16) | 2531 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 1230 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm` | 29.5 mm | 5 (n=16) | 11 (n=16) | 534 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 217 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm` | 12.5 mm | 14 (n=16) | 2 (n=16) | 6324 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 3225 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm` | 16.4 mm | 14 (n=16) | 2 (n=16) | 4737 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 2351 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm` | 20.5 mm | 9 (n=16) | 7 (n=16) | 3514 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 1715 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm` | 44.8 mm | 4 (n=16) | 12 (n=16) | 755 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 321 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm` | 18.3 mm | 14 (n=16) | 2 (n=16) | 6678 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 3446 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm` | 24.6 mm | 12 (n=16) | 4 (n=16) | 4796 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 2389 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm` | 28.4 mm | 11 (n=16) | 5 (n=16) | 3891 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 1953 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm` | 48.6 mm | 4 (n=16) | 12 (n=16) | 1477 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 623 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm` | 45 mm | 14 (n=16) | 2 (n=16) | 6752 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 3327 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm` | 50.2 mm | 12 (n=16) | 4 (n=16) | 5898 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 2903 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm` | 66.9 mm | 8 (n=16) | 8 (n=16) | 3840 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 1782 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm` | 97 mm | 4 (n=16) | 12 (n=16) | 1653 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 691 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.8 mm | 16 (n=16) | 0 (n=16) | 9216 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 4722 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.1 mm | 15 (n=16) | 1 (n=16) | 7083 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 3573 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 2.1 mm | 11 (n=16) | 5 (n=16) | 3098 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 1576 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm` | 4.9 mm | 5 (n=16) | 11 (n=16) | 585 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 265 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.6 mm | 14 (n=16) | 2 (n=16) | 8986 (n=16) | 6 (n=7 muestra chica) | 1 (n=7 muestra chica) | 4624 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 12 (n=16) | 4 (n=16) | 7132 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3586 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.3 mm | 10 (n=16) | 6 (n=16) | 3257 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 1602 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.2 mm | 5 (n=16) | 11 (n=16) | 1262 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 618 (n=7 muestra chica) |
| crecida | `lluvia_24h_mm` | 10.3 mm | 7 (n=8) | 1 (n=8) | 3431 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 1668 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 19 mm | 6 (n=8) | 2 (n=8) | 1272 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 626 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 24.3 mm | 4 (n=8) | 4 (n=8) | 774 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 376 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm` | 50.4 mm | 3 (n=8) | 5 (n=8) | 74 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 35 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 19.2 mm | 7 (n=8) | 1 (n=8) | 3849 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1907 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 34.3 mm | 6 (n=8) | 2 (n=8) | 1454 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 645 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 43.1 mm | 4 (n=8) | 4 (n=8) | 856 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 356 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm` | 62.8 mm | 2 (n=8) | 6 (n=8) | 208 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 97 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 22.8 mm | 8 (n=8) | 0 (n=8) | 5312 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 2642 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 35.6 mm | 7 (n=8) | 1 (n=8) | 2765 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1293 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 49.2 mm | 5 (n=8) | 3 (n=8) | 1420 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 594 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm` | 81.1 mm | 2 (n=8) | 6 (n=8) | 218 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 105 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 48.8 mm | 7 (n=8) | 1 (n=8) | 6148 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3020 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 52.6 mm | 6 (n=8) | 2 (n=8) | 5522 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2700 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 93.3 mm | 4 (n=8) | 4 (n=8) | 1860 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 789 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm` | 148.4 mm | 2 (n=8) | 6 (n=8) | 207 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 56 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.6 mm | 7 (n=8) | 1 (n=8) | 4629 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 2268 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.3 mm | 7 (n=8) | 1 (n=8) | 2673 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1344 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 3.6 mm | 5 (n=8) | 3 (n=8) | 1134 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 551 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 9.2 mm | 2 (n=8) | 6 (n=8) | 89 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 40 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 2.7 mm | 8 (n=8) | 0 (n=8) | 4609 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 2295 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 7 (n=8) | 1 (n=8) | 3942 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1923 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.5 mm | 5 (n=8) | 3 (n=8) | 1813 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 854 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 9.2 mm | 2 (n=8) | 6 (n=8) | 233 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 110 (n=4 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 10 (n=14) | 4 (n=14) | 270 (n=14) | 6 (n=17) | 11 (n=17) | 112 (n=17) |
| nieve | `nieve_24h_cm` | 0.2 cm | 9 (n=14) | 5 (n=14) | 231 (n=14) | 6 (n=17) | 11 (n=17) | 101 (n=17) |
| nieve | `nieve_24h_cm` | 0.8 cm | 6 (n=14) | 8 (n=14) | 114 (n=14) | 3 (n=17) | 14 (n=17) | 44 (n=17) |
| nieve | `nieve_72h_cm` | 0.2 cm | 11 (n=14) | 3 (n=14) | 557 (n=14) | 10 (n=17) | 7 (n=17) | 221 (n=17) |
| nieve | `nieve_72h_cm` | 0.6 cm | 9 (n=14) | 5 (n=14) | 362 (n=14) | 4 (n=17) | 13 (n=17) | 148 (n=17) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=14) | 8 (n=14) | 202 (n=14) | 2 (n=17) | 15 (n=17) | 80 (n=17) |
| nieve | `nieve_72h_cm` | 2.5 cm | 3 (n=14) | 11 (n=14) | 84 (n=14) | 1 (n=17) | 16 (n=17) | 36 (n=17) |
| nieve | `nieve_7d_cm` | 0.2 cm | 11 (n=14) | 3 (n=14) | 1138 (n=14) | 10 (n=17) | 7 (n=17) | 447 (n=17) |
| nieve | `nieve_7d_cm` | 0.6 cm | 10 (n=14) | 4 (n=14) | 768 (n=14) | 4 (n=17) | 13 (n=17) | 318 (n=17) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=14) | 8 (n=14) | 269 (n=14) | 2 (n=17) | 15 (n=17) | 88 (n=17) |
| nieve | `nieve_7d_cm` | 2.9 cm | 5 (n=14) | 9 (n=14) | 189 (n=14) | 0 (n=17) | 17 (n=17) | 72 (n=17) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 11 (n=16) | 5 (n=16) | 5806 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3348 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 9 (n=16) | 7 (n=16) | 3061 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 1715 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 4 (n=16) | 12 (n=16) | 1598 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 911 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 2 (n=16) | 14 (n=16) | 670 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 386 (n=7 muestra chica) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 2 (n=16) | 14 (n=16) | 312 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 171 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 9 (n=16) | 7 (n=16) | 6084 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 3347 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 5 (n=16) | 11 (n=16) | 3153 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 1748 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 3 (n=16) | 13 (n=16) | 1635 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 904 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 2 (n=16) | 14 (n=16) | 669 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 330 (n=7 muestra chica) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 1 (n=16) | 15 (n=16) | 310 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 162 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 5 (n=16) | 11 (n=16) | 6177 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 3350 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 5 (n=16) | 11 (n=16) | 3227 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 1766 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 3 (n=16) | 13 (n=16) | 1653 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 873 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 1 (n=16) | 15 (n=16) | 670 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 293 (n=7 muestra chica) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 1 (n=16) | 15 (n=16) | 317 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 133 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 7 (n=16) | 9 (n=16) | 6448 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3546 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 4 (n=16) | 12 (n=16) | 3296 (n=16) | 4 (n=7 muestra chica) | 3 (n=7 muestra chica) | 1761 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 1 (n=16) | 15 (n=16) | 1658 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 823 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 1 (n=16) | 15 (n=16) | 661 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 296 (n=7 muestra chica) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 1 (n=16) | 15 (n=16) | 307 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 138 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 11 (n=16) | 5 (n=16) | 5803 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3233 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 9 (n=16) | 7 (n=16) | 3023 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 1626 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 4 (n=16) | 12 (n=16) | 1590 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 872 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 3 (n=16) | 13 (n=16) | 654 (n=16) | 1 (n=7 muestra chica) | 6 (n=7 muestra chica) | 312 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 (n=16) | 14 (n=16) | 316 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 149 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 7 (n=16) | 9 (n=16) | 6097 (n=16) | 5 (n=7 muestra chica) | 2 (n=7 muestra chica) | 3203 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 5 (n=16) | 11 (n=16) | 3201 (n=16) | 3 (n=7 muestra chica) | 4 (n=7 muestra chica) | 1734 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 4 (n=16) | 12 (n=16) | 1621 (n=16) | 2 (n=7 muestra chica) | 5 (n=7 muestra chica) | 795 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 2 (n=16) | 14 (n=16) | 651 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 291 (n=7 muestra chica) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 2 (n=16) | 14 (n=16) | 303 (n=16) | 0 (n=7 muestra chica) | 7 (n=7 muestra chica) | 158 (n=7 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p80 | 6 (n=8) | 2 (n=8) | 5810 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3352 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 3 (n=8) | 5 (n=8) | 3067 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1717 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1599 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 911 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 3 (n=8) | 5 (n=8) | 669 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 386 (n=4 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 2 (n=8) | 6 (n=8) | 312 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 171 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 6 (n=8) | 2 (n=8) | 6089 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3349 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 3 (n=8) | 5 (n=8) | 3156 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1751 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1635 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 905 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 2 (n=8) | 6 (n=8) | 669 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 331 (n=4 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 310 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 162 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 5 (n=8) | 3 (n=8) | 6177 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3355 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 4 (n=8) | 4 (n=8) | 3229 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1772 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1653 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 878 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 1 (n=8) | 7 (n=8) | 670 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 294 (n=4 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 317 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 133 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 4 (n=8) | 4 (n=8) | 6453 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 3554 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 4 (n=8) | 4 (n=8) | 3297 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 1766 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1656 (n=8) | 1 (n=4 muestra chica) | 3 (n=4 muestra chica) | 825 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 2 (n=8) | 6 (n=8) | 660 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 298 (n=4 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 307 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 140 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 7 (n=8) | 1 (n=8) | 5809 (n=8) | 2 (n=4 muestra chica) | 2 (n=4 muestra chica) | 3238 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 3 (n=8) | 5 (n=8) | 3029 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1630 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 3 (n=8) | 5 (n=8) | 1591 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 873 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 3 (n=8) | 5 (n=8) | 654 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 313 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 317 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 149 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 4 (n=8) | 4 (n=8) | 6102 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 3212 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 4 (n=8) | 4 (n=8) | 3203 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 1739 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 4 (n=8) | 4 (n=8) | 1622 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 797 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=8) | 7 (n=8) | 653 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 291 (n=4 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=8) | 7 (n=8) | 305 (n=8) | 0 (n=4 muestra chica) | 4 (n=4 muestra chica) | 158 (n=4 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 323 (n=14) | 8 (n=17) | 9 (n=17) | 141 (n=17) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=14) | 4 (n=14) | 298 (n=14) | 8 (n=17) | 9 (n=17) | 132 (n=17) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=14) | 4 (n=14) | 265 (n=14) | 8 (n=17) | 9 (n=17) | 113 (n=17) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=14) | 10 (n=14) | 186 (n=14) | 4 (n=17) | 13 (n=17) | 70 (n=17) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 117 (n=14) | 4 (n=17) | 13 (n=17) | 40 (n=17) |
| nieve | `nieve_72h_cm_pct` | p80 | 13 (n=14) | 1 (n=14) | 700 (n=14) | 11 (n=17) | 6 (n=17) | 277 (n=17) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=14) | 3 (n=14) | 608 (n=14) | 10 (n=17) | 7 (n=17) | 237 (n=17) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=14) | 7 (n=14) | 450 (n=14) | 7 (n=17) | 10 (n=17) | 171 (n=17) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=14) | 11 (n=14) | 265 (n=14) | 5 (n=17) | 12 (n=17) | 83 (n=17) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 162 (n=14) | 2 (n=17) | 15 (n=17) | 50 (n=17) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 1271 (n=14) | 10 (n=17) | 7 (n=17) | 493 (n=17) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=14) | 8 (n=14) | 971 (n=14) | 7 (n=17) | 10 (n=17) | 362 (n=17) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=14) | 9 (n=14) | 658 (n=14) | 6 (n=17) | 11 (n=17) | 212 (n=17) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=14) | 12 (n=14) | 359 (n=14) | 2 (n=17) | 15 (n=17) | 102 (n=17) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=14) | 13 (n=14) | 181 (n=14) | 1 (n=17) | 16 (n=17) | 68 (n=17) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 24 | 18.3 | 4.7 | 87 |
| lluvia | `lluvia_48h_mm` | 24 | 33.6 | 11.0 | 83 |
| lluvia | `lluvia_72h_mm` | 24 | 39.0 | 18.2 | 75 |
| lluvia | `lluvia_7d_mm` | 24 | 71.5 | 49.4 | 76 |
| lluvia | `lluvia_max_horaria_24h_mm` | 24 | 2.6 | 0.9 | 82 |
| lluvia | `lluvia_max_horaria_72h_mm` | 24 | 4.1 | 1.8 | 76 |
| nieve | `nieve_24h_cm` | 14 | 0.0 | 0.0 | 47 |
| nieve | `nieve_72h_cm` | 14 | 1.2 | 0.0 | 95 |
| nieve | `nieve_7d_cm` | 14 | 1.7 | 0.0 | 89 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 4.9 mm | 24 (n=24) | 0 (n=24) | 7198 (n=24) | 4 (n=11) | 7 (n=11) | 3791 (n=11) |
| lluvia | `lluvia_24h_mm` | 6.9 mm | 22 (n=24) | 2 (n=24) | 5372 (n=24) | 4 (n=11) | 7 (n=11) | 2754 (n=11) |
| lluvia | `lluvia_24h_mm` | 18.3 mm | 13 (n=24) | 11 (n=24) | 1369 (n=24) | 1 (n=11) | 10 (n=11) | 660 (n=11) |
| lluvia | `lluvia_24h_mm` | 34 mm | 6 (n=24) | 18 (n=24) | 353 (n=24) | 0 (n=11) | 11 (n=11) | 159 (n=11) |
| lluvia | `lluvia_48h_mm` | 11.7 mm | 21 (n=24) | 3 (n=24) | 6672 (n=24) | 4 (n=11) | 7 (n=11) | 3432 (n=11) |
| lluvia | `lluvia_48h_mm` | 16.7 mm | 21 (n=24) | 3 (n=24) | 4612 (n=24) | 3 (n=11) | 8 (n=11) | 2282 (n=11) |
| lluvia | `lluvia_48h_mm` | 33.6 mm | 13 (n=24) | 11 (n=24) | 1495 (n=24) | 1 (n=11) | 10 (n=11) | 678 (n=11) |
| lluvia | `lluvia_48h_mm` | 50.1 mm | 6 (n=24) | 18 (n=24) | 527 (n=24) | 0 (n=11) | 11 (n=11) | 219 (n=11) |
| lluvia | `lluvia_72h_mm` | 19 mm | 22 (n=24) | 2 (n=24) | 6451 (n=24) | 3 (n=11) | 8 (n=11) | 3324 (n=11) |
| lluvia | `lluvia_72h_mm` | 25.2 mm | 19 (n=24) | 5 (n=24) | 4608 (n=24) | 2 (n=11) | 9 (n=11) | 2306 (n=11) |
| lluvia | `lluvia_72h_mm` | 39 mm | 14 (n=24) | 10 (n=24) | 2318 (n=24) | 1 (n=11) | 10 (n=11) | 1063 (n=11) |
| lluvia | `lluvia_72h_mm` | 54.5 mm | 6 (n=24) | 18 (n=24) | 1072 (n=24) | 0 (n=11) | 11 (n=11) | 437 (n=11) |
| lluvia | `lluvia_7d_mm` | 47.3 mm | 21 (n=24) | 3 (n=24) | 6367 (n=24) | 3 (n=11) | 8 (n=11) | 3122 (n=11) |
| lluvia | `lluvia_7d_mm` | 50.3 mm | 18 (n=24) | 6 (n=24) | 5872 (n=24) | 3 (n=11) | 8 (n=11) | 2897 (n=11) |
| lluvia | `lluvia_7d_mm` | 71.5 mm | 12 (n=24) | 12 (n=24) | 3393 (n=24) | 2 (n=11) | 9 (n=11) | 1561 (n=11) |
| lluvia | `lluvia_7d_mm` | 116 mm | 7 (n=24) | 17 (n=24) | 869 (n=24) | 1 (n=11) | 10 (n=11) | 379 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1 mm | 24 (n=24) | 0 (n=24) | 7748 (n=24) | 6 (n=11) | 5 (n=11) | 3936 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.5 mm | 21 (n=24) | 3 (n=24) | 4992 (n=24) | 5 (n=11) | 6 (n=11) | 2495 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm` | 2.6 mm | 16 (n=24) | 8 (n=24) | 2151 (n=24) | 1 (n=11) | 10 (n=11) | 1068 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm` | 5.7 mm | 6 (n=24) | 18 (n=24) | 373 (n=24) | 0 (n=11) | 11 (n=11) | 187 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.8 mm | 22 (n=24) | 2 (n=24) | 8021 (n=24) | 7 (n=11) | 4 (n=11) | 4102 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm` | 2.2 mm | 20 (n=24) | 4 (n=24) | 6262 (n=24) | 5 (n=11) | 6 (n=11) | 3221 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm` | 4.1 mm | 14 (n=24) | 10 (n=24) | 2148 (n=24) | 0 (n=11) | 11 (n=11) | 1037 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm` | 5.7 mm | 7 (n=24) | 17 (n=24) | 960 (n=24) | 0 (n=11) | 11 (n=11) | 501 (n=11) |
| nieve | `nieve_24h_cm` | 0.1 cm | 10 (n=14) | 4 (n=14) | 270 (n=14) | 6 (n=17) | 11 (n=17) | 112 (n=17) |
| nieve | `nieve_24h_cm` | 0.2 cm | 9 (n=14) | 5 (n=14) | 231 (n=14) | 6 (n=17) | 11 (n=17) | 101 (n=17) |
| nieve | `nieve_24h_cm` | 0.8 cm | 6 (n=14) | 8 (n=14) | 114 (n=14) | 3 (n=17) | 14 (n=17) | 44 (n=17) |
| nieve | `nieve_72h_cm` | 0.2 cm | 11 (n=14) | 3 (n=14) | 557 (n=14) | 10 (n=17) | 7 (n=17) | 221 (n=17) |
| nieve | `nieve_72h_cm` | 0.6 cm | 9 (n=14) | 5 (n=14) | 362 (n=14) | 4 (n=17) | 13 (n=17) | 148 (n=17) |
| nieve | `nieve_72h_cm` | 1.3 cm | 6 (n=14) | 8 (n=14) | 202 (n=14) | 2 (n=17) | 15 (n=17) | 80 (n=17) |
| nieve | `nieve_72h_cm` | 2.5 cm | 3 (n=14) | 11 (n=14) | 84 (n=14) | 1 (n=17) | 16 (n=17) | 36 (n=17) |
| nieve | `nieve_7d_cm` | 0.2 cm | 11 (n=14) | 3 (n=14) | 1138 (n=14) | 10 (n=17) | 7 (n=17) | 447 (n=17) |
| nieve | `nieve_7d_cm` | 0.6 cm | 10 (n=14) | 4 (n=14) | 768 (n=14) | 4 (n=17) | 13 (n=17) | 318 (n=17) |
| nieve | `nieve_7d_cm` | 2.2 cm | 6 (n=14) | 8 (n=14) | 269 (n=14) | 2 (n=17) | 15 (n=17) | 88 (n=17) |
| nieve | `nieve_7d_cm` | 2.9 cm | 5 (n=14) | 9 (n=14) | 189 (n=14) | 0 (n=17) | 17 (n=17) | 72 (n=17) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 17 (n=24) | 7 (n=24) | 5796 (n=24) | 7 (n=11) | 4 (n=11) | 3345 (n=11) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 12 (n=24) | 12 (n=24) | 3057 (n=24) | 4 (n=11) | 7 (n=11) | 1713 (n=11) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 7 (n=24) | 17 (n=24) | 1594 (n=24) | 2 (n=11) | 9 (n=11) | 910 (n=11) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 5 (n=24) | 19 (n=24) | 666 (n=24) | 0 (n=11) | 11 (n=11) | 386 (n=11) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 4 (n=24) | 20 (n=24) | 310 (n=24) | 0 (n=11) | 11 (n=11) | 171 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 15 (n=24) | 9 (n=24) | 6077 (n=24) | 6 (n=11) | 5 (n=11) | 3343 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3149 (n=24) | 4 (n=11) | 7 (n=11) | 1746 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1631 (n=24) | 3 (n=11) | 8 (n=11) | 903 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 4 (n=24) | 20 (n=24) | 666 (n=24) | 1 (n=11) | 10 (n=11) | 330 (n=11) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 308 (n=24) | 0 (n=11) | 11 (n=11) | 162 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 10 (n=24) | 14 (n=24) | 6169 (n=24) | 5 (n=11) | 6 (n=11) | 3348 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 9 (n=24) | 15 (n=24) | 3222 (n=24) | 5 (n=11) | 6 (n=11) | 1765 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 6 (n=24) | 18 (n=24) | 1649 (n=24) | 3 (n=11) | 8 (n=11) | 873 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 2 (n=24) | 22 (n=24) | 668 (n=24) | 1 (n=11) | 10 (n=11) | 293 (n=11) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 316 (n=24) | 0 (n=11) | 11 (n=11) | 133 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 11 (n=24) | 13 (n=24) | 6441 (n=24) | 6 (n=11) | 5 (n=11) | 3544 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 8 (n=24) | 16 (n=24) | 3291 (n=24) | 5 (n=11) | 6 (n=11) | 1759 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 4 (n=24) | 20 (n=24) | 1654 (n=24) | 3 (n=11) | 8 (n=11) | 821 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 658 (n=24) | 1 (n=11) | 10 (n=11) | 296 (n=11) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 2 (n=24) | 22 (n=24) | 306 (n=24) | 1 (n=11) | 10 (n=11) | 138 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 18 (n=24) | 6 (n=24) | 5793 (n=24) | 7 (n=11) | 4 (n=11) | 3231 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 12 (n=24) | 12 (n=24) | 3018 (n=24) | 3 (n=11) | 8 (n=11) | 1626 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 7 (n=24) | 17 (n=24) | 1585 (n=24) | 1 (n=11) | 10 (n=11) | 872 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 6 (n=24) | 18 (n=24) | 650 (n=24) | 1 (n=11) | 10 (n=11) | 312 (n=11) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 314 (n=24) | 0 (n=11) | 11 (n=11) | 149 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 11 (n=24) | 13 (n=24) | 6090 (n=24) | 5 (n=11) | 6 (n=11) | 3203 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 9 (n=24) | 15 (n=24) | 3196 (n=24) | 3 (n=11) | 8 (n=11) | 1734 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 8 (n=24) | 16 (n=24) | 1616 (n=24) | 2 (n=11) | 9 (n=11) | 795 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 3 (n=24) | 21 (n=24) | 649 (n=24) | 0 (n=11) | 11 (n=11) | 291 (n=11) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 3 (n=24) | 21 (n=24) | 301 (n=24) | 0 (n=11) | 11 (n=11) | 158 (n=11) |
| nieve | `nieve_24h_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 323 (n=14) | 8 (n=17) | 9 (n=17) | 141 (n=17) |
| nieve | `nieve_24h_cm_pct` | p90 | 10 (n=14) | 4 (n=14) | 298 (n=14) | 8 (n=17) | 9 (n=17) | 132 (n=17) |
| nieve | `nieve_24h_cm_pct` | p95 | 10 (n=14) | 4 (n=14) | 265 (n=14) | 8 (n=17) | 9 (n=17) | 113 (n=17) |
| nieve | `nieve_24h_cm_pct` | p98 | 4 (n=14) | 10 (n=14) | 186 (n=14) | 4 (n=17) | 13 (n=17) | 70 (n=17) |
| nieve | `nieve_24h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 117 (n=14) | 4 (n=17) | 13 (n=17) | 40 (n=17) |
| nieve | `nieve_72h_cm_pct` | p80 | 13 (n=14) | 1 (n=14) | 700 (n=14) | 11 (n=17) | 6 (n=17) | 277 (n=17) |
| nieve | `nieve_72h_cm_pct` | p90 | 11 (n=14) | 3 (n=14) | 608 (n=14) | 10 (n=17) | 7 (n=17) | 237 (n=17) |
| nieve | `nieve_72h_cm_pct` | p95 | 7 (n=14) | 7 (n=14) | 450 (n=14) | 7 (n=17) | 10 (n=17) | 171 (n=17) |
| nieve | `nieve_72h_cm_pct` | p98 | 3 (n=14) | 11 (n=14) | 265 (n=14) | 5 (n=17) | 12 (n=17) | 83 (n=17) |
| nieve | `nieve_72h_cm_pct` | p99 | 2 (n=14) | 12 (n=14) | 162 (n=14) | 2 (n=17) | 15 (n=17) | 50 (n=17) |
| nieve | `nieve_7d_cm_pct` | p80 | 11 (n=14) | 3 (n=14) | 1271 (n=14) | 10 (n=17) | 7 (n=17) | 493 (n=17) |
| nieve | `nieve_7d_cm_pct` | p90 | 6 (n=14) | 8 (n=14) | 971 (n=14) | 7 (n=17) | 10 (n=17) | 362 (n=17) |
| nieve | `nieve_7d_cm_pct` | p95 | 5 (n=14) | 9 (n=14) | 658 (n=14) | 6 (n=17) | 11 (n=17) | 212 (n=17) |
| nieve | `nieve_7d_cm_pct` | p98 | 2 (n=14) | 12 (n=14) | 359 (n=14) | 2 (n=17) | 15 (n=17) | 102 (n=17) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=14) | 13 (n=14) | 181 (n=14) | 1 (n=17) | 16 (n=17) | 68 (n=17) |
