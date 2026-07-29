"""Verifica que las dependencias de Python del plugin esten instaladas.

No instala nada: si falta algo, imprime el comando exacto para instalarlo y
sale con codigo 1. Pensado para correr desde el hook SessionStart, donde
instalar por cuenta propia en el entorno del usuario no seria seguro.

Uso:
    python verificar_dependencias.py            # avisa y sale con 0 (modo hook)
    python verificar_dependencias.py --strict   # sale con 1 si falta algo
"""
import importlib.util
import sys

# nombre del modulo que se importa -> paquete que se instala con pip
DEPENDENCIAS = {
    "fitz": "pymupdf",       # PyMuPDF se importa como 'fitz'
    "openpyxl": "openpyxl",
}


def faltantes():
    return [
        pip_name
        for modulo, pip_name in DEPENDENCIAS.items()
        if importlib.util.find_spec(modulo) is None
    ]


def main():
    pendientes = faltantes()
    if not pendientes:
        return 0

    print("[revisor-planos] Faltan dependencias de Python: " + ", ".join(pendientes))
    print("El agente no podra leer memorias en PDF ni escribir el Excel de hallazgos.")
    print("Instalalas con:")
    print(f'  "{sys.executable}" -m pip install ' + " ".join(pendientes))
    print("Este plugin NO instala nada por su cuenta: la instalacion la decides tu.")
    # Por defecto salimos con 0 para que el hook SessionStart no se reporte como
    # fallido; el aviso ya quedo en stdout, que es lo que llega al agente.
    return 1 if "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
