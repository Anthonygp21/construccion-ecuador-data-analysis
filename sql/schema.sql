-- Esquema estrella para permisos de construccion (INEC 2011-2014)
DROP TABLE IF EXISTS permisos;
DROP TABLE IF EXISTS dim_provincia;
DROP TABLE IF EXISTS dim_material;
DROP TABLE IF EXISTS dim_tipo_obra;

CREATE TABLE dim_provincia (
    provincia_id INTEGER PRIMARY KEY,
    provincia    TEXT NOT NULL,
    region       TEXT NOT NULL
);

CREATE TABLE dim_material (
    material_id INTEGER PRIMARY KEY,
    descripcion TEXT NOT NULL
);

CREATE TABLE dim_tipo_obra (
    tipo_obra_id INTEGER PRIMARY KEY,
    descripcion  TEXT NOT NULL
);

CREATE TABLE permisos (
    permiso_id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    anio                         INTEGER NOT NULL,
    mes                          INTEGER,
    provincia_id                 INTEGER REFERENCES dim_provincia(provincia_id),
    canton_cod                   INTEGER,
    propiedad                    TEXT,
    tipo_obra                    TEXT,
    material_estructura          TEXT,
    material_pared               TEXT,
    material_cubierta            TEXT,
    financiamiento               TEXT,
    superficie_total_m2          REAL,
    superficie_residencial_m2    REAL,
    superficie_no_residencial_m2 REAL,
    superficie_terreno_m2        REAL,
    valor_edificacion_usd        REAL,
    num_viviendas                REAL
);

CREATE INDEX idx_permisos_prov ON permisos(provincia_id);
CREATE INDEX idx_permisos_anio ON permisos(anio);
