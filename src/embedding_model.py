from langchain_huggingface import HuggingFaceEmbeddings

def embedding_function():
    model_name = 'sentence-transformers/all-mpnet-base-v2'
    embedding = HuggingFaceEmbeddings(model_name=model_name)
    return embedding