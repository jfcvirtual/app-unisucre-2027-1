# ============================================================
# Verificación: media, mediana y moda (rendimiento de maíz)
# Estadística Aplicada con Python y R · Semana 03 · Sesión 1
# ============================================================

# Paso 1. Datos del ejemplo: rendimiento de maíz en t/ha (10 fincas)
rendimientos <- c(3.8, 4.5, 4.2, 5.1, 3.6, 4.2, 2.1, 4.8, 4.2, 4.5)

# Paso 2. Media y mediana con las funciones de R base
media   <- mean(rendimientos)
mediana <- median(rendimientos)

# Paso 3. R no trae función para la moda: la construimos
moda <- function(x) {
  frecuencias <- table(x)                          # cuenta cuántas veces aparece cada valor
  as.numeric(names(frecuencias)[frecuencias == max(frecuencias)])  # el (los) más frecuente(s)
}

cat("=== Con todas las fincas ===\n")
cat("Media   :", round(media, 2), "t/ha\n")
cat("Mediana :", round(mediana, 2), "t/ha\n")
cat("Moda    :", moda(rendimientos), "t/ha\n")

# Paso 4. Efecto del valor extremo: se excluye la finca encharcada (mínimo)
sin_extremo <- rendimientos[rendimientos != min(rendimientos)]
cat("\n=== Sin la finca encharcada ===\n")
cat("Media   :", round(mean(sin_extremo), 2), "t/ha\n")
cat("Mediana :", round(median(sin_extremo), 2), "t/ha\n")
