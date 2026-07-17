"""Exporta un dataset desnormalizado listo para importar en Power BI."""
from pathlib import Path
import sqlite3
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
DB = BASE / "data" / "construccion.db"
OUT = BASE / "powerbi" / "datos_powerbi.csv"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    df = pd.read_sql(
        "SELECT p.anio, p.mes, d.provincia, d.region, p.propiedad, p.tipo_obra, "
        "p.material_estructura, p.superficie_total_m2, p.valor_edificacion_usd, "
        "p.num_viviendas "
        "FROM permisos p JOIN dim_provincia d ON p.provincia_id=d.provincia_id", con)
    con.close()
    df.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(f"[ok] {OUT.name}: {len(df)} filas")


if __name__ == "__main__":
    main()
