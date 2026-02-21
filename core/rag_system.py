import os
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# 1. Dynamic Path Setup
# Ye line current file ki location se project root dhoondti hai
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "catalog.csv")
INDEX_PATH = os.path.join(BASE_DIR, "faiss_index")

# 2. Embeddings Initialize
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_rag():
    # Check karein ke file maujood hai ya nahi
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: File nahi mili is raste par: {DATA_PATH}")
        return

    print("🔄 Loading catalog and building index...")
    df = pd.read_csv(DATA_PATH)
    docs = []
    
    for _, row in df.iterrows():
        content = f"{row['outfit_name']} - Price: ${row['price']} - Description: {row['description']} - Body Type: {row['body_type']} - Occasion: {row['occasion']} - Gender: {row['gender']}"
        docs.append(Document(page_content=content, metadata={"image_url": row['image_url']}))

    # 3. Text Splitting
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    chunks = []
    for doc in docs:
        split_chunks = splitter.split_documents([doc])
        chunks.extend(split_chunks)
        
    # 4. Vector Store Creation
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save index locally
    vector_store.save_local(INDEX_PATH)  
    print(f"✅ RAG built and saved at: {INDEX_PATH}")
    print("🚀 Ready for queries!")
    return vector_store

if __name__ == "__main__":
    build_rag()