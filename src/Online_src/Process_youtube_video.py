# import dependencies
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma
from src.embedding_model import embedding_function
from dotenv import load_dotenv
from datetime import datetime
import os
import re


# load environmental variable
load_dotenv()

class ProcessYoutube:
    def __init__(self, URL:str):
        self.URL = URL
        self.content = None
        self.vector_store = None
        

    # Function to extract the id from URL
    def get_video_ID(self, URL:str):
        IDs= URL.split('=')
        return str(IDs[1])


    # Function: To get transcription of video 
    def extract_content(self, URL:str):
        # Replace with your YouTube video ID
        video_id = self.get_video_ID(URL)

        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Print the transcript
        for entry in transcript:
            self.content += f"{entry['start']:.2f}s: {entry['text']}\n"
        
        
    # convert into chunks
    def split_into_chunks(self):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )
        return splitter.split_text(self.content)


    # get the vector store
    def get_vector_store(self, URL:str):
        
        # extract content
        self.extract_content(URL)
        
        # chunks
        chunks = self.split_into_chunks()
        
        # unique id for each 
        UQID = datetime.now().strftime('%d%m%Y_%H%M%S')
        CHROMA = f'vecDatabase/VideoDatabase/Chroma_{UQID}'
        os.makedirs(CHROMA, exist_ok=True)
        
        vector_store = Chroma.from_texts(
            self.content, embedding=embedding_function(), persist_directory=CHROMA
        )
        
        self.vector_store = vector_store
        return vector_store
        
    