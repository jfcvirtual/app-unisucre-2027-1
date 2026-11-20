"""
Registro Docente (reemplaza a AppSheet)
---------------------------------------
Protegido con contraseña (st.secrets["docente"]["clave"]).
Permite:
  1. Registrar una sesión nueva, con el pendiente de la sesión anterior ya cargado.
  2. Editar un registro existente.
  3. Ver el historial y un resumen para los informes de PRISMAU.
"""

from datetime import date

import pandas as pd
import streamlit as st

from nucleo.contenido import ASIGNATURAS, cargar_plan, datos_semana
from nucleo.registro import (COLUMNAS, ESTADOS, MOTIVOS, TEMA_SOCIALIZACION,
                             nuevo_id, obtener_almacen, socializaciones,
                             ultimo_pendiente)

st.set_page_config(page_title="Registro docente", page_icon="📝", layout="wide")
st.title("📝 Registro docente de sesiones")

# ---------------------------------------------------------------
# 1) Acceso con contraseña
# ---------------------------------------------------------------
try:
    clave_correcta = st.secrets["docente"]["clave"]
except Exception:
    clave_correcta = "unisucre"  # solo para pruebas locales sin secrets.toml
if not st.session_state.get("docente_ok"):
    clave = st.text_input("Contraseña del docente", type="password")
    if st.button("Entrar"):
        st.session_state["docente_ok"] = (clave == clave_correcta)
        st.rerun()
    st.stop()

almacen = obtener_almacen()
st.caption(f"Almacenamiento: **{almacen.nombre}**")
df = almacen.leer()

# Lista de todos los grupos: (texto visible, clave asignatura, etiqueta en la hoja)
GRUPOS = [(f"{a['nombre']} · {g}", clave, etiqueta)
          for clave, a in ASIGNATURAS.items() for g, etiqueta in a["grupos"].items()]


def formulario(valores: dict, clave_form: str) -> dict | None:
    """Formulario común para crear o editar un registro."""
    with st.form(clave_form):
        c1, c2, c3, c4 = st.columns(4)
        fecha = c1.date_input("Fecha", value=pd.to_datetime(valores.get("Fecha") or date.today()))
        semana = c2.number_input("Semana", 1, 16, int(float(valores.get("Semana") or 1)))
        sesion = c3.number_input("Sesión No", 1, 40, int(float(valores.get("Sesión No") or 1)))
        tipo = c4.selectbox("Tipo de sesión", ["Presencial", "Virtual"],
                            index=0 if valores.get("Tipo Sesión", "Presencial") == "Presencial" else 1)

        c5, c6 = st.columns(2)
        estado = c5.selectbox("Estado", ESTADOS,
                              index=ESTADOS.index(valores["Estado"]) if valores.get("Estado") in ESTADOS else 0)
        motivo = c6.selectbox("Motivo (si no se dictó o fue parcial)", MOTIVOS,
                              index=MOTIVOS.index(valores["Motivo"]) if valores.get("Motivo") in MOTIVOS else 0)

        tema = st.text_area("Tema planeado", valores.get("Tema", ""), height=90)
        cubierto = st.text_area("✅ Lo que se cubrió", valores.get("Cubierto", ""), height=90)
        pendiente = st.text_area("⏳ Lo que quedó pendiente", valores.get("Pendiente", ""), height=90)

        u1, u2 = st.columns(2)
        doc1 = u1.text_input("Documento1 URL (RPubs, guía…)", valores.get("Documento1 URL", ""))
        doc2 = u2.text_input("Documento2 URL (Colab…)", valores.get("Documento2 URL", ""))
        doc3 = u1.text_input("Documento3 URL (diapositivas…)", valores.get("Documento3 URL", ""))
        video = u2.text_input("Video URL", valores.get("Video URL", ""))
        obs = st.text_area("Observaciones", valores.get("Observaciones", ""), height=90)

        if not st.form_submit_button("💾 Guardar", type="primary"):
            return None
    return {
        "Fecha": fecha.isoformat(), "Semana": int(semana), "Sesión No": int(sesion),
        "Tipo Sesión": tipo, "Estado": estado, "Motivo": motivo,
        # Se mantiene la columna histórica "Sesión OK?" para compatibilidad
        "Sesión OK?": "TRUE" if estado == "Dictada" else "FALSE",
        "Tema": tema, "Cubierto": cubierto, "Pendiente": pendiente,
        "Documento1 URL": doc1, "Documento2 URL": doc2, "Documento3 URL": doc3,
        "Video URL": video, "Observaciones": obs,
    }


tab_nueva, tab_social, tab_editar, tab_historial = st.tabs(
    ["➕ Nueva sesión", "📜 Socialización del plan", "✏️ Editar registro",
     "📈 Historial y resumen"])

