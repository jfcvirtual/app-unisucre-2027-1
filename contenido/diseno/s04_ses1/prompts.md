### 🤖 Prompts de verificación
Úsalos **después** de construir tu tabla ANOVA a mano.

**Prompt para Python (Google Colab):**
```text
Escribe un código en Python, comentado paso a paso para un estudiante de
Ingeniería Agrícola, que analice un Diseño Completamente al Azar: (1) crea un
DataFrame de pandas con las columnas Tratamiento y Rendimiento usando estos
datos: [PEGA AQUÍ TUS DATOS]; (2) calcula A MANO con pandas el factor de
corrección, SC total, SC tratamientos y SC error; (3) arma la tabla ANOVA con
statsmodels (ols y anova_lm) para comparar; (4) calcula el valor F de tabla
con scipy.stats.f.ppf para alfa = 0.05; (5) calcula el coeficiente de variación.
```

**Prompt para R (Posit Cloud):**
```text
Escribe un script de R, comentado paso a paso para un estudiante de Ingeniería
Agrícola, que analice un Diseño Completamente al Azar: (1) crea un data.frame
con Tratamiento (factor) y Rendimiento con estos datos: [PEGA AQUÍ TUS DATOS];
(2) calcula con R base el factor de corrección y las sumas de cuadrados;
(3) ajusta el modelo con aov() y muestra summary(); (4) calcula F de tabla con
qf(0.95, gl1, gl2); (5) calcula el coeficiente de variación con
agricolae::cv.model().
```

> 👇 Abajo tienes el **código de referencia** del ejemplo resuelto.
