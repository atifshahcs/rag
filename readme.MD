
# RAG Assistant

A simple Retrieval-Augmented Generation (RAG) assistant that indexes your PDF files into a ChromaDB vector store and queries them using a local LLM via Ollama.

---

## 1. Add your data

Put your PDF files into the `data/` folder:

```bash
mkdir -p data
# copy your PDFs into this folder
cp /path/to/your/file.pdf data/



## 2. Install dependencies:

pip install -r requirements.txt
	
## 3. ingest docs into Chroma DB:

python -m app.ingest
	
## 4. Install Ollama

sudo snap install Ollam
	
	# pull the model

ollama pull llama3


## 5. Run the assistant:

python -m app.main 


## Example

<p align="center">
	<img src="RAG-SOC.gif" alt="Demo GIF" width="600">
</p>