# Changelog

Todos los cambios notables de este repositorio se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
y el versionado [SemVer](https://semver.org/lang/es/).

> A partir de la 0.4.0 este número versiona el **repositorio/marketplace**, no un plugin
> individual. Cada plugin lleva su propia versión en su `plugin.json`.

## [0.4.0] - 2026-08-03
### Añadido
- Plugin **`revisor-estructural`** (v0.1.0): agente revisor técnico de diseños estructurales
  en Colombia bajo la NSR-10. Revisa planos de cimentación, entrepisos, cubiertas y despieces
  de vigas, columnas y muros, los cruza con las memorias de cálculo y el estudio geotécnico
  cuando existen, y distingue explícitamente entre "se verificó y cumple", "se verificó y no
  cumple" y "no se pudo verificar con la documentación aportada".
- Comando `/revisar-estructural` que dispara el flujo de revisión estructural.
- Plantilla `hallazgos_estructural.xlsx` con el **mismo esquema v2** que la hidrosanitaria, a
  propósito: las dos tablas se pueden consolidar sin transformar nada para la coordinación
  inter-disciplinaria.
- `scripts/crear_plantilla.py` en el plugin estructural, para regenerar la plantilla desde cero.

### Cambiado
- **Estructura de monorepo-marketplace**: cada plugin vive ahora en `plugins/<nombre>/` con su
  propio `.claude-plugin/plugin.json`. En la raíz queda solo el catálogo
  `.claude-plugin/marketplace.json`, que pasa a listar dos entradas con `source` apuntando a
  cada subcarpeta. Los hooks y scripts ya resolvían sus rutas con `${CLAUDE_PLUGIN_ROOT}`, así
  que el movimiento no los afecta.
- El plugin hidrosanitario **conserva su nombre `revisor-planos`** para no romper las
  instalaciones existentes; sigue en su versión 0.3.0.
- README reescrito como documentación del marketplace de dos plugins.

### Corregido
- La tabla del esquema de hallazgos en el README seguía documentando el esquema v1
  (`requiere_validacion` en J, `estado` en K); ahora refleja el v2 que los scripts escriben
  desde la 0.3.0 (`nivel_confianza` en F, `estado` en M).

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
