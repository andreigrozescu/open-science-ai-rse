import os
import json
import requests
from tqdm import tqdm

# Cargar configuración desde config.json
with open('scripts/config.json', 'r') as config_file:
    config = json.load(config_file)

GRODIB_URL = config.get("grobid_url", "http://localhost:8070/api/processFulltextDocument")

# Carpeta de entrada y salida
INPUT_DIR = 'papers'
OUTPUT_DIR = 'output'

# Asegúrate de que la carpeta de salida exista
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Función para enviar PDF a Grobid y recibir XML
def process_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        files = {'input': f}
        response = requests.post(GRODIB_URL, files=files)

    if response.status_code == 200:
        # Si la solicitud fue exitosa, obtenemos el XML
        return response.text
    else:
        # Si hubo un error, mostramos el código de error
        print(f"Error al procesar el archivo {pdf_path}: {response.status_code}")
        return None

# Procesar todos los PDFs en la carpeta papers
for pdf_file in tqdm(os.listdir(INPUT_DIR), desc="Procesando documentos"):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        
        # Llamar a Grobid para extraer el XML
        xml_content = process_pdf(pdf_path)

        if xml_content:
            # Guardar el contenido XML en un archivo en la carpeta output
            xml_filename = f"{os.path.splitext(pdf_file)[0]}.xml"
            xml_path = os.path.join(OUTPUT_DIR, xml_filename)

            with open(xml_path, 'w', encoding='utf-8') as xml_file:
                xml_file.write(xml_content)

            print(f"XML guardado en: {xml_path}")

