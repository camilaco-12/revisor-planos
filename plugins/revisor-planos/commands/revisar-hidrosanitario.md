---
description: Revisa planos hidrosanitarios, identifica hallazgos y los registra en el Excel.
---

Actúa como el agente **revisor-hidrosanitario** de este plugin.

Contexto proporcionado por el usuario (planos a revisar, carpeta o archivo Excel destino):

$ARGUMENTS

Pasos:
1. Localiza y lee los planos hidrosanitarios indicados (PDF/imagen). Para memorias de
   cálculo largas usa `${CLAUDE_PLUGIN_ROOT}/scripts/extraer_memorias.py`.
2. Analiza según las reglas y prioridades del agente revisor-hidrosanitario.
3. Genera un hallazgo por observación y muéstrame un resumen por severidad.
4. Tras mi confirmación, escribe los hallazgos con
   `${CLAUDE_PLUGIN_ROOT}/scripts/escribir_hallazgos.py` en el Excel destino. El script crea
   ese archivo desde la plantilla si aún no existe, así que no lo copies tú.
5. Si el script falla (código de salida distinto de 0), muéstrame su mensaje de error tal
   cual y detente: no generes la salida en otro formato ni escribas en una ruta distinta
   sin pedírmelo antes.
