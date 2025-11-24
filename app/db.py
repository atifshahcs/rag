from pathlib import Path
from typing import Optional
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings


from langchain_chroma import Chroma

CHROMA_DIR = Path(__file__).resolve().parent.parent/"chroma_db"

def get_embedding_function():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-en-v1.5",
        model_kwargs={"device": "cpu"},               # or "cuda"
        encode_kwargs={"normalize_embeddings": True}  # VERY IMPORTANT
    )


def get_vectorstore(persist_directory: Optional[str] = None) -> Chroma:
    # Load (or create) a Chroma vector store using the same embedding model.
    persist_dir = persist_directory or str(CHROMA_DIR)
    embedding_fn = get_embedding_function()

    vectorstore = Chroma(
        collection_name="docs",
        embedding_function=embedding_fn,
        persist_directory=persist_dir,
    )
    return vectorstore