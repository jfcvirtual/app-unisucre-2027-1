## ✍️ Ejemplo resuelto a mano

### 🌽 Enunciado
Ensayo de fertilización nitrogenada en maíz (Sampués, Sucre). DCA con **4 dosis** de N (kg/ha) y **4 repeticiones**. Variable respuesta: rendimiento (t/ha).

| Tratamiento | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| N0 | 3.1 | 3.4 | 2.9 | 3.2 |
| N60 | 4.0 | 4.3 | 3.9 | 4.2 |
| N120 | 4.8 | 5.1 | 4.7 | 5.0 |
| N180 | 5.0 | 4.9 | 5.2 | 4.9 |

Con $\alpha = 0.05$: ¿la dosis de N afecta el rendimiento?

---

### Paso 1. Totales, medias y cuadrados por tratamiento

| Tratamiento | Total $Y_{i.}$ | Media $\bar{y}_{i.}$ | $Y_{i.}^2$ | $\sum_j y_{ij}^2$ |
|---|---|---|---|---|
| N0 | 12.6 | 3.15 | 158.76 | 39.82 |
| N60 | 16.4 | 4.10 | 268.96 | 67.34 |
| N120 | 19.6 | 4.90 | 384.16 | 96.14 |
| N180 | 20.0 | 5.00 | 400.00 | 100.06 |
| **Suma** | **68.6** | | **1211.88** | **303.36** |

> 💡 Ejemplo de $\sum_j y_{ij}^2$ para N0: $3.1^2 + 3.4^2 + 2.9^2 + 3.2^2 = 9.61 + 11.56 + 8.41 + 10.24 = 39.82$

### Paso 2. Factor de corrección
$$FC = \frac{68.6^2}{16} = \frac{4705.96}{16} = 294.1225$$

### Paso 3. Sumas de cuadrados
$$SC_T = 303.36 - 294.1225 = 9.2375$$
$$SC_{Tr} = \frac{1211.88}{4} - 294.1225 = 302.97 - 294.1225 = 8.8475$$
$$SC_E = 9.2375 - 8.8475 = 0.3900$$

### Paso 4. Tabla ANOVA

| Fuente | gl | SC | CM | F calc | F tabla (0.05) |
|---|---|---|---|---|---|
| Dosis de N | 3 | 8.8475 | 2.9492 | **90.74** | 3.49 |
| Error | 12 | 0.3900 | 0.0325 | | |
| Total | 15 | 9.2375 | | | |

- $CM_{Tr} = 8.8475 / 3 = 2.9492$
- $CM_E = 0.3900 / 12 = 0.0325$
- $F = 2.9492 / 0.0325 = 90.74$

### Paso 5. Decisión
$F_{calc} = 90.74 > F_{tabla} = 3.49$ → **se rechaza $H_0$**.

### Paso 6. Coeficiente de variación
$$\bar{y}_{..} = \frac{68.6}{16} = 4.2875 \qquad CV = \frac{\sqrt{0.0325}}{4.2875} \times 100 = \frac{0.1803}{4.2875} \times 100 = 4.20\ \%$$

---

### 🧑‍🌾 Interpretación agronómica
- La dosis de nitrógeno **sí afecta** el rendimiento del maíz.
- El **CV de 4.2 %** indica un ensayo muy bien conducido.
- Las medias suben de 3.15 (N0) a 4.90 (N120), pero de N120 a N180 solo se gana **0.10 t/ha**.
- ⏭️ **Pregunta abierta para la semana 5:** ¿esa diferencia entre N120 y N180 es significativa? Si no lo es, aplicar 60 kg/ha más de N **no se justifica económicamente**. Lo resolveremos con **comparaciones múltiples (Tukey)**.
