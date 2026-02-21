# AI-FitStyler 👗✨

**Upload a photo. Analyze your style. Get the perfect outfit.**

An AI-driven multi-agent fashion advisor platform that uses computer vision and RAG (Retrieval-Augmented Generation) to provide personalized outfit and jewelry recommendations based on your body type and skin tone.

## 📝 Overview
AI-FitStyler is a **sophisticated AI styling application** that automates the role of a personal fashion consultant. Unlike static suggestion tools, it uses **OpenCV** to extract physical attributes from user photos and a **Multi-Agent Architecture** to process those attributes. By leveraging a **FAISS-powered RAG pipeline**, it ensures that every recommendation is grounded in a curated fashion dataset and critiqued by an AI "Trend Agent" for maximum style impact.

## 🚀 Features
- **Automated Body Analysis** — OpenCV detects body shape (Slim, Athletic, Curvy) from photos.
- **Skin Tone Detection** — Accurate color sampling to suggest the best-matching color palettes.
- **Multi-Agent Logic** — Separate agents for analysis, fashion critique, and trend matching.
- **RAG Pipeline** — Uses FAISS Vector DB for lightning-fast retrieval from a custom outfit dataset.
- **Trend-Aware Critique** — Gemini AI reviews suggestions to ensure they meet modern fashion trends.
- **Dynamic Palettes** — Generates Hex-code based color palettes tailored to the user's complexion.
- **Budget-Friendly Filters** — Filter recommendations based on user-defined price ranges.
- **Responsive UI** — Clean, interactive dashboard built with Streamlit.

## 🛠 Tech Stack
- **Framework:** Streamlit (Python)
- **Computer Vision:** OpenCV (CV2), MediaPipe
- **AI/LLM:** Google Gemini 1.5 Flash
- **Vector Database:** FAISS (Facebook AI Similarity Search)
- **Embeddings:** HuggingFace Sentence-Transformers
- **Data Handling:** Pandas, NumPy

## ⚙️ Getting Started

### Prerequisites
- Python 3.9+
- Gemini API Key (Google AI Studio)

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Minahil-Shahid23/ai-fitstyler-multiagent.git](https://github.com/Minahil-Shahid23/ai-fitstyler-multiagent.git)
   cd ai-fitstyler-multiagent

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   
3. **Environment Setup:**
Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY="your-gemini-api-key"
   
4. **Run Application:**
   ```bash
   streamlit run app.py

## 🧠 How It Works (The Pipeline)

1. **Input:** User uploads a photo and selects an occasion (Casual, Office, Party).
2. **Vision Agent:** OpenCV processes the image to determine skin tone and body structure.
3. **Retrieval Agent:** The system converts user data into a query and searches the **FAISS Vector Store** for the top 10 matching outfits.
4. **Critique Agent:** **Gemini AI** filters these results, selecting the top items that best fit current fashion trends.
5. **Output:** User receives detected attributes, a custom color palette, and visual outfit cards.

## 📁 Project Structure

```text
ai-fitstyler/
├── app.py                      # Main Streamlit UI & Orchestration
├── requirements.txt            # Project dependencies
├── agents/                     # Multi-Agent Logic
│   ├── body_analyzer.py        # OpenCV Body detection
│   ├── skin_color_analyzer.py  # Skin tone & Palette logic
│   ├── trend_critic.py         # Gemini AI fashion critique
│   └── rag_engine.py           # FAISS retrieval logic
├── data/
│   ├── outfits.csv             # Curated fashion dataset
│   └── faiss_index/            # Pre-computed vector embeddings
└── utils/
    └── helpers.py              # Image processing utilities

```

## ✨ Technical Highlights

* **RAG Architecture:** Ensures the AI doesn't "hallucinate" and only suggests items available in the dataset.
* **Real-time Image Processing:** Optimized OpenCV masks for accurate attribute detection.
* **Scalable Search:** FAISS allows sub-millisecond search times across large datasets.
* **Secure Deployment:** Hosted on Streamlit Cloud with secure API key management.
