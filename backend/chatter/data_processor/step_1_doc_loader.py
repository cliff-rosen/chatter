from db import db
from utils.kb_service import add_document
import logging
from PyPDF2 import PdfReader
import os

logger = logging.getLogger()

def write_to_file(text):
    directory = 'outputs'
    dest = 'pages.txt'
    with open(os.path.join(directory, dest), 'a') as new_file:
        new_file.write(text)

def read_text_from_file(file_path):
    with open(file_path, 'r') as new_file:
        #clean_chunk = re.sub('\s+', ' ', chunk_text)
        #clean_chunk = clean_chunk.encode(encoding='ASCII',errors='ignore').decode()
        return new_file.read()

def read_text_from_pdf(filepath):
    print(filepath)
    page_text = ''

    try:
        reader = PdfReader(filepath)
    except Exception as e:
        print("error reading document", e)
        return

    doc_parts = []
    for page in reader.pages:
        text = page.extract_text()
        #text = text.encode(encoding='ASCII',errors='ignore').decode()
        doc_parts.append(text)
    page_text = "".join(doc_parts)
    return page_text

def run():
    filedir = 'data_processor/sources3/'
    domain_id = 1

    print('Starting job')

    files = os.listdir(filedir)
    for file in files:
        print('------------')
        print(f"processing file: {file}")
        doc_text = read_text_from_pdf(filedir + file)
        if add_document(domain_id, file, file, doc_text, doc_text):
            print("SUCCESS")
        else:
            print("FALIED TO ADD")

    print('Complete')

def go1():
    file = 'chatter/data_processor/sources/Vancomycin dosing in hemodialysis patients _ DoseMe Help Center.pdf'
    reader = PdfReader(file)
    with open('after.txt', 'w', encoding='utf-8') as new_file:
        new_file.write(text)
    for i in range(len(text)):
        print(i, text[i], ord(text[i]))
