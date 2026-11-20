# CoCo - Comic Collector

Busca una serie en Marmota y descarga uno o varios capítulos en un único CBZ para copiarlo a tu teléfono.

Consulta la [guía web de CoCo](guia-web/dist/index.html) para ver el proceso paso a paso y elegir un lector CBZ.

## Inicio en Windows

Requiere Python 3.10 o superior con pip y conexión a Internet.
Haz doble clic en `iniciar.bat`. En el primer inicio se crea `.venv` y se instalan las dependencias.

1. Escribe el nombre de la serie.
2. Selecciona el número de un resultado.
3. Selecciona posiciones de la lista de capítulos, por ejemplo `1`, `1-6` o `1,3,5-8`.
4. Espera al mensaje de CBZ completo. El archivo queda en `descargas` dentro de esta carpeta.

Los números corresponden a las posiciones mostradas, incluyendo especiales y anuales. Las selecciones repetidas se eliminan y se ordenan según la lista. Los capítulos se muestran invirtiendo el orden publicado por Marmota. Revisa sus títulos al seleccionar historias con especiales.

ENTER vuelve al buscador o sale cuando se solicita un título. Ctrl+C termina la sesión. Para continuar una descarga interrumpida, vuelve a buscar y elegir los mismos capítulos.

La carpeta `descargas/.progreso` conserva las imágenes verificadas. Puedes borrarla cuando termines, pero se perderá la posibilidad de reutilizarlas. Los CBZ se publican al terminar todas las páginas. Cada selección tiene un identificador en su nombre para distinguir recopilaciones. Repetir la misma selección actualiza su CBZ usando las páginas guardadas.

## Uso desde terminal

```powershell
.\.venv\Scripts\python.exe -m comicdl
.\.venv\Scripts\python.exe -m comicdl --destino "D:\Comics"
.\.venv\Scripts\python.exe comprobar.py
```

El adaptador consulta el buscador HTML y el endpoint de capítulos `/ajax/chapters/`. La extracción usa las imágenes del lector del sitio. Los cambios futuros de Marmota pueden requerir ajustes en `comicdl/sitios/madara.py`.

`pdf_to_cbz.py` se conserva como herramienta independiente y requiere instalar PyMuPDF en el entorno donde se ejecute. El menú principal descarga las páginas del lector directamente.
