# Altavoz diferente

[English](speaker.md) · **Español**

**Tipo:** `parts`

Elige un altavoz diferente para Lila: otra impedencia, más potencia o un
driver que encaje mejor en tu carcasa. Es una decisión de compra: el
firmware, los pines y la configuración se quedan exactamente como los
describe la [guía de construcción](../lila-build-guide.es.md).

## Qué cambia

| Área | Por defecto | Esta variación |
| --- | --- | --- |
| Altavoz | 4 Ω, altavoz pequeño para carcasa | tu elección de impedencia, potencia y tamaño |
| Configuración | — | sin cambios: no existe ninguna clave de altavoz en `.env.example` ni en Kconfig |
| Firmware | — | sin cambios |
| Carcasa | set por defecto dimensionado para el altavoz de referencia | set por defecto, salvo que el driver no encaje (ver abajo) |
| Pantalla, placa, cableado, botones, LED | — | sin cambios |

- La ruta de audio está fijada en hardware: I2S simplex al amplificador de
  la placa, datos del altavoz en el GPIO21, reloj de bit en el GPIO47 y
  selección de palabra en el GPIO48
  (`main/boards/wk-esp32s3-dev/config.h`). Tú eliges el driver que el
  amplificador mueve; nada en el repositorio lo configura.
- La [lista de compra](../lila-build-guide.es.md#lista-de-compra) especifica
  la pieza de referencia de 4 Ω. Un driver diferente contrapone volumen
  contra calor y carga en el amplificador; la potencia del amplificador no
  se puede verificar desde este repositorio, así que en caso de duda deja la
  pieza de referencia (*sin verificar*: no se ha medido ninguna alternativa
  en un dispositivo).

## Cambio en la lista de compra

Cambia una fila de la [lista de
compra](../lila-build-guide.es.md#lista-de-compra); el resto de las piezas
son las de por defecto.

| Pieza | Especificación | Cant. | Cambio |
| --- | --- | --- | --- |
| Altavoz | tu elección de impedencia, potencia y tamaño, dentro de lo que admite el amplificador de la placa | 1 | reemplaza al altavoz de referencia de 4 Ω |

El tamaño físico importa tanto como las especificaciones eléctricas: un
driver más grande que la pieza de referencia puede no caber en la carcasa.

## Configurar

Nada. No existe ninguna clave de altavoz en `.env.example` ni una opción de
Kconfig para ello, así que tu `.env` se queda exactamente como describen las
[recetas de configuración](../lila-build-guide.es.md#recetas-de-configuración)
y el mismo binario de firmware mueve la pieza nueva. Si alguna vez aparece
una opción de firmware para la salida de audio, llegará con su propio
`FEAT_XXX` y esta página lo nombrará.

## Imprimir y montar

- El set de STL por defecto encaja con el altavoz de referencia, así que
  imprimir y montar siguen la [guía](../lila-build-guide.es.md#imprimir-la-carcasa)
  sin cambios.
- Un driver físicamente más grande necesita un hueco dimensionado para él.
  Esa geometría sigue la nomenclatura de variación —
  `lila-case-wk-esp32s3-dev-speaker.stl` y sus piezas hermanas — y todavía no
  existe (*sin verificar*: no se ha impreso nada).
- El cableado y las comprobaciones de montaje son los de la guía; el altavoz
  se conecta a la salida de altavoz de la placa igual que la pieza por
  defecto.

## Estado y verificación

| Comprobación | Estado |
| --- | --- |
| Cambio de configuración necesario | ninguno — no existe ninguna clave en `.env.example` ni en Kconfig |
| Cambio de firmware necesario | ninguno |
| La carcasa por defecto encaja con el altavoz de referencia | la carcasa está diseñada para él; la impresión está pendiente en `STL/README.es.md` |
| Encaje de otros drivers en la carcasa | sin verificar — no existe ninguna geometría alternativa |
| Volumen y calidad de las alternativas | sin verificar — necesita hardware |

Vuelve al [selector](README.es.md).
