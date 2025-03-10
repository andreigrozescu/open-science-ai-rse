import os
import json
import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import textwrap
from wordcloud import WordCloud
from tqdm import tqdm

# Load configuration from config.json
with open('scripts/config.json', 'r') as config_file:
    config = json.load(config_file)

GRODIB_URL = config.get("grobid_url", "http://localhost:8070/api/processFulltextDocument")

# Input and output directories
INPUT_DIR = 'papers'
OUTPUT_DIR = 'output'
RESULTS_DIR = 'results'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Function to send PDFs to Grobid and receive XML
def process_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        files = {'input': f}
        response = requests.post(GRODIB_URL, files=files)

    if response.status_code == 200:
        # If the request was successful, retrieve the XML content
        return response.text
    else:
        # If there was an error, display the error code
        print(f"Error processing file {pdf_path}: {response.status_code}")
        return None

# Process all PDFs in the papers directory
for pdf_file in tqdm(os.listdir(INPUT_DIR), desc="Processing documents"):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        
        # Call Grobid to extract the XML
        xml_content = process_pdf(pdf_path)

        if xml_content:
            # Save the XML content in a file in the output directory
            xml_filename = f"{os.path.splitext(pdf_file)[0]}.xml"
            xml_path = os.path.join(OUTPUT_DIR, xml_filename)

            with open(xml_path, 'w', encoding='utf-8') as xml_file:
                xml_file.write(xml_content)

            print(f"XML saved in: {xml_path}")

# Generate the keyword cloud
def generate_wordcloud():
    all_text = ""
    for xml_file in os.listdir(OUTPUT_DIR):
        if xml_file.endswith(".xml"):
            tree = ET.parse(os.path.join(OUTPUT_DIR, xml_file))
            root = tree.getroot()
            abstracts = root.findall('.//tei:abstract', {'tei': 'http://www.tei-c.org/ns/1.0'})
            
            for abstract in abstracts:
                div = abstract.find('tei:div', {'tei': 'http://www.tei-c.org/ns/1.0'})
                if div is not None:
                    p = div.find('tei:p', {'tei': 'http://www.tei-c.org/ns/1.0'})
                    if p is not None and p.text:
                        all_text += p.text + " "
    
    if all_text:
        wordcloud = WordCloud(width=800, height=800, background_color='white').generate(all_text)
        plt.figure(figsize=(8, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title("Keyword Cloud")
        plt.savefig(os.path.join(RESULTS_DIR, "wordcloud.png"), format='png')
        plt.close()
        print("Keyword cloud generated.")
    else:
        print("No abstracts found to generate the word cloud.")

# Count and visualize the number of figures per article 
def count_figures():
    figures_count = {}
    for xml_file in os.listdir(OUTPUT_DIR):
        if xml_file.endswith(".xml"):
            tree = ET.parse(os.path.join(OUTPUT_DIR, xml_file))
            root = tree.getroot()
            figures = root.findall('.//tei:figure', {'tei': 'http://www.tei-c.org/ns/1.0'})
            figures_count[xml_file] = len(figures)
    
    if figures_count:
        labels = ['\n'.join(textwrap.wrap(label.replace(".xml", ""), 20)) for label in figures_count.keys()]
        plt.bar(range(len(figures_count)), list(figures_count.values()), align='center')
        plt.xticks(range(len(figures_count)), labels, rotation=90)
        plt.tight_layout()
        plt.title("Number of Figures per Article")
        plt.savefig(os.path.join(RESULTS_DIR, "figures_count.png"), format='png')
        plt.close()
        print("Figure count visualization generated.")
    else:
        print("No figures found in the articles.")

# Extract and save links from each paper
def extract_links():
    links = {}
    for xml_file in os.listdir(OUTPUT_DIR):
        if xml_file.endswith(".xml"):
            tree = ET.parse(os.path.join(OUTPUT_DIR, xml_file))
            root = tree.getroot()
            biblStructs = root.findall('.//tei:biblStruct', {'tei': 'http://www.tei-c.org/ns/1.0'})
            url_list = []
            for biblStruct in biblStructs:
                ptr = biblStruct.find('.//tei:ptr', {'tei': 'http://www.tei-c.org/ns/1.0'})
                if ptr is not None and 'target' in ptr.attrib:
                    url_list.append(ptr.attrib['target'])
            links[xml_file] = url_list
    
    with open(os.path.join(RESULTS_DIR, "extracted_links.txt"), "w") as f:
        for article, urls in links.items():
            f.write(f'Article: {article}\nLinks: {" ".join(urls)}\n\n')
    print("List of extracted links saved.")

# Execute functions
generate_wordcloud()
count_figures()
extract_links()

print("Processing complete.")

