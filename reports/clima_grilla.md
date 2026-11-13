# Clima: modelo, celda de grilla y elevación por punto

> Generado: 2026-11-13 22:59 UTC · versión `0.1.0.dev0` · commit `df74c71` · SCHEMA_VERSION 1 · fuentes `69a5852fb79566d2`

Datos: Open-Meteo Historical Weather API, modelo `era5_seamless` (ERA5 + ERA5-Land, ECMWF/Copernicus), licencia CC BY 4.0. Son datos de reanálisis en grilla, no mediciones de una estación en el punto.

- `Elev. punto`: la elevación real del punto según el modelo digital de elevación de 90 m (Copernicus GLO-90) que Open-Meteo usa para corregir la temperatura.
- `Elev. celda`: la elevación media de la celda del modelo (`elevation=nan`).
- La lluvia y la nieve salen de ERA5 (celdas de 0,25°, ~28 km); la temperatura, de ERA5-Land (0,1°, ~11 km).

## Celdas `era5`

| Punto | Celda (lat, lon) | Elev. celda (m) | Elev. punto (m) | Celda − punto (m) | Comparte celda con |
|---|---|---:|---:|---:|---|
| rn9_cuesta_barcena | -24.00, -65.50 | 2901 | 1984 | 917 | rn9_volcan |
| rn9_volcan | -24.00, -65.50 | 2901 | 2079 | 822 | rn9_cuesta_barcena |
| rn9_tumbaya | -23.75, -65.50 | 3291 | 2095 | 1196 | rn52_purmamarca_chalala, rn52_lipan_bajo |
| rn9_maimara | -23.50, -65.50 | 3584 | 2395 | 1189 | rn9_tilcara |
| rn9_tilcara | -23.50, -65.50 | 3584 | 2472 | 1112 | rn9_maimara |
| rn9_huacalera | -23.50, -65.25 | 3106 | 2656 | 450 | — |
| rn52_purmamarca_chalala | -23.75, -65.50 | 3291 | 2428 | 863 | rn9_tumbaya, rn52_lipan_bajo |
| rn52_lipan_bajo | -23.75, -65.50 | 3291 | 2593 | 698 | rn9_tumbaya, rn52_purmamarca_chalala |
| rn52_abra_potrerillos | -23.75, -65.75 | 3855 | 4204 | -349 | rn52_ronqui_angosto |
| rn52_ronqui_angosto | -23.75, -65.75 | 3855 | 3710 | 145 | rn52_abra_potrerillos |
| rn52_salinas_grandes | -23.50, -66.00 | 3493 | 3406 | 87 | — |
| rn52_susques | -23.50, -66.25 | 3639 | 3609 | 30 | — |
| rn52_paso_jama | -23.25, -67.00 | 4317 | 4281 | 36 | — |

## Celdas `era5_land`

| Punto | Celda (lat, lon) | Elev. celda (m) | Elev. punto (m) | Celda − punto (m) | Comparte celda con |
|---|---|---:|---:|---:|---|
| rn9_cuesta_barcena | -24.00, -65.50 | 2688 | 1984 | 704 | — |
| rn9_volcan | -23.90, -65.50 | 2917 | 2079 | 838 | rn9_tumbaya |
| rn9_tumbaya | -23.90, -65.50 | 2917 | 2095 | 822 | rn9_volcan |
| rn9_maimara | -23.60, -65.40 | 3420 | 2395 | 1025 | rn9_tilcara |
| rn9_tilcara | -23.60, -65.40 | 3420 | 2472 | 948 | rn9_maimara |
| rn9_huacalera | -23.40, -65.40 | 3405 | 2656 | 749 | — |
| rn52_purmamarca_chalala | -23.70, -65.50 | 3166 | 2428 | 738 | rn52_lipan_bajo |
| rn52_lipan_bajo | -23.70, -65.50 | 3166 | 2593 | 573 | rn52_purmamarca_chalala |
| rn52_abra_potrerillos | -23.70, -65.70 | 3876 | 4204 | -328 | rn52_ronqui_angosto |
| rn52_ronqui_angosto | -23.70, -65.70 | 3876 | 3710 | 166 | rn52_abra_potrerillos |
| rn52_salinas_grandes | -23.60, -65.90 | 3406 | 3406 | 0 | — |
| rn52_susques | -23.40, -66.40 | 3858 | 3609 | 249 | — |
| rn52_paso_jama | -23.20, -67.10 | 4272 | 4281 | -9 | — |

## Puntos que comparten celda

- `era5` (-24.00, -65.50): rn9_cuesta_barcena, rn9_volcan
- `era5` (-23.75, -65.75): rn52_abra_potrerillos, rn52_ronqui_angosto
- `era5` (-23.75, -65.50): rn9_tumbaya, rn52_purmamarca_chalala, rn52_lipan_bajo
- `era5` (-23.50, -65.50): rn9_maimara, rn9_tilcara
- `era5_land` (-23.90, -65.50): rn9_volcan, rn9_tumbaya
- `era5_land` (-23.70, -65.70): rn52_abra_potrerillos, rn52_ronqui_angosto
- `era5_land` (-23.70, -65.50): rn52_purmamarca_chalala, rn52_lipan_bajo
- `era5_land` (-23.60, -65.40): rn9_maimara, rn9_tilcara
