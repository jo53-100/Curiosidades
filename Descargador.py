# Este programa pretende automatizar el proceso de descarga
# de archivos de algún sitio de internet

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Set up Chrome options for automatic downloads
DOWNLOAD_DIR = r"C:\Users\shipp\Desktop\Sitio de pruebas_descargador"  # Replace with your actual download path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Initialize WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)  # Set an explicit wait time for elements to load

# Define a function to automate input and download
def automate_input_and_download(input_file_path):
    # Open the target website
    driver.get("http://www.swisstargetprediction.ch/")  # Replace with the actual URL

    # Read the file contents if input is a file, otherwise treat it as text
    if os.path.isfile(input_file_path):  # Check if the input is a file path
        with open(input_file_path, 'r') as file:
            file_contents = file.read()
    else:
        file_contents = input_file_path  # Use input directly if it's not a file path

    # Find the input box and send the text content from the file
    input_box = wait.until(EC.presence_of_element_located((By.ID, "smilesBox")))  # Using ID as per your HTML example
    input_box.clear()  # Clear any existing text in the box
    input_box.send_keys(file_contents)  # Enter the text contents of the file

    # Find and click the submit button
    submit_button = driver.find_element(By.ID, "submitButton")  # Replace with actual button ID
    submit_button.click()

    # Wait for the download link to appear and click it
    download_link = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "buttons-csv")))  # Replace with actual download link ID
    download_link.click()

    # Wait a few seconds to ensure the download completes
    time.sleep(5)


def file_reader(folder):
    if not os.path.isdir(folder):
        print(f"{folder} no es un directorio válido")
        return

    # Toma el nombre del folder y crea uno nuevo con el sufijo '_descargas'
    folder_name = os.path.basename(os.path.normpath(folder))
    new_folder_name = f"{folder_name}_descargas"
    new_folder_path = os.path.join(os.path.dirname(folder), new_folder_name)

    # Crea un nuevo folder si no existe
    os.makedirs(new_folder_path, exist_ok=True)

    # Lista todos los archivos .smi en el folder
    files = [f for f in os.listdir(folder) if f.endswith('.smi')]

    if not files:
        print("No hay archivos .smi en el folder especificado.")
        return

    # Set up Chrome options for automatic downloads
    DOWNLOAD_DIR = new_folder_path  # Replace with your actual download path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)  # Set an explicit wait time for elements to load

    for file in files:
        file_path = os.path.join(folder, file)  # Get full path of each file
        automate_input_and_download(file_path)


smiles_folder = input('Pega la ruta del folder donde están los archivos .smi:').strip().strip('"').strip("'")
file_reader(smiles_folder)

# Close the browser when done
driver.quit()

