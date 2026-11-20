"""Página de Estadística Aplicada con Python y R (201622)."""
import streamlit as st

from nucleo.vista import pagina_asignatura

st.set_page_config(page_title="Estadística · Unisucre", page_icon="📊", layout="wide")
pagina_asignatura("estadistica")
