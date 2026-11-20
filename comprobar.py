"""Comprobaciones locales de selección, empaquetado y reanudación."""
import tempfile
import unittest
import zipfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from comicdl.descargador import crear_cbz
from comicdl.models import Capitulo, Pagina
from comicdl.seleccion import seleccionar


class Respuesta:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def raise_for_status(self):
        pass

    def iter_content(self, size):
        archivo = BytesIO()
        Image.new("RGB", (8, 8), "red").save(archivo, "PNG")
        yield archivo.getvalue()


class SitioPrueba:
    def __init__(self):
        self.session = self
        self.pedidos = 0

    def obtener_paginas(self, capitulo):
        capitulo.paginas = [Pagina(i, capitulo.url + f"/{i}") for i in (1, 2)]
        return capitulo

    def get(self, *args, **kwargs):
        self.pedidos += 1
        return Respuesta()


class Comprobaciones(unittest.TestCase):
    def test_seleccion(self):
        self.assertEqual(seleccionar("5-8,1,3,5", 8), [1, 3, 5, 6, 7, 8])
        for texto in ("", "0", "3-1", "1-9", "1,", "abc", "-1"):
            with self.assertRaises(ValueError):
                seleccionar(texto, 8)

    @patch("comicdl.descargador.time.sleep")
    def test_cbz_y_reanudacion(self, dormir):
        sitio = SitioPrueba()
        capitulos = [Capitulo(str(i), f"Cap {i}", f"https://ejemplo/{i}") for i in (1, 3)]
        with tempfile.TemporaryDirectory() as carpeta:
            destino = crear_cbz(sitio, "Serie: prueba", capitulos, carpeta, lambda _: None)
            with zipfile.ZipFile(destino) as cbz:
                self.assertEqual(cbz.namelist(), [f"{i:06d}.png" for i in range(1, 5)])
                self.assertIsNone(cbz.testzip())
            self.assertEqual(sitio.pedidos, 4)
            crear_cbz(sitio, "Serie: prueba", capitulos, carpeta, lambda _: None)
            self.assertEqual(sitio.pedidos, 4)
            next((Path(carpeta) / ".progreso").iterdir()).write_bytes(b"incompleto")
            crear_cbz(sitio, "Serie: prueba", capitulos, carpeta, lambda _: None)
            self.assertEqual(sitio.pedidos, 5)

    @patch("comicdl.descargador.time.sleep")
    def test_interrupcion_conserva_cbz_y_paginas(self, dormir):
        sitio = SitioPrueba()
        capitulos = [Capitulo("1", "Cap 1", "https://ejemplo/1")]
        with tempfile.TemporaryDirectory() as carpeta:
            destino = crear_cbz(sitio, "Serie", capitulos, carpeta, lambda _: None)
            contenido = destino.read_bytes()
            # Una actualización añade una página y falla al descargarla.
            def paginas_extra(capitulo):
                capitulo.paginas = [Pagina(i, capitulo.url + f"/{i}") for i in (1, 2, 3)]
            sitio.obtener_paginas = paginas_extra
            with patch.object(sitio, "get", side_effect=OSError("Conexión interrumpida")):
                with self.assertRaises(OSError):
                    crear_cbz(sitio, "Serie", capitulos, carpeta, lambda _: None)
            self.assertEqual(destino.read_bytes(), contenido)
            self.assertEqual(len(list((Path(carpeta) / ".progreso").iterdir())), 2)
            crear_cbz(sitio, "Serie", capitulos, carpeta, lambda _: None)
            self.assertEqual(sitio.pedidos, 3)
            with zipfile.ZipFile(destino) as cbz:
                self.assertEqual(len(cbz.namelist()), 3)


if __name__ == "__main__":
    unittest.main()
