import math
import os
import re
import time
from collections import Counter

import numpy as np
import ollama
import streamlit as st
from pypdf import PdfReader


# ================= CONFIG =================
BASE_DIR = r"C:\Users\Himanshu\Downloads\chat_gpt"
PDF_DIR = BASE_DIR
STORE_DIR = os.path.join(BASE_DIR, "faiss_store")

CHUNKS_FILE = os.path.join(STORE_DIR, "chunks.npy")
META_FILE = os.path.join(STORE_DIR, "metadata.npy")

CHUNK_SIZE = 900
OVERLAP = 150
TOP_K = 2
FAST_MODEL = "qwen2.5:0.5b"
NUM_PREDICT = 180
CONTEXT_CHARS = 1600
# ==========================================


st.set_page_config(page_title="Offline PDF RAG", layout="wide")
os.makedirs(STORE_DIR, exist_ok=True)


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    pages = []
    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())
        if text:
            pages.append((text, page_no))
    return pages


def chunk_text(text, size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += size - overlap
    return chunks


@st.cache_resource(show_spinner="Loading PDF passages...")
def load_or_build_passages():
    if os.path.exists(CHUNKS_FILE) and os.path.exists(META_FILE):
        chunks = list(np.load(CHUNKS_FILE, allow_pickle=True))
        metadata = list(np.load(META_FILE, allow_pickle=True))
        return chunks, metadata, False

    chunks = []
    metadata = []
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]

    for pdf in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf)
        for page_text, page_no in extract_text_from_pdf(pdf_path):
            page_chunks = chunk_text(page_text)
            chunks.extend(page_chunks)
            metadata.extend({"pdf": pdf, "page": page_no} for _ in page_chunks)

    np.save(CHUNKS_FILE, np.array(chunks, dtype=object))
    np.save(META_FILE, np.array(metadata, dtype=object))
    return chunks, metadata, True


@st.cache_data(show_spinner=False)
def get_ollama_models():
    try:
        return [m.model for m in ollama.list().models]
    except Exception:
        return []


@st.cache_resource(show_spinner=False)
def warm_ollama_model(model_name):
    ollama.generate(
        model=model_name,
        prompt="ready",
        stream=False,
        keep_alive="10m",
        options={"num_predict": 1, "num_ctx": 512, "temperature": 0},
    )
    return True


@st.cache_data(show_spinner=False)
def passage_terms(chunks):
    return [Counter(tokenize(chunk)) for chunk in chunks]


def tokenize(text):
    return [t for t in re.findall(r"[a-zA-Z0-9]+", text.lower()) if len(t) > 2]


def retrieve_context(question, chunks, metadata, top_k=TOP_K, max_chars=CONTEXT_CHARS):
    query_terms = tokenize(question)
    if not query_terms:
        return ""

    query_counts = Counter(query_terms)
    chunk_term_counts = passage_terms(tuple(chunks))
    total_docs = max(1, len(chunks))

    document_frequency = Counter()
    for term_counts in chunk_term_counts:
        document_frequency.update(term_counts.keys())

    scored = []
    for idx, term_counts in enumerate(chunk_term_counts):
        score = 0.0
        for term, q_count in query_counts.items():
            tf = term_counts.get(term, 0)
            if tf:
                idf = math.log((1 + total_docs) / (1 + document_frequency[term])) + 1
                score += q_count * tf * idf
        if score:
            scored.append((score, idx))

    if not scored:
        scored = [(1.0, idx) for idx in range(min(top_k, len(chunks)))]

    scored.sort(reverse=True)
    context_blocks = []
    for _, idx in scored[:top_k]:
        meta = metadata[idx] if idx < len(metadata) else {}
        pdf = meta.get("pdf", "document")
        page = meta.get("page", "?")
        passage = str(chunks[idx])[:max_chars]
        context_blocks.append(f"[Source {len(context_blocks) + 1}: {pdf}, page {page}]\n{passage}")

    return "\n\n".join(context_blocks)


