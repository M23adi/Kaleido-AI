import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- 1. SETUP & SECURITY ---
# Load the API Key safely from the .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
if not api_key:
    st.error("⚠️ API Key missing! Please create a .env file with your key.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')

# --- 2. UI CONFIGURATION (The "Pre-Open" Fix) ---
# initial_sidebar_state="expanded" <-- THIS forces the sidebar to stay open!
st.set_page_config(
    page_title="Kaleido", 
    page_icon="🌈", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 3. CUSTOM STYLING ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main-header {font-size: 3rem; color: #FF4B4B; font-weight: 700;}
    .sub-text {font-size: 1.2rem; color: #555;}
    .stChatInput {padding-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    # Logo Logic (Safe Fallback)
    try:
        st.image("logo.jpg", width=120)
    except:
        st.write("🌈 Kaleido")

    st.title("Settings ⚙️")
    st.markdown("Customize your tutor:")
    
    # Inputs
    interest = st.selectbox("❤️ My Interest:", 
        ["Bollywood 🎬", "Cricket 🏏", "Video Games 🎮", "Farming 🚜", "Cooking 🍳"])
    
    language = st.selectbox("🗣️ My Language:", 
        ["Hinglish (Hindi+English)", "English", "Marathi Mix"])
    
    style = st.selectbox("🧠 My Learning Style:", 
        ["Stories & Analogies", "Visual Flowcharts", "Code Examples"])
    
    st.divider()
    
    # Clear Button
    if st.button("🗑️ Start Fresh", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown('<p class="main-header">Kaleido 🌈</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">The AI Tutor that adapts to <b>YOU</b>.</p>', unsafe_allow_html=True)

# --- THE "WELCOME SCREEN" FIX ---
# If chat is empty, show this friendly welcome message
if len(st.session_state.messages) == 0:
    st.info(f"👋 **Welcome!** I am ready to teach you in **{language}** using **{interest}** analogies.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 💡 Try asking:")
        st.code("How does the Internet work?")
        st.code("Explain Gravity")
        st.code("What is Inflation?")
    with col2:
        st.markdown("#### 🚀 Features:")
        st.markdown("- **Analogy Engine**: Learn via Cricket/Movies")
        st.markdown("- **Visual Mode**: Ask for flowcharts")
        st.markdown("- **Hinglish**: I speak your language")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Diagram rendering logic
        if "```dot" in message["content"]:
            parts = message["content"].split("```dot")
            st.markdown(parts[0]) # Text before diagram
            st.graphviz_chart(parts[1].split("```")[0], use_container_width=True) # The Diagram
            try:
                st.markdown(parts[1].split("```")[1]) # Text after diagram
            except:
                pass
        else:
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What is confusing you today?"):
    
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Dynamic Prompt
                system_instruction = f"""
                Act as Kaleido.
                CONTEXT: User loves {interest}, speaks {language}.
                TASK: Explain "{prompt}".
                RULES:
                1. Use {interest} analogies.
                2. If Style is 'Visual Flowcharts', generate valid Graphviz DOT code (start with ```dot).
                3. Keep it fun and engaging.
                """
                
                response = model.generate_content(system_instruction)
                response_text = response.text
                
                # Render Logic (Same as above)
                if "```dot" in response_text:
                    parts = response_text.split("```dot")
                    st.markdown(parts[0])
                    st.graphviz_chart(parts[1].split("```")[0], use_container_width=True)
                    try:
                        st.markdown(parts[1].split("```")[1])
                    except:
                        pass
                else:
                    st.markdown(response_text)
                
                # Save to History
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Error: {e}")