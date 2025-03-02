# from grobid_client.grobid_client import GrobidClient
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import os
import numpy as np

# from wordcloud import WordCloud
import re


# FUNCS TO OBTAIN WORDCLOUD
def get_abstract(root):
    abstract = root.find(".//{http://www.tei-c.org/ns/1.0}abstract")
    ET.tostring(abstract, encoding="utf8").decode("utf8")
    paragraph = abstract.find(".//{http://www.tei-c.org/ns/1.0}p")
    abstract = paragraph.text
    return abstract


def wordcloud(root):
    abstract = get_abstract(root)
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate(abstract)
    return wordcloud


# FUNCS TO OBTAIN FIGURE HISTOGRAM
def count_figs(root, file_path):
    figs = root.findall(".//{http://www.tei-c.org/ns/1.0}figure")
    count = len(figs)
    file = file_path.replace("extracted\\", "")[2:-15]
    file_nfigs = [file, count]
    return file_nfigs


def figs_hist(file_nfigs):
    docs = [item[0] for item in file_nfigs]
    counts = [item[1] for item in file_nfigs]
    plt.figure(figsize=(10, 6))
    plt.bar(docs, counts)

    plt.xlabel("Archivo XML")
    plt.ylabel("Número de Figuras")
    plt.title("Número de Figuras por Archivo XML")
    plt.xticks(rotation=60)
    plt.xticks(fontsize=6)
    plt.tight_layout()
    if counts != []:
        plt.savefig("./extracted/imgs/FigHist/" + "hist" + ".png")


# FUNCS TO GET LINKS FROM EACH PAPER
def get_paper_links(root):
    links = []
    if root.text:
        links.extend(re.findall(r"https://\S+", root.text))
    for child in root:
        links.extend(get_paper_links(child))
        if child.tail:
            links.extend(re.findall(r"https://\S+", child.tail))
    return links


# FUNC TO REMOVE DATA FROM PREVIOUS EXECUTIONS
def remove_files(ruta):
    for root, dirs, files in os.walk(ruta):
        for archivo in files:
            ruta_completa = os.path.join(root, archivo)
            os.remove(ruta_completa)


# SIMILARITY METRIC
def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
