from PyPDF2 import PdfReader, PdfWriter
import os

def remove_metadata_and_compress(file_path):
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(file_path)

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    # Remove metadata
    pdf_writer.add_metadata({})

    # Attempt to compress the output PDF by reducing image quality (basic compression)
    pdf_writer._root_object.update({
        "/Filter": "/FlateDecode",
        "/BitsPerComponent": 1  # This will reduce image quality to make the file lighter
    })

    # Set the output file path with '_compressed' suffix
    output_file_path = os.path.splitext(file_path)[0] + "_compressed.pdf"

    # Write the output PDF
    with open(output_file_path, 'wb') as out_file:
        pdf_writer.write(out_file)

    print(f'Metadata removed and file compressed. Output saved to: {output_file_path}')

if __name__ == "__main__":
    # Prompt the user for a file path
    file_path = input('Introduce la ruta al archivo .PDF:').strip().strip('"').strip("'")

    # Process the file
    remove_metadata_and_compress(file_path)
