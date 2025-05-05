import os
import xml.etree.ElementTree as ET

def rename_files_in_folder():
    # Pedir al usuario que introduzca la ruta de la carpeta, incluso si viene con comillas
    folder_path = input("Introduce la ruta de la carpeta donde están los archivos (puede incluir comillas): ")

    # Eliminar las comillas al principio y al final de la cadena, si las tiene
    folder_path = folder_path.strip('"').strip("'")

    # Convertir la ruta a formato raw string para manejar correctamente las barras invertidas
    folder_path = os.path.normpath(folder_path)

    # Pedir al usuario que introduzca el nombre a ignorar
    nombre_ignorado = input("Introduce el nombre a ignorar: ")

    # Verificar si la carpeta existe
    if not os.path.exists(folder_path):
        print(f"Error: La ruta especificada '{folder_path}' no existe.")
        return

    # Bandera para verificar si se encontró el nombre ignorado en algún archivo
    nombre_encontrado = False

    # Iterar sobre todos los archivos XML en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            xml_path = os.path.join(folder_path, filename)
            base_name = os.path.splitext(filename)[0]

            # Leer el archivo XML
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Inicializar variables para almacenar los nombres
            emisor_nombre = None
            receptor_nombre = None
            valor_total = None

            # Extraer 'Nombre' de <cfdi:Emisor> y <cfdi:Receptor>
            for elem in root.iter():
                if elem.tag.endswith('Emisor') and 'Nombre' in elem.attrib:
                    emisor_nombre = elem.attrib['Nombre']
                elif elem.tag.endswith('Receptor') and 'Nombre' in elem.attrib:
                    receptor_nombre = elem.attrib['Nombre']

            # Extraer 'Total' de <cfdi:Comprobante>
            for elem in root.iter():
                if elem.tag.endswith('Comprobante') and 'Total' in elem.attrib:
                    valor_total = elem.attrib['Total']

            # Verificar si el nombre ignorado aparece en el emisor o receptor
            if nombre_ignorado not in [emisor_nombre, receptor_nombre]:
                continue  # Si no está en este archivo, sigue con el siguiente archivo

            # Si llegamos aquí, significa que encontramos el nombre ignorado
            nombre_encontrado = True

            # Decidir el nombre a usar para renombrar
            if emisor_nombre == nombre_ignorado:
                character_to_find = receptor_nombre
            else:
                character_to_find = emisor_nombre

            if not character_to_find:
                print(f"No se encontró un 'Nombre' adecuado en {filename}.")
                continue

            # Tomar las primeras dos palabras del character_to_find
            character_to_find = ' '.join(character_to_find.split()[:2])

            # Construir los nuevos nombres de archivo
            new_xml_name = f"${valor_total}_{character_to_find}.xml"
            new_pdf_name = f"${valor_total}_{character_to_find}.pdf"

            # Verificar si ya existe un archivo con el nuevo nombre
            new_xml_path = os.path.join(folder_path, new_xml_name)
            if os.path.exists(new_xml_path):
                count = 1
                new_xml_path = os.path.join(folder_path, f"${valor_total}{character_to_find}{count}.xml")
                while os.path.exists(new_xml_path):
                    count += 1
                    new_xml_path = os.path.join(folder_path, f"${valor_total}{character_to_find}{count}.xml")

            # Renombrar el archivo XML
            os.rename(xml_path, new_xml_path)
            print(f"Renombrado XML: {filename} -> {new_xml_name}")

            # Renombrar el archivo PDF correspondiente
            old_pdf_path = os.path.join(folder_path, f"{base_name}.pdf")
            if os.path.exists(old_pdf_path):
                new_pdf_path = os.path.join(folder_path, new_pdf_name)
                if os.path.exists(new_pdf_path):
                    count = 1
                    new_pdf_path = os.path.join(folder_path, f"${valor_total}{character_to_find}{count}.pdf")
                    while os.path.exists(new_pdf_path):
                        count += 1
                        new_pdf_path = os.path.join(folder_path, f"${valor_total}{character_to_find}{count}.pdf")

                os.rename(old_pdf_path, new_pdf_path)
                print(f"Renombrado PDF: {base_name}.pdf -> {new_pdf_name}")
            else:
                print(f"No se encontró el PDF correspondiente para {base_name}.pdf en {folder_path}.")

    # Si no se encontró el nombre ignorado en ningún archivo, mostrar un error
    if not nombre_encontrado:
        print(f"Error: El nombre '{nombre_ignorado}' no se encontró en los archivos XML.")

# Llamada a la función
rename_files_in_folder()
