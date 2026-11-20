# CoCo — Comic Collector

[Español](README.md)

Search for a series on Marmota and download one or more chapters as a single CBZ file you can copy to your phone.

See the [CoCo web guide](https://coco-webpage.vercel.app/en/index.html) for step-by-step instructions and help choosing a CBZ reader.

## Getting started on Windows

You need Python 3.10 or later with pip and an internet connection. Double-click `iniciar.bat`. On the first run, the launcher creates `.venv` and installs the dependencies.

CoCo's terminal prompts are in Spanish.

1. Enter the series title.
2. Enter the number next to the result you want.
3. Enter the positions from the chapter list, such as `1`, `1-6`, or `1,3,5-8`.
4. Wait for `CBZ completo guardado en` to appear. The file is saved in the `descargas` folder inside the project directory.

The numbers refer to the positions in the displayed list, which includes specials and annuals. CoCo removes duplicates and puts chapters in list order. It displays chapters in reverse of the order shown on Marmota. Check the chapter titles when selecting a story that includes specials.

Press Enter at the series or chapter prompt to return to search. Press Enter at the title prompt to exit, or Ctrl+C to end the session. To resume an interrupted download, search for the same series and select the same chapters again.

The `descargas/.progreso` folder stores verified images. Deleting it after a download removes the saved pages that CoCo can reuse. CoCo saves the finished CBZ once all pages are ready. The filename includes a selection ID so you can tell collections apart. Repeating the same selection updates its CBZ using the saved pages.

## Running CoCo from the terminal

```powershell
.\.venv\Scripts\python.exe -m coco
.\.venv\Scripts\python.exe -m coco --destino "D:\Comics"
.\.venv\Scripts\python.exe comprobar.py
```

The adapter uses Marmota's HTML search and the `/ajax/chapters/` endpoint. It extracts page images from the site's reader. Future changes to Marmota may require updates to `coco/sitios/madara.py`.

`pdf_to_cbz.py` is a standalone tool. Install PyMuPDF in the environment where you run it. CoCo's main menu downloads page images directly from the site's reader.
