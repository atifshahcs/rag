from typing import TypedDict, List, Dict, Any

from langchain_ollama import OllamaLLM
from langgraph.graph import StateGraph, END

from .db import get_vectorstore


#1 Define the state 

class AgentState(TypedDict, total=False):
    question: str
    answer: str
    mode: str                 # "rag" or "direct_llm"
    sources: List[Dict[str, Any]]
    has_context: bool         # did we find any relevant docs?



def get_llm():
    """
    Check Ollama LLM if not configured
    """
    return OllamaLLM(model="llama3")  # or "mistral"


#2 Rag logic node

def rag_node(state: AgentState) -> AgentState:
    
    question = state["question"]
    llm = get_llm()
    vectorstore = get_vectorstore()

    # a: retrive docs from vec DB
    # docs = vectorstore.similarity_search(question, k=4)
    # docs_and_scores = vectorstore.similarity_search_with_relevance_scores(question, k=4)# 
    # 
   


    docs_and_scores = vectorstore.similarity_search_with_score(question, k=4)

     
    # # Debugging
    # print("=== DEBUG ===")
    # print("Question:", question)
    # for doc, score in docs_and_scores:
    #     print("score:", score, " | text:", doc.page_content[:80])
    # print("=============") 


    # exit()
    # print(docs_and_scores)

    # If nothing retrieved at all -> fallback to direct LLM
    if not docs_and_scores:
        state["has_context"] = False
        state["mode"] = "direct_llm"
        state["sources"] = []
        return state

    # Decide if the best match is good enough to trust RAG
    best_doc, best_score = docs_and_scores[0]

    # print(best_score)
    # For distance: smaller = better. You MUST tune this.
    MAX_DISTANCE = 0.5  # example value, adjust via print() experiments

    if best_score > MAX_DISTANCE:
        # Too far -> treat as "no relevant context"
        state["has_context"] = False
        state["mode"] = "direct_llm"
        state["sources"] = []
        return state

    # distance (smaller = better)
    filtered_docs = [
        (doc, score)
        for doc, score in docs_and_scores
        if score <= MAX_DISTANCE
    ]

    if not filtered_docs:
        # No relevant context found -> no RAG answer
        state["has_context"] = False
        state["mode"] = "direct_llm"  # will actually run in the next node
        state["sources"] = []
        return state
    
    # Have some context
    state["has_context"] = True

    # c: Build context string

    context_parts = []
    sources: List[Dict[str,Any]] = []

    for doc, score in filtered_docs:
        context_parts.append(doc.page_content)
        metadata = doc.metadata or {}
        sources.append(
            {
                "source": metadata.get("source", "unknown"),
                "page": metadata.get("page", None),
                "score": float(score),
            }
        )
    # print(context_parts)
    # print(type(context_parts))
    context_text = "\n\n ### \n\n".join(context_parts)

    # d: Build Rag Style prompt

    prompt = (
        "You are SoC RAG Assistant, an expert in System-on-Chip.\n\n"
        "Use ONLY the following context to answer the users question. "
        "If the answer is not clearly in the context, say you don't know.\n\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {question}\n\n"
        "Answer in a clear, concise, and technical way.\n\n"
        "Answer:"
    )

    # d: Call LLM with context

    answer = llm.invoke(prompt)

    state["answer"] = answer
    state["sources"] = sources
    state["mode"] = "rag"
    
    return state

#3 Direct LLM node

def direct_llm_node(state:AgentState) -> AgentState:
    """
    Answer the question directly with LLM without any 
    retrivel
    """

    question = state["question"]
    llm = get_llm()

    prompt = {
        "You are SoC Assistant. Answer the following hardware/SoC question "
        "based on your general knowledge. If it requires very specific "
        "project details, answer in general terms.\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    }
    # print('##########', type(prompt))
    answer = llm.invoke(str(prompt))

    state["answer"] = answer
    state["sources"] = []
    state["mode"] = "direct_llm"

    return state

#4 Build the graph via LangGraph

def build_graph():
    """
    Graph structure:
    
    rag_node => has_context = True => End
             => has_context = False => direct_llm_node => End
    """

    graph = StateGraph(AgentState)

    # a: add nodes
    graph.add_node("rag_node", rag_node)
    graph.add_node("direct_llm", direct_llm_node)

    # b: Start at RAG node
    graph.set_entry_point("rag_node")

    # c: condition edge from rag_node
    def route_after_rag (state:AgentState):        
        #if we had context and answered -> End
        if state.get("has_context", False):
            return "end"
        else:
            return "direct_llm"
        
    graph.add_conditional_edges(
        "rag_node", 
        route_after_rag,
        {
            "end": END,
            "direct_llm": "direct_llm"
        }
    )

    # After direct LLM always => End
    graph.add_edge("direct_llm", END)

    return graph.compile()

#5 Helper functino to run the agent

def run_agent(question:str)->AgentState:
    """
    Run the compiled graph given a question
    """
    graph = build_graph()
    initial_state: AgentState = {"question": question}
    final_state = graph.invoke(initial_state)

    return final_state
        