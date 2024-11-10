# VarDaan.ai 🤖

**VarDaan.ai** is an AI-powered platform that transforms any web content—be it blogs, articles, YouTube videos, or PDF documents—into a chatbot that users can interact with. By providing a URL or uploading a file, you can ask natural language questions about the content and receive accurate, contextually relevant answers in real-time.

## Features

- **Web Content as Chatbots**: Turn any web page, blog, or article into an interactive chatbot.
- **YouTube Video Chatbot**: Input a YouTube video URL and ask questions based on video content.
- **PDF Support**: Upload PDF files and generate an AI chatbot to query the content.
- **Conversational AI**: Powered by advanced natural language processing models that provide accurate answers based on the context.
- **Simple User Interface**: Easy-to-use web interface that allows users to engage with different types of content seamlessly.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)

## Installation

### Prerequisites
Make sure you have the following installed:
- **Python 3.8+**
- **pip** (Python package installer)
- **Git**

### Steps to Install and Run VarDaan.ai Locally

1. **Clone the Repository**  
   Open your terminal and run the following command to clone the repository:
   ```bash
   git clone https://github.com/amMistic/vardaan.ai.git
   ```

2. **Navigate to the Project Directory**  
   Move into the project folder:
   ```bash
   cd vardaan-ai
   ```

3. **Install Dependencies**  
   Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**  
   Create a `.env` file in the root directory and add the necessary environment variables (like API keys). Example:
   ```bash
   PINECONE_API_KEY=<your_pinecone_api_key>
   HUGGINGFACE_API_TOKEN=<your_api_token>
   ```

5. **Run the Application**  
   Start the VarDaan.ai application using Streamlit:
   ```bash
   streamlit run app.py
   ```

6. **Access the App**  
   Open your web browser and navigate to the local server link provided by Streamlit (usually `http://localhost:8501`).

## Usage

1. **Web Interface**: Once the app is running, you will see a simple input field for URLs or file uploads (PDFs).
2. **Enter Content**:
   - **For blogs/articles**: Enter the URL of the blog or article.
   - **For YouTube videos**: Enter the YouTube video URL.
   - **For PDFs**: Upload the PDF document directly into the app.
3. **Interactive Chat**: After processing the content, you can ask questions in the chat interface, and VarDaan.ai will respond based on the content provided.

### Example Commands (Future Task)
- **Blog/Article**: `vardaan.ai.http://example.com/blog-post`
- **YouTube Video**: `vardaan.ai.youtube.com/watch?v=example-video`
- **PDF**: Drag and drop a PDF document into the interface.

## Project Structure

```bash
vardaan-ai/
│
├── app.py                   # Main application entry point
├── src/                     # Source code
│   ├── Online_src/           # Web content and YouTube processing
│   ├── Offline_src/          # PDF handling
│   ├── Handle_user.py        # Handles user queries and responses
│   ├── embedding_model.py    # Embedding logic for vector storage
├── vecDatabase/             # Stores vectorized representations of content
├── requirements.txt         # List of Python dependencies
└── README.md                # Project documentation
```

## How It Works

![image](https://github.com/user-attachments/assets/f7a3ae66-278b-4c3d-882a-c36ff20bf976)

1. **Extracting Content**:
   - **Web Content**: VarDaan.ai fetches and processes text from web pages or articles using web scraping methods.
   - **YouTube**: The app uses YouTube's transcript API to extract the spoken text from videos.
   - **PDF**: For PDF files, VarDaan.ai extracts the textual content and splits it into manageable chunks.

2. **Processing & Storage**:
   - The content is split into smaller text chunks.
   - Each chunk is embedded using a pre-trained NLP model, converting the text into a vector format.
   - These vectors are stored in a vector database (Chroma) for efficient querying.

3. **Conversational Queries**:
   - When the user asks a question, VarDaan.ai retrieves relevant information from the vector store.
   - The retrieval system uses advanced language models to generate appropriate, context-aware responses.

## Tech Stack

- **Python**: Core programming language
- **Streamlit**: Web interface framework
- **LangChain**: Used for managing document chains and information retrieval
- **Chroma**: For vector storage and search capabilities
- **Hugging Face Models**: Provides the embeddings for text representation
- **YouTube Transcript API**: Used to fetch video transcripts
- **PyPDF2**: For handling PDF text extraction

## Contributing

I welcome contributions from the community! To get started:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add a new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a pull request on GitHub.
   ```bash
   git pull origin feature/your-feature-name
   ```
