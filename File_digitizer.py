"""
Analiza un pdf y usa reconocimiento
óptico de caracteres (OCR) para hacer
una transcripcion digital

...

Lee el texto y lo escribe pues
"""



import pytesseract
from pdf2image import convert_from_path
import os
from PIL import Image
import re
import glob

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  ### Esta es la ruta donde
                                                                                         ### está el programa de OCR
def process_document(pdf_path, output_txt_path, language='spa'):

    print(f"Convirtiendo PDF {pdf_path} a imágenes...")
    # Convierte PDF a imágenes
    poppler_path = r"C:\Users\shipp\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)  # 300 DPI para buena calidad

    all_text = []

    for i, page in enumerate(pages):
        print(f"Procesando página {i + 1}/{len(pages)}...")

        # Mejora de imágen para OCR
        page = page.convert('L')  # Convierte a escala de grises

        # Aplica OCR a la imágen
        text = pytesseract.image_to_string(page, lang=language)

        # Limpia el texto
        text = re.sub(r'\n{3,}', '\n\n', text)  # Quita líneas excesivas

        # Agrega un separador de páginas
        page_header = f"\n\n----- PÁGINA {i + 1} -----\n\n"
        all_text.append(page_header + text)

    # Guarda el texto a un archivo .txt
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(''.join(all_text))

    print(f"OCR completo! Texto guardado en {output_txt_path}")

    # Entrega el texto
    return ''.join(all_text)


def process_folder(folder_path, output_folder=None, language='spa'):
    # If no output folder specified, use the same folder
    if output_folder is None:
        output_folder = folder_path

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all PDF files in the folder
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return

    print(f"Found {len(pdf_files)} PDF files to process")

    # Process each PDF file
    for idx, pdf_path in enumerate(pdf_files, 1):
        print(f"\n===== Processing file {idx}/{len(pdf_files)}: {os.path.basename(pdf_path)} =====")

        # Get the filename without extension
        pdf_name_without_ext = os.path.splitext(os.path.basename(pdf_path))[0]

        # Create output paths
        output_txt_path = os.path.join(output_folder, f"{pdf_name_without_ext}.txt")

        try:
            # Process the document
            process_document(pdf_path, output_txt_path, language=language)

            print(f"Successfully processed: {os.path.basename(pdf_path)}")

        except Exception as e:
            print(f"Error processing {os.path.basename(pdf_path)}: {str(e)}")
            continue

    print(f"\n===== Batch processing complete! =====")


# Main execution
if __name__ == "__main__":
    # Specify the folder containing PDF files
    folder_path = r"C:\Users\shipp\Desktop\MINUTAS_PAROBUAP_2025\MINUTAS DE FISMAT"

    # Optional: specify a different output folder
    # output_folder = r"C:\Users\shipp\Desktop\MINUTAS_PARO 2025 BUAP\OCR_OUTPUT"

    # Process all PDFs in the folder
    process_folder(folder_path)

    # Alternative: Process with custom output folder
    # process_folder(folder_path, output_folder)