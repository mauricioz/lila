# Variaciones de construcción

[English](README.md) · **Español**

La [guía de construcción](../lila-build-guide.es.md) es la Lila por defecto:
la placa `wk-esp32s3-dev` con la pantalla ST7789 de 240x240. Esta carpeta
documenta las formas de construir otra cosa. Cada página de variación indica
solo lo que cambia respecto a esa guía — qué comprar distinto, qué configurar
y si hace falta código — con las mismas cinco secciones, para que puedas
comparar las opciones aquí y luego seguir la guía más el delta.

## Elige una variación

| Variación | Tipo | Pantalla | Qué cambia | Set de STL | Estado |
| --- | --- | --- | --- | --- | --- |
| [Pantalla circular](circular-display.es.md) | `config` | GC9A01 240x240, redonda | una línea en `.env`; la geometría del marco | set de pantalla redonda (pendiente) | construible |
| [Altavoz diferente](speaker.es.md) | `parts` | sin cambios | el altavoz que compras | set por defecto | construible |

**construible** significa que todo lo necesario ya está en este repositorio.
No significa que la variación se haya construido en un dispositivo: cada
página indica qué todavía necesita validación con hardware, y ninguna de las
dos variaciones se ha flasheado ni impreso.

## Qué significan los tipos

| Tipo | Lo que necesita la variación | Proceso |
| --- | --- | --- |
| `config` | un valor de `.env` y su set de STL | una pull request de documentación; sin código |
| `parts` | una compra diferente, mismo firmware | una pull request de documentación; sin código |
| `variant` | firmware y una variante de release propia | primero su propio `FEAT_XXX` y su rama; la página lo nombra |

Hoy no existe ninguna variación de tipo `variant` en el repositorio.

## Cómo es una página de variación

Cada página de esta carpeta sigue las mismas secciones, en el mismo orden —
`Qué cambia`, `Cambio en la lista de compra`, `Configurar`, `Imprimir y
montar`, `Estado y verificación` — declara su tipo cerca del enlace al otro
idioma y vuelve a enlazar este selector. `scripts/check_workflow.py` falla
una pull request cuando una página se desvía de esa plantilla, cuando esta
matriz y las páginas no coinciden, o cuando falta una traducción.

Cuando la tabla de arriba no se aplica a ti, empieza por la [construcción
por defecto](../lila-build-guide.es.md): la guía es el documento canónico y
las páginas de aquí solo la complementan.
