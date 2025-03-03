
# Document Processing and Analysis Script

## Description
This Python script is designed to process a set of PDFs, extract relevant information, and generate visualizations based on the extracted data. The script performs the following tasks:

1. **Process PDF files** using Grobid to extract metadata and abstracts.
2. **Generate a keyword word cloud** from the extracted abstracts.
3. **Count and visualize the number of figures** in each article.
4. **Extract and save links** found within the bibliographic structure of each article.

## Tools Used
- **requests**: To interact with the Grobid API for PDF processing.
- **xml.etree.ElementTree**: To parse and work with XML documents.
- **matplotlib**: For creating visualizations (word cloud and bar chart).
- **wordcloud**: For generating the word cloud.
- **tqdm**: For displaying a progress bar during the processing of files.

## Steps:

### 1. **Load Configuration**
The script first loads configuration settings from a `config.json` file. The configuration contains the URL for the Grobid API and the directories for input, output, and results.

```python
with open('scripts/config.json', 'r') as config_file:
    config = json.load(config_file)

GRODIB_URL = config.get("grobid_url", "http://localhost:8070/api/processFulltextDocument")
```

#### Verification:

To verify this step, I checked that the `config.json` file was loaded correctly by manually inspecting the settings. Additionally, I printed the `GRODIB_URL` to ensure that it was being read from the configuration file properly.


### 2. **Process PDF Files**
The script processes each PDF file in the `papers` folder, sending each one to the Grobid service to extract metadata and abstracts. The extracted XML content is saved in the `output` directory.

```python
def process_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        files = {'input': f}
        response = requests.post(GRODIB_URL, files=files)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error al procesar el archivo {pdf_path}: {response.status_code}")
        return None
```
#### Verification:

For verification, I manually checked the output directory to ensure that the XML files were being generated for each processed PDF. I also verified the response status code to confirm that the PDFs were successfully processed by Grobid.


### 3. **Generate Word Cloud**
Once the XML files are saved, the script parses them to extract abstracts. It concatenates the text of all abstracts to generate a word cloud. The word cloud is then saved as an image in the `results` directory.

```python
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
        print("Nube de palabras clave generada.")
```

#### Verification:

I verified the word cloud generation by manually inspecting the results directory for the wordcloud.png file.


### 4. **Count and Visualize the Number of Figures**
The script then counts the number of figures in each article by parsing the XML files and finding `tei:figure` elements. A bar chart is created to visualize the number of figures per article, which is saved in the `results` directory.

```python
def count_figures():
    figures_count = {}
    for xml_file in os.listdir(OUTPUT_DIR):
        if xml_file.endswith(".xml"):
            tree = ET.parse(os.path.join(OUTPUT_DIR, xml_file))
            root = tree.getroot()
            figures = root.findall('.//tei:figure', {'tei': 'http://www.tei-c.org/ns/1.0'})
            figures_count[xml_file] = len(figures)
    
    if figures_count:
        labels = ['
'.join(textwrap.wrap(label.replace(".xml", ""), 20)) for label in figures_count.keys()]
        plt.bar(range(len(figures_count)), list(figures_count.values()), align='center')
        plt.xticks(range(len(figures_count)), labels, rotation=90)
        plt.tight_layout()
        plt.title("Number of Figures per Article")
        plt.savefig(os.path.join(RESULTS_DIR, "figures_count.png"), format='png')
        plt.close()
        print("Visualización del número de figuras generada.")
```


### 5. **Extract and Save Links**
Finally, the script extracts URLs from the bibliographic structures in each XML file. These URLs are saved in a text file in the `results` directory.

```python
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
            f.write(f'Articulo: {article}
Links: {" ".join(urls)}

')
    print("Lista de enlaces extraída y guardada.")
```

#### Verification:

I verified the extracted links by manually inspecting the `extracted_links.txt` file and cross-referencing the URLs with those present in the XML files.


## Final Steps:
The functions `generate_wordcloud()`, `count_figures()`, and `extract_links()` are executed to process the data and generate the desired results.

```python
generate_wordcloud()
count_figures()
extract_links()

print("Procesamiento completo.")
```

## Files Generated:
- **wordcloud.png**: A word cloud image showing the most common words in the abstracts.
- **figures_count.png**: A bar chart showing the number of figures in each article.
- **extracted_links.txt**: A text file containing a list of URLs found in each article.
