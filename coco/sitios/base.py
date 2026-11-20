"""
sitios/base.py

Define el "contrato" que cualquier sitio de cómics debe cumplir.

Es una clase abstracta (ABC): no se puede instanciar directamente,
solo sirve de plantilla para que MarmotaSitio, OtroSitio, etc. la
hereden y rellenen los métodos marcados con @abstractmethod. Si una
subclase se olvida de implementar alguno, Python lanza un error apenas
intentas crear el objeto — mucho mejor que descubrirlo a mitad de una
descarga.

¿Por qué molestarse en esto en vez de simplemente escribir funciones
sueltas por sitio? Porque así el resto de tu programa (la CLI, el
descargador, el empaquetador) puede trabajar con CUALQUIER sitio sin
saber sus detalles internos. Solo le importa que el objeto tenga estos
3 métodos. Esto es "polimorfismo": te permite, más adelante, escribir
algo como

    sitios_disponibles = [MarmotaSitio(), OtroSitio(), TercerSitio()]
    resultados = []
    for sitio in sitios_disponibles:
        resultados += sitio.buscar("absolute batman")

sin un solo "if sitio == 'marmota': ... elif sitio == 'otro': ...".
"""

from abc import ABC, abstractmethod

from ..models import Capitulo, ResultadoBusqueda


class SitioComic(ABC):
    """Contrato que debe cumplir cualquier adaptador de sitio."""

    #: Nombre corto para identificar el sitio en la CLI, ej. "marmota"
    nombre: str = "base"

    @abstractmethod
    def buscar(self, query: str) -> list[ResultadoBusqueda]:
        """Busca series por palabra clave. Devuelve una lista de resultados."""
        raise NotImplementedError

    @abstractmethod
    def listar_capitulos(self, url_serie: str) -> list[Capitulo]:
        """Dada la URL de una serie, devuelve sus capítulos disponibles
        (todavía sin páginas: eso es un paso aparte porque es más pesado
        y no siempre lo necesitas, por ejemplo solo para listar)."""
        raise NotImplementedError

    @abstractmethod
    def obtener_paginas(self, capitulo: Capitulo) -> Capitulo:
        """Dado un Capitulo (con su url), rellena su lista de `paginas`
        con las URLs de las imágenes y devuelve el mismo capítulo."""
        raise NotImplementedError
