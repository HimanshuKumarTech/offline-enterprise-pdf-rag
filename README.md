# 📄 Offline Enterprise PDF RAG

> **A fully offline Retrieval-Augmented Generation (RAG) system for querying private PDF documents using local LLMs, FAISS, and Streamlit.**

---

## 📌 Overview

Offline Enterprise PDF RAG is a local AI-powered document question-answering system designed for organizations that need to search and understand private PDF documents without relying on cloud services.

The application indexes PDF documents, retrieves the most relevant passages using semantic search, and generates grounded answers using a locally running Ollama model.

Since the entire pipeline runs locally, no document content leaves the user's machine, making it suitable for confidential engineering documents, technical manuals, refinery documentation, SOPs, and enterprise knowledge bases.

---

## ✨ Features

* 📄 Local PDF document indexing
* 🔍 Fast document retrieval using FAISS (HNSW)
* 🤖 Local LLM inference using Ollama
* 💬 Interactive Streamlit chat interface
* 📚 Source document and page references
* ⚡ Local execution without cloud APIs
* 🔒 Privacy-first architecture
* 📦 Offline document storage
* 🔄 Persistent vector index
* 🛠 Easy model switching (Qwen, Phi-3, Llama)

---

## 🏗 Architecture

```text
                 PDF Documents
                       │
                       ▼
             Text Extraction
                       │
                       ▼
             Text Chunking
                       │
                       ▼
         Sentence Embeddings
                       │
                       ▼
             FAISS HNSW Index
                       │
      ┌───────────────────────────┐
      │      User Question        │
      └───────────────────────────┘
                       │
                       ▼
             Query Embedding
                       │
                       ▼
           Similarity Retrieval
                       │
                       ▼
          Relevant Document Chunks
                       │
                       ▼
          Ollama Local LLM
                       │
                       ▼
         Grounded AI Response
```

---

## 🛠 Technology Stack

| Component       | Technology                                 |
| --------------- | ------------------------------------------ |
| Frontend        | Streamlit                                  |
| Language        | Python                                     |
| PDF Reader      | pypdf                                      |
| Embedding Model | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector Database | FAISS (HNSW)                               |
| Local LLM       | Ollama                                     |
| Models          | qwen2.5, phi3:mini, llama3.1               |
| Storage         | NumPy + FAISS                              |

---

## 📂 Project Structure

```text
RAG/
│
├── app.py
├── requirements.txt
├── README.md
├── evaluation_report.json
│
├── faiss_store/
│   ├── index.faiss
│   ├── chunks.npy
│   └── metadata.npy
│
├── documents/
│   └── split-document.pdf
│
└── assets/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/HimanshuKumarTech/offline-enterprise-pdf-rag.git

cd offline-enterprise-pdf-rag
```

---

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download Ollama

https://ollama.com

Start Ollama

```bash
ollama serve
```

Download a model

```bash
ollama pull phi3:mini
```

or

```bash
ollama pull qwen2.5:0.5b
```

or

```bash
ollama pull llama3.1
```

---

## ▶ Running the Application

```bash
streamlit run app.py --server.port 8511
```

Open

```
http://localhost:8511
```

---

## 💬 Example Questions

* Explain Plant Turndown Capacity
* Explain Stream Hours and Turndown Ratio
* Explain NAPHTHA HYDROTREATER UNIT
* Explain PENEX UNIT
* Explain HOT OIL SYSTEM
* What is the operating cycle?
* Explain On Stream Factor.
* What is the design capacity of NHT?

---

## ⚙ Retrieval Pipeline

```text
User Question

↓

Sentence Embedding

↓

FAISS Search

↓

Top-K Document Chunks

↓

Prompt Construction

↓

Ollama

↓

Grounded Response
```

---

## 📊 Evaluation Results

| Metric                | Value        |
| --------------------- | ------------ |
| Model                 | qwen2.5:0.5b |
| Test Queries          | 5            |
| Top-K                 | 2            |
| Average Latency       | 8.18 sec     |
| P95 Latency           | 12.32 sec    |
| Recall@K              | 100%         |
| MRR                   | 1.00         |
| Numeric Hallucination | 0%           |
| Citation Accuracy     | 0%           |

---

## 🚀 Current Capabilities

* Local document indexing
* Local semantic retrieval
* Grounded response generation
* FAISS persistent index
* Model warm-up
* Chat history
* Multiple Ollama model support

---

## 🚧 Planned Improvements

* OCR support for scanned PDFs
* Token-based chunking
* Semantic embeddings (BGE)
* Cross-Encoder reranking
* Automatic citation formatting
* Multi-PDF indexing
* PDF upload support
* Export chat history
* Authentication
* Evaluation dashboard
* Latency monitoring
* Citation accuracy evaluation

---

## 🔒 Privacy

All processing happens locally.

* No cloud API calls
* No document uploads
* Local vector storage
* Local LLM inference
* Enterprise-friendly deployment

---

## 📈 Future Roadmap

* Enterprise RAG architecture
* OCR pipeline
* Hybrid retrieval
* Metadata enrichment
* LangChain integration
* REST API
* Docker deployment
* GPU optimization

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

## 📄 License

This project is intended for educational and enterprise research purposes.

---

## 👨‍💻 Author

**Himanshu Kumar**

Data Scientist | Software Engineer | Generative AI | Machine Learning | RAG | LLM Applications

---

⭐ If you found this project useful, consider giving it a star.
