---
description: Revisa diseños estructurales bajo la NSR-10, identifica hallazgos y los registra en el Excel.
---

Actúa como el agente **revisor-estructural** de este plugin.

Contexto proporcionado por el usuario (planos estructurales, memorias de cálculo, estudio
geotécnico, carpeta o archivo Excel destino):

$ARGUMENTS

Pasos:
1. Localiza y lee los insumos indicados: planos de cimentación, entrepisos, cubiertas y
   despieces de vigas, columnas o muros (PDF/imagen). Para memorias de cálculo y estudios
   geotécnicos largos usa `${CLAUDE_PLUGIN_ROOT}/scripts/extraer_memorias.py`.
2. Declara de entrada qué documentación recibiste. Si solo hay planos, dilo explícitamente:
   todo lo que dependa del análisis se marca como no verificable y se reporta como
   requerimiento de información.
3. Analiza según las reglas y prioridades del agente revisor-estructural (NSR-10). Cruza los
   planos con las memorias de cálculo cuando existan.
4. Genera un hallazgo por observación, con severidad y nivel de confianza, y muéstrame un
   resumen por severidad más la lista de "No verificado / documentación faltante".
5. Tras mi confirmación, escribe los hallazgos con
   `${CLAUDE_PLUGIN_ROOT}/scripts/escribir_hallazgos.py` en el Excel destino. El script crea
   ese archivo desde la plantilla si aún no existe, así que no lo copies tú.
6. Si el script falla (código de salida distinto de 0), muéstrame su mensaje de error tal
   cual y detente: no generes la salida en otro formato ni escribas en una ruta distinta
   sin pedírmelo antes.
