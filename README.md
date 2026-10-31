# Simulador SIGCP - Examen de Suboficiales PNP 2026

Simulador web del examen de ascenso para **Suboficiales de la Policía Nacional del Perú**, basado en el balotario oficial **Águila Seis (15 JUL 2026)**.

La aplicación reproduce la experiencia del **SIGCP (Sistema Integrado de Gestión de Carrera Policial)**: login con CIP, clave y token, cronómetro de 120 minutos, 100 preguntas aleatorias y calificación automática con revisión de errores.

> Proyecto educativo e independiente. No es una plataforma oficial de la PNP.

---

## Características

- **Banco de ~1,500 preguntas** extraídas automáticamente del balotario oficial en PDF (`preguntas.js`).
- **Examen aleatorio de 100 preguntas** en cada intento, con opciones mezcladas ("chocolateadas") para evitar memorizar posiciones.
- **Cronómetro de 120 minutos** con entrega automática al finalizar el tiempo.
- **Navegador de preguntas en 4 columnas** (1–100) con indicador de preguntas respondidas.
- **Calificación automática**: correctas, incorrectas y en blanco.
- **Revisión de resultados** mostrando únicamente las preguntas falladas o sin responder, con la respuesta correcta.
- **Banco de respaldo interno** si `preguntas.js` no está disponible.
- **100% frontend**: sin servidor, sin base de datos y sin instalación. Listo para desplegar en Vercel, Netlify o GitHub Pages.

---

## Stack

| Capa | Tecnología |
| --- | --- |
| Interfaz | HTML5 + CSS3 (variables CSS, Flexbox/Grid) |
| Lógica | JavaScript vanilla (ES6) |
| Datos | `preguntas.js` generado con Python |
| Extracción del PDF | [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`) |

Sin frameworks, sin dependencias de Node y sin proceso de build.

---

## Estructura del proyecto

```
Simuladorpnp/
├── index.html                                  # Aplicación completa (UI + lógica)
├── preguntas.js                                # Banco de preguntas generado (~1,498)
├── generar_banco.py                            # Extractor del PDF → preguntas.js
├── AguilaSeisBancoSuboficiales15JUL2026.PDF    # Balotario oficial de origen
└── README.md
```

---

## Uso

### 1. Abrir el simulador

No requiere instalación. Basta con abrir `index.html` en el navegador:

```powershell
Start-Process index.html
```

O servir la carpeta localmente (recomendado para evitar restricciones del navegador con archivos locales):

```powershell
python -m http.server 8000
# Luego abre http://localhost:8000
```

### 2. Credenciales de demostración

| Campo | Valor |
| --- | --- |
| CIP | `31054163` |
| Contraseña | `Huancay@26*` |
| Token | Cualquier número de 6 dígitos |

> Las credenciales están definidas como constantes en `index.html` (`CIP_VALIDO` y `PASS_VALIDA`) y son solo demostrativas.

### 3. Realizar el simulacro

1. Inicia sesión con las credenciales de demostración.
2. Pulsa **Iniciar simulacro** para comenzar el cronómetro de 120 minutos.
3. Responde marcando el círculo de la opción. Puedes navegar entre preguntas desde el panel lateral.
4. Pulsa **Finalizar** y confirma la entrega.
5. Revisa tu puntaje y las preguntas incorrectas con su respuesta correcta.

---

## Regenerar el banco de preguntas

Si actualizas el PDF del balotario, puedes volver a generar `preguntas.js`:

```powershell
pip install pymupdf
python generar_banco.py
```

Salida esperada:

```
Archivo preguntas.js creado con N preguntas.
```

El script:

1. Extrae el texto del PDF con PyMuPDF.
2. Elimina marcas de agua y URLs.
3. Separa cada pregunta por su numeración.
4. Detecta enunciado, opciones (a–e), respuesta, código y ubicación.
5. Escribe `window.BANCO_PREGUNTAS_PDF` en `preguntas.js`.

> `preguntas.js` se carga con `<script src="preguntas.js">`. Si el archivo no existe o falla, la aplicación usa el banco de respaldo interno de `index.html`.

---

## Despliegue

Al ser un sitio estático, puedes desplegarlo directamente:

**Vercel**

```powershell
vercel
```

**Netlify / GitHub Pages**: publica la raíz del repositorio como sitio estático. No se requiere configuración de build ni comando de salida.

---

## Cómo funciona la calificación

- Cada intento selecciona 100 preguntas aleatorias del banco y mezcla sus opciones.
- Una respuesta se considera correcta si coincide con la clave oficial, comparando texto normalizado (mayúsculas, espacios y puntuación final).
- Al entregar (o al agotarse el tiempo) se calculan:
  - **Correctas** → suma al puntaje.
  - **Incorrectas** → se listan en la revisión.
  - **En blanco** → se listan como "Sin responder".
- El puntaje mostrado es el número de respuestas correctas sobre 100.

---

## Aviso

Este proyecto tiene fines de **estudio y práctica**. Las preguntas provienen de un balotario público de referencia y pueden contener errores de extracción. Verifica siempre la información con las fuentes oficiales de la PNP.
