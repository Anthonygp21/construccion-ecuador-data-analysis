"""Armoniza los microdatos de edificaciones (2011-2014) en un unico CSV limpio."""
from pathlib import Path
import unicodedata
import pandas as pd
import pyreadstat

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
OUT = BASE / "data" / "processed" / "permisos_2011_2014.csv"

RUTAS_SAV = {
    2011: RAW / "edificaciones_2011_spss" / "BASE EDIF._2011.SAV",
    2012: RAW / "edificaciones_2012_spss" / "BASE EDIF._2012.sav",
    2013: RAW / "Base de datos Edificaciones 2013.SAV",
    2014: RAW / "bdd_edificaciones_2014.sav",
}

COLUMNAS = {
    "codprovf": "provincia_cod", "codcantf": "canton_cod", "propie": "propiedad_cod",
    "mes": "mes", "CTIPOBR": "tipo_obra_cod",
    "CARCO": "superficie_total_m2", "CARES": "superficie_residencial_m2",
    "CARNRES": "superficie_no_residencial_m2", "CSUTE": "superficie_terreno_m2",
    "CVAE": "valor_edificacion_usd", "NUVICAL": "num_viviendas",
    "estru": "material_estructura_cod", "pared": "material_pared_cod",
    "cubi": "material_cubierta_cod", "CDISPRFX": "financiamiento_cod",
}

# Columnas con etiqueta de valor -> nombre de la columna de texto decodificada
DECODIFICAR = {
    "codprovf": "provincia", "propie": "propiedad", "CTIPOBR": "tipo_obra",
    "estru": "material_estructura", "pared": "material_pared",
    "cubi": "material_cubierta", "CDISPRFX": "financiamiento",
}

REGION = {  # por nombre de provincia (normalizado a Title y sin tildes)
    "Azuay": "Sierra", "Bolivar": "Sierra", "Canar": "Sierra", "Carchi": "Sierra",
    "Cotopaxi": "Sierra", "Chimborazo": "Sierra", "Imbabura": "Sierra", "Loja": "Sierra",
    "Pichincha": "Sierra", "Tungurahua": "Sierra",
    "Santo Domingo De Los Tsachilas": "Sierra",
    "El Oro": "Costa", "Esmeraldas": "Costa", "Guayas": "Costa", "Los Rios": "Costa",
    "Manabi": "Costa", "Santa Elena": "Costa",
    "Morona Santiago": "Amazonia", "Napo": "Amazonia", "Pastaza": "Amazonia",
    "Zamora Chinchipe": "Amazonia", "Sucumbios": "Amazonia", "Orellana": "Amazonia",
    "Galapagos": "Insular",
}

# Nombres cortos/variantes que aparecen en algunos anios -> nombre canonico
CANON_PROVINCIA = {
    "Morona": "Morona Santiago",
    "Zamora": "Zamora Chinchipe",
    "Santo Domingo": "Santo Domingo De Los Tsachilas",
    "Santo Domingo De Los Tsachila": "Santo Domingo De Los Tsachilas",
}


def cargar_anio(anio: int):
    ruta = RUTAS_SAV[anio]
    df, meta = pyreadstat.read_sav(str(ruta), encoding="LATIN1")
    return df, meta.variable_value_labels


def _sin_tildes(s) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", str(s))
                   if not unicodedata.combining(c))


def armonizar() -> pd.DataFrame:
    frames = []
    for anio in (2011, 2012, 2013, 2014):
        df, vlabels = cargar_anio(anio)
        out = pd.DataFrame()
        out["anio"] = [anio] * len(df)
        for orig, nuevo in COLUMNAS.items():
            out[nuevo] = df[orig] if orig in df.columns else pd.NA
        for orig, texto in DECODIFICAR.items():
            if orig in df.columns and orig in vlabels:
                out[texto] = df[orig].map(vlabels[orig])
            else:
                out[texto] = pd.NA
        frames.append(out)
    full = pd.concat(frames, ignore_index=True)

    # normalizar nombre de provincia y asignar region
    #   algunos anios traen la etiqueta como "01 Azuay" (codigo + nombre) y
    #   otros como "Guayas": se elimina el prefijo numerico y se homogeniza.
    prov = full["provincia"].astype("string").str.strip()
    prov = prov.str.replace(r"^\s*\d+\s*[-.]?\s*", "", regex=True)  # quita "01 " / "1-"
    prov = prov.str.strip().str.title()
    prov = prov.map(lambda x: _sin_tildes(x) if pd.notna(x) else x)
    full["provincia"] = prov.replace(CANON_PROVINCIA)
    full["region"] = full["provincia"].map(REGION).fillna("Sin dato")

    # misma limpieza de prefijo numerico para el resto de textos decodificados
    for col in ["material_estructura", "material_pared", "material_cubierta",
                "tipo_obra", "propiedad", "financiamiento"]:
        s = full[col].astype("string").str.strip()
        s = s.str.replace(r"^\s*\d+\s*[-.]?\s*", "", regex=True)
        full[col] = s.str.strip().str.capitalize().map(
            lambda x: _sin_tildes(x) if pd.notna(x) else x)

    # tipos numericos
    for c in ["superficie_total_m2", "superficie_residencial_m2",
              "superficie_no_residencial_m2", "superficie_terreno_m2",
              "valor_edificacion_usd", "num_viviendas", "mes"]:
        full[c] = pd.to_numeric(full[c], errors="coerce")
    return full


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df = armonizar()
    df.to_csv(OUT, index=False, encoding="utf-8")
    print(f"[ok] {OUT.name}: {len(df)} filas, {len(df.columns)} columnas")


if __name__ == "__main__":
    main()
