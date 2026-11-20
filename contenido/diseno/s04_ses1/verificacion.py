# ============================================================
# Verificación: DCA · Ensayo de fertilización nitrogenada en maíz
# Diseño Experimental · Semana 04 · Sesión 1
# ============================================================

# Paso 1. Importar las librerías
import pandas as pd                          # tablas de datos
from scipy import stats                      # valor F de tabla
import statsmodels.formula.api as smf        # ajuste del modelo lineal
from statsmodels.stats.anova import anova_lm # tabla ANOVA

# Paso 2. Datos del ensayo: 4 dosis de N x 4 repeticiones (t/ha)
datos = pd.DataFrame({
    "Tratamiento": ["N0"] * 4 + ["N60"] * 4 + ["N120"] * 4 + ["N180"] * 4,
    "Rendimiento": [3.1, 3.4, 2.9, 3.2,
                    4.0, 4.3, 3.9, 4.2,
                    4.8, 5.1, 4.7, 5.0,
                    5.0, 4.9, 5.2, 4.9],
})

# Paso 3. Cálculo "a mano" con pandas (igual que en el cuaderno)
t = datos["Tratamiento"].nunique()            # número de tratamientos
r = 4                                         # repeticiones
n = len(datos)                                # total de parcelas
gran_total = datos["Rendimiento"].sum()       # Y..
FC = gran_total**2 / n                        # factor de corrección
SCT = (datos["Rendimiento"]**2).sum() - FC    # SC total
totales = datos.groupby("Tratamiento")["Rendimiento"].sum()   # Yi.
SCTr = (totales**2).sum() / r - FC            # SC tratamientos
SCE = SCT - SCTr                              # SC error
CMTr, CME = SCTr / (t - 1), SCE / (t * (r - 1))
F = CMTr / CME

print("=== Cálculo paso a paso ===")
print(f"Gran total = {gran_total:.1f}   FC = {FC:.4f}")
print(f"SC total = {SCT:.4f}   SC trat = {SCTr:.4f}   SC error = {SCE:.4f}")
print(f"CM trat = {CMTr:.4f}   CM error = {CME:.4f}   F = {F:.2f}")

# Paso 4. Valor F de tabla para alfa = 0.05
F_tabla = stats.f.ppf(0.95, t - 1, t * (r - 1))
print(f"F de tabla (0.05; {t-1}; {t*(r-1)}) = {F_tabla:.2f}")
print("Decisión:", "Se rechaza H0" if F > F_tabla else "No se rechaza H0")

# Paso 5. Verificación con statsmodels (tabla ANOVA completa)
modelo = smf.ols("Rendimiento ~ C(Tratamiento)", data=datos).fit()
print("\n=== Tabla ANOVA (statsmodels) ===")
print(anova_lm(modelo).round(4))

# Paso 6. Coeficiente de variación del ensayo
CV = (CME**0.5) / datos["Rendimiento"].mean() * 100
print(f"\nCV = {CV:.2f} %")
