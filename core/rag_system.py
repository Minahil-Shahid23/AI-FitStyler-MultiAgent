from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document  
import pandas as pd

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_rag():
    df = pd.read_csv("G:/fitstyler/data/catalog.csv")
    docs = []
    for _, row in df.iterrows():
        content = f"{row['outfit_name']} - Price: ${row['price']} - Description: {row['description']} - Body Type: {row['body_type']} - Occasion: {row['occasion']} - Gender: {row['gender']}"
        docs.append(Document(page_content=content, metadata={"image_url": row['image_url']}))

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    chunks = []
    for doc in docs:
        split_chunks = splitter.split_documents([doc])
        chunks.extend(split_chunks)
        
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("faiss_index")  
    print("RAG built and saved! Ready for queries.")
    return vector_store

if __name__ == "__main__":
    build_rag()
    
    