
---

```
# 👗 AI-FitStyler: Agentic RAG Fashion Recommender

AI-FitStyler is an advanced Agentic AI application that merges Computer Vision with Retrieval-Augmented Generation (RAG) to provide highly personalized fashion recommendations based on a user's unique Body Type and Skin Tone.

---

## 🌟 Key Features

**Vision-Based Body Analysis:**  
Utilizing MediaPipe Pose, the system identifies 33 anatomical landmarks to calculate hip-to-shoulder ratios, accurately detecting body types (Slim, Athletic, Curvy).

**Skin Tone & Palette Mapping:**  
Analyzes facial data using MediaPipe Face Mesh within the LAB Color Space to suggest a harmonious color palette that complements the user's complexion.

**Vector-Based Recommendation Engine:**  
Leverages a FAISS Vector Database and HuggingFace Embeddings to perform semantic searches, finding outfits that match style, occasion, and budget contextually rather than just by keywords.

**AI Trend Critique:**  
Features a specialized "Critique Agent" powered by local LLMs (via Ollama) to score outfits and provide stylistic reasoning.

---

## 🛠️ Technical Stack

- **Frontend:** Streamlit  
- **Computer Vision:** MediaPipe (Pose & Face Mesh)  
- **Vector Database:** FAISS  
- **Embeddings:** HuggingFace sentence-transformers/all-MiniLM-L6-v2  
- **LLM Inference:** Ollama (Llama 3.2 / Phi-3)  
- **Data Processing:** Pandas & OpenCV  

---

## 📁 Project Structure

```

fitstyler/
├── agents/
│   ├── body_analyzer.py     # Logic for Body Type & Skin Tone analysis
│   └── critique_agent.py    # AI Stylist scoring and trend analysis
├── core/
│   ├── rag_system.py        # FAISS index builder and data ingestion
│   └── recommendation_engine.py # Retrieval logic and LLM interaction
├── data/
│   └── catalog.csv          # Fashion dataset (Outfits, Prices, Occasions)
├── faiss_index/             # Persistent vector storage
└── app.py                   # Main Streamlit UI and orchestration

````

---

## ⚙️ Installation & Setup

**Initialize Virtual Environment:**
```powershell
python -m venv venv
.\venv\Scripts\activate
````

**Install Dependencies:**

```powershell
pip install -r requirements.txt
```

**Build the RAG Database:**

```powershell
python core/rag_system.py
```

**Launch Application:**

```powershell
streamlit run app.py
```

---

## 🧠 System Logic (The RAG Flow)

1. **Ingestion Phase:** The system reads catalog.csv, generates embeddings for each item, and stores them in a FAISS index.
2. **Analysis Phase:** Upon photo upload, the Vision Agent calculates the user's physical attributes.
3. **Retrieval Phase:** The Recommendation Engine queries the FAISS index using the user's profile (Gender, Body Type, Occasion, Budget) to find the top 10 matches.
4. **Generation Phase:** An LLM (via Ollama) generates a personalized explanation for why the specific outfit fits the user's style.

---



