"""
Plan de Asignatura
------------------
Página para proyectar el primer día de clase: muestra el plan OFICIAL
(FOR-FO-030 y FOR-FO-018) de cada asignatura, el acuerdo pedagógico y el
estado de la socialización por grupo. Los datos vienen de contenido/<asig>/plan.yaml.
"""

import pandas as pd
import streamlit as st

from nucleo.contenido import ASIGNATURAS, cargar_plan
from nucleo.registro import obtener_almacen, socializaciones

st.set_page_config(page_title="Plan de asignatura", page_icon="📜", layout="wide")
st.title("📜 Plan de asignatura · 2027-1")

clave = st.radio("Asignatura", list(ASIGNATURAS),
                 format_func=lambda k: f"{ASIGNATURAS[k]['icono']} {ASIGNATURAS[k]['nombre']}",
                 horizontal=True)
asig = ASIGNATURAS[clave]
plan = cargar_plan(clave)
of = plan["oficial"]

# 1) Descripción administrativa
st.subheader(f"{asig['nombre']} ({asig['codigo']})")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Semestre", of["semestre"])
c2.metric("Créditos", of["creditos"])
c3.metric("Horas totales", of["horas_totales"])
c4.metric("Semanas", len(plan["semanas"]))
st.markdown(f"**Requisitos:** {of['requisitos']}  \n"
            f"**Área:** {of['area']}  \n"
            f"**Modalidad:** {of['modalidad']}  \n"
            f"**Intensidad:** {of['intensidad']}")
st.markdown(f"**Descripción.** {of['descripcion']}")

# 2) Resultados de aprendizaje
st.subheader("🎯 Resultados de aprendizaje de la asignatura")
for i, ra in enumerate(of["resultados_aprendizaje"], start=1):
    st.markdown(f"{i}. {ra}")

# 3) Planificación semana a semana
st.subheader("🗓️ Planificación de la formación")
tabla = pd.DataFrame([{
    "Semana": s["semana"],
    "Eje": s["eje"],
    "Tema": s["tema"],
    "Sesión 1": s["sesion_1"]["titulo"],
    "Sesión 2": s["sesion_2"]["titulo"],
    "Instrumento": s.get("instrumento", ""),
    "Evidencias": s.get("evidencias", ""),
} for s in plan["semanas"]])
st.dataframe(tabla, hide_index=True, width="stretch", height=600)

# 4) Acuerdo pedagógico y estado de la socialización
st.subheader("🤝 Acuerdo pedagógico")
st.info(of["acuerdo"])
if of.get("url_plan_firmado"):
    st.link_button("📄 Ver el plan firmado (PDF)", of["url_plan_firmado"])

try:
    hechos = socializaciones(obtener_almacen().leer())
except Exception:
    hechos = {}
cols = st.columns(len(asig["grupos"]))
for col, (grupo, etiqueta) in zip(cols, asig["grupos"].items()):
    if etiqueta in hechos:
        col.success(f"Grupo {grupo}: plan socializado el {hechos[etiqueta]}")
    else:
        col.warning(f"Grupo {grupo}: socialización pendiente")
st.caption("La firma oficial del representante del curso se registra en el FOR-FO-018 "
           "por el canal institucional; esta página es solo de apoyo.")
