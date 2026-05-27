import os
from dotenv import load_dotenv

# CRITICAL FIX: Load environment variables BEFORE initializing the LLM
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from backend.tools import execute_python_code, search_tool

# Initialize the state-of-the-art Gemini 3.5 Flash model
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3)

# Define Prompts
explainer_prompt = """You are the Concept Explainer for EduFaster-AI, teaching Python Basics. 
Break down complex Python concepts into simple analogies. 
You have two tools:
1. Use the search_tool (Wikipedia) if you need to look up a precise computer science definition.
2. CRITICAL: You must use the execute_python_code tool to test and verify any code snippets before showing them to the user."""

quiz_prompt = """You are the Quiz Generator. Based on the concept just explained, generate 1 multiple-choice question to test the user. Keep it focused on Python."""

feedback_prompt = """You are the Feedback Analyzer. Review the user's answer to a quiz or their general question. 
Critique it for accuracy. Tell them if they are right or wrong and explain why."""

# Create agents safely WITHOUT the version-dependent modifier keyword
explainer_agent = create_react_agent(llm, tools=[execute_python_code, search_tool])
quiz_agent = create_react_agent(llm, tools=[search_tool])
feedback_agent = create_react_agent(llm, tools=[])
