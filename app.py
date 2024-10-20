from src.Online_src.Process_webText import OnlineSRC
from src.Offline_src.text_entity_handler import ProcessPDF
from src.Online_src.Process_youtube_video import ProcessYoutube
from langchain_core.messages import AIMessage, HumanMessage
from src.Handle_user import get_response
import streamlit as st
import re

def is_valid_url(URL):
    # Simple regex to validate a URL format
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,})|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # IPv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, URL) is not None

def main():
    st.set_page_config('VarDaan.ai')
    
    # Main content
    st.markdown("<h1 style='text-align: center; color: #ececf1;'>VarDaan.ai 🤖</h1>", unsafe_allow_html=True)
    
    # session variables
    if 'visible' not in st.session_state:
        st.session_state.visible = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
        AIMessage(content='Hi! I am BlogGPT. Your Personal Blog Assistant. How can I assist you today?')
        ]
    

    # side bar
    with st.sidebar:
        st.sidebar.markdown("### Enter the URL of the Text Entity or YouTube video Entity:")
        URL = st.text_input('Drop Entity URL')
        Upload_file = st.file_uploader('Drop PDF(s) here..', accept_multiple_files=True)
        
        if URL :
            if URL and is_valid_url(URL):
                if 'youtube.com' in URL:
                    st.warning("Processing a YouTube video might take a few minutes, please be patient.")
                    if 'vector_store' not in st.session_state or st.session_state.vector_store is None:
                        if st.button('Process'):
                            with st.spinner('Processing...'):
                                try:
                                    st.session_state.vector_store = ProcessYoutube().get_vector_store(URL)
                                except Exception as e:
                                    st.error(f"Error processing YouTube video: {e}")
                                    st.session_state.visible = False
                                else:
                                    st.session_state.visible = True
                else:
                    st.warning("Processing may take time depending on the content size, please be patient. ;)")
                    if 'vector_store' not in st.session_state or st.session_state.vector_store is None:
                        if st.button('Process'):
                            with st.spinner('Processing...'):
                                try:
                                    st.session_state.vector_store = OnlineSRC().get_vector_store(URL)
                                except Exception as e:
                                    st.error(f"Error processing URL: {e}")
                                    st.session_state.visible = False
                                else:
                                    st.session_state.visible = True
            else:
                st.error('Please Provide Valid URL!! (- _-)')

        elif Upload_file:
            st.warning("Processing may take time depending on the content size, please be patient.;)")
            if 'vector_store' not in st.session_state or st.session_state.vector_store is None:
                if st.button('Process'):
                    with st.spinner('Processing...'):
                        st.session_state.vector_store = ProcessPDF().get_vector_store(Upload_file)
                    st.session_state.visible = True


    # if conent is processed 
    if st.session_state.visible:
        user_query = st.chat_input('[o_o]: Ask me anything!!')
        
        if user_query:
            response = get_response(user_query, st.session_state.vector_store)
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=response))
            
            # Display chat messages
            for message in st.session_state.chat_history:
                if isinstance(message, AIMessage):
                    with st.chat_message("AI"):
                        st.write(message.content)
                elif isinstance(message, HumanMessage):
                    with st.chat_message("Human"):
                        st.write(message.content)
if __name__ == '__main__':
    main()