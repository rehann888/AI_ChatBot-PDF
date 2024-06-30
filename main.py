import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from htmltemplate import css, bot_template, user_template
import sentence_transformers  

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    st.write(f"sentence_transformers version: {sentence_transformers.__version__}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = Ollama(
        model="qwen2:1.5b",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
    )
    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    st.session_state.messages.append({"role": "user", "content": user_question})
    st.session_state.messages.append({"role": "assistant", "content": response['answer']})

def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.title("💬 ChatbotPDF AI")
    st.caption("🚀 projectby_reyhanterra;")


    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing"):
                    try:
                        raw_text = get_pdf_text(pdf_docs)

                        text_chunks = get_text_chunks(raw_text)

                        vectorstore = get_vectorstore(text_chunks)

                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.success("Documents processed successfully.")
                    except Exception as e:
                        st.error(f"Error processing documents: {e}")
            else:
                st.error("Please upload at least one PDF file.")

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if st.session_state.conversation:
        if user_question := st.chat_input("Ask a question about your documents:"):
            handle_userinput(user_question)
            st.session_state.chat_history.clear()

            for msg in st.session_state.messages[-2:]:
                st.chat_message(msg["role"]).write(msg["content"])

if __name__ == '__main__':
    main()
