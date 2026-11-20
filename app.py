"""
app.py — Punto de entrada y menú de navegación
Ingeniería Agrícola · Universidad de Sucre · Semestre 2027-1
Docente: Justo Fuentes Cuello

Ejecutar en el computador:   streamlit run app.py
"""

import streamlit as st

st.set_page_config(page_title="Lápiz y Algoritmo · Unisucre 2027-1",
                   page_icon="✏️", layout="wide")

# Menú lateral con nombres en español (con tildes)
menu = st.navigation([
    st.Page("inicio.py", title="Inicio", icon="✏️", default=True),
    st.Page("pages/1_Plan_de_Asignatura.py", title="Plan de asignatura", icon="📜"),
    st.Page("pages/2_Estadistica.py", title="Estadística", icon="📊"),
    st.Page("pages/3_Diseno_Experimental.py", title="Diseño Experimental", icon="🌱"),
    st.Page("pages/4_Registro_Docente.py", title="Registro docente", icon="📝"),
])
menu.run()
