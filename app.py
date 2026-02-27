# import streamlit as st
# from core.rag_system import build_rag 
# from agents.body_analyzer import analyze_body_from_photo
# from agents.skin_color_analyzer import detect_skin_tone_and_palette  # New agent for skin
# from agents.outfit_generator import generate_outfit_suggestions 
# from agents.trend_critic import critique_trends 
# import requests
# from io import BytesIO
# from PIL import Image
# import os 
# import random
# import time 
# import logging 


# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("app_log.txt"), 
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# logger.info("App started – AI-FitStyler loading...")

# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #2c3e50;
#         text-align: center;
#         text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
#         margin-bottom: 0;  # Removed margin-bottom for no white line below heading
#     }
#     .color-box {
#         border-radius: 12px;
#         border: 2px solid #e0e0e0;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-weight: bold;
#         color: white;
#         text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
#         cursor: pointer;
#         transition: box-shadow 0.3s ease;
#     }
#     .color-box:hover {
#         box-shadow: 0 4px 12px rgba(0,0,0,0.15);
#     }
#     .upload-section {
#         background: #f8f9fa;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         margin: 10px 0;
#     }
# </style>
# """, unsafe_allow_html=True)

# st.markdown('<h1 class="main-header">🛍️ AI-FitStyler: Your Personal Fashion Advisor</h1>', unsafe_allow_html=True)

# st.sidebar.header("Your Details")
# gender = st.sidebar.selectbox("Gender", ["male", "female", "other"])
# occasion = st.sidebar.selectbox("Occasion", ["casual", "party", "office"])
# budget = st.sidebar.number_input("Budget ($)", min_value=10, max_value=1000, value=50)

# logger.info(f"User inputs: Gender={gender}, Occasion={occasion}, Budget=${budget}")

# if st.sidebar.button("Clear Cache"):
#     st.cache_data.clear()
#     logger.info("Cache cleared by user")
#     st.sidebar.success("Cache cleared – rerun suggestions!")

# with st.container():
#     st.markdown('<div class="upload-section">', unsafe_allow_html=True)
#     uploaded_photo = st.file_uploader("Upload your full-body photo (for auto body type)", type=["jpg", "png"])
#     st.markdown('</div>', unsafe_allow_html=True)

# body_type = "slim" 
# if uploaded_photo is not None:
#     logger.info("Photo uploaded – starting analysis")
#     temp_path = "temp_photo.jpg"
#     with open(temp_path, "wb") as f:
#         f.write(uploaded_photo.getbuffer())
#     body_type = analyze_body_from_photo(temp_path)
#     logger.info(f"Body type detected: {body_type}")
#     st.success(f"**Auto Detected Body Type: {body_type.upper()}**")
    
#     skin_tone, palette = detect_skin_tone_and_palette(temp_path)
#     logger.info(f"Skin tone detected: {skin_tone}, Palette length: {len(palette)}")
#     st.success(f"**Auto Detected Skin Tone: {skin_tone.upper()}**")
    
#     st.subheader("✨ Recommended Colors for Your Skin Tone:")
#     st.write(" ")  # Gap for spacing
#     cols = st.columns(len(palette))
#     for i, color in enumerate(palette):
#         with cols[i]:
#             st.markdown(f"""
#             <div class="color-box" style="background-color: {color}; width: 100%; height: 80px; margin: 10px 5px;">
#                 {color}
#             </div>
#             """, unsafe_allow_html=True)
#     st.write(" ")  
    
#     image = Image.open(uploaded_photo)
#     st.image(image, caption="Your Photo Analyzed!", width=300)
    
#     if os.path.exists(temp_path):
#         os.remove(temp_path)
#         logger.info("Temp photo cleaned up")
# else:
#     body_type = st.sidebar.selectbox("Body Type (Manual if no photo)", ["slim", "curvy", "athletic"])
#     logger.info(f"Manual body type selected: {body_type}")

