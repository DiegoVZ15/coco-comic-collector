# Guía web de CoCo

Abre `dist/index.html` en el navegador. La guía usa HTML, CSS y JavaScript, sin instalación ni compilación.

- `dist/index.html` contiene los pasos, los lectores CBZ y las preguntas frecuentes.
- `dist/styles.css` define el diseño adaptable y la paleta en `:root`.
- `dist/guide.js` controla el menú móvil, el filtro de lectores y la copia de comandos.

## Enlazar el repositorio

En `dist/guide.js`, asigna a `repositoryUrl` la URL del repositorio público de CoCo, como `https://github.com/usuario/CoCo`. Con el valor vacío, la guía enlaza las instrucciones oficiales de GitHub para descargar un ZIP.

Para alojar la guía, publica el contenido de `dist/` como un sitio estático. En GitHub Pages, usa `dist/` como origen del artefacto de publicación mediante GitHub Actions, o copia su contenido a la carpeta `docs/` de la rama que uses como origen.
