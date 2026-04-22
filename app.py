import streamlit as st
from src.brain import RAGBrain
from src.processor import DocumentProcessor
from langchain_core.messages import HumanMessage, AIMessage
import os
import shutil
import json

# Page configuration
st.set_page_config(
    page_title="AstroCorp Universal AI",
    page_icon="🤖",
    layout="wide"
)

# Advanced Custom CSS
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stSidebar { background-color: #161b22; border-right: 1px solid #30363d; }
    .stChatFloatingInputContainer { background-color: #0d1117; }
    .upload-section {
        padding: 15px;
        border: 2px dashed #30363d;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Management & Upload
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=70)
    st.title("AstroCorp AI")
    st.caption("Universal Knowledge Assistant")
    st.markdown("---")

    # 📤 File Uploader
    st.subheader("📤 Upload Knowledge")
    uploaded_files = st.file_uploader("Upload PDF documents", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🔥 Process Uploaded Files"):
            with st.status("📥 Saving & Indexing...", expanded=True) as status:
                # 1. Clear old files first (to keep library clean)
                if os.path.exists("data"):
                    shutil.rmtree("data")
                os.makedirs("data")
                
                # 2. Save new files
                for uploaded_file in uploaded_files:
                    with open(os.path.join("data", uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.write(f"Saved: {uploaded_file.name}")
                
                processor = DocumentProcessor()
                processor.process_and_store()
                st.session_state.brain = RAGBrain()
                status.update(label="✅ All Files Indexed!", state="complete")
                st.rerun()

    st.markdown("---")
    
    # 📁 Library View
    st.subheader("📚 Current Library")
    if os.path.exists("data"):
        lib_files = [f for f in os.listdir("data") if f.endswith('.pdf')]
        if lib_files:
            for f in lib_files:
                st.markdown(f"🔹 `{f}`")
        else:
            st.info("Library is empty.")

    # 🛠 Controls
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔴 Reset Knowledge Base"):
        if os.path.exists("data"):
            shutil.rmtree("data")
            os.makedirs("data")
        if os.path.exists("vector_store"):
            shutil.rmtree("vector_store")
        st.session_state.brain = RAGBrain()
        st.success("Knowledge Base Reset!")
        st.rerun()

    # 🎫 Ticket Tracking System
    st.markdown("---")
    st.subheader("🎫 Support Tickets")
    if os.path.exists("tickets"):
        tickets = sorted(os.listdir("tickets"), reverse=True)
        if tickets:
            for t_file in tickets[:5]: # Show last 5 tickets
                with open(os.path.join("tickets", t_file), "r") as f:
                    t_data = json.load(f)
                    with st.expander(f"#{t_file.split('_')[1].split('.')[0]} - {t_data['summary'][:20]}..."):
                        st.write(f"**From:** {t_data['name']}")
                        st.write(f"**Email:** {t_data['email']}")
                        st.write(f"**Desc:** {t_data['description']}")
        else:
            st.info("No active tickets.")
    else:
        st.info("No tickets created yet.")

# Main Interface
if "messages" not in st.session_state:
    st.session_state.messages = [AIMessage(content="Hello! I am your AI assistant. Upload your PDFs or ask me anything about the existing knowledge base.")]

if "brain" not in st.session_state:
    st.session_state.brain = RAGBrain()

# Chat Display
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
        st.markdown(msg.content)

# Chat Input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 Thinking..."):
            try:
                response = st.session_state.brain.query(prompt, st.session_state.messages[:-1])
                st.markdown(response)
                st.session_state.messages.append(AIMessage(content=response))
            except Exception as e:
                st.error(f"Error: {e}")
