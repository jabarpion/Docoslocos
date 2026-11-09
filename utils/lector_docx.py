from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def leer_docx(ruta_docx, idioma="spa", psm=6):
    """
    Extrae las imágenes de un DOCX y recupera su texto mediante OCR.

    Devuelve un texto identificado por imagen.
    No modifica el documento original.
    """

    ruta_docx = Path(ruta_docx)

    if not ruta_docx.is_file():
        raise FileNotFoundError(
            f"No se encontró el documento: {ruta_docx}"
        )

    resultados = []

    with ZipFile(ruta_docx) as documento:
        imagenes = sorted(
            nombre
            for nombre in documento.namelist()
            if nombre.startswith("word/media/")
            and Path(nombre).suffix.lower()
            in (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")
        )

        if not imagenes:
            return "El DOCX no contiene imágenes para procesar."

        with TemporaryDirectory(prefix="docoslocos_ocr_") as temporal:
            carpeta = Path(temporal)

            for indice, nombre in enumerate(imagenes, start=1):
                try:
                    contenido = documento.read(nombre)

                    imagen = Image.open(
                        BytesIO(contenido)
                    ).convert("L")

                    imagen = imagen.resize(
                        (imagen.width * 3, imagen.height * 3),
                        Image.Resampling.LANCZOS
                    )

                    imagen = ImageOps.autocontrast(imagen)
                    imagen = ImageEnhance.Contrast(imagen).enhance(1.5)
                    imagen = imagen.filter(ImageFilter.SHARPEN)

                    archivo_png = carpeta / f"imagen_{indice}.png"
                    imagen.save(archivo_png)

                    proceso = subprocess.run(
                        [
                            "tesseract",
                            str(archivo_png),
                            "stdout",
                            "-l", idioma,
                            "--psm", str(psm),
                        ],
                        capture_output=True,
                        text=True,
                        check=True,
                    )

                    texto = proceso.stdout.strip()

                    resultados.append(
                        f"IMAGEN {indice}: {Path(nombre).name}\n"
                        f"{texto if texto else '[Sin texto reconocido]'}"
                    )

                except Exception as error:
                    resultados.append(
                        f"IMAGEN {indice}: {Path(nombre).name}\n"
                        f"[Error de procesamiento: {type(error).__name__}]"
                    )

    return "\n\n".join(resultados)
