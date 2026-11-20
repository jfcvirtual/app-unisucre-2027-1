"""
nucleo/contenido.py
-------------------
Lee los planes semanales (plan.yaml) y los archivos de cada sesión
(teoria.md, ejemplo.md, prompts.md, verificacion.py, verificacion.R).

El CONTENIDO vive en la carpeta /contenido y está separado del CÓDIGO:
para agregar una sesión nueva solo hay que crear su carpeta con los
archivos .md, sin tocar la programación.
"""

from pathlib import Path

import yaml

# Carpeta raíz donde están los contenidos de las asignaturas
RAIZ_CONTENIDO = Path(__file__).resolve().parent.parent / "contenido"

# Asignaturas disponibles: clave interna -> datos generales
ASIGNATURAS = {
    "estadistica": {
        "nombre": "Estadística Aplicada con Python y R",
        "codigo": "201622",
        "icono": "📊",
        # Así se escriben en la columna "Asignatura" de la Google Sheet
        # (se conserva la misma codificación que se usaba en AppSheet)
        "grupos": {"G1": "Est_Grupo_1", "G2": "Est_Grupo_2"},
    },
    "diseno": {
        "nombre": "Diseño Experimental",
        "codigo": "201636",
        "icono": "🌱",
        "grupos": {
            "G1": "Diseño_Experimental Grupo_1",
            "G2": "Diseño_Experimental Grupo_2",
        },
    },
}

# Archivos que puede tener cada sesión (todos son opcionales)
ARCHIVOS_SESION = {
    "teoria": "teoria.md",
    "ejemplo": "ejemplo.md",
    "prompts": "prompts.md",
    "python": "verificacion.py",
    "r": "verificacion.R",
}


def cargar_plan(asignatura: str) -> dict:
    """Devuelve el plan de 16 semanas de una asignatura (plan.yaml)."""
    ruta = RAIZ_CONTENIDO / asignatura / "plan.yaml"
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)


def carpeta_sesion(asignatura: str, semana: int, sesion: int) -> Path:
    """Ruta de la carpeta de una sesión, p. ej. contenido/diseno/s04_ses1."""
    return RAIZ_CONTENIDO / asignatura / f"s{semana:02d}_ses{sesion}"


def cargar_sesion(asignatura: str, semana: int, sesion: int) -> dict:
    """
    Lee los archivos disponibles de una sesión.
    Devuelve un diccionario {tipo: texto}; si un archivo no existe,
    simplemente no aparece en el diccionario.
    """
    carpeta = carpeta_sesion(asignatura, semana, sesion)
    textos = {}
    for clave, nombre in ARCHIVOS_SESION.items():
        ruta = carpeta / nombre
        if ruta.exists():
            textos[clave] = ruta.read_text(encoding="utf-8")
    return textos


def datos_semana(plan: dict, semana: int) -> dict:
    """Busca en el plan la información de una semana concreta."""
    for s in plan.get("semanas", []):
        if s["semana"] == semana:
            return s
    return {}
