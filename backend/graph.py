from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from backend.agents import (
    explainer_agent, quiz_agent, feedback_agent, llm, 
    explainer_prompt, quiz_prompt, feedback_prompt
)

# Define shared state/memory
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_agent: str

# Helper function to safely extract text from Gemini's output structure
def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # If Gemini returns a list of dictionaries, extract the text keys
        return " ".join([part.get("text", "") for part in content if isinstance(part, dict) and "text" in part])
    return str(content)

# Supervisor Logic
supervisor_prompt = """You are the Supervisor for EduFaster-AI, teaching Python Basics.
Based on the conversation, route to the next agent:
- 'Explainer' to teach a new concept.
- 'Quizzer' to test the user after an explanation.
- 'Reviewer' to analyze a user's answer.
- 'FINISH' if the user's query is fully answered or they are done.
Respond ONLY with one of these exact words."""

def supervisor_node(state: AgentState):
    messages = list(state['messages'])
    response = llm.invoke([{"role": "system", "content": supervisor_prompt}] + messages)
    
    # Safely extract text using our helper
    decision_text = extract_text(response.content).strip()
    
    # Failsafe: Clean up possible markdown or punctuation from Gemini
    for keyword in ["Explainer", "Quizzer", "Reviewer", "FINISH"]:
        if keyword.lower() in decision_text.lower():
            return {"next_agent": keyword}
            
    return {"next_agent": "Explainer"} # Default fallback

# Bulletproof execution function that manually injects the system prompt
def run_worker_node(agent, state: AgentState, agent_name: str, system_prompt: str):
    messages = [SystemMessage(content=system_prompt)] + list(state["messages"])
    result = agent.invoke({"messages": messages})
    
    # Safely extract text from the final message before sending to UI
    final_message_content = extract_text(result["messages"][-1].content)
    return {"messages": [AIMessage(content=final_message_content, name=agent_name)]}

def explainer_node(state: AgentState):
    return run_worker_node(explainer_agent, state, "Explainer", explainer_prompt)

def quizzer_node(state: AgentState):
    return run_worker_node(quiz_agent, state, "Quizzer", quiz_prompt)

def reviewer_node(state: AgentState):
    return run_worker_node(feedback_agent, state, "Reviewer", feedback_prompt)

# Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("Explainer", explainer_node)
workflow.add_node("Quizzer", quizzer_node)
workflow.add_node("Reviewer", reviewer_node)

workflow.add_edge(START, "Supervisor")

# Conditional routing
workflow.add_conditional_edges(
    "Supervisor",
    lambda x: x["next_agent"],
    {
        "Explainer": "Explainer",
        "Quizzer": "Quizzer",
        "Reviewer": "Reviewer",
        "FINISH": END
    }
)

# Return to END to stream to Streamlit UI
workflow.add_edge("Explainer", END)
workflow.add_edge("Quizzer", END)
workflow.add_edge("Reviewer", END)

# Compile
app_graph = workflow.compile()
