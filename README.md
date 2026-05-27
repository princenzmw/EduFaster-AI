# EduFaster-AI: Personalized Education Multi-Agent System 🎓

EduFaster-AI is an adaptive tutoring system designed to teach Python Basics. Built using a multi-agent architecture via LangGraph, it divides cognitive labor among specialized AI agents to deliver a superior learning experience.

## 🎥 Demo Preview

<!--[![EduFaster AI Demo](https://github.com/user-attachments/assets/db21037f-a79d-4bd5-9082-622d7b74b394)](media/demo.mp4) -->

<p align="center">
  <a href="media/demo.mp4">
    <img 
      src="https://github.com/user-attachments/assets/db21037f-a79d-4bd5-9082-622d7b74b394"
      width="1000"
      alt="EduFaster AI Demo"
    >
  </a>
</p>

<p align="center">
  Click the GIF above to watch the full demo video.
</p>

## 🏗 Architecture Diagram
*This workflow relies on the LangGraph hierarchical supervisor pattern.*

```mermaid
graph TD
    User([User Input]) --> Supervisor{Supervisor Agent}
    Supervisor -->|Teaches new concept| Explainer[Concept Explainer]
    Supervisor -->|Tests knowledge| Quizzer[Quiz Generator]
    Supervisor -->|Critiques answers| Reviewer[Feedback Analyzer]
    Supervisor -->|Conversation ends| End([FINISH])
    
    Explainer --> Tools[(Python REPL & Search Tools)]
    Tools --> Explainer
    
    Explainer --> User
    Quizzer --> User
    Reviewer --> User
