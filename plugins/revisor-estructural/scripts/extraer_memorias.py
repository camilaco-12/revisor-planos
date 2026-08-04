"""Extrae el texto de un PDF (p.ej. la memoria de calculo estructural) a un .txt.

Uso:
    python extraer_memorias.py <ruta_pdf> [ruta_salida_txt]

Se usa para leer documentos de muchas paginas (memorias de calculo, estudios
geotecnicos) que no se pueden renderizar con la herramienta Read. En estructural
es habitual que la memoria traiga cientos de paginas de salidas del programa de
analisis, asi que este script suele ser el primer paso de la revision.
"""
import sys
import fitz  # PyMuPDF


def extraer(ruta_pdf, ruta_txt):
    doc = fitz.open(ruta_pdf)
    partes = []
    for i, pagina in enumerate(doc, start=1):
        partes.append(f"\n===== PAGINA {i} =====\n")
        partes.append(pagina.get_text())
    doc.close()
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("".join(partes))
    print(f"OK: {len(partes)//2} paginas -> {ruta_txt}")


if __name__ == "__main__":
    pdf = sys.argv[1]
    txt = sys.argv[2] if len(sys.argv) > 2 else pdf.rsplit(".", 1)[0] + ".txt"
    extraer(pdf, txt)
