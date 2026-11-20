### 🤖 Prompts de verificación
Úsalos **después** de resolver a mano. Pídele a tu agente de IA el código, ejecútalo y compara con tu cuaderno.

**Prompt para Python (Google Colab):**
```text
Escribe un código en Python, comentado paso a paso para un estudiante de
Ingeniería Agrícola, que: (1) cree una lista con estos rendimientos de maíz
en t/ha: [PEGA AQUÍ TUS DATOS]; (2) calcule la media, la mediana y la moda
usando el módulo statistics y también pandas; (3) recalcule la media y la
mediana sin el valor mínimo; (4) imprima todo con 2 decimales. No uses
funciones que no te haya pedido.
```

**Prompt para R (Posit Cloud):**
```text
Escribe un script de R base, comentado paso a paso para un estudiante de
Ingeniería Agrícola, que: (1) cree un vector con estos rendimientos de maíz
en t/ha: [PEGA AQUÍ TUS DATOS]; (2) calcule media y mediana; (3) como R no
tiene función de moda, cree una función moda() usando table(); (4) recalcule
la media y la mediana sin el valor mínimo; (5) imprima con round(, 2).
```

> 👇 Abajo tienes el **código de referencia** del ejemplo resuelto, para comparar.
