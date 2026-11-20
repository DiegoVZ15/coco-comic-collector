"""
config.py

Configuración global compartida por todos los sitios y módulos.

Centralizarla acá evita lo que pasaba en el script original: el
`user_agent` estaba escrito a mano en una sola variable, y si mañana
quieres cambiarlo (o agregar más headers) tendrías que buscarlo en
cada archivo nuevo que crees. Con un único lugar, cualquier módulo que
lo necesite hace `from coco.config import HEADERS`.
"""

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
)

HEADERS = {"User-Agent": USER_AGENT}

# Tiempo máximo (segundos) que esperamos una respuesta antes de
# considerar que la petición falló. Sin esto, una petición colgada
# puede congelar tu programa indefinidamente.
TIMEOUT_SEGUNDOS = 15

# Segundos de espera entre descarga de cada imagen. Es buena práctica
# (y buena educación) no bombardear un servidor ajeno con pedidos
# simultáneos: además de ser cortés, muchos sitios banean IPs que
# hacen demasiadas peticiones muy rápido.
DELAY_ENTRE_DESCARGAS = 1.5
