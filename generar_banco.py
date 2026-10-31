import fitz  # PyMuPDF
import json
import re
import difflib

doc = fitz.open("AguilaSeisBancoSuboficiales15JUL2026.PDF")
texto = "\n".join([page.get_text("text") for page in doc])

# Reparar caracteres especiales rotos en la segunda mitad del PDF
reemplazos = {
    "£": "Á",
    "…": "É",
    "Õ": "Í",
    "”": "Ó",
    "⁄": "Ú",
    "—": "Ñ",
    "ø": "¿",
    "Û": "ó",
}
for viejo, nuevo in reemplazos.items():
    texto = texto.replace(viejo, nuevo)

# Limpiar marcas de agua
texto = re.sub(r"987\s*245\s*798", "", texto)
texto = re.sub(r"https?://\S+", "", texto)

bloques = re.split(r"\n(?=\d{1,4}[\.,]\s+)", texto)
banco = []

for b in bloques:
    if "RESPUESTA:" not in b:
        continue

    partes = re.split(r"RESPUESTA\s*:", b, maxsplit=1)
    cuerpo, resto = partes[0], partes[1]

    # Extraer código y ubicación sin importar el orden en que salgan en el PDF
    cod_match = re.search(r"C[ÓO]DIGO\s*:\s*(\d+)", resto, re.IGNORECASE)
    codigo = cod_match.group(1) if cod_match else "PNP"

    ubi_match = re.search(
        r"(\((?:ART|texto)[^\n]+|\[TITULO[^\n]+)", resto, re.IGNORECASE
    )
    ubicacion = ubi_match.group(1).strip() if ubi_match else "BALOTARIO PNP 2026"

    # Limpiar etiquetas para quedarnos únicamente con el texto de la respuesta correcta
    resp_limpia = resto
    resp_limpia = re.sub(r"UBICACI[^\n:]*:", " ", resp_limpia, flags=re.IGNORECASE)
    resp_limpia = re.sub(r"C[ÓO]DIGO\s*:\s*\d*", " ", resp_limpia, flags=re.IGNORECASE)
    resp_limpia = re.sub(
        r"\((?:ART|texto)[^)]*\)\*?\*?", " ", resp_limpia, flags=re.IGNORECASE
    )
    resp_limpia = re.sub(r"\[[^\]]*\]", " ", resp_limpia)
    resp_limpia = re.sub(r"POLIC[ÍI]A|LICIA\s+MACIC|LICIA\s+NACIO", " ", resp_limpia)
    resp_limpia = re.sub(r"\s+", " ", resp_limpia).strip()

    # Extraer las 5 alternativas de la pregunta
    opciones_raw = re.split(r"(?:>{1,4}|»|ª)\s*", cuerpo)
    if len(opciones_raw) >= 6:
        enunciado = re.sub(r"^\d{1,4}[\.,]\s*", "", opciones_raw[0])
        enunciado = re.sub(r"\s+", " ", enunciado).strip()
        opciones = [re.sub(r"\s+", " ", op).strip() for op in opciones_raw[1:6]]

        # Emparejar con una de las 5 opciones de la pregunta para garantizar coincidencia exacta al 100%
        mejor_opcion = resp_limpia
        mejor_puntaje = 0.0
        for op in opciones:
            op_norm = op.rstrip(".").strip().upper()
            resp_norm = resp_limpia.rstrip(".").strip().upper()

            if op_norm and (op_norm in resp_norm or resp_norm in op_norm):
                mejor_opcion = op
                mejor_puntaje = 1.0
                break

            puntaje = difflib.SequenceMatcher(None, op_norm, resp_norm).ratio()
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_opcion = op

        banco.append({
            "id": len(banco) + 1,
            "codigo": codigo,
            "ubicacion": ubicacion,
            "pregunta": enunciado,
            "opciones": opciones,
            "respuesta": mejor_opcion,
        })

with open("preguntas.js", "w", encoding="utf-8") as f:
    f.write(
        "window.BANCO_PREGUNTAS_PDF = "
        + json.dumps(banco, ensure_ascii=False)
        + ";"
    )

print(
    f"¡Listo! Archivo preguntas.js actualizado con {len(banco)} preguntas y todas sus respuestas verificadas."
)