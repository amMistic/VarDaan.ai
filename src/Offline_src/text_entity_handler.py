from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from src.embedding_model import embedding_function
from datetime import datetime
import os

class ProcessPDF:
    def __init__(self, uploaded_pdfs=None) -> None:
        self.vector_store = None
        self.upload_files = uploaded_pdfs
        
    def extract_content(self, upload_files):
        for pdf in upload_files:
            reader = PdfReader(pdf)
            content = ''
            for page in reader.pages:
                content += page.extract_text()
        return content
    
    def get_vector_store(self, upload_files):
        # extract the content from the documents
        content = self.extract_content(upload_files)
        
        # split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            separators='\n'
        )
        chunks = splitter.split_text(content)
        
        UQID = datetime.now().strftime('%d%m%Y_%H%M%S')
        CHROMA = f'vecDatabase/PDFDatabase/chroma_{UQID}'
        os.makedirs(CHROMA,exist_ok=True)
        
        # perform embedding over chunks to converted into numerical data format and store that into vector store
        vector_store = Chroma.from_texts(
            chunks, embedding=embedding_function(), persist_directory=CHROMA
        )
        
        self.vector_store = vector_store
        return vector_store        
                
        
        
        