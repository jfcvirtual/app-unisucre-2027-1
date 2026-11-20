"""
nucleo/registro.py
------------------
Registro de sesiones (reemplaza a AppSheet).

- En producción lee y escribe en la MISMA Google Sheet que usaba AppSheet,
  en una pestaña nueva para el semestre (p. ej. "Sesiones_2027_S_1").
  Así se conserva todo el historial desde 2023.
- Si no hay credenciales configuradas (pruebas en el computador),
  guarda los datos en un archivo CSV local: datos/registro_local.csv.
"""

import uuid
from pathlib import Path

import pandas as pd
import streamlit as st

# Columnas históricas de la hoja (iguales a las de AppSheet) + 4 nuevas
COLUMNAS = [
    "ID", "Asignatura", "Fecha", "Semana", "Sesión No", "Tipo Sesión",
    "Sesión OK?", "Tema", "Documento1 URL", "Documento2 URL",
    "Documento3 URL", "Video URL", "Observaciones",
    # Columnas nuevas para el seguimiento planeado vs. ejecutado
    "Estado", "Motivo", "Cubierto", "Pendiente",
]

ESTADOS = ["Dictada", "Parcial", "No dictada"]

# Motivos frecuentes tomados del registro 2026-2
MOTIVOS = [
    "", "Aire acondicionado dañado", "Sala no disponible o asignada a otro docente",
    "Sin listas de estudiantes", "Festivo", "Fallas de internet o plataforma",
    "Baja asistencia", "Actividad institucional", "Otro",
]

RUTA_LOCAL = Path(__file__).resolve().parent.parent / "datos" / "registro_local.csv"


class _AlmacenCSV:
    """Almacén local en CSV (solo para pruebas sin Google Sheets)."""

    nombre = "CSV local (modo de prueba)"

    def leer(self) -> pd.DataFrame:
        if RUTA_LOCAL.exists():
            return pd.read_csv(RUTA_LOCAL, dtype=str).fillna("")
        return pd.DataFrame(columns=COLUMNAS)

    def guardar_todo(self, df: pd.DataFrame) -> None:
        RUTA_LOCAL.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(RUTA_LOCAL, index=False)

    def agregar(self, fila: dict) -> None:
        df = self.leer()
        df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
        self.guardar_todo(df[COLUMNAS])

    def actualizar(self, id_: str, fila: dict) -> None:
        df = self.leer()
        for col, valor in fila.items():
            df.loc[df["ID"] == id_, col] = valor
        self.guardar_todo(df[COLUMNAS])


def _leer_credenciales() -> dict:
    """
    Credenciales de la cuenta de servicio. Se aceptan dos formas en los Secrets:
      1. gcp_json = ''' {contenido completo del archivo .json} '''   (recomendada)
      2. [gcp_service_account] con cada campo por separado
    """
    import json

    if "gcp_json" in st.secrets["registro"]:          # dentro de [registro]
        return json.loads(st.secrets["registro"]["gcp_json"])
    if "gcp_json" in st.secrets:                      # al inicio del archivo
        return json.loads(st.secrets["gcp_json"])
    return dict(st.secrets["gcp_service_account"])


class _AlmacenGoogle:
    """Almacén en Google Sheets mediante una cuenta de servicio."""

    nombre = "Google Sheets"

    def __init__(self):
        import gspread  # se importa aquí para no exigirlo en modo CSV

        credenciales = _leer_credenciales()
        cliente = gspread.service_account_from_dict(credenciales)
        libro = cliente.open_by_key(st.secrets["registro"]["sheet_id"])
        pestaña = st.secrets["registro"].get("pestana", "Sesiones_2027_S_1")
        try:
            self.hoja = libro.worksheet(pestaña)
        except gspread.WorksheetNotFound:
            # Si la pestaña del semestre no existe, se crea con sus encabezados
            self.hoja = libro.add_worksheet(pestaña, rows=300, cols=len(COLUMNAS))
            self.hoja.append_row(COLUMNAS)

    def leer(self) -> pd.DataFrame:
        filas = self.hoja.get_all_records(default_blank="")
        df = pd.DataFrame(filas, dtype=str)
        # Quita espacios sobrantes en los encabezados ("Asignatura " -> "Asignatura")
        df.columns = [c.strip() for c in df.columns] if len(df.columns) else COLUMNAS
        for col in COLUMNAS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNAS].fillna("")

    def agregar(self, fila: dict) -> None:
        self.hoja.append_row([str(fila.get(c, "")) for c in COLUMNAS],
                             value_input_option="USER_ENTERED")

    def actualizar(self, id_: str, fila: dict) -> None:
        celda = self.hoja.find(id_, in_column=1)
        if celda is None:
            raise ValueError(f"No se encontró el registro {id_}")
        valores = [str(fila.get(c, "")) for c in COLUMNAS]
        self.hoja.update(values=[valores], range_name=f"A{celda.row}",
                         value_input_option="USER_ENTERED")


@st.cache_resource
def obtener_almacen():
    """Usa Google Sheets si hay credenciales en st.secrets; si no, CSV local."""
    try:
        hay_credenciales = "registro" in st.secrets and (
            "gcp_json" in st.secrets["registro"] or "gcp_json" in st.secrets
            or "gcp_service_account" in st.secrets)
    except Exception:  # no existe secrets.toml: modo de prueba local
        hay_credenciales = False
    if not hay_credenciales:
        return _AlmacenCSV()
    try:
        return _AlmacenGoogle()
    except Exception as error:  # credenciales mal configuradas
        st.warning(f"No se pudo conectar con Google Sheets ({error}). "
                   "Se usará el CSV local.")
    return _AlmacenCSV()


def nuevo_id() -> str:
    """Identificador corto de 8 caracteres, como los que generaba AppSheet."""
    return uuid.uuid4().hex[:8]


def ultimo_pendiente(df: pd.DataFrame, asignatura_grupo: str) -> pd.Series | None:
    """Devuelve el último registro de un grupo (para arrastrar su pendiente)."""
    sub = df[(df["Asignatura"].str.strip() == asignatura_grupo)
             & ~df["Tema"].str.startswith("SOCIALIZACIÓN", na=False)].copy()
    if sub.empty:
        return None
    sub["_fecha"] = pd.to_datetime(sub["Fecha"], errors="coerce", dayfirst=False)
    sub["_sesion"] = pd.to_numeric(sub["Sesión No"], errors="coerce")
    sub = sub.sort_values(["_fecha", "_sesion"])
    return sub.iloc[-1]


# ---------------------------------------------------------------
# Socialización del plan de asignatura (constancia de apoyo)
# Se guarda como un registro más de la hoja, con un tema fijo.
# NO reemplaza la firma oficial del representante en el FOR-FO-018.
# ---------------------------------------------------------------
TEMA_SOCIALIZACION = "SOCIALIZACIÓN DEL PLAN DE ASIGNATURA"


def socializaciones(df: pd.DataFrame) -> dict:
    """Devuelve {etiqueta_grupo: fecha} de los grupos con el plan ya socializado."""
    sub = df[df["Tema"].str.startswith(TEMA_SOCIALIZACION, na=False)]
    return {fila["Asignatura"].strip(): fila["Fecha"] for _, fila in sub.iterrows()}
