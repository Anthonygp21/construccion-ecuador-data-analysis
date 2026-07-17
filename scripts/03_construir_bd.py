"""Construye la base SQLite con esquema estrella desde el CSV armonizado."""
from pathlib import Path
import sqlite3
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
SCHEMA = BASE / "sql" / "schema.sql"
DB = BASE / "data" / "construccion.db"
CSV = BASE / "data" / "processed" / "permisos_2011_2014.csv"


def construir(db_path: str, csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    con = sqlite3.connect(db_path)
    con.executescript(SCHEMA.read_text(encoding="utf-8"))

    # dim_provincia
    prov = (df[["provincia", "region"]].dropna(subset=["provincia"])
            .drop_duplicates().sort_values("provincia").reset_index(drop=True))
    prov.insert(0, "provincia_id", range(1, len(prov) + 1))
    prov.to_sql("dim_provincia", con, if_exists="append", index=False)
    mapa_prov = dict(zip(prov["provincia"], prov["provincia_id"]))

    # dim_material (union de los tres materiales)
    mats = pd.unique(pd.concat([
        df["material_estructura"], df["material_pared"], df["material_cubierta"]
    ]).dropna())
    dim_mat = pd.DataFrame({"material_id": range(1, len(mats) + 1),
                            "descripcion": sorted(mats)})
    dim_mat.to_sql("dim_material", con, if_exists="append", index=False)

    # dim_tipo_obra
    tos = pd.unique(df["tipo_obra"].dropna())
    dim_to = pd.DataFrame({"tipo_obra_id": range(1, len(tos) + 1),
                           "descripcion": sorted(tos)})
    dim_to.to_sql("dim_tipo_obra", con, if_exists="append", index=False)

    # tabla de hechos
    hechos = df.copy()
    hechos["provincia_id"] = hechos["provincia"].map(mapa_prov)
    cols = ["anio", "mes", "provincia_id", "canton_cod", "propiedad", "tipo_obra",
            "material_estructura", "material_pared", "material_cubierta",
            "financiamiento", "superficie_total_m2", "superficie_residencial_m2",
            "superficie_no_residencial_m2", "superficie_terreno_m2",
            "valor_edificacion_usd", "num_viviendas"]
    hechos = hechos[hechos["provincia_id"].notna()]
    hechos[cols].to_sql("permisos", con, if_exists="append", index=False)

    con.commit()
    con.close()
    print(f"[ok] BD creada en {db_path}")


def main() -> None:
    construir(str(DB), str(CSV))


if __name__ == "__main__":
    main()
