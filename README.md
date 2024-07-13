# AI ChatbotPDF

![](P.png)

## Project Description
ChatbotPDF AI is an application that allows users to upload multiple PDF documents and interact with a chatbot that can answer questions based on the contents of those documents.

## Main Features
- Uploading and processing multiple PDF documents.
- Splits text into smaller pieces for further processing.
- Converts text into embeddings using the `HuggingFaceEmbeddings` model.
- Stores the embedding in the `FAISS` vector store.
- Using the LLM model `Ollama` to manage interactive conversations.

## Technologies Used
- `Streamlit`: For the user interface.
- `PyPDF2`: For text extraction from PDF.
- `langchain`: For NLP and conversational memory management.
- `sentence-transformers`: For text embedding.
- `FAISS`: For embedding storage and quick search.

## How to Run the Project

### Prerequisites
- Python 3.7 or higher
- Virtual environment (optional but recommended)

### Usage Example

1. **Open the application**: Launch the application in a web browser by running `streamlit run main.py`.
   
2. **Upload PDF documents**: Use the sidebar to upload one or multiple PDF documents.

3. **Start processing**: Click the "Process" button to initiate the text extraction and embedding process.

4. **Ask questions**: In the chat section of the interface, type your questions related to the uploaded documents to receive answers based on their content.


