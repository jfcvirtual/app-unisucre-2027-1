"""
nucleo/vista.py
---------------
Dibuja la página de una asignatura. La usan pages/1_... y pages/2_...

Cada sesión se recorre en el orden de "El Lápiz y el Algoritmo":
  Plan → 1. Teoría → 2. Ejemplo a mano → 3. Ejercicio personal
       → 4. Verificación (Python y R) → 5. Auditoría
Las pestañas NO se bloquean: el estudiante puede apoyarse en cualquier
agente de IA, pero la ruta sugerida está numerada.
"""

import contextlib
import io

import pandas as pd
import streamlit as st

from nucleo.contenido import ASIGNATURAS, cargar_plan, cargar_sesion, datos_semana
from nucleo.ejercicios import GENERADORES
from nucleo.registro import obtener_almacen


def _selector_semana(plan: dict) -> tuple[int, int]:
    """Barra lateral: elegir semana (1 a 16) y sesión (1 o 2)."""
    st.sidebar.header("📅 Navegación")
    opciones = [s["semana"] for s in plan["semanas"]]
    semana = st.sidebar.selectbox(
        "Semana", opciones,
        format_func=lambda n: f"Semana {n:02d} · {datos_semana(plan, n)['tema']}",
    )
    sesion = st.sidebar.radio("Sesión", [1, 2], horizontal=True,
                              format_func=lambda n: f"Sesión {n}")
    return semana, sesion


def _pestaña_plan(clave: str, info_semana: dict, sesion: int) -> None:
    """Contenidos planeados y lo que dice el registro docente para ambos grupos."""
    info_ses = info_semana.get(f"sesion_{sesion}", {})
    st.markdown(f"**{info_semana.get('eje', '')}**")
    if info_semana.get("resultado"):
        st.markdown(f"🎓 **Resultado de aprendizaje:** {info_semana['resultado']}")
    if info_semana.get("instrumento"):
        st.markdown(f"📏 **Instrumento:** {info_semana['instrumento']}  \n"
                    f"📂 **Evidencias:** {info_semana.get('evidencias', '')}")
    st.subheader("🎯 Contenidos planeados")
    for item in info_ses.get("contenidos", []):
        st.markdown(f"- {item}")
    if info_ses.get("actividad"):
        st.info(f"**Actividad evaluativa:** {info_ses['actividad']}")

    st.subheader("📋 Estado según el registro docente")
    try:
        df = obtener_almacen().leer()
    except Exception as error:
        st.warning(f"No se pudo leer el registro: {error}")
        return
    semana = str(info_semana["semana"])
    for grupo, etiqueta in ASIGNATURAS[clave]["grupos"].items():
        sub = df[(df["Asignatura"].str.strip() == etiqueta)
                 & (df["Semana"].astype(str).str.replace(".0", "", regex=False) == semana)]
        with st.expander(f"Grupo {grupo}", expanded=False):
            if sub.empty:
                st.caption("Aún no hay registros de esta semana para el grupo.")
                continue
            for _, fila in sub.iterrows():
                st.markdown(f"**{fila['Fecha']} · Estado:** {fila['Estado'] or '—'}")
                if fila["Cubierto"]:
                    st.markdown(f"✅ **Cubierto:** {fila['Cubierto']}")
                if fila["Pendiente"]:
                    st.markdown(f"⏳ **Pendiente:** {fila['Pendiente']}")


def _pestaña_ejercicio(nombre_generador: str | None) -> None:
    """Datos personalizados según el código estudiantil."""
    if not nombre_generador or nombre_generador not in GENERADORES:
        st.caption("Esta sesión no tiene ejercicio personal.")
        return
    codigo = st.text_input("Escribe tu código estudiantil", max_chars=15,
                           key=f"codigo_{nombre_generador}")
    if not codigo:
        st.caption("Con tu código se generan **tus propios datos**.")
        return
    enunciado, df = GENERADORES[nombre_generador](codigo)
    st.markdown(enunciado)
    st.dataframe(df, hide_index=True, width="stretch")
    st.download_button("⬇️ Descargar mis datos (CSV)", df.to_csv(index=False),
                       file_name=f"datos_{nombre_generador}_{codigo}.csv")
    st.warning("✍️ Resuélvelo **primero en tu cuaderno** (mínimo 20 minutos sin pantallas). "
               "Luego pasa a la pestaña 4 para verificar con código.")


