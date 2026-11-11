# Construir, flashear, imprimir y montar Lila

[English](lila-build-guide.md) · **Español**

Esta guía lleva a una máquina nueva desde una carpeta vacía hasta una Lila
funcionando: la lista de compra, el toolchain, una compilación configurada,
el firmware en la placa, la carcasa impresa y el asistente cableado y
montado. Está escrita para la placa `wk-esp32s3-dev` con la pantalla ST7789
de 240x240, que es el perfil de Lila.

La guía se escribió sobre el repositorio, no sobre un dispositivo: los comandos
son los de los scripts de este repositorio, pero la impresión y el flasheo no
los ejecutó quien escribió estas líneas. Todo lo marcado como *sin verificar*
necesita una placa real.

| Paso | Resultado |
| --- | --- |
| [Lista de compra](#lista-de-compra) | cada parte que comprar, con especificación y cantidad |
| [Instalar ESP-IDF](#instalar-esp-idf) | el toolchain que compila el firmware |
| [Configurar la compilación](#obtener-el-código-y-configurar-env) | un `.env` que describe tu Lila |
| [Recetas de configuración](#recetas-de-configuración) | bloques `.env` listos para copiar |
| [Compilar](#compilar-el-firmware) | `build/merged-binary.bin` |
| [Flashear](#flashear-el-dispositivo) | Lila funcionando en la placa |
| [Primer arranque](#primer-arranque) | lo que debe mostrar el log |
| [Imprimir](#imprimir-la-carcasa) | las piezas de la carcasa |
| [Montar](#montar-y-cablear) | las tablas de cableado y los pasos con comprobación |
| [Comprobar](#comprobar-que-lila-funciona) | prueba de que cada subsistema funciona |
| [Problemas frecuentes](#problemas-frecuentes) | soluciones a los fallos habituales |
| [Y ahora qué](#y-ahora-qué) | el resto de la documentación |

## Lista de compra

Todo lo que Lila necesita. Los vendedores y los precios varían según la
región; lo que importa es la especificación. La placa es la única parte para
la que está escrito el firmware.

### Hardware

| Parte | Especificación | Cant. | Dónde va |
| --- | --- | --- | --- |
| Placa de desarrollo | `wk-esp32s3-dev` (ESP32-S3N16R8: 16 MB de flash, 8 MB de PSRAM) | 1 | el cerebro; el README de la placa enlaza la tienda |
| Pantalla | ST7789 240x240, módulo SPI de 7 pines: GND, VCC, SCL, SDA, RES, DC, BLK (sin hilo CS) | 1 | frente de la carcasa |
| Altavoz | 4 Ω, altavoz pequeño para carcasa | 1 | dentro de la carcasa, en la salida de altavoz de la placa |
| Cable USB-C | cable de **datos**, no de solo carga | 1 | alimentación y flasheo |
| Filamento | PLA o PETG | 1 rollo — una carcasa usa una fracción mínima | la carcasa ([ajustes de impresión](../STL/README.es.md)) |
| Archivos de la carcasa | las piezas `.stl` de [`STL/`](../STL/) | 1 juego | los imprimes tú o un servicio de impresión |

Un módulo con línea CS también funciona: cambia una línea de configuración
([la receta](#pantalla-con-línea-cs)), no la lista de partes.

### Herramientas

| Elemento | Detalle |
| --- | --- |
| Ordenador | Windows, Linux o macOS con unos 20 GB de disco libre |
| Toolchain | ESP-IDF `release/v6.1` (mínimo soportado: v6.0.1) — se instala en el siguiente paso |
| Impresora | FDM con boquilla de 0,4 mm, 200x200x200 mm o mayor — opcional, cualquier servicio de impresión puede imprimir los archivos `.stl` |
| Herramientas de mano | pelacables o un soldador, según cómo termine sus pines el módulo de la pantalla |

La documentación del upstream describe las placas y el montaje general en
[78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32); esta guía solo
cubre el camino de Lila.

## Instalar ESP-IDF

Lila se compila con ESP-IDF `release/v6.1`. La documentación oficial de
Espressif tiene las instrucciones completas — instálala desde ahí, no la copies
aquí:

| Sistema | Página oficial | Versión corta |
| --- | --- | --- |
| Windows | [ESP-IDF Tools Installer](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/windows-installer.html) | ejecuta el instalador, elige ESP32-S3 y abre el acceso directo **ESP-IDF PowerShell** que crea |
| Linux | [instalación en Linux](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/linux.html) | instala las dependencias y ejecuta el script de abajo |
| macOS | [instalación en macOS](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/macos.html) | instala las dependencias y ejecuta el script de abajo |

En Linux y macOS:

```bash
git clone -b release/v6.1 --recursive https://github.com/espressif/esp-idf.git ~/esp-idf
cd ~/esp-idf
./install.sh esp32s3
```

Cada terminal nueva necesita el entorno cargado:

```bash
. ~/esp-idf/export.sh          # Linux y macOS
```

```powershell
C:\Espressif\frameworks\esp-idf-v6.1\export.ps1   # Windows PowerShell
```

Compruébalo antes de seguir:

```bash
idf.py --version
```

La extensión de VS Code es opcional; todos los comandos de esta guía funcionan
en una terminal normal. Consulta la
[página oficial](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/vscode-config.html).

## Obtener el código y configurar `.env`

```bash
git clone https://github.com/mauricioz/lila.git
cd lila
cp .env.example .env
```

```powershell
git clone https://github.com/mauricioz/lila.git
cd lila
Copy-Item .env.example .env
```

Abre `.env` en cualquier editor de texto. Todos los valores son opcionales; los
valores por defecto ya describen una Lila en español, con la palabra de
activación `lila` y una pantalla ST7789 de 7 pines:

| Clave | Por defecto | Cuándo cambiarla |
| --- | --- | --- |
| `LILA_BOARD` | `wk-esp32s3-dev` | si compilas otra placa |
| `LILA_NAME` | `wk-esp32s3-dev` | si compilas otra variante; también es la identidad de la placa en las OTA |
| `LILA_LANGUAGE` | `es-ES` | si quieres otro idioma de interfaz |
| `LILA_WAKE_WORD` | `custom:lila` | si quieres otra palabra, un modelo WakeNet o `disabled` |
| `LILA_DISPLAY` | `LCD_ST7789_240X240_7PIN` | si tu módulo tiene línea CS: usa `LCD_ST7789_240X240` |
| `LILA_TAVILY_API_KEY` | *(vacío)* | si quieres la herramienta `web.search`; pide una clave en [tavily.com](https://tavily.com) |
| `LILA_TELEGRAM_BOT_TOKEN` | *(vacío)* | si quieres la herramienta `self.telegram.send`; crea el bot con [@BotFather](https://t.me/BotFather) |
| `LILA_TELEGRAM_CHAT_ID` | *(vacío)* | si usas la herramienta de Telegram; lee el id en `https://api.telegram.org/bot<token>/getUpdates` |
| `LILA_SDKCONFIG` | *(vacío)* | si necesitas un `CONFIG_KEY=VALUE` en bruto |
| `LILA_ZIP` | `0` | ponle `1` para además empaquetar `releases/*.zip` |

`.env` contiene tus credenciales, así que está en el `.gitignore`: nunca lo
copies en una incidencia, un pull request o una captura de pantalla. Las claves
se dejan vacías en `.env.example` a propósito.

La palabra de activación `custom:lila` es un comando MultiNet personalizado.
Solo funciona en los targets ESP32-S3, S31 y P4, y hace que la compilación
incluya en la partición de assets el modelo MultiNet 7 cuantizado en inglés.

## Recetas de configuración

La tabla de arriba explica cada clave por separado. Estos son contenidos
completos de `.env` para los ajustes que aparecen más a menudo: elige el más
parecido, cópialo sobre tu `.env`, ajústalo y recompila — todo cambio en
`.env` necesita una compilación nueva antes de llegar al dispositivo.

### Mínima — sin credenciales

```bash
# Lila de fábrica: interfaz en español, palabra de activación "lila", ST7789 de 7 pines, sin herramientas opcionales.
LILA_BOARD=wk-esp32s3-dev
LILA_NAME=wk-esp32s3-dev
LILA_LANGUAGE=es-ES
LILA_WAKE_WORD=custom:lila
LILA_DISPLAY=LCD_ST7789_240X240_7PIN
```

### Familiar — Telegram y búsqueda web

```bash
# Todo lo de la Mínima, más las dos herramientas opcionales:
LILA_TAVILY_API_KEY=               # clave de https://tavily.com
LILA_TELEGRAM_BOT_TOKEN=           # token de @BotFather
LILA_TELEGRAM_CHAT_ID=             # tu chat id
```

Déjame una clave vacía y la herramienta correspondiente simplemente no existe
en la compilación — ese es el comportamiento deseado, no un error. Rellena los
valores en tu propio `.env`; nunca los subas al repositorio.

### Otra palabra de activación

```bash
# otro comando personalizado (MultiNet; solo ESP32-S3, S31 y P4):
LILA_WAKE_WORD=custom:robot

# o un modelo WakeNet, o desactiva la detección:
# LILA_WAKE_WORD=hiesp
# LILA_WAKE_WORD=disabled
```

### Pantalla con línea CS

```bash
LILA_DISPLAY=LCD_ST7789_240X240    # modo SPI 0 en lugar del modo 3
```

### Otro idioma de interfaz

```bash
LILA_LANGUAGE=en-US                 # el repositorio incluye 41 locales
```

La lista autoritativa no necesita ESP-IDF:

```bash
python scripts/build.py --list-languages
```

### Avanzado — overrides en bruto y empaquetado

```bash
LILA_SDKCONFIG=CONFIG_SOME_VALUE=1  # override en bruto, se aplica después de todas las opciones derivadas
LILA_ZIP=1                          # además empaqueta releases/<version>_<name>.zip
```

## Compilar el firmware

Primero previsualiza el comando: imprime exactamente lo que se va a ejecutar,
sin tocar el árbol:

```bash
python scripts/build_lila.py --dry-run
```

Y después compila:

```bash
python scripts/build_lila.py
```

El wrapper traduce `.env` a opciones de `scripts/build.py`, y la compilación:

1. selecciona el target (`esp32s3`) y escribe `sdkconfig`;
2. compila la partición de assets, incluidos los modelos de palabra de
   activación;
3. compila el firmware con `idf.py build`;
4. une los binarios en `build/merged-binary.bin`.

La primera compilación descarga las dependencias y compila todo el firmware:
tarda bastante. Las siguientes reutilizan la caché y son mucho más rápidas. Si
cambias de placa o de variante, el script reconfigura el árbol.

## Flashear el dispositivo

Localiza el puerto serie y flashea:

```bash
idf.py -p COM5 flash monitor
```

```bash
idf.py -p /dev/ttyUSB0 flash monitor        # Linux
idf.py -p /dev/cu.usbmodem101 flash monitor  # macOS
```

`COM5` es un ejemplo: usa el puerto que aparece al conectar la placa. El
monitor muestra el log y se sale con `Ctrl + ]`.

Si el puerto no aparece:

- desconecta y vuelve a conectar la placa y busca un nuevo dispositivo
  `USB JTAG/serial debug unit`;
- algunas placas solo aparecen tras un segundo reinicio: mantén pulsado
  **BOOT**, pulsa y suelta **RESET**, y suelta **BOOT**;
- en macOS usa `/dev/cu.usbmodem*` (la variante `cu.`), no `/dev/tty.*`.

Para empezar desde un flash limpio:

```bash
idf.py -p COM5 erase-flash flash monitor
```

## Primer arranque

Ejecuta esto justo después de flashear, con todas las piezas todavía sobre la
mesa: es la primera comprobación de toda la obra. El dispositivo se conecta al
Wi-Fi configurado, muestra la cara en la pantalla y escucha la palabra de
activación. Qué buscar en el log:

- el nombre de la placa y la conexión al Wi-Fi;
- el modelo de palabra de activación en uso (`Lila`, con el prefijo `custom:`);
- el arranque de la pantalla: se enciende la retroiluminación y aparece la cara;
- ninguna URL en el log: los helpers HTTP de Lila imprimen una etiqueta del
  proveedor, como `Telegram API` o `Tavily API`, nunca la URL de la petición,
  así que el token del bot nunca llega al log;
- `Telegram message sent` después de pedirle a Lila que te mande un mensaje.

Que las herramientas no estén compiladas es normal: solo se registran cuando
sus credenciales estaban en `.env` en el momento de compilar.

## Imprimir la carcasa

Los archivos `.stl` viven en [`STL/`](../STL/) y están indexados en
[`STL/README.es.md`](../STL/README.es.md) (inglés:
[`STL/README.md`](../STL/README.md)). El índice nombra cada archivo, la
convención de nombres y los ajustes de impresión.

Punto de partida para el laminador:

| Ajuste | Valor |
| --- | --- |
| Material | PLA o PETG |
| Altura de capa | 0,2 mm |
| Paredes | 3 |
| Relleno | 20 % (30 % para la tapa) |
| Boquilla | 0,4 mm |
| Tolerancia | holgura de 0,2–0,3 mm para los encajes a presión |

Imprime por separado el cuerpo de la carcasa y el marco de la pantalla, para
poder colocar la pantalla antes de cerrar la tapa. Conserva la primera
impresión como prueba.

*Sin verificar*: la geometría de `STL/` todavía se está ajustando, así que
trata la primera impresión como un prototipo y corrige en el laminador antes de
pedir un archivo nuevo.

## Montar y cablear

La `wk-esp32s3-dev` lleva el micrófono, el amplificador, los botones y el LED
en la propia placa. Tú cableas exactamente dos cosas — la pantalla y el
altavoz — y cada valor de pin de abajo está leído de
`main/boards/wk-esp32s3-dev/config.h`.

*Sin verificar*: las tablas vienen de la configuración de la placa; el
cableado no se comprobó en una placa física con esta carcasa.

### Cableado de la pantalla

El módulo ST7789 de 7 pines:

| Pin del módulo | Pin de la placa | Señal |
| --- | --- | --- |
| BLK | GPIO10 | retroiluminación |
| SDA (MOSI) | GPIO8 | datos SPI |
| SCL (CLK) | GPIO9 | reloj SPI |
| DC | GPIO12 | datos / comando |
| RES | GPIO13 | reset |
| VCC | 3.3 V | alimentación |
| GND | GND | masa |

El módulo no tiene hilo CS; el firmware igualmente maneja una línea CS en
GPIO11, así que en este módulo ese pin queda sin conectar. Un módulo que saca
un hilo CS lo conecta a GPIO11 y compila con `LILA_DISPLAY=LCD_ST7789_240X240`
— el modo SPI (3 frente a 0) es la única diferencia entre los dos símbolos.

### Cableado del altavoz

Dos hilos desde el altavoz hasta la salida de altavoz de la placa: el
amplificador está en la placa. El enlace I2S entre el chip y ese amplificador
está fijo en la placa y no necesita cableado — se lista solo como referencia:

| Referencia | Pin |
| --- | --- |
| Datos del altavoz (DOUT) | GPIO21 |
| BCLK del altavoz | GPIO47 |
| LRCK del altavoz | GPIO48 |

### Ya está en la placa

| Función | Pin | Nota |
| --- | --- | --- |
| WS del micrófono | GPIO40 | micrófono integrado |
| SCK del micrófono | GPIO42 | micrófono integrado |
| Datos del micrófono | GPIO41 | micrófono integrado |
| Botón de arranque | GPIO0 | también entra en el bootloader |
| Volumen arriba / abajo | GPIO38 / GPIO39 | |
| LED de estado | GPIO14 | |

### Pasos de montaje

Cada paso termina en una comprobación: no sigas hasta que pase. Depurar sobre
la mesa es mucho más barato que depurar a través de una carcasa cerrada.

1. **Flashea y prueba sobre la mesa primero** —
   [Flashear el dispositivo](#flashear-el-dispositivo) con todas las piezas
   sobre la mesa.
   - Comprobación: el log de arranque llega al final sin reinicios, la
     retroiluminación se enciende y aparece la cara en la pantalla.
2. **Fija la placa en el cuerpo de la carcasa.**
   - Comprobación: el puerto USB-C queda alineado con la abertura y el cable
     entra sin fuerza.
3. **Conecta la pantalla** con la tabla de arriba.
   - Comprobación: reinicia la placa; la retroiluminación se enciende en
     cuanto arranca.
4. **Conecta el altavoz** a la salida de altavoz de la placa.
   - Comprobación: pídele cualquier cosa a Lila; se oye la respuesta a
     volumen normal, sin crepitar.
5. **Coloca la pantalla en su marco** y enruta los hilos sin apretar ninguno.
   - Comprobación: la cara queda centrada en la abertura y ningún hilo queda
     atrapado entre el marco y el cuerpo.
6. **Cierra la tapa.**
   - Comprobación: la junta queda pareja por todos lados, el marco no se movió
     y nada suelta ruido.
7. **Ejecuta la comprobación completa** —
   [Comprobar que Lila funciona](#comprobar-que-lila-funciona) de principio a
   fin sobre el asistente terminado.

## Comprobar que Lila funciona

| Comprobación | Cómo |
| --- | --- |
| Arranca | el monitor muestra el log de arranque y no hay reinicios |
| Ve la pantalla | aparece la cara y la retroiluminación está encendida |
| Te oye | la palabra de activación ilumina la pantalla |
| Habla | el altavoz reproduce la respuesta |
| Busca | pídele el tiempo; `web.search` responde si Tavily está configurado |
| Te escribe | pídele que mande un mensaje de Telegram |

`web.search` y `self.telegram.send` solo existen si sus credenciales estaban
en `.env` **antes** de compilar. Cambiar `.env` más tarde exige compilar de
nuevo.

## Problemas frecuentes

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| `idf.py: command not found` | el entorno no está cargado | ejecuta `. ~/esp-idf/export.sh` (o el script de PowerShell) en esa terminal |
| `A custom wake word requires ESP32-S3/S31/P4` | la palabra `custom:<palabra>` en otro chip | usa un modelo WakeNet o `disabled` en los demás targets |
| La pantalla se queda negra | símbolo de panel equivocado o modo SPI equivocado | revisa `LILA_DISPLAY` según tu módulo: 7 pines es `LCD_ST7789_240X240_7PIN` |
| La pantalla se enciende pero no muestra nada | la pantalla está cableada a pines equivocados | revisa BLK, SDA, SCL, DC y RES según la tabla de la pantalla de arriba |
| La pantalla muestra caracteres raros | modo SPI o cableado que no cuadran | los módulos de 7 pines usan el modo 3; los que tienen CS, el modo 0 |
| No hay sonido | altavoz sin conectar, o salida equivocada | revisa el cableado del altavoz de arriba y que los dos hilos lleguen a la salida de altavoz de la placa |
| El puerto desaparece al flashear | la placa reinicia en el bootloader | pulsa **BOOT**, toca **RESET**, suelta **BOOT** y flashea otra vez |
| La primera compilación tarda muchísimo | se están descargando las dependencias | deja que termine; las siguientes usan la caché |
| `web.search` no existe | no había clave de Tavily al compilar | pon `LILA_TAVILY_API_KEY` en `.env` y recompila |
| La herramienta de Telegram no existe | faltaban el token o el chat id al compilar | pon las dos claves en `.env` y recompila |
| Aparece una URL en el log | no es una compilación de Lila | Lila registra `Telegram API` / `Tavily API`; actualiza el firmware |

## Y ahora qué

| Buscas | Ve a |
| --- | --- |
| Esta guía en inglés | [`lila-build-guide.md`](lila-build-guide.md) |
| La portada de Lila | [`README.es.md`](../README.es.md) (inglés: [`README.md`](../README.md)) |
| El índice de impresión 3D | [`STL/README.es.md`](../STL/README.es.md) |
| Documentación de la placa | [`main/boards/wk-esp32s3-dev/README.md`](../main/boards/wk-esp32s3-dev/README.md) |
| Lista de placas, releases y montaje general | [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) |
| Documentación de ESP-IDF | [docs de Espressif](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/index.html) |
