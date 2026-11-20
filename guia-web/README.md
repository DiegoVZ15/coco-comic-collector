# Guía web de CoCo — Comic Collector

Abre `dist/index.html` en el navegador. La guía usa HTML, CSS y JavaScript, sin instalación ni compilación.

- `dist/index.html` contiene la guía en español y `dist/en/index.html` la versión en inglés. El enlace ES/EN cambia de idioma.
- `dist/styles.css` define el diseño adaptable y la paleta en `:root`.
- `dist/guide.js` comparte el menú móvil, el filtro de lectores y la copia de comandos entre ambas versiones.

## Enlazar el repositorio

En `dist/guide.js`, asigna a `repositoryUrl` la URL del repositorio público de CoCo, como `https://github.com/usuario/CoCo`. Con el valor vacío, la guía enlaza las instrucciones oficiales de GitHub para descargar un ZIP.

## Publicar en Vercel desde GitHub

1. Sube el proyecto a GitHub y confirma que `guia-web/dist/` contiene `index.html`, `en/index.html`, `styles.css`, `guide.js` y `assets/`.
2. En el panel de Vercel, elige **Add New → Project** e importa el repositorio.
3. Selecciona `guia-web/dist` como **Root Directory** y **Other** como **Framework Preset**.
4. Activa **Override** en **Build Command** y deja el campo vacío. Usa `.` como **Output Directory** si necesitas indicarlo manualmente.
5. Pulsa **Deploy** y abre el dominio `vercel.app` que te asigne Vercel. Los cambios que subas a la rama de producción se publicarán automáticamente.

Vercel sirve la guía. Los visitantes descargan CoCo desde GitHub y utilizan `iniciar.bat` en su computadora.

[Documentación de compilación de Vercel](https://vercel.com/docs/builds/configure-a-build) · [Conectar un repositorio](https://vercel.com/docs/git)

Para publicar en GitHub Pages, usa `dist/` como origen del artefacto en GitHub Actions o copia su contenido a `docs/` y elige esa carpeta como origen.
