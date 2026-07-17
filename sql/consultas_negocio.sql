-- ============================================================
-- Consultas de negocio - Permisos de Construccion Ecuador (INEC)
-- Fuente: INEC, Encuesta de Edificaciones 2011-2014 (CC BY 4.0)
-- ============================================================

-- P1: Provincias con mas permisos y mayor superficie a construir
SELECT d.provincia, d.region,
       COUNT(*)                          AS num_permisos,
       ROUND(SUM(p.superficie_total_m2)) AS superficie_total_m2
FROM permisos p JOIN dim_provincia d ON p.provincia_id = d.provincia_id
GROUP BY d.provincia, d.region
ORDER BY num_permisos DESC;

-- P2: Evolucion anual: permisos, superficie y valor de edificacion
SELECT anio,
       COUNT(*)                              AS num_permisos,
       ROUND(SUM(superficie_total_m2))       AS superficie_total_m2,
       ROUND(SUM(valor_edificacion_usd), 2)  AS valor_total_usd
FROM permisos
GROUP BY anio ORDER BY anio;

-- P3: Reparto residencial vs no residencial (superficie por anio)
SELECT anio,
       ROUND(SUM(superficie_residencial_m2))     AS sup_residencial,
       ROUND(SUM(superficie_no_residencial_m2))  AS sup_no_residencial
FROM permisos GROUP BY anio ORDER BY anio;

-- P4: Material de estructura predominante por region
SELECT d.region, p.material_estructura, COUNT(*) AS num_permisos
FROM permisos p JOIN dim_provincia d ON p.provincia_id = d.provincia_id
WHERE p.material_estructura IS NOT NULL
GROUP BY d.region, p.material_estructura
ORDER BY d.region, num_permisos DESC;

-- P5: Obra publica vs privada: participacion y valor promedio
SELECT propiedad,
       COUNT(*)                             AS num_permisos,
       ROUND(AVG(valor_edificacion_usd), 2) AS valor_promedio_usd
FROM permisos WHERE propiedad IS NOT NULL
GROUP BY propiedad ORDER BY num_permisos DESC;

-- P6: Viviendas nuevas autorizadas por anio y provincia (top 10)
SELECT d.provincia, p.anio, ROUND(SUM(p.num_viviendas)) AS viviendas
FROM permisos p JOIN dim_provincia d ON p.provincia_id = d.provincia_id
GROUP BY d.provincia, p.anio
ORDER BY viviendas DESC LIMIT 10;

-- P7: Estacionalidad: permisos por mes
SELECT mes, COUNT(*) AS num_permisos
FROM permisos WHERE mes BETWEEN 1 AND 12
GROUP BY mes ORDER BY mes;

-- P8: Valor promedio por m2 por provincia (top 15, superficie > 0)
SELECT d.provincia,
       ROUND(SUM(p.valor_edificacion_usd) / NULLIF(SUM(p.superficie_total_m2), 0), 2) AS usd_por_m2
FROM permisos p JOIN dim_provincia d ON p.provincia_id = d.provincia_id
WHERE p.superficie_total_m2 > 0
GROUP BY d.provincia
ORDER BY usd_por_m2 DESC LIMIT 15;
