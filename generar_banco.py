import fitz  # pip install pymupdf
import json
import re

doc = fitz.open("AguilaSeisBancoSuboficiales15JUL2026.PDF")
texto = "\n".join([page.get_text("text") for page in doc])

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

    respuesta = re.split(r"UBICACI[ÓO]N\s*:|C[ÓO]DIGO\s*:", resto)[0]
    respuesta = re.sub(r"\s+", " ", respuesta).strip()

    cod_match = re.search(r"C[ÓO]DIGO\s*:\s*(\d+)", resto)
    ubi_match = re.search(r"UBICACI[ÓO]N\s*:\s*([^\n]+)", resto)

    opciones_raw = re.split(r"(?:>{1,4}|»|ª)\s*", cuerpo)
    if len(opciones_raw) >= 6:
        enunciado = re.sub(r"^\d{1,4}[\.,]\s*", "", opciones_raw[0])
        enunciado = re.sub(r"\s+", " ", enunciado).strip()
        opciones = [re.sub(r"\s+", " ", op).strip() for op in opciones_raw[1:6]]

        banco.append({
            "id": len(banco) + 1,
            "codigo": cod_match.group(1) if cod_match else "",
            "ubicacion": ubi_match.group(1).strip() if ubi_match else "BALOTARIO PNP 2026",
            "pregunta": enunciado,
            "opciones": opciones,
            "respuesta": respuesta
        })

with open("preguntas.js", "w", encoding="utf-8") as f:
    f.write("window.BANCO_PREGUNTAS_PDF = " + json.dumps(banco, ensure_ascii=False) + ";")

print(f"Archivo preguntas.js creado con {len(banco)} preguntas.")