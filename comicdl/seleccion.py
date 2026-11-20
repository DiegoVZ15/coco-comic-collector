import re


def seleccionar(texto, total):
    """Devuelve posiciones únicas y ordenadas a partir de números y rangos."""
    posiciones = set()
    for parte in texto.split(","):
        match = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+)\s*)?", parte)
        if not match:
            raise ValueError("Usa números y rangos, por ejemplo 1,3,5-8.")
        inicio = int(match[1])
        fin = int(match[2] or match[1])
        if not 1 <= inicio <= fin <= total:
            raise ValueError(f"Cada rango debe avanzar entre 1 y {total}.")
        posiciones.update(range(inicio, fin + 1))
    return sorted(posiciones)
