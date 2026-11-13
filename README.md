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
```

El estado del Paso de Jama (Vialidad MOP Chile y argentina.gob.ar) se guarda cada 3 horas
con un workflow de GitHub Actions en la rama `data-snapshots`. Ninguna de las dos fuentes
tiene historial: los datos empiezan el día en que arrancó el colector.

Etapas (una por target de Make): `make geo` (rutas, Tren Solar y puntos críticos desde
OpenStreetMap; los GeoJSON quedan en `assets/geo/`), `make datos`, `make calibrar`, `make precision`,
`make reporte`. `make tablero` queda para el día 2.

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
  hidrológico ni un pronóstico oficial.
- **Puntos críticos:** las coordenadas salen de un objeto de OpenStreetMap y solo se marcan
  `verificado: true` si están a menos de 500 m de la traza (ver
  [reports/geo_verificacion.md](reports/geo_verificacion.md)). Los km son distancias medidas
  sobre la geometría de OSM: en RN 9 se calibran con hitos kilométricos cercanos a San
  Salvador de Jujuy y hacia el norte son extrapolados; en RN 52 el km 0 es el empalme con
  RN 9 (supuesto). Pueden diferir de la progresiva oficial de Vialidad Nacional.
- **Clima de grilla:** Open-Meteo devuelve valores de una celda de grilla cuya elevación
  puede diferir de la del punto real, sobre todo en la Puna.
