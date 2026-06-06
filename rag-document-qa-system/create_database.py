from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_community.document_loaders import TextLoader
import os
import shutil

CHROMA_PATH = "chroma"
DATA_PATH = "data/books"


def main():
    print("🚀 Starting database creation...")
    generate_data_store()


def generate_data_store():
    documents = load_documents()

    if len(documents) == 0:
        print("❌ No documents found in data/books")
        return

    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    print("📂 Loading documents safely...")

    docs = []

    # manually load .md files (NO unstructured, NO DirectoryLoader issues)
    for file in os.listdir(DATA_PATH):
        if file.endswith(".md"):
            file_path = os.path.join(DATA_PATH, file)

            loader = TextLoader(file_path, encoding="utf-8")
            docs.extend(loader.load())

    print(f"Loaded {len(docs)} documents")
    return docs


def split_text(documents: list[Document]):
    print("✂️ Splitting text into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    return chunks


def save_to_chroma(chunks: list[Document]):
    print("🧠 Creating embeddings + vector DB...")

    # delete old DB
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )

    print("✅ Database created successfully!")


if __name__ == "__main__":
    main()