#Este es un script que necesitaba felipe, checa unos valores en el formato .xml del sat y modifica los nombres de archivos

import os
import xml.etree.ElementTree as ET

def rename_files_in_folder(folder_path, specified_emisor):
    # Iterate over all XML files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            xml_path = os.path.join(folder_path, filename)
            base_name = os.path.splitext(filename)[0]

            # Read the XML file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Initialize variables to store the names
            emisor_nombre = None
            receptor_nombre = None

            # Extract 'Nombre' from <cfdi:Emisor> and <cfdi:Receptor> elements
            for elem in root.iter():
                if elem.tag.endswith('Emisor') and 'Nombre' in elem.attrib:
                    emisor_nombre = elem.attrib['Nombre']
                elif elem.tag.endswith('Receptor') and 'Nombre' in elem.attrib:
                    receptor_nombre = elem.attrib['Nombre']

            #Verifica que el nombre a ignorar aparezca en la factura
            if nombre_ignorado not in [emisor_nombre, receptor_nombre]:
                print(f"'{nombre_ignorado}' no está en {filename}.")
                continue

            # Extract 'Total' from <cfdi:Comprobante> element
            for elem in root.iter():
                if elem.tag.endswith('Comprobante') and 'Total' in elem.attrib:
                    valor_total = elem.attrib['Total']

            # Determine the correct name to use for renaming
            if emisor_nombre == specified_emisor:
                character_to_find = receptor_nombre
            else:
                character_to_find = emisor_nombre

            if not character_to_find:
                print(f"Ningún nombre adecuado encontrado en {xml_path}.")
                continue

            # Extract the first two words from the character_to_find
            character_to_find = ' '.join(character_to_find.split()[:2])

            # Construct new file names with '$valor_total' first, followed by the name
            new_xml_name = f"${valor_total}_{character_to_find}.xml"
            new_pdf_name = f"${valor_total}_{character_to_find}.pdf"

            # Check if the new XML filename already exists
            new_xml_path = os.path.join(folder_path, new_xml_name)
            if os.path.exists(new_xml_path):
                count = 1
                new_xml_path = os.path.join(folder_path, f"${valor_total}_{character_to_find}_{count}.xml")
                while os.path.exists(new_xml_path):
                    count += 1
                    new_xml_path = os.path.join(folder_path, f"${valor_total}_{character_to_find}_{count}.xml")

            # Rename the XML file
            os.rename(xml_path, new_xml_path)
            print(f"XML renombrado: {filename} -> {new_xml_name}")

            # Look for the corresponding PDF file
            old_pdf_path = os.path.join(folder_path, f"{base_name}.pdf")
            if os.path.exists(old_pdf_path):
                new_pdf_path = os.path.join(folder_path, new_pdf_name)
                # Check if the new PDF filename already exists
                if os.path.exists(new_pdf_path):
                    count = 1
                    new_pdf_path = os.path.join(folder_path, f"${valor_total}{character_to_find}_{count}.pdf")
                    while os.path.exists(new_pdf_path):
                        count += 1
                        new_pdf_path = os.path.join(folder_path, f"${valor_total}{character_to_find}_{count}.pdf")

                os.rename(old_pdf_path, new_pdf_path)
                print(f"PDF renombrado: {base_name} -> {new_pdf_name}")
            else:
                print(f"No existe un PDF que coincida con {base_name} en {folder_path}.")

# Example usage
folder_path = input('Introduce la ruta a la carpeta con los archivos .xml .pdf:').strip().strip('"').strip("'")
nombre_ignorado = input('Introduce el nombre a ignorar:').strip()

rename_files_in_folder(folder_path, nombre_ignorado)