"""Página de Diseño Experimental (201636)."""
import streamlit as st

from nucleo.vista import pagina_asignatura

st.set_page_config(page_title="Diseño Experimental · Unisucre", page_icon="🌱", layout="wide")
pagina_asignatura("diseno")
