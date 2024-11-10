from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from src.embedding_model import embedding_function
from dotenv import load_dotenv
from datetime import datetime
import os

# # load all environmental variables
load_dotenv()

# # Initialize Pinecone
# api_key = str(os.getenv('PINECONE_API_KEY'))
# pinecone.init(api_key=api_key, environment="us-east-1")
# index_name = "vardaan-1o"

UQID = datetime.now().strftime('%d%m%Y_%H%M%S')
CHROMA = f'vecDatabase/BlogDatabase/chroma_{UQID}'
os.makedirs(CHROMA,exist_ok=True)

class OnlineSRC:
    def __init__(self) -> None:
        self.url = None
        self.document = None

    def extract_content(self, url:str):
        loader = WebBaseLoader(url)
        document = loader.load()
        return document
    
    def get_vector_store(self, url:str):
        self.url = url
        content = self.extract_content(url)
        
        # Initialize the Text Splitter correctly
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(content)
        
        vector_store = Chroma.from_documents(
            chunks, embedding_function(), persist_directory=CHROMA
        )
        self.vector_store = vector_store
        return vector_store
    