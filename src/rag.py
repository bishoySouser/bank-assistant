import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DB_DIR = "./vector_db"
DATA_PATH = "./data/knowledge.txt"

def get_embedding_function():
    # نموذج BAAI/bge-small-en-v1.5 خفيف جداً وسريع عبر ONNX بدون PyTorch
    return FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def build_vector_store():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"لم يتم العثور على الملف: {DATA_PATH}")

    print("جاري تحميل وثائق منتجات CIB...")
    loader = TextLoader(DATA_PATH, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        separators=["\n\n", "\n", " - ", " "]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"تم تقسيم النص إلى {len(chunks)} مقطع.")

    print("جاري بناء التضمينات محلياً بسرعة وبدون استهلاك مساحة...")
    embeddings = get_embedding_function()
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print(f"تم الانتهاء بنجاح وحفظ الـ Vector Store في: {DB_DIR}")
    return vector_db

def get_retriever():
    embeddings = get_embedding_function()
    vector_db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )
    return vector_db.as_retriever(search_kwargs={"k": 2})

if __name__ == "__main__":
    build_vector_store()