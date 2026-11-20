"""
models.py

Estructuras de datos que viajan entre las distintas partes del
programa (scraper -> descargador -> empaquetador -> CLI).

Usamos `dataclasses` en vez de diccionarios sueltos (como el
`thisdict` del script original) por tres razones concretas:

  1. Autocompletado: tu editor sabe que un Capitulo tiene `.numero`,
     `.titulo`, etc. Con un dict tendrías que recordar las claves
     exactas ("numero" vs "número" vs "num"...).
  2. Si te equivocas escribiendo un campo, Python te avisa de
     inmediato en vez de fallar en silencio con un KeyError en medio
     de una descarga de 40 páginas.
  3. Documentan el proyecto: cualquiera que abra este archivo entiende
     qué información maneja el programa sin tener que leer el scraper.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pagina:
    """Una sola imagen (página) dentro de un capítulo."""

    indice: int  # posición dentro del capítulo (1, 2, 3...): la usamos
    #              para nombrar el archivo y que el .cbz respete el
    #              orden de lectura correcto.
    url: str


@dataclass
class Capitulo:
    """Un capítulo de una serie."""

    numero: str  # "1", "2.5", "Annual 1"... por eso es texto y no int
    titulo: str
    url: str  # página del capítulo; de aquí sacamos sus páginas
    paginas: list[Pagina] = field(default_factory=list)


@dataclass
class ResultadoBusqueda:
    """Una serie encontrada al buscar por palabra clave."""

    titulo: str
    url: str  # url de la página principal de la serie
    sitio: str  # nombre del adaptador de origen (ej. "marmota"),
    #             útil cuando busques en varios sitios a la vez
    portada_url: Optional[str] = None
