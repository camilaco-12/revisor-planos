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
   `${CLAUDE_PLUGIN_ROOT}/scripts/escribir_hallazgos.py` en el Excel destino (si no existe,
   parte de la plantilla en `${CLAUDE_PLUGIN_ROOT}/templates/hallazgos_hidrosanitario.xlsx`).
