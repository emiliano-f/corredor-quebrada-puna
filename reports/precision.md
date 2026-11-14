# Precisión de la extracción

> Generado: 2026-11-14 14:52 UTC · versión `0.1.0.dev0` · commit `9e27ada` · SCHEMA_VERSION 2 · fuentes `b3dab32ad1adf821`

Etiquetas leídas de `reports/revision_manual.csv` (valores sí: 1/si/ok/x; no: 0/no/mal; vacío = sin etiquetar). Muestra estratificada por causa (semilla 42: aluvion 8, crecida 8, nieve 8, otras 6).

## ¿Es un corte en el corredor? (`ok_corte`)

si = corte de ruta en el corredor; no = no es un corte; fuera = corte fuera del corredor. Tasa = si / etiquetadas.

| estrato | si | no | fuera | tasa si |
|---|---|---|---|---|
| todos | 25 | 4 | 1 | 83% (n=30) |
| aluvion | 7 | 0 | 0 | 100% (n=7) |
| crecida | 3 | 0 | 0 | 100% (n=3) |
| nieve | 8 | 0 | 0 | 100% (n=8) |
| otras | 7 | 4 | 1 | 58% (n=12) |

## Fecha, punto y causa (solo filas con `ok_corte` = si)

n = filas etiquetadas en ese campo. Precisión = correctos / etiquetados.

| estrato | fecha | punto | causa |
|---|---|---|---|
| todos | 92% (n=25) | 64% (n=25) | 76% (n=25) |
| aluvion | 86% (n=7) | 29% (n=7) | 86% (n=7) |
| crecida | 100% (n=3) | 33% (n=3) | 67% (n=3) |
| nieve | 100% (n=8) | 100% (n=8) | 100% (n=8) |
| otras | 86% (n=7) | 71% (n=7) | 43% (n=7) |
