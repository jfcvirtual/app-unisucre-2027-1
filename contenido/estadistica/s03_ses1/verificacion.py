# ============================================================
# Verificación: media, mediana y moda (rendimiento de maíz)
# Estadística Aplicada con Python y R · Semana 03 · Sesión 1
# ============================================================

# Paso 1. Importar las librerías
import statistics          # funciones estadísticas básicas de Python
import pandas as pd        # manejo de tablas de datos

# Paso 2. Datos del ejemplo: rendimiento de maíz en t/ha (10 fincas)
rendimientos = [3.8, 4.5, 4.2, 5.1, 3.6, 4.2, 2.1, 4.8, 4.2, 4.5]

# Paso 3. Media: suma de los datos dividida entre n
media = statistics.mean(rendimientos)

# Paso 4. Mediana: valor central de los datos ordenados
mediana = statistics.median(rendimientos)

# Paso 5. Moda: valor que más se repite (multimode devuelve todas las modas)
modas = statistics.multimode(rendimientos)

print("=== Con todas las fincas ===")
print(f"Media   : {media:.2f} t/ha")
print(f"Mediana : {mediana:.2f} t/ha")
print(f"Moda(s) : {modas}")

# Paso 6. Lo mismo con pandas (como se hará con datasets grandes)
serie = pd.Series(rendimientos, name="Rendimiento_t_ha")
print("\n=== Verificación con pandas ===")
print(f"Media   : {serie.mean():.2f}")
print(f"Mediana : {serie.median():.2f}")
print(f"Moda    : {serie.mode().tolist()}")

# Paso 7. Efecto del valor extremo: se excluye la finca encharcada (mínimo)
sin_extremo = [x for x in rendimientos if x != min(rendimientos)]
print("\n=== Sin la finca encharcada ===")
print(f"Media   : {statistics.mean(sin_extremo):.2f} t/ha")
print(f"Mediana : {statistics.median(sin_extremo):.2f} t/ha")
