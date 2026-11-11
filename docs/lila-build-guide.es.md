# Construir, flashear, imprimir y montar Lila

[English](lila-build-guide.md) · **Español**

Esta guía lleva a una máquina nueva desde una carpeta vacía hasta una Lila
funcionando: instalar el toolchain, configurar la compilación, compilar el
firmware, flashearlo, imprimir la carcasa y montarla. Está escrita para la
placa `wk-esp32s3-dev` con la pantalla ST7789 de 240x240, que es el perfil de
Lila.

La guía se escribió sobre el repositorio, no sobre un dispositivo: los comandos
son los de los scripts de este repositorio, pero la impresión y el flasheo no
los ejecutó quien escribió estas líneas. Todo lo marcado como *sin verificar*
necesita una placa real.

| Paso | Resultado |
| --- | --- |
| [Instalar ESP-IDF](#instalar-esp-idf) | el toolchain que compila el firmware |
| [Configurar la compilación](#obtener-el-código-y-configurar-env) | un `.env` que describe tu Lila |
| [Compilar](#compilar-el-firmware) | `build/merged-binary.bin` |
| [Flashear](#flashear-el-dispositivo) | Lila funcionando en la placa |
| [Imprimir](#imprimir-la-carcasa) | las piezas de la carcasa |
| [Montar](#montar-y-cablear) | un asistente terminado sobre la mesa |

## Qué necesitas

| Elemento | Detalle |
| --- | --- |
| Placa | `wk-esp32s3-dev` (ESP32-S3N16R8) |
| Pantalla | ST7789 240x240, módulo de 7 pines (GND, VCC, SCL, SDA, RES, DC, BLK) |
| Altavoz | 4 Ω, conectado a la salida I2S del amplificador de la placa |
| Cable | USB-C, para alimentación y para flashear |
| Ordenador | Windows, Linux o macOS con unos 20 GB de disco libre |
| Toolchain | ESP-IDF `release/v6.1` (mínimo soportado: v6.0.1) |
| Impresora | FDM con boquilla de 0,4 mm, para la carcasa (opcional) |

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

El dispositivo se conecta al Wi-Fi configurado, muestra la cara en la pantalla
y escucha la palabra de activación. Qué buscar en el log:

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

Orden de montaje:

1. fija la placa en el cuerpo de la carcasa;
2. conecta la pantalla y el altavoz;
3. coloca la pantalla en su marco;
4. cierra la tapa y atornilla;
5. conecta el USB-C y arranca el dispositivo.

El mapa de pines de la placa `wk-esp32s3-dev`, leído de
`main/boards/wk-esp32s3-dev/config.h`:

| Función | Pin |
| --- | --- |
| Retroiluminación | GPIO10 |
| MOSI de la pantalla (SDA) | GPIO8 |
| CLK de la pantalla (SCL) | GPIO9 |
| DC de la pantalla | GPIO12 |
| Reset de la pantalla | GPIO13 |
| WS del micrófono | GPIO40 |
| SCK del micrófono | GPIO42 |
| Datos del micrófono | GPIO41 |
| Datos del altavoz (DOUT) | GPIO21 |
| BCLK del altavoz | GPIO47 |
| LRCK del altavoz | GPIO48 |
| Botón de arranque | GPIO0 |
| Volumen arriba / abajo | GPIO38 / GPIO39 |
| LED de estado | GPIO14 |

El módulo ST7789 de 7 pines no tiene línea CS, y por eso el valor por defecto
`LILA_DISPLAY` es `LCD_ST7789_240X240_7PIN` (modo SPI 3). Si tu módulo tiene
hilo CS, compila con `LILA_DISPLAY=LCD_ST7789_240X240` (modo SPI 0).

*Sin verificar*: la tabla anterior viene de la configuración de la placa, pero
el cableado no se comprobó en una placa física con esta carcasa.

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
| La pantalla muestra caracteres raros | modo SPI o cableado que no cuadran | los módulos de 7 pines usan el modo 3; los que tienen CS, el modo 0 |
| No hay sonido | altavoz sin conectar, o pines I2S equivocados | revisa los pines del altavoz en la tabla de arriba y el amplificador |
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
