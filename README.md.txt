<<<<<<< HEAD
# RAG-Based PDF Question Answering System

This project is a Retrieval-Augmented Generation (RAG) application that allows users to ask questions from PDF documents and receive answers based on the document content. It extracts text from PDFs, converts the text into embeddings, stores them in a FAISS vector index, retrieves the most relevant chunks for a question, and uses a local Ollama language model to generate the final answer.

## Features

- PDF text extraction using `pypdf`
- Text chunking for better retrieval
- Embedding generation using Sentence Transformers
- Fast semantic search using FAISS
- Local LLM response generation using Ollama
- Streamlit-based chat interface
- Private document processing on the local system

## Tech Stack

- Python
- Streamlit
- Ollama
- FAISS
- Sentence Transformers
- NumPy
- pypdf

## Project Structure

```text
AI-Tutor-main/
├── app.py
├── requirements.txt
├── README.md
└── tests/
```

## How It Works

1. PDF files are read from the configured local folder.
2. Text is extracted from each PDF page.
3. Extracted text is split into smaller chunks.
4. Each chunk is converted into a vector embedding.
5. Embeddings are stored in a FAISS index.
6. When the user asks a question, the question is also converted into an embedding.
7. FAISS retrieves the most relevant PDF chunks.
8. Retrieved chunks are sent to an Ollama model as context.
9. The generated answer is displayed in the Streamlit chat interface.

## Requirements

Install the required Python packages using:

```powershell
pip install -r requirements.txt
```

You also need Ollama installed on your system.

## Setup and Run

1. Open PowerShell and go to the project folder:

```powershell
cd D:\AI-Tutor-main
```

2. Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Start Ollama in another PowerShell window:

```powershell
ollama serve
```

5. Pull a model if not already installed:

```powershell
ollama pull llama3
```

6. Run the Streamlit application:

```powershell
streamlit run app.py
```

7. Open the application in a browser:

```text
http://localhost:8501
```

## PDF Folder Configuration

The current application reads PDF files from this folder:

```python
BASE_DIR = r"D:\chat_gpt"
```

Place your PDF files in that folder, or update `BASE_DIR` in `app.py` to match your preferred PDF location.

## Main File

The main file of this project is:

```text
app.py
```

Run it using Streamlit:

```powershell
streamlit run app.py
```

## Limitations

- The PDF folder path is currently hardcoded.
- First-time indexing may take time for large PDF collections.
- Answer quality depends on PDF text extraction quality and the selected Ollama model.
- Ollama must be running before asking questions in the app.

## Future Improvements

- Add PDF upload support from the Streamlit interface
- Make the PDF folder configurable from the UI
- Add support for deleting or refreshing indexed documents
- Improve source citation display in answers
- Add user-friendly error handling for missing models or empty PDF folders

=======
# RAG-Based PDF Question Answering System

This project is a Retrieval-Augmented Generation (RAG) application that allows users to ask questions from PDF documents and receive answers based on the document content. It extracts text from PDFs, converts the text into embeddings, stores them in a FAISS vector index, retrieves the most relevant chunks for a question, and uses a local Ollama language model to generate the final answer.

## Features

- PDF text extraction using `pypdf`
- Text chunking for better retrieval
- Embedding generation using Sentence Transformers
- Fast semantic search using FAISS
- Local LLM response generation using Ollama
- Streamlit-based chat interface
- Private document processing on the local system

## Tech Stack

- Python
- Streamlit
- Ollama
- FAISS
- Sentence Transformers
- NumPy
- pypdf

## Project Structure

```text
AI-Tutor-main/
├── app.py
├── requirements.txt
├── README.md
└── tests/
```

## How It Works

1. PDF files are read from the configured local folder.
2. Text is extracted from each PDF page.
3. Extracted text is split into smaller chunks.
4. Each chunk is converted into a vector embedding.
5. Embeddings are stored in a FAISS index.
6. When the user asks a question, the question is also converted into an embedding.
7. FAISS retrieves the most relevant PDF chunks.
8. Retrieved chunks are sent to an Ollama model as context.
9. The generated answer is displayed in the Streamlit chat interface.

## Requirements

Install the required Python packages using:

```powershell
pip install -r requirements.txt
```

You also need Ollama installed on your system.

## Setup and Run

1. Open PowerShell and go to the project folder:

```powershell
cd D:\AI-Tutor-main
```

2. Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Start Ollama in another PowerShell window:

```powershell
ollama serve
```

5. Pull a model if not already installed:

```powershell
ollama pull llama3
```

6. Run the Streamlit application:

```powershell
streamlit run app.py
```

7. Open the application in a browser:

```text
http://localhost:8501
```

## PDF Folder Configuration

The current application reads PDF files from this folder:

```python
BASE_DIR = r"D:\chat_gpt"
```

Place your PDF files in that folder, or update `BASE_DIR` in `app.py` to match your preferred PDF location.

## Main File

The main file of this project is:

```text
app.py
```

Run it using Streamlit:

```powershell
streamlit run app.py
```

## Limitations

- The PDF folder path is currently hardcoded.
- First-time indexing may take time for large PDF collections.
- Answer quality depends on PDF text extraction quality and the selected Ollama model.
- Ollama must be running before asking questions in the app.

## Future Improvements

- Add PDF upload support from the Streamlit interface
- Make the PDF folder configurable from the UI
- Add support for deleting or refreshing indexed documents
- Improve source citation display in answers
- Add user-friendly error handling for missing models or empty PDF folders

>>>>>>> 2377e52cfb54d142fedc39fcdbcb518227878bef
