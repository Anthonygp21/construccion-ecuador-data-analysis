# Dashboard de Power BI — Permisos de Construcción en Ecuador

Esta carpeta contiene el dataset limpio y una guía para construir un dashboard interactivo en
**Power BI Desktop** a partir de los datos ya procesados del proyecto.

> El archivo `.pbix` no se incluye porque Power BI Desktop no se ejecutó en este entorno. En su
> lugar entregamos el dataset listo para importar y las instrucciones exactas para reconstruir
> el dashboard en minutos.

## Archivo de datos

`datos_powerbi.csv` — un registro por permiso de construcción, ya desnormalizado (unido con la
dimensión de provincia). Se genera con `python scripts/05_exportar_powerbi.py`.

**Columnas:**

| Columna | Tipo | Descripción |
|---|---|---|
| `anio` | entero | Año del permiso (2011–2014) |
| `mes` | entero | Mes (1–12) |
| `provincia` | texto | Provincia |
| `region` | texto | Costa / Sierra / Amazonía / Insular |
| `propiedad` | texto | Pública / Privada |
| `tipo_obra` | texto | Tipo de obra |
| `material_estructura` | texto | Material de la estructura |
| `superficie_total_m2` | decimal | Superficie total a construir (m²) |
| `valor_edificacion_usd` | decimal | Valor de la edificación (USD) |
| `num_viviendas` | decimal | Nº de viviendas por edificación |

## Pasos

1. **Instalar** Power BI Desktop (gratis) desde Microsoft Store o el sitio de Microsoft.
2. **Importar datos:** *Inicio → Obtener datos → Texto/CSV* → seleccionar `datos_powerbi.csv`.
   Confirmar que el separador es coma y la codificación 65001 (UTF-8).
3. **Crear medidas (DAX):** en la vista de datos, *Nueva medida*:
   ```DAX
   Total Permisos = COUNTROWS('datos_powerbi')
   Valor Total = SUM('datos_powerbi'[valor_edificacion_usd])
   Superficie Total = SUM('datos_powerbi'[superficie_total_m2])
   Valor por m2 = DIVIDE([Valor Total], [Superficie Total])
   Total Viviendas = SUM('datos_powerbi'[num_viviendas])
   ```
4. **Construir los visuales sugeridos:**
   - **Tarjetas KPI:** `Total Permisos`, `Valor Total`, `Total Viviendas`, `Valor por m2`.
   - **Mapa** (o gráfico de barras) por `provincia`, tamaño = `Total Permisos`.
   - **Gráfico de líneas:** eje = `anio`, valores = `Total Permisos` y `Valor Total`.
   - **Barras apiladas:** eje = `region`, leyenda = `material_estructura`.
   - **Anillo:** `propiedad` (Pública vs Privada) por `Valor Total`.
   - **Segmentadores (filtros):** `anio`, `region`, `propiedad`.
5. **Formato:** título "Permisos de Construcción en Ecuador (2011–2014)" y una nota de pie:
   *"Fuente: INEC — Encuesta de Edificaciones (CC BY 4.0)."*

## Fuente de datos

INEC — Encuesta de Edificaciones (Permisos de Construcción), 2011–2014.
Licencia CC BY 4.0 · <https://www.ecuadorencifras.gob.ec/edificaciones-bases-de-datos/>
