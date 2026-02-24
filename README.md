# 🌈 Kaleido: The Adaptive AI Tutor
> *Don't just learn it. Relate to it.*

**[Click Here](https://kaleidoai.streamlit.app/) to try it**
Kaleido is an intelligent educational agent which solves the problem of "One-Size-Fits-All" education by dynamically restructuring complex topics to match the student's **Interests**, **Language**, and **Learning Style**.

## 🆕 What's New in v2.0?
**Enterprise RAG Integration:** Upload PDFs (textbooks/syllabuses) to anchor the AI's knowledge in your specific course material.
**Multilingual Embeddings:** Powered by Cohere, providing native-level support for Hinglish and Marathi Mix.
**Gemini 2.5 Flash Brain:** Upgraded to the latest model for faster, more accurate reasoning.
**Animated "Aero" UI:** A modern, interactive interface featuring a dotted developer grid, animated backgrounds, and pulsing AI status icons.

## 🚀 The Problem
Students struggle with complex engineering concepts because:
1.  **Language Barriers:** Textbooks are often in high-level English.
2.  **Lack of Engagement:** Abstract concepts feel disconnected from real life.
3.  **Rigid Formats:** Visual learners are forced to read long text.

## 💡 The Solution
Kaleido acts as a Contextual Translation Engine, now reinforced with Retrieval-Augmented Generation (RAG) to provide grounded, course-specific tutoring.
* **For the Cricket Lover:** Explain "Digestion" using "Bowling Yorkers."
* **For the Visual Learner:** Instantly generate **Flowcharts** using Graphviz.
* **For the Rural Student:** Explain "Cloud Computing" using "Water Storage" analogies in Hinglish.
* **NEW: The Librarian Feature:** Upload your specific college syllabus or PDF chapter; Kaleido "memorizes" it to answer questions using only your verified course material.

## 🛠️ Tech Stack
* **LLM (The Brain):** Google Gemini 2.5 Flash API — Optimized for high-speed reasoning and massive context windows.
**Embeddings (The Search Engine):** Cohere Multilingual-v3.0 — Enterprise-grade vector embeddings with native support for Indian dialects.
**Vector Database:** FAISS (Facebook AI Similarity Search) — Handles high-dimensional document retrieval with sub-millisecond latency.
**Orchestration:** LangChain (RetrievalQA) — Chains the document retrieval logic with the LLM generator.
**Frontend:** Streamlit (Python) — Featuring a custom "Aurora" animated UI with interactive CSS physics and Glassmorphism.
**Visualization:** Graphviz — Real-time "Diagrams as Code" generation.

## 📸 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/M23adi/Kaleido-AI.git
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the app:
    ```bash
    streamlit run app.py
Built with ❤️    
   
