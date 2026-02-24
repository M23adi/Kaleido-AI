import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ========= RAG IMPORTS =========
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import CohereEmbeddings 

# ========= 1. SETUP =========
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY") 

if not GOOGLE_API_KEY or not COHERE_API_KEY:
    st.error("⚠️ Missing API Keys in .env file (Need both GOOGLE_API_KEY and COHERE_API_KEY)")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ========= 2. PAGE CONFIG =========
st.set_page_config(
    page_title="Kaleido | Your AI Tutor",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========= 3. "AI STARTUP" CSS & INTERACTIVITY =========
st.markdown("""
<style>
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    
    /* 🌟 THE "DEVELOPER CANVAS" GRID BACKGROUND */
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117 !important;
        background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
    }
    
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: -10%;
        left: 20%;
        width: 60%;
        height: 50%;
        background: radial-gradient(circle, rgba(255, 75, 75, 0.05) 0%, rgba(14, 17, 23, 0) 70%);
        z-index: -1;
        pointer-events: none;
    }

    /* 🌟 INTERACTIVE CARD PHYSICS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(22, 27, 34, 0.8) !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5), 0 0 15px rgba(255, 75, 75, 0.15) !important;
        border-color: rgba(255, 75, 75, 0.4) !important;
    }

    /* 🌟 THE GOLDEN AI STAR ANIMATION */
    @keyframes aiShine {
        0% { transform: scale(0.9) rotate(0deg); opacity: 0.8; text-shadow: 0 0 10px rgba(255, 215, 0, 0.4); }
        50% { transform: scale(1.1) rotate(10deg); opacity: 1; text-shadow: 0 0 20px rgba(255, 215, 0, 0.8), 0 0 35px rgba(255, 255, 255, 0.5); }
        100% { transform: scale(0.9) rotate(0deg); opacity: 0.8; text-shadow: 0 0 10px rgba(255, 215, 0, 0.4); }
    }
    .ai-sparkle {
        font-size: 3.5rem;
        animation: aiShine 2.5s infinite ease-in-out;
        display: inline-block;
        margin-bottom: -15px;
    }
</style>
""", unsafe_allow_html=True)

# ========= 4. SIDEBAR =========
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0;'>🌈</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-top: -15px;'>Kaleido</h2>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("🎯 Personalize")
    interest = st.selectbox("❤️ My Interest:", ["Bollywood 🎬", "Cricket 🏏", "Video Games 🎮", "Farming 🚜", "Cooking 🍳"])
    language = st.selectbox("🗣️ My Language:", ["Hinglish (Hindi+English)", "English", "Marathi Mix"])
    style = st.selectbox("🧠 Learning Style:", ["Stories & Analogies", "Visual Flowcharts", "Code Examples"])

    st.markdown("---")
    
    st.subheader("📚 Open-Book Mode")
    st.caption("Upload a textbook chapter or syllabus to anchor the AI's knowledge.")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        if ("current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name):
            with st.spinner("🧠 Vectorizing textbook..."):
                temp_path = "temp_textbook.pdf"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                loader = PyPDFLoader(temp_path)
                pages = loader.load()

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1200, chunk_overlap=150, separators=["\n\n", "\n", ".", " ", ""]
                )
                chunks = text_splitter.split_documents(pages)
                chunks = [c for c in chunks if len(c.page_content.strip()) > 50]

                embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, model="embed-multilingual-v3.0")
                vector_db = FAISS.from_documents(chunks, embeddings)

                st.session_state.vector_db = vector_db
                st.session_state.current_file = uploaded_file.name

            # ✨ THE NEW GOLDEN AI SHINE ANIMATION ✨
            st.toast(f"Kaleido has mastered {uploaded_file.name}!", icon="✨")
            st.markdown("""
                <div style="text-align: center; padding: 15px; border-radius: 10px; background: rgba(255, 215, 0, 0.05); border: 1px solid rgba(255, 215, 0, 0.2); margin-top: 10px;">
                    <div class="ai-sparkle">✨</div>
                    <h4 style="color: #FFD700; margin-top: 10px; font-weight: 700;">Knowledge Synthesized</h4>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Reset Chat & Memory", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.pop("vector_db", None)
        st.session_state.pop("current_file", None)
        st.rerun()

# ========= 5. MAIN CHAT INTERFACE =========
if "messages" not in st.session_state:
    st.session_state.messages = []

# BULLETPROOF TITLE
st.markdown(
    """
    <h1 style='font-size: 4rem; font-weight: 900; 
    background: -webkit-linear-gradient(45deg, #FF4B4B, #FF904B); 
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
    margin-bottom: -20px;'>
    Kaleido
    </h1>
    """, 
    unsafe_allow_html=True
)
st.markdown(f"**Adapting to your brain using `{interest}` in `{language}`.**")
st.markdown("<br>", unsafe_allow_html=True)


# BULLETPROOF NATIVE CARDS
if not st.session_state.messages:
    st.markdown("### 👋 Welcome to your perfect tutor.")
    st.write("I am Kaleido. I don't just give you answers; I translate complex engineering topics into concepts you already love. How can I help you today?")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.subheader("🏏 The Analogy Engine")
            st.write("Stuck on an algorithm? I'll explain it like a cricket match, a blockbuster movie, or a video game boss fight.")
            
    with col2:
        with st.container(border=True):
            st.subheader("👁️ Visual Flowcharts")
            st.write("Select 'Visual Flowcharts' in the sidebar, and I will draw diagrams and architecture maps directly on the screen.")
            
    with col3:
        with st.container(border=True):
            st.subheader("📚 Document Chat")
            st.write("Upload your college syllabus or textbook chapter in the sidebar. I'll read it and answer questions based **only** on your material.")

# Render Chat History
for msg in st.session_state.messages:
    avatar_icon = "🧑‍🎓" if msg["role"] == "user" else "🌈"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        if "```dot" in msg["content"]:
            parts = msg["content"].split("```dot")
            st.markdown(parts[0])
            st.graphviz_chart(parts[1].split("```")[0], use_container_width=True)
            try:
                st.markdown(parts[1].split("```")[1])
            except:
                pass
        else:
            st.markdown(msg["content"])

# ========= 6. USER INPUT =========
if prompt := st.chat_input("What is confusing you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🌈"):
        with st.spinner("Thinking..."):
            try:
                system_prompt = f"""
You are Kaleido, a personalized AI tutor.
User interest: {interest}
User language: {language}
Learning style: {style}

Rules:
1. Use {interest} analogies to explain concepts in {language}.
2. If style is Visual Flowcharts, output Graphviz DOT code starting with ```dot
3. If style is Code Examples, show code snippets
4. Be engaging and simple
"""
                # ROUTER
                if "vector_db" in st.session_state:
                    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
                    rag = RetrievalQA.from_chain_type(
                        llm=llm,
                        retriever=st.session_state.vector_db.as_retriever()
                    )
                    response = rag.invoke({"query": f"{system_prompt}\n\nQuestion: {prompt}"})
                    answer = response.get("result", "I couldn't find that in the document.")
                else:
                    response = model.generate_content(f"{system_prompt}\n\nQuestion: {prompt}")
                    answer = response.text

                # Render output 
                if "```dot" in answer:
                    parts = answer.split("```dot")
                    st.markdown(parts[0])
                    st.graphviz_chart(parts[1].split("```")[0], use_container_width=True)
                    try:
                        st.markdown(parts[1].split("```")[1])
                    except:
                        pass
                else:
                    st.markdown(answer)

                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                st.error(f"❌ Error: {e}")