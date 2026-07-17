import sqlite3
import re
import pathlib


def test_todas_las_consultas_devuelven_filas():
    sql_text = pathlib.Path("sql/consultas_negocio.sql").read_text(encoding="utf-8")
    bloques = re.split(r"(?=-- P\d+:)", sql_text)
    consultas = [b for b in bloques if b.strip().startswith("-- P")]
    assert len(consultas) == 8, f"esperaba 8 consultas, hay {len(consultas)}"
    con = sqlite3.connect("data/construccion.db")
    for c in consultas:
        etiqueta = c.splitlines()[0]
        filas = con.execute(c).fetchall()
        assert len(filas) > 0, f"sin filas: {etiqueta}"
    con.close()
