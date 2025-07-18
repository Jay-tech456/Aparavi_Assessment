The `README.md` that reflects my current architecture, with clear iteration steps, tool usage, and an honest caveat about the work-in-progress: 

---

# 🧠 Multi-Agent PDF Reasoning System (WIP)

> ⚠️ **Note:** This is not a completed product. This repository contains the first working iteration of a multi-agent architecture built for intelligent querying and reasoning over unstructured PDF data within the 24 hour threshold

---

## 🛠️ Summary

This project implements a **two-agent system** designed to process unstructured PDF documents, build a vector-based semantic representation, and provide queryable insights using a lightweight large language model (Mistral 7B).

---
# Overview



<img width="2400" height="1686" alt="image" src="https://github.com/user-attachments/assets/07b20f5e-b3c2-4d39-afa4-2bffa6f64afe" />
Current State of the Application's Frontend


## Objective 
This project aims to process and understand unsorted data from PDF documents.

## Data Content

PDF files may contain:

- **Document elements:**  
  - Objects (e.g., company logo)  
  - Text (e.g., company information)  
  - Page numbers

- **Images containing:**  
  1. Text  
  2. Objects
 
## Higher Level Reference Diagram 
<img width="2518" height="1174" alt="image" src="https://github.com/user-attachments/assets/52253a51-fc7b-4176-b736-27b06186642d" />
## System Flow

As per the requirements, there are two agents involved in the pipeline:

1. **OCR Agent** – Handles unstructured datasets using an OCR engine.
2. **Query Agent** – Processes standard user queries.

The frontend sends a POST request, and the API Gateway routes the request based on whether we need to **construct** or **read from** the knowledge graph.

If the user attaches a PDF, the first service (OCR Agent) is triggered.

Below are the two development phases I went through:

- **Phase 1:** A non-optimal initial solution that lacked dynamic decision-making and relied solely on basic extraction.
- **Phase 2:** An improved system leveraging Natural Language Processing to invoke appropriate tools and apply decision-making capabilities to build and interact with the knowledge graph.


The second agent uses a standard Retrieval-Augmented Generation (RAG) pipeline with agentic AI, where it gathers and indexes data to handle queries from the end user. The model then responds with relevant information.


## OCR Agent Workflow - Agent #1

1. **Phase 1:** Scan everything in the document — objects, text, and page numbers.  
2. **Phase 2:** Decide whether to use OCR, PDF parsing, or both methods.

The document is scanned page by page as a fallback approach.

If parsing with `pymdPDF` fails, OCR will be used as a backup.

## Goal

Extract relevant information and learn the structure of the data. If the surface-level content is unclear, perform a deeper scan page by page.



## ✅ First Iteration (Agent 1) 

### 📥 PDF Intake + Reasoning Engine

The first agent receives a raw PDF input and determines the appropriate pipeline based on the content:

* **PDFTextExtractor** – Parses text directly from the PDF.
* **PDFOCRExtractor** – Invoked when scanned/image-based documents are detected (via heuristic or failure fallback).
* **Nomic Embedding** – Embeds chunked document text for vectorization.
* **Pinecone Vector Store** – Stores embedded document chunks for fast semantic retrieval.
* **Tree-of-Thoughts Prompting** – Used to guide LLM reasoning and chunk filtering.
* **LLM Used** – [Mistral 7B](https://mistral.ai/) via API for scalable local-style LLM use.

This agent **decides** whether OCR is needed and preprocesses the data accordingly before passing it into the vector or SQL database. 

<img width="1306" height="1000" alt="image" src="https://github.com/user-attachments/assets/b2e8230c-4897-4f4d-a059-8564e73b9ae0" />
This is not an optimal solution because it only performs linear filtering and does not fully implement the fallback method discussed earlier.
For example, a PDF can contain both images and textual metadata; however, this approach does not utilize a hybrid method to handle them.


## ✅ Second Iteration (Agent 1) 

### 📥 PDF Intake + Reasoning Engine

<img width="2044" height="968" alt="image" src="https://github.com/user-attachments/assets/aea39cf6-fe41-4ca8-b303-250f67571028" />

Using an orchestration of many open-source tools and technologies.

## System Overview

This system includes the following components:

- **PyMDPDF** – For parsing text-based PDFs  
- **Tesseract** – OCR tool for extracting text from image-based PDFs  
- **CockroachDB** – Serves as our SQL database  
- **Pinecone** – Serves as our vector database for storing embeddings

We invoke a system prompt inspired by the *Tree of Thoughts* framework, featuring three imaginary expert agents. These agents have access to the tools above and collaborate to extract, transform, and load data into a knowledge graph structure.

The LLM does **not** have direct access to the PDF. Instead, it understands the decisions it needs to make and which tools to invoke appropriately.

> **Note:** Pinecone is **not** a knowledge graph. It is used to store reasoning information in a vectorized format for similarity-based retrieval.

Once the tools have been invoked and data has been processed, the structured output is stored in the SQL database (CockroachDB).


---

## 🤖 Second Agent (Agent 2)

### 🔎 Query Understanding & Knowledge Graph Reasoning

This agent is invoked post-vectorization and knowledge graph configuration. 

<img width="1862" height="906" alt="image" src="https://github.com/user-attachments/assets/b3192120-0e3d-40e1-bc65-f931f0e9009a" />



* **Semantic Query Matching** – Pulls relevant document chunks from the Pinecone index.
* **Knowledge Graph Retrieval ** – Utilize structured entities and relationships from text.
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

## 📂 Project Structure

### `Demo/`
Contains all demo-related components.

- **`frontend/`**  
  Built using [Vercel's](https://vercel.com/) **V0** UI tool and the **Next.js** framework. This folder contains the code for the user-facing interface.

- **`backend/`**  
  Contains the backend infrastructure.  
  > ⚠️ *Note:* This is built on top of the initial Proof of Concept (PoC) and does **not yet support Agent #2 (RAG Agent).*

### `Jupyter_Notebook/`
Includes both iterations of the agent pipelines for experimentation and testing within Jupyter environments.

### `Testing_Tool/`
Early testing scripts and utilities for the first filtering agent.

- **`sample_image_generator.py`**  
  A simple utility script that creates sample images for testing the OCR engine.



