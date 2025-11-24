from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from .db import get_embedding_function, CHROMA_DIR

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Folder where you put your RAG Documents

def load_documents():
    docs = []

    for path in DATA_DIR.rglob("*"):
        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            docs.extend(loader.load())
        elif path.suffix.lower() in [".txt", ".md"]:
            loader = TextLoader(str(path), encoding="utf-8")
            docs.extend(loader.load())
        # Add more types if you want
    return docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return splitter.split_documents(documents)

def main():
    
    print(f"Loading documents from {DATA_DIR} ...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")

    print("Splitting documents into chunks...")
    chunks = split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    embedding_fn = get_embedding_function()

    print(f"Creating Chroma DB at {CHROMA_DIR} ...")
    CHROMA_DIR.mkdir(exist_ok=True, parents=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_fn,
        collection_name="docs",
        persist_directory=str(CHROMA_DIR),
    )

    print("Ingestion complete.")


if __name__ == "__main__":
    main()