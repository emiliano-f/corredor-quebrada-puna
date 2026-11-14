# Corredor Quebrada–Puna

Alertas de riesgo de corte para la **Ruta Nacional 9** (Quebrada de Humahuaca, a lo largo
del Tren Solar) y la **Ruta Nacional 52** (Purmamarca → Cuesta de Lipán → Susques → Paso
de Jama), en Jujuy, Argentina.

La base es un **catálogo histórico de cortes** armado a partir de noticias locales (solo
metadatos: enlace, medio, fecha, titular y bajada) y cruzado con datos meteorológicos
reales, para calibrar umbrales simples de lluvia y nieve por causa.

> Estado: base del repositorio (día 1). Las etapas del pipeline se van conectando en los
> próximos PR; ver [CHANGELOG.md](CHANGELOG.md).

## Inicio rápido

Requisitos: [uv](https://docs.astral.sh/uv/) (instala Python 3.11 solo).

```bash
make setup          # uv sync + hooks de pre-commit
make check          # lint, tipos, tests, docs-check y auditoría de dependencias
uv run corredor --version
uv run corredor manifest   # escribe data/manifest.json
make snapshot-jama  # agrega el estado actual del Paso de Jama a snapshots/jama_estado.jsonl
make clima          # clima horario de Open-Meteo 2016→hoy por punto + antecedentes
uv run corredor recolectar # metadatos de notas de las fuentes activas → data/corredor.duckdb
make datos          # recolectar + clima + Jama → eventos deduplicados en DuckDB y Parquet
make reporte        # reports/calidad_catalogo.md y reports/revision_manual.csv
make calibrar       # reports/validacion.md (umbrales en mm/cm y en percentil por celda)
make precision      # precisión por campo y por estrato desde reports/revision_manual.csv etiquetado
```

El estado del Paso de Jama (Vialidad MOP Chile y argentina.gob.ar) se guarda cada 3 horas
con un workflow de GitHub Actions en la rama `data-snapshots`. Ninguna de las dos fuentes
tiene historial: los datos empiezan el día en que arrancó el colector.

Etapas (una por target de Make): `make geo` (rutas, Tren Solar y puntos críticos desde
OpenStreetMap; los GeoJSON quedan en `assets/geo/`), `make clima`, `make datos`, `make calibrar`,
`make precision`, `make reporte`. `make tablero` queda para el día 2.

`make clima` respeta el tope diario de llamadas a Open-Meteo (`clima.max_llamadas_diarias`
en `config.yaml`: 1500; 500 si no se configura): si lo alcanza, se detiene con un aviso y la corrida
siguiente sigue desde la caché.

La configuración vive en [`config.yaml`](config.yaml) (puntos críticos y fuentes). Ninguna
etapa necesita claves; la extracción con LLM es opcional y solo se activa con la variable
de entorno `LLM_API_KEY`.

## Documentación

- [docs/FUENTES.md](docs/FUENTES.md): relevamiento de fuentes (tiers y exclusiones).
- [docs/SCRAPING.md](docs/SCRAPING.md): cómo se recolecta cada fuente.
- [docs/DATOS.md](docs/DATOS.md): diccionario de datos.
- [CONTRIBUTING.md](CONTRIBUTING.md): flujo de trabajo y cómo agregar una fuente.
- Los números (eventos, umbrales, precisión) están en `reports/`, generados por el
  pipeline; no se copian a mano en la documentación.

## Fuentes de datos y licencias

- **Noticias:** se guardan solo metadatos y se enlaza siempre a la nota original en cada
  medio. No se copia ni se republica el texto completo. Listado de medios en
  [docs/FUENTES.md](docs/FUENTES.md).
- **OpenStreetMap:** © colaboradores de OpenStreetMap, datos bajo licencia
  [ODbL](https://www.openstreetmap.org/copyright).
- **Open-Meteo:** datos meteorológicos de [Open-Meteo.com](https://open-meteo.com/), bajo
  licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Código bajo licencia [MIT](LICENSE).

## Limitaciones

- **Sesgo de cobertura de prensa:** un corte que no salió en los medios no está en el
  catálogo. Los medios grandes cubren más los eventos de RN 9 y los eventos grandes;
  algunos medios tienen archivo solo desde años recientes.
- **Umbrales simples:** una regla por causa, igual para todos los puntos; no es un modelo
  hidrológico ni un pronóstico oficial. Cada umbral se muestra en unidades de ERA5 y como
  percentil de la celda en la misma estación (2016–2022); se ajusta con 2016–2022 y se
  prueba con 2023 en adelante (ver [reports/validacion.md](reports/validacion.md)).
- **Extracción por reglas:** los eventos salen del titular, la bajada y la URL, no del
  texto de la nota; una nota sin lugar ni km queda sin punto crítico. La precisión medida
  a mano está en `reports/precision.md`.
- **Puntos críticos:** las coordenadas salen de un objeto de OpenStreetMap y solo se marcan
  `verificado: true` si están a menos de 500 m de la traza (ver
  [reports/geo_verificacion.md](reports/geo_verificacion.md)). Los km son distancias medidas
  sobre la geometría de OSM: en RN 9 se calibran con hitos kilométricos cercanos a San
  Salvador de Jujuy y hacia el norte son extrapolados; en RN 52 el km 0 es el empalme con
  RN 9 (supuesto). Pueden diferir de la progresiva oficial de Vialidad Nacional.
- **Clima de grilla, no de estación:** el histórico es reanálisis ERA5 (modelo
  `era5_seamless` de Open-Meteo), no mediciones en el punto. La lluvia y la nieve salen de
  celdas de 0,25° (~28 km) y la temperatura de celdas de 0,1° (~11 km).
- **Elevación de la celda distinta a la del punto:** en la Quebrada la celda de lluvia
  está entre 450 y 1.200 m más alta que la ruta (por ejemplo Tumbaya: +1.196 m), porque
  promedia las laderas y cumbres vecinas; en la Puna la diferencia baja a decenas de
  metros. La temperatura se corrige por altura, la lluvia no.
- **Puntos que comparten celda:** varios puntos tienen la misma serie de lluvia y nieve
  (Volcán y Cuesta de Bárcena; Tumbaya, Purmamarca y Lipán bajo; Maimará y Tilcara;
  Abra de Potrerillos y Ronqui Angosto), así que el clima no los distingue. El detalle por
  punto está en `reports/clima_grilla.md` y en [docs/DATOS.md](docs/DATOS.md).
- **Celdas que mezclan Quebrada y yungas:** las celdas de ERA5 de la Quebrada abarcan
  también las laderas orientales, más húmedas, así que los milímetros absolutos no son la
  lluvia que cae en la ruta. Las cifras por celda están en [docs/DATOS.md](docs/DATOS.md).
- **Cantidad de lluvia sesgada:** ERA5 sobreestima la lluvia en las laderas andinas (en
  la celda de Volcán da unos 2.000 mm por año, contra unos 1.170 mm del modelo IFS de
  9 km en 2024); los umbrales se calibran contra los cortes, no se leen como milímetros
  reales.
- **Últimos días sin dato:** ERA5 se publica con unos 5 días de demora; esos días quedan
  vacíos en el histórico (para el presente se usa el pronóstico).
- **Uso no comercial:** la API gratuita de Open-Meteo permite solo uso no comercial y
  exige atribución (CC BY 4.0).
