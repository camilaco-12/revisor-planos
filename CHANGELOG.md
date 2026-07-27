# Changelog

Todos los cambios notables de este plugin se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
y el versionado [SemVer](https://semver.org/lang/es/).

## [0.1.0] - 2026-07-24
### Añadido
- Agente `revisor-hidrosanitario`: revisión técnica de planos hidrosanitarios (Colombia).
- Comando `/revisar-hidrosanitario` que dispara el flujo de revisión.
- Script `extraer_memorias.py` para extraer texto de PDFs largos (PyMuPDF).
- Script `escribir_hallazgos.py` para registrar hallazgos en Excel vía append (openpyxl).
- Plantilla `hallazgos_hidrosanitario.xlsx` con el esquema de salida.
- Documentación: README, LICENSE (MIT), guía de instalación como plugin/marketplace.