def _pestaña_verificacion(textos: dict) -> None:
    """Prompts para IA y código de referencia en Python y R."""
    if "prompts" in textos:
        st.markdown(textos["prompts"])
    col_py, col_r = st.columns(2)
    with col_py:
        st.markdown("#### 🐍 Python (Google Colab)")
        if "python" in textos:
            st.code(textos["python"], language="python")
            if st.button("▶️ Ejecutar aquí", key="ejecutar_py"):
                salida = io.StringIO()
                with contextlib.redirect_stdout(salida):
                    exec(textos["python"], {"__name__": "__main__"})
                st.text(salida.getvalue())
    with col_r:
        st.markdown("#### 📘 R (Posit Cloud)")
        if "r" in textos:
            st.code(textos["r"], language="r")
            st.caption("Copia el script y ejecútalo en Posit Cloud.")


def _pestaña_auditoria() -> None:
    """Tabla para comparar el resultado manual con el del código."""
    st.markdown("Anota tus resultados **a mano** y los del **código**. "
                "La app calcula la diferencia; tú explicas por qué existe.")
    base = pd.DataFrame({"Cálculo": ["", "", ""],
                         "A mano": [None, None, None],
                         "Código": [None, None, None]})
    tabla = st.data_editor(base, num_rows="dynamic", width="stretch",
                           key="auditoria",
                           column_config={
                               "A mano": st.column_config.NumberColumn(format="%.4f"),
                               "Código": st.column_config.NumberColumn(format="%.4f")})
    tabla = tabla.dropna(subset=["A mano", "Código"])
    if not tabla.empty:
        tabla["Diferencia"] = (tabla["A mano"] - tabla["Código"]).abs()
        st.dataframe(tabla, hide_index=True, width="stretch")
    st.markdown("**Preguntas de cierre (en tu cuaderno):**\n"
                "1. ¿Coincidieron tus resultados? Si no, ¿en qué paso estuvo la diferencia?\n"
                "2. ¿Qué significa el resultado para el productor o el ingeniero?\n"
                "3. ¿Qué decisión agronómica tomarías con esta información?")


def pagina_asignatura(clave: str) -> None:
    """Página completa de una asignatura."""
    asig = ASIGNATURAS[clave]
    plan = cargar_plan(clave)
    semana, sesion = _selector_semana(plan)
    info_semana = datos_semana(plan, semana)
    info_ses = info_semana.get(f"sesion_{sesion}", {})

    st.title(f"{asig['icono']} {asig['nombre']}")
    st.markdown(f"### Semana {semana:02d} · Sesión {sesion}: {info_ses.get('titulo', info_semana['tema'])}")
    st.caption("Ruta sugerida: **1 → 5**. Puedes apoyarte en cualquier agente de IA; "
               "lo importante es que lo **escribas y lo entiendas** en tu cuaderno.")

    textos = cargar_sesion(clave, semana, sesion)
    pestañas = st.tabs(["🗓️ Plan", "📖 1. Teoría", "✍️ 2. Ejemplo a mano",
                        "🧑‍🌾 3. Ejercicio personal", "💻 4. Verificación",
                        "🔎 5. Auditoría"])
    with pestañas[0]:
        _pestaña_plan(clave, info_semana, sesion)
    with pestañas[1]:
        st.markdown(textos.get("teoria", "_Contenido en preparación._"))
    with pestañas[2]:
        st.markdown(textos.get("ejemplo", "_Contenido en preparación._"))
    with pestañas[3]:
        _pestaña_ejercicio(info_ses.get("ejercicio"))
    with pestañas[4]:
        if {"prompts", "python", "r"} & textos.keys():
            _pestaña_verificacion(textos)
        else:
            st.markdown("_Contenido en preparación._")
    with pestañas[5]:
        _pestaña_auditoria()