def extract_grounded_facts(context):
    facts = []
    line_patterns = [
        ("NHT Unit turndown", r"NHT Unit\s*:\s*([^\n\r]+)"),
        ("PENEX Unit turndown", r"PENEX Unit\s*:\s*([^\n\r]+)"),
        ("CCR Platforming Unit turndown", r"CCR Platforming Unit\s*:\s*([^\n\r]+)"),
    ]
    compact_patterns = [
        ("On-stream factor", r"on\s*-?\s*stream factor.*?(\d+\s*hours per annum)"),
        ("Operating cycle", r"minimum\s+operating\s+cycle\s+of\s+([^.\n\r]+)"),
        ("NHT design capacity/feed", r"NHT unit is designed to process\s+([^.\n\r]+)"),
        ("Contaminants removed", r"reduce contaminants such as\s+([^.\n\r]+)"),
        ("NHT splitter/routing", r"The hydrotreated\s+and stripped Naphtha.*?CCR platforming unit\."),
    ]

    for label, pattern in line_patterns:
        match = re.search(pattern, context, flags=re.IGNORECASE)
        if match:
            facts.append(f"- {label}: {match.group(1).strip()}")

    compact_context = " ".join(context.split())
    for label, pattern in compact_patterns:
        match = re.search(pattern, compact_context, flags=re.IGNORECASE)
        if match:
            facts.append(f"- {label}: {match.group(1).strip()}")

    return "\n".join(facts) if facts else "- No exact fact patterns extracted; use the source context directly."


def generate_answer(model_name, question, context):
    facts = extract_grounded_facts(context)
    prompt = f"""You are a precise PDF question-answering assistant.
Use ONLY the context below. The answer is likely present in the context.
Do not add outside knowledge.
Preserve technical names, numbers, units, and temperature ranges exactly as written.
Write a useful detailed answer in short bullets.
Cover the relevant points: overview, capacity/feed, purpose, routing, turndown/operating notes, and missing details.
Separate design capacity from turndown capacity. Do not merge them.
Include source references like [Source 1] for document facts.
If a specific detail is missing, write "Not specified in the provided context" only for that detail.
Use the extracted facts exactly. Do not change percentages or units.

Extracted exact facts:
{facts}

Context:
{context}

Question: {question}

Answer:"""

    response_stream = ollama.generate(
        model=model_name,
        prompt=prompt,
        stream=True,
        keep_alive="10m",
        options={
            "temperature": 0,
            "num_predict": NUM_PREDICT,
            "num_ctx": 2048,
            "top_k": 20,
            "top_p": 0.8,
        },
    )
    for chunk in response_stream:
        yield chunk.get("response", "")


chunks, metadata, built_now = load_or_build_passages()

st.title("Offline Enterprise PDF RAG")
st.caption("Fast local chat over your PDFs")

with st.sidebar:
    st.header("Model")
    models = get_ollama_models()
    if not models:
        st.error("Ollama is not running.")
        st.code("ollama serve")
        st.stop()

    default_model = FAST_MODEL if FAST_MODEL in models else models[0]
    model_name = st.selectbox("Select model", models, index=models.index(default_model))
    try:
        warm_ollama_model(model_name)
        st.success(f"Model ready: {model_name}")
    except Exception as exc:
        st.error(f"Ollama warm-up failed: {exc}")
        st.stop()

    if built_now:
        st.success(f"Index created: {len(chunks)} passages.")
    else:
        st.info(f"Index loaded: {len(chunks)} passages.")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if not chunks:
    st.warning(f"No PDF text found in {PDF_DIR}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question from all PDFs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    context = retrieve_context(prompt, chunks, metadata)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("Thinking..."):
                answer = ""
                for token in generate_answer(model_name, prompt, context):
                    answer += token
                    placeholder.markdown(answer + " |")
            answer = answer.strip() or "No response returned from Ollama."
            placeholder.markdown(answer)
        except Exception as exc:
            answer = f"Ollama error: {exc}"
            placeholder.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
