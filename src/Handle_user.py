from langchain.chains.retrieval import create_retrieval_chain
from langchain_groq import ChatGroq 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# load the environment variables
load_dotenv()

# Create the conversational RAG Pipeline
def RAG_conversational_chain(vector_store):
    
    # llm
    llm = ChatGroq(
        model_name = 'Llama3-8b-8192'
    )
    
    # retrieval
    retriever = vector_store.as_retriever()
    
    # prompt
    system_prompt = (
        "You are an intelligent assistant. Answer user queries based on the retrieved context. "
        "If the context answers the question, respond clearly. If not, admit you don't know, "
        "and suggest where to find more information. Be polite and relevant."
        "\n\nContext: {context}\n\nAnswer the user's query."
    )
    
    
    #chat prompt
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
    )
    
    # Combine the data sources and form coversational chain
    QA_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    
    # return rag
    return create_retrieval_chain(retriever, QA_chain)

def get_response(user_query: str, vector_store=None):
    
    # Build the conversational Chain
    RAG_chain = RAG_conversational_chain(vector_store)
    
    # process the query
    response = RAG_chain.invoke({
        'input' : user_query
    })
    
    return response.get('answer', "Sorry!! Can't address your current query :(").replace('Assistant:','').replace('assistant:','')