## ✍️ Ejemplo resuelto a mano

### 🌽 Enunciado
La cooperativa registró el rendimiento de maíz (t/ha) de **10 fincas** en la cosecha de 2026-B. La finca F07, ubicada en zona baja, sufrió **encharcamiento**.

| Finca | F01 | F02 | F03 | F04 | F05 | F06 | F07 | F08 | F09 | F10 |
|---|---|---|---|---|---|---|---|---|---|---|
| t/ha | 3.8 | 4.5 | 4.2 | 5.1 | 3.6 | 4.2 | **2.1** | 4.8 | 4.2 | 4.5 |

Calcula la **media**, la **mediana** y la **moda**, y decide cuál presentar al banco.

---

### Paso 1. Media
1. Suma de los datos:
   $3.8 + 4.5 + 4.2 + 5.1 + 3.6 + 4.2 + 2.1 + 4.8 + 4.2 + 4.5 = 41.0$
2. Divide entre $n = 10$:

$$\bar{x} = \frac{41.0}{10} = \mathbf{4.10\ t/ha}$$

### Paso 2. Mediana
1. **Ordena** los datos de menor a mayor:
   $2.1,\ 3.6,\ 3.8,\ 4.2,\ \underline{4.2},\ \underline{4.2},\ 4.5,\ 4.5,\ 4.8,\ 5.1$
2. Como $n = 10$ es **par**, promedia las posiciones 5 y 6:

$$Me = \frac{4.2 + 4.2}{2} = \mathbf{4.20\ t/ha}$$

### Paso 3. Moda
1. Cuenta las repeticiones: $4.2$ aparece **3 veces**, $4.5$ aparece 2 veces y el resto, 1 vez.

$$Mo = \mathbf{4.2\ t/ha}$$

### Paso 4. Efecto del valor extremo
Si se **excluye** la finca encharcada (F07):

| Medida | Con F07 | Sin F07 | Cambio |
|---|---|---|---|
| Media | 4.10 | 4.32 | **+0.22** |
| Mediana | 4.20 | 4.20 | **0.00** |

> 🔎 La **mediana no se movió**; la media sí. Esto confirma que la media es sensible a los valores extremos.

---

### 🧑‍🌾 Interpretación agronómica
- El rendimiento típico de la cooperativa es de **4.2 t/ha** (mediana y moda coinciden).
- La media (4.10) está "castigada" por una sola finca afectada por el encharcamiento.
- ✅ **Recomendación:** presentar al banco la **mediana (4.2 t/ha)** e informar aparte el caso de la F07 como un riesgo de drenaje que conviene atender.
