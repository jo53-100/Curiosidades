##Esto pretende unir pdfs

import PyPDF2
import os

## Esto cuenta cuántas páginas tiene el pdf que se está manipulando
def get_pdf_pages(ruta_pdf):
    with open(ruta_pdf, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)
    return num_pages


def main():
    pdf_writer = PyPDF2.PdfWriter()
    print("Bienvenido al costurero de PDFs !!!")

    while True:
        # Se le pide al usuario un archivo
        ruta_pdf = input("Escribe la ruta al archivo PDF: ").strip().strip("'").strip('"')

        if not os.path.isfile(ruta_pdf):
            print("Archivo no encontrado, por favor escribe una ruta válida.")
            continue

        num_pages = get_pdf_pages(ruta_pdf)
        print(f"El archivo tiene {num_pages} páginas.")

        choice = input("¿Quieres incluir todo el archivo (todo) o especificar un rango de páginas (rango)?"
                       "(todo/rango): ").strip().lower()

        if choice == 'todo':
            with open(ruta_pdf, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    pdf_writer.add_page(page)
        elif choice == 'rango':
            page_range = input("Introduce los rangos que quieras unir (por ejemplo, 1-3, 5): ").strip()
            ranges = page_range.split(',')
            with open(ruta_pdf, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for r in ranges:
                    if '-' in r:
                        start, end = map(int, r.split('-'))
                        for i in range(start - 1, end):
                            pdf_writer.add_page(reader.pages[i])
                    else:
                        pdf_writer.add_page(reader.pages[int(r) - 1])
        else:
            print("Opción invalida, por favor escribe 'todo' o 'rango'.")
            continue

        # Ask if user wants to add more files
        another = input("¿Quieres agregar otro PDF? s/n : ").strip().lower()
        if another != 's':
            break

    # Save the combined PDF
    ruta_nueva = input("Escribe el nombre del nuevo pdf (por ejemplo: ejemplo.pdf) ").strip()
    with open(ruta_nueva, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"He cosido los archivos y los guardé en {ruta_nueva}!")


if __name__ == "__main__":
    main()
