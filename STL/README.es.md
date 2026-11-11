# Archivos 3D de Lila

[English](README.md) · **Español**

Esta carpeta contiene los archivos `.stl` de la carcasa de Lila: las piezas
imprimibles que convierten la placa `wk-esp32s3-dev` y su pantalla ST7789 de
240x240 en un pequeño asistente de escritorio. La guía de construcción explica
todo el camino, desde flashear el firmware hasta montar la carcasa:

- [Construir, flashear, imprimir y montar](../docs/lila-build-guide.es.md)
- [Build, flash, print and assemble](../docs/lila-build-guide.md)

## Hardware de destino

| Elemento | Valor |
| --- | --- |
| Placa | `wk-esp32s3-dev` (ESP32-S3N16R8) |
| Pantalla | ST7789 240x240, módulo de 7 pines (`LCD_ST7789_240X240_7PIN`) |
| Audio | micrófono y amplificador integrados en la placa |
| Alimentación | USB-C |

La carcasa está diseñada solo para esa placa. Otra placa necesita sus propios
archivos y su propia variante, nunca una copia adaptada de estos.

## Convención de nombres

```
lila-<pieza>-<placa>.stl
```

| Pieza | Significado |
| --- | --- |
| `case` | cuerpo de la carcasa |
| `lid` | tapa frontal o superior |
| `panel` | marco alrededor de la pantalla |
| `button` | pulsador |
| `mount` | soporte de mesa, de pared o separador |

Ejemplo: `lila-case-wk-esp32s3-dev.stl`. Minúsculas, guiones, extensión `.stl`,
sin espacios y sin números de versión en el nombre.

## Archivos

| Archivo | Pieza | Estado |
| --- | --- | --- |
| `lila-case-wk-esp32s3-dev.stl` | cuerpo de la carcasa | pendiente |
| `lila-lid-wk-esp32s3-dev.stl` | tapa frontal | pendiente |
| `lila-panel-wk-esp32s3-dev.stl` | marco de la pantalla | pendiente |

Las filas marcadas como *pendiente* son los huecos que debe llenar la
geometría. El índice se publica antes que la geometría a propósito: la guía y
los ajustes de impresión son estables mientras la primera impresión todavía se
está ajustando.

## Ajustes de impresión

Punto de partida para una impresora FDM de 200x200x200 mm con boquilla de
0,4 mm:

| Ajuste | Valor |
| --- | --- |
| Material | PLA o PETG (PLA es más fácil de ajustar, PETG aguanta mejor el calor) |
| Altura de capa | 0,2 mm |
| Paredes | 3 |
| Relleno | 20 % (30 % para la tapa) |
| Soportes | solo donde el archivo los pida; revisa el modelo en el laminador |
| Boquilla | 0,4 mm |
| Tolerancia | holgura de 0,2–0,3 mm para los encajes a presión |

Imprime por separado el cuerpo de la carcasa y el marco, para poder colocar la
pantalla antes de cerrar la tapa. Conserva la primera impresión como prueba: un
encaje demasiado apretado se corrige en el laminador, un diseño demasiado
apretado necesita un archivo nuevo.

## Añadir un archivo

1. Nombra el archivo con la convención de arriba y publícalo en esta carpeta.
2. Añade una fila a la tabla de este archivo **y** a la de
   [`README.md`](README.md).
3. Anota los ajustes de impresión que funcionaron y los soportes que necesite
   la pieza.

La carpeta está versionada con git, así que los archivos viajan con el
repositorio. Mantén cada archivo pequeño: un STL ASCII de una pieza sencilla
pesa bastante menos de un megabyte, y un STL binario es aún más pequeño.

## Estado

La geometría todavía no está publicada: la carcasa se está imprimiendo y
ajustando, y los archivos llegan aquí a medida que se terminan. Todo lo que en
este repositorio describe la carcasa —la guía, el orden de cableado y los
ajustes de impresión— está escrito para la placa `wk-esp32s3-dev` y el panel
ST7789 de 240x240.
