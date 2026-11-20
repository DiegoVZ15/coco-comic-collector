"""
probar_fase0.py

Comprueba que la Fase 0 funciona: extrae las páginas del mismo
capítulo que usaba tu script original, pero ya con la arquitectura
nueva. Corre esto (desde la carpeta coco/) con:

    python probar_fase0.py

Si ves una lista de URLs de imágenes al final, la Fase 0 está lista y
podemos pasar a la Fase 1 (buscar y listar_capitulos).
"""

from coco.models import Capitulo
from coco.sitios.marmota import MarmotaSitio

CAPITULO_DE_PRUEBA = Capitulo(
    numero="1",
    titulo="Absolute Batman #1",
    url="https://marmota.me/comic/absolute-batman-2024/absolute-batman-1/",
)

if __name__ == "__main__":
    sitio = MarmotaSitio()
    capitulo = sitio.obtener_paginas(CAPITULO_DE_PRUEBA)

    print(f"Encontré {len(capitulo.paginas)} páginas:")
    for pagina in capitulo.paginas[:3]:
        print(f"  [{pagina.indice}] {pagina.url}")
    if len(capitulo.paginas) > 3:
        print(f"  ... y {len(capitulo.paginas) - 3} más")
