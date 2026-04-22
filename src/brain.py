from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from src.config import MODEL_NAME, SYSTEM_PROMPT
from src.processor import DocumentProcessor
from src.tools import tools as ticket_tools
import json

class RAGBrain:
    def __init__(self):
        self.processor = DocumentProcessor()
        self.vector_store = self.processor.get_vector_store()
        # Gemini-ni tool-lar bilan bog'laymiz
        self.llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0).bind_tools(ticket_tools)
        
    def _search_docs(self, query: str):
        """Hujjatlardan ma'lumot qidirish."""
        if not self.vector_store:
            return "No documents found. Please sync documents first."
        
        docs = self.vector_store.similarity_search(query, k=5)
        results = []
        for doc in docs:
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "?")
            results.append(f"Content: {doc.page_content}\nSource: {source} (Page {page})\n---")
        return "\n".join(results)

    def query(self, user_input, chat_history):
        """Agent o'rniga ishlaydigan aqlli Router funksiya."""
        
        # 1. Hujjatdan qidiruv (RAG qismi)
        context = ""
        if self.vector_store:
            context = self._search_docs(user_input)
        
        # 2. Promp-ni tayyorlash
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT + f"\n\nContext from documents:\n{context}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
        chain = prompt_template | self.llm
        
        # 3. LLM-dan javob olish
        response = chain.invoke({"input": user_input, "history": chat_history})
        
        # 4. Agar LLM Tool chaqirmoqchi bo'lsa (masalan Ticket ochish)
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "create_support_ticket":
                    # Ticket ochish funksiyasini chaqiramiz
                    from src.tools import create_support_ticket
                    result = create_support_ticket.invoke(tool_call["args"])
                    return result
        
        # 5. Extract text cleanly (Gemini 2.5 returns a list of dicts sometimes)
        content = response.content
        if isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
                elif isinstance(item, str):
                    text_parts.append(item)
            return "\n".join(text_parts)
            
        return str(content)

