# Revisor de Planos — Plugin para Claude Code

Plugin de [Claude Code](https://docs.claude.com/en/docs/claude-code) que incorpora un
**agente revisor técnico de planos de ingeniería**. El agente lee planos, identifica
hallazgos según reglas y normativa colombiana, y los registra en un formulario Excel
(un hallazgo por fila).

Arranca con **diseños hidrosanitarios** y está pensado para evolucionar a otras disciplinas
(estructural, eléctrico, gas, etc.) y a **revisión de coordinación inter-disciplinaria**.

## Capturas

Salida real del agente sobre un proyecto de prueba (Planta de Beneficio de Café,
Barichara – Santander): 12 hallazgos registrados en el formulario.

![Resumen por severidad](docs/img/resumen-severidad.png)

![Formulario de hallazgos diligenciado](docs/img/ejemplo-hallazgos.png)

## Qué incluye

| Componente | Descripción |
|---|---|
| `agents/revisor-hidrosanitario.md` | Agente revisor senior de planos hidrosanitarios (Colombia). |
| `commands/revisar-hidrosanitario.md` | Comando `/revisar-hidrosanitario` que dispara el flujo. |
| `scripts/extraer_memorias.py` | Extrae texto de PDFs largos (memorias de cálculo) con PyMuPDF. |
| `scripts/escribir_hallazgos.py` | Escribe los hallazgos en el Excel (append) con openpyxl; crea el archivo desde la plantilla si no existe. |
| `scripts/verificar_dependencias.py` | Avisa si faltan `pymupdf` u `openpyxl`. |
| `hooks/hooks.json` | Hook `SessionStart` que ejecuta la verificación de dependencias. |
| `templates/hallazgos_hidrosanitario.xlsx` | Plantilla del formulario de hallazgos. |

## Requisitos

- Claude Code.
- Python 3.9+ con las dependencias:
  ```bash
  pip install pymupdf openpyxl
  ```

Al iniciar cada sesión, el plugin verifica que ambas estén instaladas y, si falta alguna,
imprime el comando exacto de instalación para tu intérprete de Python. **El plugin nunca
instala nada por su cuenta**: la instalación siempre la decides tú. Puedes ejecutar la
verificación a mano:

```bash
python scripts/verificar_dependencias.py
```

## Instalación como plugin

Este repositorio es a la vez un **plugin** y un **marketplace** de un solo plugin.

```
# 1. Agrega este repo como marketplace
/plugin marketplace add camilaco-12/revisor-planos

# 2. Instala el plugin
/plugin install revisor-planos@revisores-ingenieria
```

O, para desarrollo local, agrega la carpeta como marketplace:

```
/plugin marketplace add /ruta/a/revisor-planos
```

## Uso

1. Ten a mano los planos (PDF/imagen). No necesitas crear el Excel: si la ruta destino no
   existe, se genera automáticamente a partir de la plantilla incluida.
2. Ejecuta el comando:
   ```
   /revisar-hidrosanitario  Revisa los planos en ./04_DISENO_HIDROSANITARIO y escribe en ./hallazgos.xlsx
   ```
   o simplemente pídele a Claude que use el agente `revisor-hidrosanitario`.
3. El agente te mostrará un **resumen por severidad** y, tras tu confirmación, escribirá los
   hallazgos en el Excel.

### Escritura manual de hallazgos

```bash
python scripts/escribir_hallazgos.py hallazgos.json ruta/al/formulario.xlsx
# opciones: --dry-run (no guarda)   --fecha AAAA-MM-DD
```

La ruta del Excel es obligatoria. Si el archivo **no existe**, el script copia la plantilla
a esa ruta (creando las carpetas necesarias) y escribe sobre la copia; si **ya existe**,
hace *append* continuando la numeración de IDs. El guardado es atómico: si falla a mitad de
camino, el archivo original queda intacto.

El JSON es una lista de objetos con las claves: `disciplina`, `hallazgo`, `ubicacion`,
`severidad`, `referencia_normativa`, `riesgo`, `justificacion_tecnica`, `accion_correctiva`,
`requiere_validacion`, `plano_referencia`.

Códigos de salida: `0` OK · `2` error de permisos · `3` error de entrada · `4` falta una
dependencia.

## Esquema del formulario de hallazgos

| Col | Campo | Quién lo llena |
|---|---|---|
| A | `ID` | Script (consecutivo) |
| B | `disciplina` | Agente |
| C | `hallazgo` | Agente |
| D | `ubicacion` | Agente |
| E | `severidad` | Agente (`Crítica`/`Alta`/`Media`/`Baja`) |
| F | `referencia_normativa` | Agente |
| G | `riesgo` | Agente |
| H | `justificacion_tecnica` | Agente |
| I | `accion_correctiva` | Agente |
| J | `requiere_validacion` | Agente (`TRUE`/`FALSE`) |
| K | `estado` | Seguimiento manual (por defecto "Pendiente") |
| L | `plano_referencia` | Agente |
| M | `fecha_deteccion` | Script (fecha del día) |

El encabezado está en la **fila 4** y los datos empiezan en la **fila 5**.

## Solución de problemas en Windows

Si la escritura al Excel falla, el script se detiene con código `2` y un mensaje que explica
la causa y los pasos a seguir — **no genera una salida alternativa ni escribe en otra ruta**.
El archivo destino queda intacto y ningún hallazgo se pierde a medias.

Las dos causas habituales:

1. **El Excel está abierto.** El script detecta el archivo de bloqueo `~$archivo.xlsx` que
   crea Excel y te lo dice directamente. Cierra el libro y reintenta.
2. **Acceso controlado a carpetas** (protección anti-ransomware de Windows Defender), típico
   si el Excel está en Escritorio, Documentos o Imágenes. Autoriza tu `python.exe` en
   *Seguridad de Windows → Protección contra virus y amenazas → Protección contra ransomware
   → Permitir una app a través del acceso controlado* (el mensaje de error incluye la ruta
   exacta de tu intérprete), o usa una ruta destino fuera de esas carpetas.

También puede fallar si la carpeta es de solo lectura o está en OneDrive sin sincronizar.

## Roadmap

- [x] Agente revisor hidrosanitario + escritura a Excel.
- [ ] Agentes para otras disciplinas (estructural, eléctrico, gas…).
- [ ] Revisión de coordinación inter-disciplinaria (interferencias entre disciplinas).

## Licencia

MIT — ver [LICENSE](LICENSE).
