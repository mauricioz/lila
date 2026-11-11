# Pantalla circular

[English](circular-display.md) · **Español**

**Tipo:** `config`

Cambia la ST7789 cuadrada de 240x240 por una pantalla redonda GC9A01 de
240x240. El firmware ya la admite, así que esta página es solo el delta
respecto a la [guía de construcción](../lila-build-guide.es.md), que sigue
siendo el documento canónico.

## Qué cambia

| Área | Por defecto | Esta variación |
| --- | --- | --- |
| Pantalla | ST7789 240x240, módulo de 7 pines | GC9A01 240x240, módulo redondo |
| Configuración | `LILA_DISPLAY=LCD_ST7789_240X240_7PIN` | `LILA_DISPLAY=LCD_GC9A01_240X240` |
| Controlador de la pantalla | rama ST7789 | la rama `esp_lcd_new_panel_gc9a01` ya presente en el código de la placa |
| Geometría | cristal cuadrado de 240x240 | cristal redondo de 240x240: las esquinas del framebuffer quedan fuera del área visible |
| Carcasa | marco por defecto | marco de pantalla redonda (geometría pendiente) |
| Placa, cableado, altavoz, botones, LED | — | sin cambios |

- La opción de pantalla ya está en Kconfig para esta placa
  (`LCD_GC9A01_240X240`, "GC9A01 240*240 Circle"), la geometría está en
  `config.h` y la rama del controlador en `wk-esp32s3-dev.cc`. Sin cambios de
  código y sin rama nueva.
- El cableado no cambia: se aplica tal cual la tabla de conexiones de la
  pantalla en la [guía](../lila-build-guide.es.md#montar-y-cablear). El
  firmware siempre controla el chip-select en el GPIO11, así que conecta ahí
  un cable de CS si tu módulo lo trae, y sigue el requisito del propio módulo
  si no lo trae (*sin verificar* para el módulo de cualquier vendedor).
- La pantalla es redonda y el framebuffer sigue midiendo 240x240: la
  interfaz dibujada en las esquinas queda fuera del cristal.

## Cambio en la lista de compra

Solo cambian dos filas de la [lista de
compra](../lila-build-guide.es.md#lista-de-compra); el resto de las piezas
son las de por defecto.

| Pieza | Especificación | Cant. | Cambio |
| --- | --- | --- | --- |
| Pantalla | módulo SPI redondo GC9A01 240x240 | 1 | reemplaza al módulo ST7789 de 7 pines |
| Archivos de la carcasa | set de pantalla redonda: `lila-panel-wk-esp32s3-dev-circular-display.stl` más las piezas de cuerpo y tapa que necesite | 1 set | reemplaza la geometría del marco por defecto — pendiente, ver el [índice de impresión 3D](../../STL/README.es.md) |

Los pines varían entre los módulos de cada vendedor: el módulo debe exponer
las señales SPI de la tabla de conexiones de la pantalla de la guía. *sin
verificar*: no se ha probado ningún módulo redondo concreto.

## Configurar

Añade una línea a `.env` (ver [Configurar la
compilación](../lila-build-guide.es.md#obtener-el-código-y-configurar-env)):

```env
LILA_DISPLAY=LCD_GC9A01_240X240
```

Desde la raíz del repositorio, confirma que la compilación elige la
pantalla:

```sh
python scripts/build_lila.py --dry-run
```

El comando impreso debe contener `CONFIG_LCD_GC9A01_240X240=y`. Cualquier
cambio en `.env` requiere una compilación nueva para que surta efecto. El
idioma, la palabra de activación, las credenciales y el resto de las recetas
no cambian en las [recetas de
configuración](../lila-build-guide.es.md#recetas-de-configuración).

## Imprimir y montar

- El set de pantalla redonda sigue la nomenclatura de variación: su marco es
  `lila-panel-wk-esp32s3-dev-circular-display.stl`. La geometría está
  pendiente, así que no se ha impreso ninguna carcasa de pantalla redonda
  (*sin verificar*).
- El montaje sigue el [orden con comprobaciones](../lila-build-guide.es.md#montar-y-cablear)
  de la guía: primero la prueba en el banco, las tablas de cableado sin
  cambios y después cerrar la carcasa alrededor del cristal redondo.

## Estado y verificación

| Comprobación | Estado |
| --- | --- |
| Opción de pantalla en Kconfig para esta placa | presente (`main/Kconfig.projbuild`) |
| Geometría y controlador en el código de la placa | presente (`config.h`, `wk-esp32s3-dev.cc`) |
| `.env` selecciona la pantalla a través de `build_lila.py` | verificado en el host con `--dry-run` |
| Flashear en una pantalla redonda real | sin verificar — necesita hardware |
| Geometría de la carcasa de pantalla redonda | pendiente (la ranura de nombres existe en `STL/README.es.md`) |

Vuelve al [selector](README.es.md).
