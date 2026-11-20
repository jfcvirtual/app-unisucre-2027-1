"""
nucleo/ejercicios.py
--------------------
Generadores de datos PERSONALIZADOS para el "Ejercicio personal" de cada sesión.

Cada estudiante escribe su código estudiantil y recibe sus propios datos
(la semilla aleatoria sale del código). Así:
  - cada quien resuelve a mano con números distintos,
  - el docente puede regenerar exactamente los mismos datos para calificar.

Las RESPUESTAS no se muestran en la app (quedan en el repositorio privado).
"""

import hashlib

import numpy as np
import pandas as pd


def semilla(codigo: str, etiqueta: str) -> int:
    """Convierte código estudiantil + nombre del ejercicio en una semilla fija."""
    texto = f"{codigo.strip().upper()}-{etiqueta}"
    return int(hashlib.sha256(texto.encode()).hexdigest(), 16) % (2**32)


def rendimiento_maiz(codigo: str) -> tuple[str, pd.DataFrame]:
    """Estadística S03: rendimiento de maíz (t/ha) en 11 fincas de Sucre."""
    rng = np.random.default_rng(semilla(codigo, "rendimiento_maiz"))
    municipios = ["Sincelejo", "Corozal", "Sampués", "Los Palmitos", "Morroa",
                  "San Pedro", "Since", "Galeras", "Betulia", "Ovejas", "Chalán"]
    rend = np.round(rng.normal(4.2, 0.9, size=11).clip(1.5, 7.5), 1)
    # Se fuerza un valor repetido para que haya moda
    rend[rng.integers(0, 11)] = rend[rng.integers(0, 11)]
    df = pd.DataFrame({"Finca": [f"F{i+1:02d}" for i in range(11)],
                       "Municipio": municipios,
                       "Rendimiento_t_ha": rend})
    enunciado = ("Con los rendimientos de maíz de **tus** 11 fincas, calcula **a mano**: "
                 "media, mediana y moda. Luego decide cuál medida representa mejor "
                 "el rendimiento típico de la zona y justifícalo.")
    return enunciado, df


def dca_fertilizacion(codigo: str) -> tuple[str, pd.DataFrame]:
    """Diseño S04: DCA con 4 dosis de N en maíz, 4 repeticiones."""
    rng = np.random.default_rng(semilla(codigo, "dca_fertilizacion"))
    dosis = [0, 60, 120, 180]
    efecto = {0: 3.2, 60: 4.1, 120: 4.9, 180: 5.0}
    filas = []
    for d in dosis:
        for r in range(1, 5):
            y = round(float(rng.normal(efecto[d], 0.35)), 1)
            filas.append({"Tratamiento": f"N{d}", "Dosis_kgN_ha": d,
                          "Repetición": r, "Rendimiento_t_ha": y})
    df = pd.DataFrame(filas)
    enunciado = ("Con **tus** datos del ensayo de fertilización nitrogenada, construye "
                 "**a mano** la tabla ANOVA del DCA (SC, gl, CM, F) y concluye con "
                 "α = 0.05 si la dosis de N afecta el rendimiento.")
    return enunciado, df


# Registro de generadores disponibles: nombre (en plan.yaml) -> función
GENERADORES = {
    "rendimiento_maiz": rendimiento_maiz,
    "dca_fertilizacion": dca_fertilizacion,
}
