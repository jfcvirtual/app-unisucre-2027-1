# ✏️ El Lápiz y el Algoritmo · Unisucre 2027-1

App en Streamlit para **Estadística Aplicada con Python y R (201622)** y **Diseño Experimental (201636)**,
del programa de Ingeniería Agrícola de la Universidad de Sucre.
Docente: **Justo Fuentes Cuello**.

## 🧭 Qué hace

| Para el estudiante | Para el docente |
|---|---|
| Teoría de cada semana para tomar apuntes | Registro de sesiones (reemplaza a AppSheet) |
| Ejemplos de ingeniería resueltos a mano | Pendiente de la sesión anterior cargado de forma automática |
| Ejercicio con **datos personales** (según el código estudiantil) | Estado: Dictada / Parcial / No dictada + motivo |
| Prompts y código de verificación en Python y R | Resumen e historial descargable para PRISMAU |
| Tabla de auditoría: a mano vs. código | Constancia de socialización del plan por grupo |
| Plan de asignatura oficial (semana a semana) | |

> ⚠️ Los `plan.yaml` reproducen el **FOR-FO-018 2027-1**. Si el plan oficial cambia, se actualiza primero el
> formato institucional y luego el `plan.yaml`. Pegue el enlace del PDF firmado en `url_plan_firmado`.

## 📁 Estructura

```
app.py                      Menú de navegación (nombres con tildes)
inicio.py                   Página de inicio
pages/
  1_Plan_de_Asignatura.py   Plan oficial para socializar el primer día
  2_Estadistica.py
  3_Diseno_Experimental.py
  4_Registro_Docente.py     Protegido con contraseña
nucleo/
  contenido.py              Lee planes y sesiones
  vista.py                  Pestañas de cada sesión
  ejercicios.py             Datos personalizados por estudiante
  registro.py               Google Sheets (o CSV local en pruebas)
contenido/
  estadistica/plan.yaml     Plan oficial de 16 semanas (FOR-FO-030 / FOR-FO-018 2027-1)
  estadistica/s03_ses1/     teoria.md, ejemplo.md, prompts.md, verificacion.py, verificacion.R
  diseno/...
```

## ➕ Agregar una sesión nueva

1. Crear la carpeta `contenido/<asignatura>/sSS_sesN` (por ejemplo, `contenido/diseno/s05_ses1`).
2. Poner allí los archivos que tenga listos: `teoria.md`, `ejemplo.md`, `prompts.md`,
   `verificacion.py`, `verificacion.R`. Los que falten aparecen como "en preparación".
3. (Opcional) Agregar un generador en `nucleo/ejercicios.py` y escribir su nombre en
   `plan.yaml` con la clave `ejercicio:`.
4. `git push` → Streamlit Cloud actualiza la app sola.

## ▶️ Ejecutar en el computador o en Codespaces

```bash
pip install -r requirements.txt
streamlit run app.py
```
Sin `secrets.toml`, el registro se guarda en `datos/registro_local.csv` y la contraseña de prueba es `unisucre`.

## 🔗 Conectar con la Google Sheet (la de AppSheet)

1. En **console.cloud.google.com**: crear el proyecto `app-unisucre` y habilitar **Google Sheets API**.
2. **IAM y administración → Cuentas de servicio → Crear**: nombre `registro-sesiones` (sin roles).
3. En la cuenta creada: **Claves → Agregar clave → Crear clave nueva → JSON** (se descarga un archivo `.json`).
4. Abrir la Google Sheet de AppSheet → **Compartir** con el correo `client_email` del JSON como **Editor**.
5. En Streamlit Cloud → **Manage app → Settings → Secrets**, pegar la plantilla de
   `.streamlit/secrets.toml.ejemplo` con el `sheet_id` y el contenido COMPLETO del `.json`
   entre las comillas `'''` de `gcp_json`.
6. Si la pestaña `Sesiones_2027_S_1` no existe, la app la crea con sus encabezados.

> 🔒 El archivo `.json` es una llave: no se sube a GitHub ni se comparte por chat o WhatsApp.

## ☁️ Publicar en Streamlit Community Cloud

1. Subir este repositorio a GitHub (público).
2. En share.streamlit.io → **New app** → elegir el repositorio y `app.py`.
3. En **Settings → Secrets** pegar el contenido de `secrets.toml`.

## 🔒 Qué NO va en este repositorio
- `secrets.toml` (ya está en `.gitignore`).
- **Rúbricas y respuestas de las actividades evaluadas** → Drive o repositorio privado.
