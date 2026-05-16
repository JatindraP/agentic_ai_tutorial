import yaml
from pathlib import Path
import os

RAG_PATH = Path(__file__).parent
YML_CONFIG_PATH = RAG_PATH/'config.yml'
RESOURCE_PATH = RAG_PATH/'resources'

# with open("config.yml", "r") as file:
#     data = yaml.safe_load(file)
# print(data)

def load_config():
    with open(YML_CONFIG_PATH, "r") as file:
        data = yaml.safe_load(file)
    return data

def get_pdf_path(doc:str):
    config = load_config()
    doc_path = RESOURCE_PATH/'pdf'/config['rag']['pdf'][doc]
    return doc_path

def get_config(*args):
    config = load_config()
    value = config
    for arg in args:
        value = value.get(arg)
        if value is None:
            raise KeyError(f"Key '{arg}' not found in the configuration.")
    return value

def get_word_path(doc:str):
    config = load_config()
    doc_path = RESOURCE_PATH/'word'/config['rag']['word'][doc]
    return doc_path

def get_project_base_path():
    return os.getcwd()



