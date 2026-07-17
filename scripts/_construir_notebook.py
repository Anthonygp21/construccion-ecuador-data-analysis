"""Genera notebooks/analisis_construccion.ipynb de forma programatica."""
from pathlib import Path
import nbformat as nbf

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "notebooks" / "analisis_construccion.ipynb"

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell(
    "# Análisis de Permisos de Construcción en Ecuador (2011–2014)\n\n"
    "**Fuente:** INEC — Encuesta de Edificaciones (Permisos de Construcción). "
    "Licencia CC BY 4.0.\n\n"
    "Este notebook explora ~109.500 permisos de construcción reales para responder "
    "preguntas de negocio sobre inversión por provincia, tendencias temporales, "
    "mezcla residencial/no residencial, materiales por región y estacionalidad."
))

cells.append(nbf.v4.new_code_cell(
    "import sqlite3\n"
    "from pathlib import Path\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n\n"
    "sns.set_theme(style='whitegrid')\n"
    "plt.rcParams['figure.dpi'] = 110\n"
    "FIG = Path('../reports/figuras'); FIG.mkdir(parents=True, exist_ok=True)\n"
    "con = sqlite3.connect('../data/construccion.db')\n"
    "print('Conectado. Total permisos:',\n"
    "      con.execute('SELECT COUNT(*) FROM permisos').fetchone()[0])"
))

# P1
cells.append(nbf.v4.new_markdown_cell("## 1. Provincias con más permisos"))
cells.append(nbf.v4.new_code_cell(
    "q1 = '''SELECT d.provincia, COUNT(*) num_permisos\n"
    "        FROM permisos p JOIN dim_provincia d ON p.provincia_id=d.provincia_id\n"
    "        GROUP BY d.provincia ORDER BY num_permisos DESC LIMIT 10'''\n"
    "df1 = pd.read_sql(q1, con)\n"
    "fig, ax = plt.subplots(figsize=(8,5))\n"
    "sns.barplot(df1, y='provincia', x='num_permisos', hue='provincia',\n"
    "            palette='viridis', legend=False, ax=ax)\n"
    "ax.set_title('Top 10 provincias por número de permisos (2011-2014)')\n"
    "ax.set_xlabel('Permisos'); ax.set_ylabel('')\n"
    "fig.tight_layout(); fig.savefig(FIG/'01_provincias.png', bbox_inches='tight')\n"
    "df1"
))

# P2
cells.append(nbf.v4.new_markdown_cell("## 2. Evolución anual: permisos y valor de edificación"))
cells.append(nbf.v4.new_code_cell(
    "q2 = '''SELECT anio, COUNT(*) num_permisos,\n"
    "        SUM(valor_edificacion_usd)/1e6 valor_millones_usd\n"
    "        FROM permisos GROUP BY anio ORDER BY anio'''\n"
    "df2 = pd.read_sql(q2, con)\n"
    "fig, ax1 = plt.subplots(figsize=(8,5))\n"
    "ax1.bar(df2['anio'], df2['num_permisos'], color='#4C72B0', alpha=0.7, label='Permisos')\n"
    "ax1.set_ylabel('Permisos'); ax1.set_xlabel('Año'); ax1.set_xticks(df2['anio'])\n"
    "ax2 = ax1.twinx()\n"
    "ax2.plot(df2['anio'], df2['valor_millones_usd'], color='#C44E52', marker='o',\n"
    "         linewidth=2.5, label='Valor (M USD)')\n"
    "ax2.set_ylabel('Valor de edificación (millones USD)')\n"
    "ax1.set_title('Evolución de permisos y valor de edificación')\n"
    "fig.tight_layout(); fig.savefig(FIG/'02_evolucion.png', bbox_inches='tight')\n"
    "df2"
))

# P3
cells.append(nbf.v4.new_markdown_cell("## 3. Superficie residencial vs no residencial"))
cells.append(nbf.v4.new_code_cell(
    "q3 = '''SELECT anio,\n"
    "        SUM(superficie_residencial_m2)/1e6 residencial,\n"
    "        SUM(superficie_no_residencial_m2)/1e6 no_residencial\n"
    "        FROM permisos GROUP BY anio ORDER BY anio'''\n"
    "df3 = pd.read_sql(q3, con).set_index('anio')\n"
    "fig, ax = plt.subplots(figsize=(8,5))\n"
    "df3.plot(kind='bar', stacked=True, ax=ax, color=['#55A868','#8172B3'])\n"
    "ax.set_title('Superficie a construir por año (millones de m²)')\n"
    "ax.set_ylabel('Millones de m²'); ax.set_xlabel('Año')\n"
    "ax.legend(['Residencial','No residencial'])\n"
    "fig.tight_layout(); fig.savefig(FIG/'03_residencial.png', bbox_inches='tight')\n"
    "df3"
))

