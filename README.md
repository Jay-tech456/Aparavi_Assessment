Here’s a solid draft for your `README.md` that reflects your current architecture, with clear iteration steps, tool usage, and an honest caveat about the work-in-progress nature of the project:

---

# 🧠 Multi-Agent PDF Reasoning System (WIP)

> ⚠️ **Note:** This is not a completed product. This repository contains the first working iteration of a multi-agent architecture built for intelligent querying and reasoning over unstructured PDF data.

---

## 🛠️ Summary

This project implements a **two-agent system** designed to process unstructured PDF documents, build a vector-based semantic representation, and provide queryable insights using a lightweight large language model (Mistral 7B).

---

## ✅ First Iteration (Agent 1)

### 📥 PDF Intake + Reasoning Engine

The first agent receives a raw PDF input and determines the appropriate pipeline based on the content:

* **PDFTextExtractor** – Parses text directly from the PDF.
* **PDFOCRExtractor** – Invoked when scanned/image-based documents are detected (via heuristic or failure fallback).
* **Nomic Embedding** – Embeds chunked document text for vectorization.
* **Pinecone Vector Store** – Stores embedded document chunks for fast semantic retrieval.
* **Tree-of-Thoughts Prompting** – Used to guide LLM reasoning and chunk filtering.
* **LLM Used** – [Mistral 7B](https://mistral.ai/) via API for scalable local-style LLM use.

This agent **decides** whether OCR is needed and preprocesses the data accordingly before passing it into the vector store.

---

## 🤖 Second Agent (Agent 2)

### 🔎 Query Understanding & Knowledge Graph Reasoning

This agent is invoked post-vectorization and handles:

* **Semantic Query Matching** – Pulls relevant document chunks from the Pinecone index.
* **Knowledge Graph Construction** – Builds structured entities and relationships from text.
* **LLM Response Generation** – Generates natural language answers grounded in the indexed data using Mistral 7B.
* Designed to answer **context-specific** queries about the document (e.g. policies, dates, summaries, etc).

---

## 📚 Stack

* **Python**
* **LangChain**
* **Pinecone**
* **Nomic Embedding**
* **Mistral 7B API**
* **Tree of Thoughts Prompting**
* **fitz (PyMuPDF), PIL, pytesseract** (for OCR PDF handling)

---

## 🚧 Roadmap

* [ ] Add retry/fallback logic on OCR engine
* [ ] Improve semantic chunking & memory management
* [ ] Add tracing/logging on agent decision paths
* [ ] Add front-end interface for document upload + chat
* [ ] Support multiple documents in a single session

---

## 🙋‍♂️ Why?

This project aims to create a **cost-efficient**, **LLM-integrated**, and **agentic pipeline** for extracting insights from dense business documents, contracts, or reports that are traditionally opaque or scanned.

---

Let me know if you'd like this exported as a `README.md` file or formatted differently (bullet-heavy, academic, etc).
