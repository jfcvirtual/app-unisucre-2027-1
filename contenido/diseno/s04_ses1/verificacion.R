# ============================================================
# Verificación: DCA · Ensayo de fertilización nitrogenada en maíz
# Diseño Experimental · Semana 04 · Sesión 1
# ============================================================

# Paso 1. Datos del ensayo: 4 dosis de N x 4 repeticiones (t/ha)
datos <- data.frame(
  Tratamiento = factor(rep(c("N0", "N60", "N120", "N180"), each = 4),
                       levels = c("N0", "N60", "N120", "N180")),
  Rendimiento = c(3.1, 3.4, 2.9, 3.2,
                  4.0, 4.3, 3.9, 4.2,
                  4.8, 5.1, 4.7, 5.0,
                  5.0, 4.9, 5.2, 4.9)
)

# Paso 2. Cálculo "a mano" con R base (igual que en el cuaderno)
t <- nlevels(datos$Tratamiento)                 # número de tratamientos
r <- 4                                          # repeticiones
n <- nrow(datos)                                # total de parcelas
FC   <- sum(datos$Rendimiento)^2 / n            # factor de corrección
SCT  <- sum(datos$Rendimiento^2) - FC           # SC total
totales <- tapply(datos$Rendimiento, datos$Tratamiento, sum)  # Yi.
SCTr <- sum(totales^2) / r - FC                 # SC tratamientos
SCE  <- SCT - SCTr                              # SC error
F    <- (SCTr / (t - 1)) / (SCE / (t * (r - 1)))

cat("FC =", round(FC, 4), "\n")
cat("SC total =", round(SCT, 4), " SC trat =", round(SCTr, 4),
    " SC error =", round(SCE, 4), "\n")
cat("F calculado =", round(F, 2), "\n")

# Paso 3. Valor F de tabla para alfa = 0.05
F_tabla <- qf(0.95, t - 1, t * (r - 1))
cat("F de tabla =", round(F_tabla, 2), "\n")

# Paso 4. Verificación con aov()
modelo <- aov(Rendimiento ~ Tratamiento, data = datos)
summary(modelo)

# Paso 5. Coeficiente de variación (paquete agricolae)
# install.packages("agricolae")   # solo la primera vez
library(agricolae)
cat("CV =", round(cv.model(modelo), 2), "%\n")
