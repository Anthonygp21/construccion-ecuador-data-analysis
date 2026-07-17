import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "arm", pathlib.Path("scripts/02_armonizar_datos.py"))
arm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arm)


def test_armonizar_estructura():
    df = arm.armonizar()
    for col in ["anio", "provincia", "canton_cod", "propiedad", "tipo_obra",
                "superficie_total_m2", "valor_edificacion_usd", "num_viviendas",
                "material_estructura", "material_pared", "region"]:
        assert col in df.columns, f"falta {col}"
    assert set(df["anio"].unique()) == {2011, 2012, 2013, 2014}
    assert len(df) > 50_000
    assert str(df["provincia"].dtype) in ("object", "string", "str")
    assert df["provincia"].notna().mean() > 0.95
    # las provincias no deben conservar el prefijo numerico "01 Azuay"
    muestra = set(df["provincia"].dropna().unique())
    assert not any(str(p)[:1].isdigit() for p in muestra)
    assert {"Guayas", "Pichincha", "Azuay"} <= muestra
