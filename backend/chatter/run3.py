print("starting")

import local_secrets as secrets
import os

from llama_index import VectorStoreIndex, SimpleDirectoryReader


OPENAI_API_KEY = secrets.OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

print("loading director...")
documents = SimpleDirectoryReader("data_1").load_data()
print("directory loaded.")

# for document in documents:
for document in documents:
    print("===========================================================================")
    print(document.metadata["file_name"])
    print(document.text)
