import argparse
from pathlib import Path

import requests

from .descargador import crear_cbz
from .seleccion import seleccionar
from .sitios.marmota import MarmotaSitio


def ejecutar(sitio, carpeta):
    while True:
        consulta = input("\nNombre del cómic (ENTER para salir): ").strip()
        if not consulta:
            return
        try:
            print("Buscando…")
            resultados = sitio.buscar(consulta)
            if not resultados:
                print("No se encontraron series. Prueba otro nombre.")
                continue
            for i, resultado in enumerate(resultados, 1):
                print(f"{i:3}. {resultado.titulo}")
            texto = input("Serie (número, ENTER para volver): ").strip()
            if not texto:
                continue
            if not texto.isdecimal() or not 1 <= int(texto) <= len(resultados):
                print("Selecciona un número de la lista.")
                continue
            serie = resultados[int(texto) - 1]
            print("Consultando capítulos…")
            capitulos = sitio.listar_capitulos(serie.url)
            if not capitulos:
                print("El sitio no devolvió capítulos para esta serie.")
                continue
            for i, capitulo in enumerate(capitulos, 1):
                print(f"{i:3}. {capitulo.titulo}")
            print("Usa las posiciones de esta lista, incluidos especiales y anuales.")
            while True:
                texto = input("Capítulos (ej. 1,3,5-8, ENTER para volver): ").strip()
                if not texto:
                    break
                try:
                    posiciones = seleccionar(texto, len(capitulos))
                    break
                except ValueError as error:
                    print(error)
            if not texto:
                continue
            elegidos = [capitulos[i - 1] for i in posiciones]
            print(f"Creando un CBZ con {len(elegidos)} capítulo(s).")
            destino = crear_cbz(sitio, serie.titulo, elegidos, carpeta)
            print(f"\nCBZ completo guardado en\n{destino.resolve()}")
        except (requests.RequestException, OSError, ValueError, SyntaxError) as error:
            print(f"No se pudo completar la operación: {error}")
            print("Puedes repetir la selección para aprovechar las páginas guardadas.")


def main():
    parser = argparse.ArgumentParser(description="Busca cómics y reúne capítulos en un CBZ.")
    parser.add_argument("--destino", type=Path, default=Path(__file__).resolve().parents[1] / "descargas", help="Carpeta de los CBZ")
    args = parser.parse_args()
    sitio = MarmotaSitio()
    print("ComicDL — Marmota")
    print(f"Descargas en {args.destino.resolve()}")
    try:
        ejecutar(sitio, args.destino)
    except (KeyboardInterrupt, EOFError):
        print("\nSesión terminada. Las páginas guardadas permiten reanudar la descarga.")
    finally:
        sitio.session.close()