# ---------------------------------------------------------------
# 2) Nueva sesión
# ---------------------------------------------------------------
with tab_nueva:
    eleccion = st.selectbox("Asignatura y grupo", GRUPOS, format_func=lambda g: g[0])
    _, clave_asig, etiqueta = eleccion
    previo = ultimo_pendiente(df, etiqueta)

    sugerido = {"Tema": "", "Semana": 1, "Sesión No": 1}
    if previo is not None:
        st.info(f"**Última sesión ({previo['Fecha']}) · Estado: {previo['Estado'] or '—'}**\n\n"
                f"⏳ **Pendiente:** {previo['Pendiente'] or previo['Observaciones'] or '—'}")
        sesion_sig = int(float(previo["Sesión No"] or 0)) + 1
        semana_sig = int(float(previo["Semana"] or 1)) + (1 if sesion_sig % 2 == 1 else 0)
        semana_sig = min(semana_sig, 16)
        sugerido.update({"Semana": semana_sig, "Sesión No": sesion_sig,
                         "Tema": previo["Pendiente"]})
    # Agrega lo planeado para esa semana y sesión
    plan_sem = datos_semana(cargar_plan(clave_asig), sugerido["Semana"])
    num_ses = 1 if sugerido["Sesión No"] % 2 == 1 else 2
    titulo_plan = plan_sem.get(f"sesion_{num_ses}", {}).get("titulo", "")
    if titulo_plan:
        sugerido["Tema"] = (f"PENDIENTE ANTERIOR: {sugerido['Tema']}\n\n" if sugerido["Tema"] else "") \
            + f"PLANEADO S{sugerido['Semana']:02d}-Ses{num_ses}: {titulo_plan}"

    datos = formulario(sugerido, f"form_nuevo_{etiqueta}")
    if datos:
        datos.update({"ID": nuevo_id(), "Asignatura": etiqueta})
        almacen.agregar(datos)
        st.success("Sesión registrada.")
        st.rerun()

# ---------------------------------------------------------------
# 2b) Constancia de socialización del plan de asignatura
# ---------------------------------------------------------------
with tab_social:
    st.markdown("Registre aquí la **socialización y concertación** del plan con cada grupo. "
                "Es una constancia de apoyo para PRISMAU: la firma oficial del representante "
                "se hace en el **FOR-FO-018** por el canal institucional.")
    hechos = socializaciones(df)
    for _, _, etiqueta in GRUPOS:
        estado = f"✅ {hechos[etiqueta]}" if etiqueta in hechos else "⏳ pendiente"
        st.markdown(f"- **{etiqueta}:** {estado}")
    with st.form("form_socializacion"):
        grupo_soc = st.selectbox("Asignatura y grupo", GRUPOS, format_func=lambda g: g[0])
        c1, c2, c3 = st.columns([1, 2, 1])
        fecha_soc = c1.date_input("Fecha de concertación", value=date.today())
        representante = c2.text_input("Nombre del estudiante representante")
        codigo_rep = c3.text_input("Código estudiantil")
        url_firmado = st.text_input("URL del plan firmado (PDF en Drive)")
        obs_soc = st.text_area("Observaciones", height=80)
        if st.form_submit_button("💾 Guardar constancia", type="primary"):
            if not representante.strip():
                st.error("Escriba el nombre del representante.")
            else:
                almacen.agregar({
                    "ID": nuevo_id(), "Asignatura": grupo_soc[2],
                    "Fecha": fecha_soc.isoformat(), "Semana": 1, "Sesión No": "",
                    "Tipo Sesión": "Presencial", "Sesión OK?": "TRUE",
                    "Tema": TEMA_SOCIALIZACION, "Estado": "Constancia", "Motivo": "",
                    "Cubierto": "Plan de asignatura (FOR-FO-030 y FOR-FO-018) socializado y concertado",
                    "Pendiente": "" if url_firmado else "Subir el PDF firmado",
                    "Documento1 URL": url_firmado, "Documento2 URL": "",
                    "Documento3 URL": "", "Video URL": "",
                    "Observaciones": f"Representante: {representante.strip()} ({codigo_rep.strip()}). {obs_soc}".strip(),
                })
                st.success("Constancia registrada.")
                st.rerun()

# ---------------------------------------------------------------
# 3) Editar registro existente
# ---------------------------------------------------------------
with tab_editar:
    if df.empty:
        st.caption("Aún no hay registros.")
    else:
        recientes = df.iloc[::-1]
        id_sel = st.selectbox(
            "Registro", recientes["ID"],
            format_func=lambda i: " · ".join(
                recientes.loc[recientes["ID"] == i, ["Fecha", "Asignatura", "Sesión No"]]
                .astype(str).iloc[0]))
        fila = df[df["ID"] == id_sel].iloc[0].to_dict()
        datos = formulario(fila, f"form_editar_{id_sel}")
        if datos:
            datos.update({"ID": id_sel, "Asignatura": fila["Asignatura"]})
            almacen.actualizar(id_sel, datos)
            st.success("Registro actualizado.")
            st.rerun()

# ---------------------------------------------------------------
# 4) Historial y resumen para PRISMAU
# ---------------------------------------------------------------
with tab_historial:
    if df.empty:
        st.caption("Aún no hay registros.")
    else:
        filtro = st.multiselect("Filtrar por grupo", sorted(df["Asignatura"].unique()))
        vista = df[df["Asignatura"].isin(filtro)] if filtro else df
        c1, c2, c3 = st.columns(3)
        c1.metric("Dictadas", int((vista["Estado"] == "Dictada").sum()))
        c2.metric("Parciales", int((vista["Estado"] == "Parcial").sum()))
        c3.metric("No dictadas", int((vista["Estado"] == "No dictada").sum()))
        motivos = vista.loc[vista["Motivo"] != "", "Motivo"].value_counts()
        if not motivos.empty:
            st.markdown("**Motivos de sesiones no dictadas o parciales**")
            st.bar_chart(motivos, horizontal=True)
        st.dataframe(vista[COLUMNAS], hide_index=True, width="stretch")
        st.download_button("⬇️ Descargar historial (CSV)", vista.to_csv(index=False),
                           file_name="registro_sesiones.csv")
