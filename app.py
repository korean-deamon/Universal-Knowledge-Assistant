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
            
            # Allow syncing existing files without re-uploading
            if st.button("🔄 Sync Existing Library"):
                with st.status("📥 Indexing existing files...", expanded=True) as status:
                    processor = DocumentProcessor()
                    processor.process_and_store()
                    st.session_state.brain = RAGBrain()
                    status.update(label="✅ All Files Indexed!", state="complete")
                    st.rerun()
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
        json_tickets = sorted(
            [f for f in os.listdir("tickets") if f.endswith(".json")],
            reverse=True
        )
        if json_tickets:
            for t_file in json_tickets[:5]:
                with open(os.path.join("tickets", t_file), "r") as f:
                    t_data = json.load(f)
                ticket_id = t_data.get("id", t_file.split("_")[1].split(".")[0])
                status = t_data.get("status", "Open")
                status_icon = "🟢" if status == "Open" else "⚫"
                with st.expander(f"{status_icon} #{ticket_id} — {t_data['summary'][:22]}..."):
                    st.markdown(f"**From:** {t_data['name']}")
                    st.markdown(f"**Email:** {t_data['email']}")
                    st.markdown(f"**Created:** {t_data.get('created_at', 'N/A')}")
                    st.markdown(f"**Status:** {status}")
                    st.markdown(f"**Issue:** {t_data['description'][:120]}{'...' if len(t_data['description']) > 120 else ''}")
                    if t_data.get("github_url"):
                        st.markdown(f"[View on GitHub]({t_data['github_url']})")
                    html_path = os.path.join("tickets", f"ticket_{ticket_id}.html")
                    if os.path.exists(html_path):
                        with open(html_path, "r", encoding="utf-8") as hf:
                            html_content = hf.read()
                        st.download_button(
                            label="⬇️ Download HTML",
                            data=html_content,
                            file_name=f"ticket_{ticket_id}.html",
                            mime="text/html",
                            key=f"dl_{ticket_id}"
                        )
        else:
            st.info("No active tickets.")
    else:
        st.info("No tickets created yet.")

    # 📝 Manual Ticket Form
    st.markdown("---")
    with st.expander("📝 Create Ticket Manually"):
        with st.form("manual_ticket_form", clear_on_submit=True):
            t_name  = st.text_input("Full Name", placeholder="John Doe")
            t_email = st.text_input("Email", placeholder="john@example.com")
            t_summary = st.text_input("Issue Summary", placeholder="Short title of the problem")
            t_desc  = st.text_area("Description", placeholder="Describe the problem in detail...", height=100)
            submitted = st.form_submit_button("🎫 Submit Ticket")
            if submitted:
                if t_name and t_email and t_summary and t_desc:
                    from src.tools import create_support_ticket
                    result = create_support_ticket.invoke({
                        "name": t_name, "email": t_email,
                        "summary": t_summary, "description": t_desc
                    })
                    st.success(result)
                    st.rerun()
                else:
                    st.warning("Please fill in all fields.")

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
                # Ticket form hint — show when AI suggests creating a ticket
                ticket_keywords = ["support ticket", "qo'llab-quvvatlash chiptasi", "ticket yaratish",
                                   "create a ticket", "open a ticket", "chipta", "ticket"]
                if any(kw in response.lower() for kw in ticket_keywords):
                    st.info("💡 Ticket yaratish uchun chap paneldagi **📝 Create Ticket Manually** bo'limidan foydalaning.")
            except Exception as e:
                st.error(f"Error: {e}")
