import os
import requests
from bs4 import BeautifulSoup

# URL de Grobid en Docker
GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

def extract_text_from_pdf(pdf_path):
    """Envía un PDF a Grobid y devuelve el texto extraído."""
    with open(pdf_path, 'rb') as pdf_file:
        response = requests.post(GROBID_URL, files={'input': pdf_file}, data={'consolidateHeader': 1})
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "xml")
        return soup.get_text()
    else:
        print(f"Error procesando {pdf_path}")
        return None

# Carpeta de entrada y salida
pdf_folder = "papers/"
output_folder = "extracted_texts/"
os.makedirs(output_folder, exist_ok=True)

# Procesar todos los PDFs
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        extracted_text = extract_text_from_pdf(pdf_path)
        
        if extracted_text:
            output_file = os.path.join(output_folder, filename.replace(".pdf", ".txt"))
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"Texto extraído y guardado en {output_file}")

print("¡Extracción de textos completada!")
