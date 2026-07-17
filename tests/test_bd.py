import importlib.util
import pathlib
import sqlite3

spec = importlib.util.spec_from_file_location(
    "bd", pathlib.Path("scripts/03_construir_bd.py"))
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)


def test_construir_bd(tmp_path):
    db = tmp_path / "test.db"
    bd.construir(str(db), "data/processed/permisos_2011_2014.csv")
    con = sqlite3.connect(db)
    cur = con.cursor()
    assert cur.execute("SELECT COUNT(*) FROM permisos").fetchone()[0] > 50_000
    assert cur.execute("SELECT COUNT(*) FROM dim_provincia").fetchone()[0] >= 20
    huerfanos = cur.execute(
        "SELECT COUNT(*) FROM permisos p LEFT JOIN dim_provincia d "
        "ON p.provincia_id=d.provincia_id WHERE d.provincia_id IS NULL").fetchone()[0]
    assert huerfanos == 0
    con.close()
