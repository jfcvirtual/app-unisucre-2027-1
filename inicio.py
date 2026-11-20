"""
inicio.py — Página de inicio
Ingeniería Agrícola · Universidad de Sucre · Semestre 2027-1
Docente: Justo Fuentes Cuello

Ejecutar en el computador:   streamlit run app.py
"""

import streamlit as st


st.title("✏️ El Lápiz y el Algoritmo")
st.markdown("#### Ingeniería Agrícola · Universidad de Sucre · Semestre 2027-1")

c1, c2 = st.columns(2)
with c1:
    st.markdown("### 📊 Estadística Aplicada con Python y R")
    st.caption("Código 201622 · Grupos G1 y G2")
    st.page_link("pages/2_Estadistica.py", label="Entrar a Estadística", icon="📊")
with c2:
    st.markdown("### 🌱 Diseño Experimental")
    st.caption("Código 201636 · Grupos G1 y G2")
    st.page_link("pages/3_Diseno_Experimental.py", label="Entrar a Diseño Experimental", icon="🌱")

st.divider()
st.markdown("""
### 🧭 Cómo estudiar cada sesión

1. **Teoría** → lee, consulta con tu agente de IA y **toma apuntes a mano** en tu cuaderno.
2. **Ejemplo a mano** → sigue paso a paso el cálculo manual de un caso agrícola real.
3. **Ejercicio personal** → con tu código estudiantil obtienes **tus propios datos**;
   resuélvelo en papel (mínimo **20 minutos sin pantallas**).
4. **Verificación** → comprueba tus resultados con **Python** y con **R**.
5. **Auditoría** → compara a mano vs. código e **interpreta** el resultado para el productor.

> 🌾 *Como en el campo: primero se conoce el suelo con las manos, después se confirma con el laboratorio.*
""")
