import streamlit as st
from backend.graph import app_graph
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

# --- Custom CSS for Liquid Glass UI ---
st.set_page_config(page_title="EduFaster-AI", layout="wide")
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 EduFaster-AI: Personalized Python Tutor")
st.caption("Powered by Multi-Agent Architecture (LangGraph & Gemini 3.5 Flash)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me about Python (e.g., 'Teach me about loops'):"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process through LangGraph Multi-Agent System
    with st.chat_message("assistant"):
        with st.spinner("Agents are collaborating..."):
            langchain_msgs = [HumanMessage(content=m["content"]) if m["role"] == "user" else m["content"] for m in st.session_state.messages]
            
            # Invoke graph
            result = app_graph.invoke({"messages": langchain_msgs})
            
            # Extract final message from agents
            final_msg = result["messages"][-1]
            response_text = f"**[{final_msg.name}]**\n\n{final_msg.content}"
            
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