# P4
cells.append(nbf.v4.new_markdown_cell("## 4. Material de estructura por región"))
cells.append(nbf.v4.new_code_cell(
    "q4 = '''SELECT d.region, p.material_estructura, COUNT(*) n\n"
    "        FROM permisos p JOIN dim_provincia d ON p.provincia_id=d.provincia_id\n"
    "        WHERE p.material_estructura IS NOT NULL\n"
    "        GROUP BY d.region, p.material_estructura'''\n"
    "df4 = pd.read_sql(q4, con)\n"
    "piv = df4.pivot_table(index='region', columns='material_estructura',\n"
    "                      values='n', fill_value=0)\n"
    "pct = piv.div(piv.sum(axis=1), axis=0) * 100\n"
    "fig, ax = plt.subplots(figsize=(9,5))\n"
    "sns.heatmap(pct, annot=True, fmt='.1f', cmap='YlGnBu', ax=ax,\n"
    "            cbar_kws={'label':'% dentro de la región'})\n"
    "ax.set_title('Material de estructura por región (% de permisos)')\n"
    "ax.set_xlabel(''); ax.set_ylabel('')\n"
    "fig.tight_layout(); fig.savefig(FIG/'04_materiales_region.png', bbox_inches='tight')\n"
    "pct.round(1)"
))

# P5
cells.append(nbf.v4.new_markdown_cell("## 5. Obra pública vs privada"))
cells.append(nbf.v4.new_code_cell(
    "q5 = '''SELECT propiedad, COUNT(*) num_permisos,\n"
    "        AVG(valor_edificacion_usd) valor_promedio\n"
    "        FROM permisos WHERE propiedad IS NOT NULL GROUP BY propiedad'''\n"
    "df5 = pd.read_sql(q5, con)\n"
    "fig, ax = plt.subplots(figsize=(7,5))\n"
    "sns.barplot(df5, x='propiedad', y='valor_promedio', hue='propiedad',\n"
    "            palette='rocket', legend=False, ax=ax)\n"
    "ax.set_title('Valor promedio por permiso: pública vs privada')\n"
    "ax.set_ylabel('USD promedio'); ax.set_xlabel('')\n"
    "for i, v in enumerate(df5['valor_promedio']):\n"
    "    ax.text(i, v, f'${v:,.0f}', ha='center', va='bottom')\n"
    "fig.tight_layout(); fig.savefig(FIG/'05_publico_privado.png', bbox_inches='tight')\n"
    "df5"
))

# P7
cells.append(nbf.v4.new_markdown_cell("## 6. Estacionalidad (permisos por mes)"))
cells.append(nbf.v4.new_code_cell(
    "q7 = '''SELECT mes, COUNT(*) num_permisos FROM permisos\n"
    "        WHERE mes BETWEEN 1 AND 12 GROUP BY mes ORDER BY mes'''\n"
    "df7 = pd.read_sql(q7, con)\n"
    "meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']\n"
    "fig, ax = plt.subplots(figsize=(9,5))\n"
    "sns.lineplot(x=df7['mes'], y=df7['num_permisos'], marker='o', ax=ax, color='#4C72B0')\n"
    "ax.set_xticks(range(1,13)); ax.set_xticklabels(meses)\n"
    "ax.set_title('Estacionalidad: permisos emitidos por mes (2011-2014)')\n"
    "ax.set_ylabel('Permisos'); ax.set_xlabel('')\n"
    "fig.tight_layout(); fig.savefig(FIG/'06_estacionalidad.png', bbox_inches='tight')\n"
    "df7"
))

cells.append(nbf.v4.new_markdown_cell(
    "## Conclusiones\n\n"
    "- **Concentración geográfica:** Guayas y Pichincha lideran la actividad de "
    "construcción, reflejando a Guayaquil y Quito como polos económicos.\n"
    "- **Hormigón armado** es el material de estructura dominante en todas las regiones.\n"
    "- La **obra pública** es escasa en número pero de valor unitario mucho mayor "
    "que la privada.\n"
    "- Se observan patrones de **estacionalidad** en la emisión mensual de permisos.\n\n"
    "*Datos: INEC — Encuesta de Edificaciones 2011-2014 (CC BY 4.0).*"
))

nb["cells"] = cells
OUT.parent.mkdir(parents=True, exist_ok=True)
nbf.write(nb, str(OUT))
print(f"[ok] notebook creado: {OUT}")
