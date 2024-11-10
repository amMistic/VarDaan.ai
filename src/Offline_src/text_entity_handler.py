import concurrent.futures
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from src.embedding_model import embedding_function
from datetime import datetime
import os

class ProcessPDF:
    def __init__(self, uploaded_pdfs=None) -> None:
        self.vector_store = None
        self.upload_files = uploaded_pdfs

    # Efficient text extraction using pdfplumber
    def extract_content(self, pdf_file):
        content = ''
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                content += page.extract_text()
        return content
 
    # Handle multiple files with threading
    def extract_content_threaded(self, upload_files):
        contents = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(self.extract_content, pdf): pdf for pdf in upload_files}
            for future in concurrent.futures.as_completed(future_to_file):
                pdf = future_to_file[future]
                try:
                    content = future.result()
                    contents.append(content)
                except Exception as e:
                    print(f"Error processing file {pdf}: {e}")
        return contents

    # Efficient PDF processing
    def get_vector_store(self, upload_files):
        # Extract content using threads
        contents = self.extract_content_threaded(upload_files)

        # Combine all contents into a single string
        full_content = " ".join(contents)

        # Efficient chunking
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100  # Adjust chunk overlap to reduce redundancy
        )
        chunks = splitter.split_text(full_content)

        # Unique ID for vector store
        UQID = datetime.now().strftime('%d%m%Y_%H%M%S')
        CHROMA = f'vecDatabase/PDFDatabase/chroma_{UQID}'
        os.makedirs(CHROMA, exist_ok=True)

        # Perform embedding and store the result in vector store
        vector_store = Chroma.from_texts(
            chunks, embedding=embedding_function(), persist_directory=CHROMA
        )
        self.vector_store = vector_store
        return vector_store
