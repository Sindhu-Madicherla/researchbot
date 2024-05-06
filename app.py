import streamlit as st
import os
from io import StringIO
from ResearchBot.utils.common import *
from ResearchBot.variables.configs import Configs
from ResearchBot.components.response_synthesis import ResponseSynthesis
from ResearchBot.components.data_ingestion import DataIngestion

st.set_page_config(page_title="Research Bot",
                    page_icon='🤖'
                    # layout='centered',
                    # initial_sidebar_state='collapsed')
)


def embed_data(papers):
    with st.spinner(text="Fetching the data from arxiv and loading. This might take a while"):
        data_ingestion = DataIngestion(papers=papers)
        data_ingestion.main()


@st.cache_resource(show_spinner=False)
def load_data():
    if not os.listdir(Configs.articles_dir):
        st.write("No articles are uploaded. Please upload documents")
        
    with st.spinner(text="Loading and indexing the research docs – hang tight! This should take 1-2 minutes."):
        response_generator = ResponseSynthesis()
        return response_generator


# If a file is uploaded, or if articles directory is empty, create embeddings
uploaded_file = st.file_uploader("Upload Input file")
if uploaded_file or not os.path.exists(Configs.articles_dir) :
    if uploaded_file:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        papers = str(stringio.read()).rstrip('\r\n')
        embed_data(papers=papers)
    else :
        embed_data(papers=Configs.papers)
    
    print('Will embed asap !')
    # embed_data()
    
response_generator = load_data()
st.title("Research Bot 🤖")
if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question !"}
    ]        

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    

for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = response_generator.chat(user_query=prompt)
            st.write(response.content)
            message = {"role": "assistant", "content": response.content}
            st.session_state.messages.append(message) 

