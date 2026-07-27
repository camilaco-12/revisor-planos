"""Escribe hallazgos hidrosanitarios en el Excel del proyecto (append).

Lee un JSON (lista de objetos con las 9 claves del esquema + 'plano_referencia')
y agrega una fila por hallazgo en la hoja 'Hallazgos hidrosanitarios' de
hallazgos_hidrosanitario.xlsx, sin sobrescribir filas existentes.

Mapeo de columnas (encabezado en la fila 4, datos desde la fila 5):
    A  ID                     -> consecutivo, continua el maximo existente
    B  disciplina
    C  hallazgo
    D  ubicacion
    E  severidad
    F  referencia_normativa
    G  riesgo
    H  justificacion_tecnica
    I  accion_correctiva
    J  requiere_validacion    -> TRUE / FALSE
    K  estado                 -> por defecto 'Pendiente'
    L  plano_referencia
    M  fecha_deteccion        -> por defecto la fecha de hoy

Uso:
    python escribir_hallazgos.py <ruta_json> [<ruta_xlsx>] [--fecha AAAA-MM-DD] [--dry-run]
"""
import argparse
import datetime as dt
import json
import os

from openpyxl import load_workbook

HOJA = "Hallazgos hidrosanitarios"
FILA_ENCABEZADO = 4
FILA_INICIO_DATOS = 5
DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_DEFECTO = os.path.join(DIR, "hallazgos_hidrosanitario.xlsx")

# columna (indice 1-based) -> clave del JSON
CAMPOS = {
    2: "disciplina",
    3: "hallazgo",
    4: "ubicacion",
    5: "severidad",
    6: "referencia_normativa",
    7: "riesgo",
    8: "justificacion_tecnica",
    9: "accion_correctiva",
}


def bool_txt(valor):
    if isinstance(valor, bool):
        return "TRUE" if valor else "FALSE"
    return "TRUE" if str(valor).strip().lower() in ("true", "1", "si", "sí") else "FALSE"


def ultima_fila_con_datos(ws):
    """Ultima fila con un hallazgo real (col C).

    El formato trae filas de plantilla con el ID pre-numerado pero vacias; por
    eso la ocupacion se mide por la columna 'hallazgo', no por el ID.
    """
    ultima = FILA_INICIO_DATOS - 1
    for fila in range(FILA_INICIO_DATOS, ws.max_row + 1):
        if ws.cell(fila, 3).value not in (None, ""):
            ultima = fila
    return ultima


def max_id(ws, hasta_fila):
    """Maximo ID entre filas que tienen un hallazgo real (ignora IDs de plantilla)."""
    maximo = 0
    for fila in range(FILA_INICIO_DATOS, hasta_fila + 1):
        if ws.cell(fila, 3).value in (None, ""):
            continue
        val = ws.cell(fila, 1).value
        try:
            maximo = max(maximo, int(val))
        except (TypeError, ValueError):
            continue
    return maximo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("xlsx", nargs="?", default=XLSX_DEFECTO)
    ap.add_argument("--fecha", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true", help="No guarda; solo reporta que haria")
    args = ap.parse_args()

    with open(args.json, encoding="utf-8") as f:
        hallazgos = json.load(f)

    wb = load_workbook(args.xlsx)
    ws = wb[HOJA]

    ultima = ultima_fila_con_datos(ws)
    siguiente_id = max_id(ws, ultima) + 1
    fila = ultima + 1

    for i, h in enumerate(hallazgos):
        ws.cell(fila, 1, siguiente_id + i)
        for col, clave in CAMPOS.items():
            ws.cell(fila, col, h.get(clave, ""))
        ws.cell(fila, 10, bool_txt(h.get("requiere_validacion", False)))
        ws.cell(fila, 11, h.get("estado", "Pendiente"))
        ws.cell(fila, 12, h.get("plano_referencia", ""))
        ws.cell(fila, 13, h.get("fecha_deteccion", args.fecha))
        fila += 1

    print(f"Hallazgos a escribir: {len(hallazgos)}")
    print(f"Primera fila nueva: {ultima + 1}  |  ID inicial: {siguiente_id}")
    if args.dry_run:
        print("DRY-RUN: no se guardo el archivo.")
        return
    wb.save(args.xlsx)
    print(f"OK: guardado en {args.xlsx}")


if __name__ == "__main__":
    main()
