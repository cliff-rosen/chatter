print('starting')

import local_secrets as secrets
import os

from llama_index import VectorStoreIndex, SimpleDirectoryReader


OPENAI_API_KEY = secrets.OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY


documents = SimpleDirectoryReader("data").load_data()

#for document in documents:
document = documents[0]
print(document.metadata['file_name'])