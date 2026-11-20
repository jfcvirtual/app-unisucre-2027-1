## 📖 Diseño Completamente al Azar (DCA)

> ✍️ **Toma apuntes en tu cuaderno** de cada recuadro. Puedes consultar con tu agente de IA, pero **escribe con tus propias palabras**.

### 🌾 Situación de interés
Un agricultor de **Sampués (Sucre)** quiere saber si vale la pena aumentar la dosis de nitrógeno en su maíz. Se montó un ensayo en un lote **plano y homogéneo** con 4 dosis y 4 repeticiones. ¿Las dosis producen rendimientos **realmente** diferentes o las diferencias se deben al azar?

---

### 1. ¿Cuándo usar un DCA?
- Las **unidades experimentales son homogéneas** (mismo suelo, pendiente, manejo).
- Típico en **invernadero, laboratorio** o lotes muy uniformes.
- Los tratamientos se asignan **completamente al azar** a las parcelas.

> 🔎 **Analogía:** es como repartir bolsas de semilla en un lote parejo: como todas las parcelas son iguales, basta con sortear qué tratamiento va en cada una.

### 2. Modelo lineal aditivo

$$y_{ij} = \mu + \tau_i + \varepsilon_{ij}$$

| Símbolo | Significado |
|---|---|
| $y_{ij}$ | Rendimiento de la repetición $j$ del tratamiento $i$ |
| $\mu$ | Media general |
| $\tau_i$ | Efecto del tratamiento $i$ (dosis de N) |
| $\varepsilon_{ij}$ | Error experimental, $\varepsilon_{ij} \sim N(0, \sigma^2)$ |

### 3. Hipótesis
- $H_0: \tau_1 = \tau_2 = \dots = \tau_t = 0$ (las dosis **no** afectan el rendimiento)
- $H_1:$ al menos un $\tau_i \neq 0$

### 4. Fórmulas para el cálculo manual
Con $t$ tratamientos, $r$ repeticiones y $n = t \cdot r$:

1. **Gran total:** $Y_{..} = \sum y_{ij}$
2. **Factor de corrección:** $FC = \dfrac{Y_{..}^2}{n}$
3. **SC total:** $SC_T = \sum y_{ij}^2 - FC$
4. **SC tratamientos:** $SC_{Tr} = \dfrac{\sum Y_{i.}^2}{r} - FC$
5. **SC error:** $SC_E = SC_T - SC_{Tr}$

### 5. Tabla ANOVA

| Fuente | gl | SC | CM | F |
|---|---|---|---|---|
| Tratamientos | $t-1$ | $SC_{Tr}$ | $SC_{Tr}/(t-1)$ | $CM_{Tr}/CM_E$ |
| Error | $t(r-1)$ | $SC_E$ | $SC_E/[t(r-1)]$ | |
| Total | $n-1$ | $SC_T$ | | |

**Regla de decisión:** si $F_{calc} > F_{tabla}(\alpha;\ t-1;\ t(r-1))$, se **rechaza** $H_0$.

### 6. Coeficiente de variación
$$CV = \frac{\sqrt{CM_E}}{\bar{y}_{..}} \times 100$$
En ensayos de campo con maíz, un CV **menor de 15 %** suele indicar un experimento bien conducido.

---

### 🤖 Prompt de estudio guiado
```text
Actúa como mi tutor de Diseño Experimental en modo guiado. NO me des las
respuestas. Explícame con un ensayo de fertilización de maíz en Sucre por qué
el ANOVA compara la variación ENTRE tratamientos con la variación DENTRO de
ellos. Hazme una pregunta a la vez y, al final, pídeme que escriba con mis
palabras qué significa una F grande.
```
