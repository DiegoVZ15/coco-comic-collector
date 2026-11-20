from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import HEADERS, TIMEOUT_SEGUNDOS
from ..models import Capitulo, Pagina, ResultadoBusqueda
from .base import SitioComic


class MadaraSitio(SitioComic):
    dominio = ""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

    def html(self, url, **kwargs):
        response = self.session.get(url, timeout=TIMEOUT_SEGUNDOS, **kwargs)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def buscar(self, query):
        soup = self.html(self.dominio + "/", params={"s": query, "post_type": "wp-manga"})
        resultados = {}
        visitadas = set()
        while True:
            for enlace in soup.select(".post-title a"):
                url = urljoin(self.dominio, enlace.get("href", ""))
                resultados[url] = ResultadoBusqueda(enlace.get_text(" ", strip=True), url, self.nombre)
            siguiente = soup.select_one("a.next.page-numbers")
            if not siguiente:
                break
            url = urljoin(self.dominio, siguiente["href"])
            if url in visitadas:
                break
            visitadas.add(url)
            soup = self.html(url)
        return list(resultados.values())

    def listar_capitulos(self, url_serie):
        soup = self.html(url_serie)
        if not soup.select("li.wp-manga-chapter"):
            response = self.session.post(url_serie.rstrip("/") + "/ajax/chapters/", timeout=TIMEOUT_SEGUNDOS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        capitulos = {}
        for enlace in soup.select("li.wp-manga-chapter a[href]"):
            url = urljoin(url_serie, enlace["href"])
            titulo = enlace.get_text(" ", strip=True)
            capitulos[url] = Capitulo(titulo, titulo, url)
        return list(reversed(list(capitulos.values())))

    def obtener_paginas(self, capitulo):
        soup = self.html(capitulo.url)
        paginas = []
        for img in soup.select("img.wp-manga-chapter-img"):
            fuente = (img.get("data-src") or img.get("src") or "").strip()
            if fuente:
                paginas.append(Pagina(len(paginas) + 1, urljoin(capitulo.url, fuente)))
        if not paginas:
            raise ValueError("El sitio no devolvi? p?ginas para " + capitulo.titulo)
        capitulo.paginas = paginas
        return capitulo