# @st.cache_data
# def get_suggestions(gender, body_type, occasion, budget):
#     """Cached function for outfit suggestions – fast on repeat inputs."""
#     logger.info("Generating outfit suggestions...")
#     polished = generate_outfit_suggestions(gender, body_type, occasion, budget)
#     logger.info(f"Polished suggestions generated: {len(polished)}")
#     if not polished:
#         logger.warning("No polished suggestions – RAG issue?")
#         return [] 
    
#     critiqued = critique_trends(polished, occasion, body_type, gender)
#     logger.info(f"Trend critique done: {len(critiqued)} suggestions")
#     random.seed(random.randint(1, 1000))
#     random.shuffle(critiqued)
    
#     filtered_critiqued = []
#     for sug in critiqued:
#         gen = sug.get('gender', 'unknown')
#         price_str = sug['price'].replace("$", "").strip()
#         price = float(price_str) if price_str.replace('.', '').isdigit() else 0
        
#         if gen.lower() == gender.lower() and price <= budget:
#             filtered_critiqued.append(sug)
    
#     logger.info(f"Filtered suggestions: {len(filtered_critiqued)}")
#     return filtered_critiqued[:3]

# if st.button("Get Outfit Suggestions!"):
#     logger.info("Outfit suggestions button clicked")
#     with st.spinner("Analyzing and searching outfits..."):
#         progress_bar = st.progress(0)
#         status_text = st.empty()
#         for i in range(100):
#             progress_bar.progress(i + 1)
#             status_text.text(f'Analyzing... {i+1}%')
#             time.sleep(0.01) 
#         status_text.empty()
    
#     critiqued = get_suggestions(gender, body_type, occasion, budget)
    
#     if not critiqued:
#         logger.warning("No outfits available – showing warning")
#         st.warning("NO OUTFIT AVAILABLE . TRY DIFFERENT BUDGET!")
#     else:
#         logger.info(f"Showing {len(critiqued)} outfits to user")
#         st.success("✨ Outfits ready! Check your personalized style below.")
#         st.header(f"Your {occasion.capitalize()} Outfits for {body_type.capitalize()} {gender.capitalize()} (Budget: ${budget})")
#         for i, sug in enumerate(critiqued):
#             col1, col2 = st.columns(2)
#             with col1:
#                 try:
#                     response = requests.get(sug['image_url'])
#                     if response.status_code == 200:
#                         img = Image.open(BytesIO(response.content))
#                         st.image(img, caption=sug['name'], width=200)
#                     else:
#                         logger.warning(f"Image load failed for {sug['name']} – URL: {sug['image_url']}")
#                         st.write("🖼️ Image not loaded (URL issue)")
#                 except Exception as e:
#                     logger.error(f"Image load error for {sug['name']}: {e}")
#                     st.write("🖼️ Image load error – check connection")
            
#             with col2:
#                 st.write(f"**{sug['name']}**")
#                 st.write(f"💰 Price: ${sug['price']}")
#                 st.write(f"✨ Why Perfect: {sug['explanation'][:200]}...")
#                 st.write(f"🌟 Trend Score: {sug['trend_score']} – {sug['trend_comment'][:100]}...")
# st.write("---")
# st.write("Built with LangChain, Streamlit & FAISS | Full Multi-Agent Fashion Advisor Ready!")

import streamlit as st
from core.rag_system import build_rag 
from agents.body_analyzer import analyze_body_from_photo
from agents.skin_color_analyzer import detect_skin_tone_and_palette 
from agents.outfit_generator import generate_outfit_suggestions 
from agents.trend_critic import critique_trends 
import requests
from io import BytesIO
from PIL import Image
import os 
import random
import time 

# --- Professional UI Configuration ---
st.set_page_config(page_title="AI-FitStyler | Your AI Stylist", page_icon="🛍️", layout="wide")

