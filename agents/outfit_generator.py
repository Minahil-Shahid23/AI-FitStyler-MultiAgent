import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Root path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS 
from core.rag_system import build_rag  

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def generate_outfit_suggestions(gender, body_type, occasion, budget):
    try:
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        print("Saved RAG loaded – fast!")
    except:
        print("RAG index not found.")
        return []
   
    query = f"{gender} {body_type} {occasion} outfit under ${budget}"
    raw_results = vector_store.similarity_search(query, k=10) 
    
    polished_suggestions = []
    for doc in raw_results:
        content = doc.page_content
        gen = "unknown"
        if " - Gender: " in content:
            parts = content.split(" - Gender: ")
            if len(parts) > 1:
                gen = parts[1].split(" ")[0].strip()
               
        lines = content.split(" - ")
        outfit_name = lines[0].strip()
        price = lines[1].replace("Price: $", "").strip()
        
        explanation = f"This {outfit_name} is perfect for your {body_type} {gender} {occasion} style – trendy, comfy, and under ${budget}! 😎"
        
        polished_suggestions.append({
            'name': outfit_name,
            'price': price,
            'image_url': doc.metadata.get('image_url', ''),
            'explanation': explanation,
            'content': content,
            'gender': gen 
        })
    
    return polished_suggestions
























# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

# from langchain_ollama import OllamaLLM
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS 

# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# llm = OllamaLLM(model="phi3:mini")

# def generate_outfit_suggestions(gender, body_type, occasion, budget):
#     # Load saved index only – no build
#     try:
#         vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
#         print("Saved RAG loaded – fast!")
#     except:
#         print("RAG index not found. Run 'python core/rag_system.py' first to build it.")
#         return []  # Empty return, app mein error show ho jayega
    
#     query = f"{gender} {body_type} {occasion} outfit under ${budget}"
#     raw_results = vector_store.similarity_search(query, k=1) 
    
#     polished_suggestions = []
#     for doc in raw_results:
#         content = doc.page_content
#         gen = "unknown"
#         if " - Gender: " in content:
#             parts = content.split(" - Gender: ")
#             if len(parts) > 1:
#                 gen = parts[1].split(" ")[0].strip()
                
#         lines = content.split(" - ")
#         outfit_name = lines[0].strip()
#         price = lines[1].replace("Price: $", "").strip()
        
#         prompt = f"{outfit_name} (${price}) for {gender} {body_type} {occasion}. Why perfect? (1 sentence)."
#         explanation = llm.invoke(prompt)
        
#         polished_suggestions.append({
#             'name': outfit_name,
#             'price': price,
#             'image_url': doc.metadata.get('image_url', ''),
#             'explanation': explanation,
#             'content': content,
#             'gender': gen 
#         })
    
#     return polished_suggestions