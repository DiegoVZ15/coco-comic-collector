import hashlib
import json
import re
import time
import uuid
import zipfile
from pathlib import Path

from PIL import Image

from .config import DELAY_ENTRE_DESCARGAS, TIMEOUT_SEGUNDOS


def nombre_seguro(texto):
    nombre = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", texto).strip(" .")[:100]
    if not nombre:
        nombre = "Comic"
    if nombre.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)], *[f"LPT{i}" for i in range(1, 10)]}:
        nombre = "_" + nombre
    return nombre


def extension_imagen(ruta):
    with Image.open(ruta) as imagen:
        formato = imagen.format
        imagen.load()
    extensiones = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "GIF": ".gif"}
    if formato not in extensiones:
        raise ValueError(f"Formato de imagen no admitido: {formato}")
    return extensiones[formato]


def crear_cbz(sitio, titulo, capitulos, carpeta, informar=print):
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    cache = carpeta / ".progreso"
    cache.mkdir(exist_ok=True)
    archivos = []
    for numero, capitulo in enumerate(capitulos, 1):
        informar(f"Capítulo {numero}/{len(capitulos)} — {capitulo.titulo}")
        sitio.obtener_paginas(capitulo)
        for pagina in capitulo.paginas:
            clave = hashlib.sha256((capitulo.url + "\n" + pagina.url).encode()).hexdigest()
            ruta = cache / clave
            extension = None
            if ruta.exists():
                try:
                    extension = extension_imagen(ruta)
                except (OSError, ValueError, SyntaxError):
                    ruta.unlink()
            if extension is None:
                temporal = cache / (clave + "." + uuid.uuid4().hex + ".part")
                try:
                    with sitio.session.get(pagina.url, headers={"Referer": capitulo.url}, timeout=TIMEOUT_SEGUNDOS, stream=True) as respuesta:
                        respuesta.raise_for_status()
                        with temporal.open("wb") as salida:
                            for bloque in respuesta.iter_content(65536):
                                salida.write(bloque)
                    extension = extension_imagen(temporal)
                    temporal.replace(ruta)
                finally:
                    temporal.unlink(missing_ok=True)
                time.sleep(DELAY_ENTRE_DESCARGAS)
            informar(f"  Página {pagina.indice}/{len(capitulo.paginas)} lista")
            archivos.append((ruta, f"{len(archivos) + 1:06d}{extension}"))
    if not archivos:
        raise ValueError("La selección no contiene páginas.")
    identidad = json.dumps([c.url for c in capitulos], ensure_ascii=False)
    codigo = hashlib.sha256(identidad.encode()).hexdigest()[:10]
    destino = carpeta / f"{nombre_seguro(titulo)} - {len(capitulos)} caps - {codigo}.cbz"
    temporal = carpeta / (destino.stem + "." + uuid.uuid4().hex + ".part")
    try:
        with zipfile.ZipFile(temporal, "w", compression=zipfile.ZIP_STORED) as cbz:
            for ruta, nombre in archivos:
                cbz.write(ruta, nombre)
        temporal.replace(destino)
    finally:
        temporal.unlink(missing_ok=True)
    return destino