# Custom CSS for Luxury/Modern Feel
st.markdown("""
<style>
    /* Main Background & Font */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #1e3d59, #ff4b4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .sub-header {
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Modern Card Styling */
    .outfit-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .outfit-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(45deg, #ff4b4b, #ff7675);
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }

    /* Color Palette Circles */
    .color-circle {
        border-radius: 50%;
        height: 60px;
        width: 60px;
        margin: 10px auto;
        border: 3px solid white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .upload-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #ff4b4b;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<h1 class="main-header">🛍️ AI-FITSTYLER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Multi-Agent AI System for Personalized Fashion Analysis</p>', unsafe_allow_html=True)

# --- Sidebar Inputs ---
st.sidebar.markdown("### 👤 User Profile")
gender = st.sidebar.selectbox("Gender", ["Female", "Male", "Other"])
occasion = st.sidebar.selectbox("Occasion", ["Casual", "Party", "Office", "Wedding"])
budget = st.sidebar.slider("Budget Limit ($)", 10, 1000, 150)

if st.sidebar.button("Clear Cache"):
    st.cache_data.clear()
    st.sidebar.success("Environment Reset Successful!")

# --- Main Layout ---
col_main1, col_main2 = st.columns([1, 1])

with col_main1:
    st.markdown("### 📸 Image Analysis")
    uploaded_photo = st.file_uploader("Upload full-body photo for AI Analysis", type=["jpg", "png"])
    
    if uploaded_photo is not None:
        temp_path = "temp_photo.jpg"
        with open(temp_path, "wb") as f:
            f.write(uploaded_photo.getbuffer())
        
        # Agents Processing
        with st.spinner("AI Agents Analyzing Body & Skin Tone..."):
            body_type = analyze_body_from_photo(temp_path)
            skin_tone, palette = detect_skin_tone_and_palette(temp_path)
        
        st.success(f"**Analysis Complete:** {body_type.capitalize()} Frame | {skin_tone.capitalize()} Tone")
        
        # Display Skin Palette
        st.markdown("#### ✨ Suggested Color Palette")
        p_cols = st.columns(len(palette))
        for i, color in enumerate(palette):
            with p_cols[i]:
                st.markdown(f'<div class="color-circle" style="background-color: {color};"></div>', unsafe_allow_html=True)
                st.caption(f"<center>{color}</center>", unsafe_allow_html=True)
        
        st.image(Image.open(uploaded_photo), caption="Analyzed Profile", use_container_width=True)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
    else:
        body_type = st.selectbox("Manual Body Type (No Photo)", ["Slim", "Curvy", "Athletic"])

# --- Suggestion Engine ---
@st.cache_data
def get_suggestions(gender, body_type, occasion, budget):
    polished = generate_outfit_suggestions(gender, body_type, occasion, budget)
    if not polished: return []
    
    critiqued = critique_trends(polished, occasion, body_type, gender)
    random.shuffle(critiqued)
    
    filtered = [s for s in critiqued if float(s['price'].replace("$", "").strip()) <= budget]
    return filtered[:3]

with col_main2:
    st.markdown("### 👗 Style Recommendations")
    if st.button("Generate Signature Look"):
        with st.spinner("Searching Global Trends..."):
            results = get_suggestions(gender, body_type, occasion, budget)
        
        if not results:
            st.warning("No outfits found within this budget. Try increasing it!")
        else:
            for sug in results:
                # Custom Card Layout using HTML for Professional Look
                st.markdown(f"""
                <div class="outfit-card">
                    <div style="display: flex; gap: 20px; align-items: flex-start;">
                        <div style="flex: 1;">
                            <img src="{sug['image_url']}" style="width: 100%; border-radius: 12px; border: 1px solid #eee;">
                        </div>
                        <div style="flex: 1.5;">
                            <h3 style="margin-top:0; color:#1e3d59;">{sug['name']}</h3>
                            <span style="background:#ffeaa7; padding:2px 8px; border-radius:5px; font-weight:bold;">${sug['price']}</span>
                            <p style="margin-top:10px; font-size:0.9rem;"><b>AI Insight:</b> {sug['explanation'][:250]}...</p>
                            <div style="background:#f1f2f6; padding:10px; border-radius:8px; border-left:4px solid #ff4b4b;">
                                <p style="margin:0; font-size:0.85rem;"><b>Trend Critique:</b> {sug['trend_comment']}</p>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<center>Powered by <b>Gemini 1.5 Flash</b> | <b>FAISS RAG</b> | <b>Multi-Agent Orchestration</b></center>", unsafe_allow_html=True)


logger.info("App session ended")
