# Lila

[English](README.md) · **Español**

**Lila** es un fork personal del [XiaoZhi AI Chatbot](https://github.com/78/xiaozhi-esp32),
el asistente de voz de código abierto creado por [78](https://github.com/78) y la
comunidad de XiaoZhi. Mi hija **Sophie** eligió el nombre, así que este pequeño
asistente se llama Lila a partir de ahora.

El mérito de todo lo que hace funcionar este firmware es del proyecto original:
el pipeline de audio, los motores de palabras de activación ESP-SR, las placas,
los protocolos WebSocket y MQTT/UDP, el servidor MCP, la documentación y años de
ingeniería cuidadosa. Gracias, 78, y gracias a todas las personas que han
contribuido allí. Lila solo añade unos pocos toques personales por encima, y
hereda la licencia MIT del proyecto original.

Este README documenta **solo Lila**. La documentación del proyecto original, la
lista de placas, sus traducciones y el soporte de la comunidad viven en
[78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32); consulta
[Proyecto upstream](#proyecto-upstream) al final de esta página.

## Lo que Lila aporta frente al upstream

Cada cambio es aditivo: sin un archivo `.env` y sin credenciales de API, una
compilación de Lila se comporta exactamente igual que el upstream.

- **Compilaciones configuradas desde `.env`** — `scripts/build_lila.py` lee
  placa, variante, idioma, palabra de activación, panel de pantalla, credenciales
  de API, opciones extra de sdkconfig y el zip desde `.env` (ver `.env.example`)
  y se los pasa a `scripts/build.py`. `--dry-run` imprime el comando exacto.
- **Palabras de activación MultiNet personalizadas desde la CLI** —
  `scripts/build.py --wake-word custom:<palabra>` convierte cualquier palabra en
  un comando MultiNet, que `scripts/build_default_assets.py` empaqueta en la
  partición de assets. No hace falta tocar el código ni el sdkconfig, y el
  perfil de Lila se activa con `custom:lila`.
- **Overrides de sdkconfig en bruto** — una opción repetible
  `--sdkconfig KEY=VALUE` que se aplica después de todas las opciones derivadas,
  que es la forma de inyectar claves de API y elegir el panel LCD sin tocar el
  árbol de fuentes.
- **Herramienta MCP `web.search`** — búsqueda web respaldada por Tavily, que
  solo se registra cuando `XIAOZHI_TAVILY_API_KEY` no está vacía. Devuelve la
  respuesta de la búsqueda más los resultados numerados y permite una sola
  búsqueda en curso.
- **Herramienta MCP `self.telegram.send`** — envía un mensaje de Telegram y
  solo se registra cuando están definidos `XIAOZHI_TELEGRAM_BOT_TOKEN` y
  `XIAOZHI_TELEGRAM_CHAT_ID`. El envío se hace en una tarea de un solo uso para
  que el bucle principal de eventos nunca se bloquee con la red.
- **Perfil de hardware de Lila** — español (`es-ES`) por defecto, la palabra de
  activación `lila` y un panel ST7789 de 240x240 (`LCD_ST7789_240X240_7PIN`, o
  `LCD_ST7789_240X240` cuando el módulo tiene línea CS), todo seleccionable
  desde `.env` y compatible con el cableado ST7789 de 7 pines que usa esta
  compilación en la placa `wk-esp32s3-dev`.
- **Cambios de placa documentados** —
  `main/boards/wk-esp32s3-dev/README.md` documenta el wrapper, las dos variantes
  de pantalla y las dos herramientas opcionales.
- **Un flujo de desarrollo** — especificaciones, estándares, skills para agentes,
  comprobaciones de CI en el host y una política de solo pull requests para
  `main` (ver [Flujo de desarrollo](#flujo-de-desarrollo)).

## Inicio rápido

Primero carga tu entorno de ESP-IDF `release/v6.1` (consulta la
[guía de instalación de upstream](https://github.com/78/xiaozhi-esp32#development-environment)),
y después:

```bash
cp .env.example .env                      # edita idioma, palabra, panel y claves
python scripts/build_lila.py --dry-run    # imprime el comando
python scripts/build_lila.py              # compila
```

Las dos herramientas también se pueden activar en cualquier placa desde
`idf.py menuconfig` (`Xiaozhi Assistant` → `Tavily API key`, `Telegram bot
token`, `Telegram chat ID`).

## Guía de construcción y carcasa impresa en 3D

Una guía paso a paso lleva a una máquina nueva desde una carpeta vacía hasta
una Lila funcionando: instalar ESP-IDF en Windows, Linux o macOS, configurar
`.env`, compilar, flashear, imprimir la carcasa y montarla.

| Guía | Inglés | Español |
| --- | --- | --- |
| Compilar, flashear, imprimir y montar | [`docs/lila-build-guide.md`](docs/lila-build-guide.md) | [`docs/lila-build-guide.es.md`](docs/lila-build-guide.es.md) |
| Archivos para impresión 3D (`.stl`) | [`STL/README.md`](STL/README.md) | [`STL/README.es.md`](STL/README.es.md) |

Los archivos `.stl` viven en [`STL/`](STL/). La carcasa está pensada para la
placa `wk-esp32s3-dev` con el panel ST7789 de 240x240; el índice nombra cada
archivo, los ajustes de impresión y lo que queda pendiente.

## Flujo de desarrollo

Lila se desarrolla con el proceso que él mismo entrega: una especificación, una
rama, CI y un pull request. **`main` está protegido y nunca recibe un push
directo** — cada cambio, incluidas las ediciones de proceso y documentación,
llega mediante un pull request.

| Paso | Dónde |
| --- | --- |
| Vista general del proceso y mapa | [`process/README.md`](process/README.md) |
| Pipeline completo y puertas de calidad | [`process/WORKFLOW.md`](process/WORKFLOW.md) |
| Reglas por área de cambio | [`process/STANDARDS.md`](process/STANDARDS.md), [`process/standards/`](process/standards/) |
| Especificaciones de features (`FEAT_XXX`) | [`process/specs/`](process/specs/) |
| Features ya entregadas y previstas | [`process/ROADMAP.md`](process/ROADMAP.md) |
| OpenSpec, CodeGraph y RTK | [`process/TOOLING.md`](process/TOOLING.md) |
| Configuración de protección de rama | [`.github/BRANCH_PROTECTION.md`](.github/BRANCH_PROTECTION.md) |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) |

El desarrollo dirigido por especificaciones usa [OpenSpec](https://github.com/Fission-AI/OpenSpec)
para los cambios que alteran un contrato, más un documento `FEAT_XXX` por
feature. [CodeGraph](https://github.com/colbymchenry/codegraph) indexa el
firmware para que un agente encuentre símbolos y rutas de llamada sin leer
archivos enteros, y [RTK](https://github.com/rtk-ai/rtk) comprime la salida de
los comandos para mantener pequeño el contexto del agente. Los tres son
opcionales para compilar el firmware.

Las skills para OpenCode y Claude Code están en el propio repositorio
(`.opencode/skills/` es el origen y `.claude/skills/` es la copia generada) para
que el pipeline, la selección de estándares y las puertas de revisión se
comporten igual en las dos herramientas.

```bash
# Las comprobaciones que CI ejecuta en cada pull request
python -m compileall -q scripts
python scripts/sync_skills.py --check
python scripts/check_workflow.py
python -m unittest discover -s scripts/tests -v

# Previsualiza la compilación configurada sin arrancar ESP-IDF
python scripts/build_lila.py --dry-run

# Estilo de C/C++ en las líneas que cambia el commit
python scripts/check_format.py --base origin/main
```

CI está dividido en dos: `ci.yml` ejecuta las comprobaciones del host y
`clang-format` en cada pull request, mientras que `firmware-build.yml` es una
compilación manual y reproducible de Lila en el contenedor de ESP-IDF 6.1. Un
pull request indica qué comprobaciones se ejecutaron y qué sigue pendiente de
validar en un dispositivo físico.

## Proyecto upstream

Lila se apoya en [XiaoZhi AI Chatbot](https://github.com/78/xiaozhi-esp32) de
[78](https://github.com/78) y de la comunidad de XiaoZhi, y conserva su licencia
MIT. Todo lo que no sea una añadido de Lila vive en el upstream:

| Buscas | Ve a |
| --- | --- |
| Esta página en español | [`README.es.md`](README.es.md) |
| Vista general del proyecto, features y traducciones del upstream | [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) |
| Placas soportadas y matriz de releases | [lista de placas del upstream](https://github.com/78/xiaozhi-esp32#supports-138-board-directories-and-171-release-variants-partial-list) |
| Releases del firmware | [releases del upstream](https://github.com/78/xiaozhi-esp32/releases) |
| Instalación de ESP-IDF y guía de flasheo | [README del upstream](https://github.com/78/xiaozhi-esp32#development-environment) |
| Documentación de placas y firmware | [`docs/`](docs/) en este repositorio, docs del upstream |
| Features propias de Lila | [Lo que Lila aporta frente al upstream](#lo-que-lila-aporta-frente-al-upstream) |
| Planes de release de Lila | [`process/ROADMAP.md`](process/ROADMAP.md) |

Los cambios del upstream no se incorporan automáticamente; Lila los sigue a
mano y mantiene su propia línea de releases.
