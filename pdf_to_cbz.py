import sys
import os
import zipfile
import pymupdf

print("Script iniciado")

if len(sys.argv) < 2:
    print("No se proporcionó ningún PDF.")
    print('Uso: python pdf_to_cbz.py "archivo.pdf"')
    input("Presiona ENTER para salir...")
    sys.exit()

pdf_path = sys.argv[1]

print(f"PDF recibido: {pdf_path}")

if not os.path.exists(pdf_path):
    print("ERROR: El PDF no existe.")
    input("Presiona ENTER para salir...")
    sys.exit()

print("Abriendo PDF...")

doc = pymupdf.open(pdf_path)

print(f"PDF abierto correctamente.")
print(f"Número de páginas: {len(doc)}")

output_path = os.path.splitext(pdf_path)[0] + ".cbz"

print(f"Creando: {output_path}")

with zipfile.ZipFile(output_path, "w", zipfile.ZIP_STORED) as cbz:

    for i, page in enumerate(doc, start=1):

        print(f"Convirtiendo página {i}/{len(doc)}...")

        pixmap = page.get_pixmap(dpi=150)

        filename = f"{i:04d}.jpg"

        cbz.writestr(
            filename,
            pixmap.tobytes("jpg")
        )

doc.close()

print()
print("================================")
print("       CONVERSION TERMINADA")
print("================================")
print(f"CBZ: {output_path}")

input("Presiona ENTER para salir...")