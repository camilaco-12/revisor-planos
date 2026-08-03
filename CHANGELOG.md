# Changelog

Todos los cambios notables de este plugin se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
y el versionado [SemVer](https://semver.org/lang/es/).

## [0.3.0] - 2026-08-03
### Añadido
- Columna `nivel_confianza` (Alta/Media/Baja) en el esquema de hallazgos, separada de la
  severidad: la severidad mide qué tan grave es el hallazgo y la confianza qué tan seguro
  está el agente de que sea real. Es obligatoria y se valida antes de tocar el disco.
- Verificación del encabezado (fila 4) antes de escribir: un Excel con el esquema anterior
  se rechaza en vez de dejar cada dato en la columna equivocada.
- Script `migrar_esquema.py` para migrar archivos del esquema v1 al v2 conservando los
  hallazgos, con respaldo `.v1.bak.xlsx`. La conversión es conservadora: los hallazgos con
  `requiere_validacion = TRUE` pasan a confianza `Baja` y los `FALSE` quedan vacíos.
- Listas desplegables en la plantilla para disciplina, severidad, nivel de confianza y estado.
- Desglose por nivel de confianza en el resumen que imprime `escribir_hallazgos.py`.

### Cambiado
- Esquema de columnas v2: `nivel_confianza` entra en la columna F y `estado` se desplaza a
  la M. `estado` es de seguimiento manual: las filas nuevas siempre nacen en "Pendiente".

### Eliminado
- Campo booleano `requiere_validacion`, reemplazado por `nivel_confianza`.

## [0.2.0] - 2026-07-28
### Añadido
- `escribir_hallazgos.py` crea el Excel destino desde la plantilla cuando no existe,
  incluidas las carpetas intermedias.
- Guardado atómico: un fallo a mitad de escritura ya no puede dejar el Excel truncado.
- Mensajes accionables ante errores de permisos en Windows (Excel abierto detectado por su
  archivo de bloqueo `~$`, Acceso controlado a carpetas de Defender, carpeta de solo
  lectura), con código de salida `2`.
- Códigos de salida diferenciados: `0` OK, `2` permisos, `3` entrada, `4` dependencias.
- Script `verificar_dependencias.py` y hook `SessionStart` que avisan si faltan `pymupdf` u
  `openpyxl`. El plugin no instala nada por su cuenta.
- Instrucciones explícitas al agente para reportar los fallos de escritura en vez de
  generar una salida alternativa.

### Cambiado
- La ruta del Excel destino es ahora un argumento **obligatorio** de
  `escribir_hallazgos.py`; el valor por defecto anterior apuntaba a un archivo inexistente
  dentro de `scripts/`.

## [0.1.0] - 2026-07-24
### Añadido
- Agente `revisor-hidrosanitario`: revisión técnica de planos hidrosanitarios (Colombia).
- Comando `/revisar-hidrosanitario` que dispara el flujo de revisión.
- Script `extraer_memorias.py` para extraer texto de PDFs largos (PyMuPDF).
- Script `escribir_hallazgos.py` para registrar hallazgos en Excel vía append (openpyxl).
- Plantilla `hallazgos_hidrosanitario.xlsx` con el esquema de salida.
- Documentación: README, LICENSE (MIT), guía de instalación como plugin/marketplace.
