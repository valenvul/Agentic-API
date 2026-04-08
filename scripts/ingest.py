import argparse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.config import settings

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Path to the source file to ingest")
    args = parser.parse_args()

    with open(args.file_path, "r", encoding="utf-8") as f:
        content = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_text(content)

    documents = [Document(page_content=chunk, metadata={"source": args.file_path}) for chunk in chunks]
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    Chroma.from_documents(documents, embeddings, persist_directory=settings.CHROMA_DB_PATH)
    
    print(f"Stored {len(documents)} chunks")

if __name__ == "__main__": main()

          