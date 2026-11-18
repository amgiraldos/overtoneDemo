# Generador del sitio overtonelab.com

Respaldo del código que arma las páginas del sitio. Las páginas ya terminadas están en la raíz del repositorio; esto es lo que las produce.

## Archivos
- `build.py`: arma las páginas en español e inglés (portada, agendar, gracias, privacidad) y los datos estructurados.
- `textos.py`: todos los textos en español e inglés, y los planes con sus precios.
- `privacy.py`: texto de la política de privacidad.
- `embudo.css`, `embudo.js`: estilos y comportamiento (videos en las tarjetas, calendario de agendar).
- `config.js`: dirección del servicio de agendar (Cloudflare Worker) y el video de la página de gracias.

## Cómo usarlo
1. Copia esta carpeta a un lugar de trabajo.
2. Genera las páginas: `python3 build.py <carpeta_de_salida>`
3. El programa NO copia `embudo.css`, `embudo.js` ni `config.js`: cópialos a `assets/embudo/` de la carpeta de salida.
4. Copia el resultado a la raíz del repositorio (sin tocar `sitemap.xml`, `robots.txt`, `llms.txt`, `404.html`, `CNAME`, `c-z32vapznzn/` ni `assets/embudo/img`).

## Que no se pierda
- El `sitemap.xml`, `llms.txt` y `404.html` se editan a mano en la raíz.
- La etiqueta de verificación de Search Console está en `build.py` (constante GSC).
- Si cambias los precios o la cantidad de videos de un plan, cámbialos también en la ficha de Google Maps.
