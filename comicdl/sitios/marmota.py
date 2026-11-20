"""
sitios/marmota.py

Adaptador específico para marmota.me. Como el sitio usa el tema
Madara, casi todo el trabajo ya vive en MadaraSitio — acá solo fijamos
el dominio y el nombre.

Esto es, a propósito, casi vacío: es la prueba de que la arquitectura
funciona. Cuando agregues tu segundo sitio (si también es Madara),
este archivo es literalmente la plantilla: cópialo y cambia estas dos
líneas.
"""

from .madara import MadaraSitio


class MarmotaSitio(MadaraSitio):
    nombre = "marmota"
    dominio = "https://marmota.me"
