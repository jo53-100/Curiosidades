"""
Funciona en linux!
Analiza un pdf y usa reconocimiento
óptico de caracteres (OCR) para hacer
una transcripcion digital
"""

import pytesseract
from pdf2image import convert_from_path
import os

import re
import glob


def process_document(pdf_path, output_txt_path, language='spa'):
    print(f"Convirtiendo PDF {pdf_path} a imágenes...")

    try:
        pages = convert_from_path(pdf_path, 300)  # 300 DPI for good quality

    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        print("Make sure poppler is installed: sudo apt-get install poppler-utils")
        return None

    all_text = []

    for i, page in enumerate(pages):
        print(f"Procesando página {i + 1}/{len(pages)}...")

        # Image improvement for OCR
        page = page.convert('L')  # Convert to grayscale

        try:
            # Apply OCR to the image
            text = pytesseract.image_to_string(page, lang=language)
        except Exception as e:
            print(f"Error in OCR processing: {e}")
            print("Make sure tesseract is installed: sudo apt-get install tesseract-ocr tesseract-ocr-spa")
            continue

        # Clean the text
        text = re.sub(r'\n{3,}', '\n\n', text)  # Remove excessive lines

        # Add page separator
        page_header = f"\n\n----- PÁGINA {i + 1} -----\n\n"
        all_text.append(page_header + text)

    # Save text to .txt file
    try:
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(''.join(all_text))
        print(f"OCR completo! Texto guardado en {output_txt_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

    # Return the text
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
            result = process_document(pdf_path, output_txt_path, language=language)

            if result:
                print(f"Successfully processed: {os.path.basename(pdf_path)}")
            else:
                print(f"Failed to process: {os.path.basename(pdf_path)}")

        except Exception as e:
            print(f"Error processing {os.path.basename(pdf_path)}: {str(e)}")
            continue

    print(f"\n===== Batch processing complete! =====")


# Main execution
if __name__ == "__main__":
    # Specify the folder containing PDF files
    folder_path = r"/home/galen/Desktop/sitio_de_pruebas"

    # Check if tesseract is available
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version {version} is available!")
    except:
        print("Tesseract not found. Please install with:")
        print("sudo apt-get install tesseract-ocr tesseract-ocr-spa")
        exit(1)

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        exit(1)

    # Process all PDFs in the folder
    process_folder(folder_path)