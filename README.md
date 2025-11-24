
# RAG Assistant

A simple Retrieval-Augmented Generation (RAG) assistant that indexes your PDF files into a ChromaDB vector store and queries them using a local LLM via Ollama.

---

## 1. Add your data

Put your PDF files into the `data/` folder:

```bash
mkdir -p data
# copy your PDFs into this folder
cp /path/to/your/file.pdf data/
```

## 2. Install dependencies:
```bash
pip install -r requirements.txt
```
	
## 3. ingest docs into Chroma DB:
```bash
python -m app.ingest
```

## 4. Install Ollama
```bash
sudo snap install Ollam
	
# pull the model

ollama pull llama3
```

## 5. Run the assistant:
```bash
python -m app.main 
```

## Demo

<p align="center">
	<img src="RAG-SOC.gif" alt="Demo GIF" width="600">
</p>


flowchart TD
    U[User Question<br/>(e.g., "What is a SoC?")] --> S1[Step 1: Try to Find Info<br/>in the Document Library<br/>(Search in Vector Database)]

    S1 --> D{Match in<br/>vector database?}

    D -->|Yes| RAG[Step 2A: RAG Answer<br/>(from your uploaded SoC documents)]
    D -->|No| LLM[Step 2B: Direct LLM Answer<br/>(use general LLM knowledge)]

    RAG --> RAGRESP[Assistant responds with<br/>answer + citations (sources)]
    LLM --> LLMRESP[Assistant responds with<br/>general answer<br/>(no sources)]
