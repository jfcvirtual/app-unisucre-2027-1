## 📖 Medidas de tendencia central

> ✍️ **Toma apuntes en tu cuaderno** de cada recuadro. Puedes consultar con tu agente de IA para entender mejor, pero **escribe con tus propias palabras**.

### 🌾 Situación de interés
Una cooperativa de **Corozal (Sucre)** quiere saber cuál es el rendimiento "típico" de maíz de sus asociados para negociar un crédito. ¿Qué número debe presentar al banco?

Las **medidas de tendencia central** responden a esa pregunta: resumen un conjunto de datos en **un solo valor representativo**.

---

### 1. Media aritmética ($\bar{x}$)
Es el **punto de equilibrio** de los datos: la suma de todos los valores dividida entre cuántos son.

$$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$

- 🔎 **Analogía:** si los bultos de maíz de todas las fincas se reunieran y se repartieran por partes iguales, la media es lo que le tocaría a cada finca.
- ⚠️ **Sensible a valores extremos:** una finca inundada en la Mojana arrastra la media hacia abajo.

### 2. Mediana ($Me$)
Es el **valor del centro** cuando los datos están **ordenados**.

- Si $n$ es **impar**: $Me = x_{\left(\frac{n+1}{2}\right)}$
- Si $n$ es **par**: $Me = \dfrac{x_{\left(\frac{n}{2}\right)} + x_{\left(\frac{n}{2}+1\right)}}{2}$

- 🔎 **Analogía:** si las fincas se ponen en fila de menor a mayor rendimiento, la mediana es la finca del medio.
- ✅ **Robusta:** casi no cambia con valores extremos.

### 3. Moda ($Mo$)
Es el valor que **más se repite**.

- Puede no existir, o haber varias (bimodal, multimodal).
- Es la **única** medida útil para variables **cualitativas** (p. ej., la variedad de maíz más sembrada).

---

### 🧭 ¿Cuál usar?

| Situación | Medida recomendada |
|---|---|
| Datos simétricos, sin valores extremos | **Media** |
| Datos con valores extremos o asimétricos (ingresos, áreas de finca) | **Mediana** |
| Variables cualitativas o el valor más frecuente | **Moda** |

> 📌 **Regla práctica:** si la media y la mediana están **muy separadas**, hay asimetría o valores extremos.

---

### 🤖 Prompt de estudio guiado (cópialo en tu agente de IA)
```text
Actúa como mi tutor de estadística en modo guiado. NO me des respuestas directas.
Quiero entender la diferencia entre media, mediana y moda usando rendimientos
de maíz de fincas de Sucre (Colombia). Hazme una pregunta a la vez, espera mi
respuesta y corrígeme con pistas. Al final, pídeme que escriba un resumen de
5 líneas con mis propias palabras.
```
