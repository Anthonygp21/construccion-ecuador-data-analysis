import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "descarga", pathlib.Path("scripts/01_descargar_datos.py"))
descarga = importlib.util.module_from_spec(spec)
spec.loader.exec_module(descarga)


def test_urls_cubren_2011_2014():
    urls = descarga.urls_datos()
    assert set(urls) == {2011, 2012, 2013, 2014}
    for y, u in urls.items():
        assert u.startswith("https://www.ecuadorencifras.gob.ec/")
        assert str(y) in u and u.endswith("_spss.zip")
