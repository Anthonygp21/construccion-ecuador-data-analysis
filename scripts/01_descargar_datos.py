"""Descarga reproducible de los microdatos de edificaciones del INEC (2011-2014)."""
from pathlib import Path
import urllib.request

BASE = ("https://www.ecuadorencifras.gob.ec/documentos/datos/"
        "Estadisticas_Economicas/Encuesta_Edificaciones/Edificaciones_spss")
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def urls_datos() -> dict[int, str]:
    return {y: f"{BASE}/bdd_edificaciones_{y}_spss.zip" for y in (2011, 2012, 2013, 2014)}


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for y, url in urls_datos().items():
        dest = RAW / f"bdd_edificaciones_{y}_spss.zip"
        if dest.exists():
            print(f"[skip] {dest.name} ya existe")
            continue
        print(f"[descargando] {y} ...")
        urllib.request.urlretrieve(url, dest)
        print(f"[ok] {dest.name} ({dest.stat().st_size} bytes)")
    print("Descarga completa. Descomprima los .zip antes de armonizar.")


if __name__ == "__main__":
    main()
