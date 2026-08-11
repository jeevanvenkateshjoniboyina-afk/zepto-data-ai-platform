import os
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END

# ==========================================================
# Configuration
# ==========================================================

MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="support_assistant/chroma_db"
)

collection = client.get_collection("zepto_support")


# ==========================================================
# Graph State
# ==========================================================

class GraphState(TypedDict):
    query: str
    intent: str
    retrieved_docs: list
    answer: str
    sources: list
    confidence: float


# ==========================================================
# Node 1 : Intent Classification
# ==========================================================

def classify_intent(state: GraphState):

    query = state["query"].lower()

    keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours"
    ]

    if any(keyword in query for keyword in keywords):
        state["intent"] = "policy_question"
    else:
        state["intent"] = "general_question"

    return state


# ==========================================================
# Node 2 : Retrieve + Answer
# ==========================================================

def retrieve_and_answer(state: GraphState):

    query_embedding = MODEL.encode(
        state["query"]
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_documents = results["documents"][0]
    retrieved_ids = results["ids"][0]

    state["retrieved_docs"] = retrieved_documents
    state["sources"] = retrieved_ids

    if MOCK_LLM:

        top_document = retrieved_documents[0]

        state["answer"] = (
            "Based on the retrieved context: "
            + top_document[:200]
        )

        state["confidence"] = 1.0

    else:

        # Optional Groq/OpenAI implementation later

        state["answer"] = (
            "Real LLM mode is not implemented."
        )

        state["confidence"] = 0.5

    return state


# ==========================================================
# Node 3 : Direct Answer
# ==========================================================

def direct_answer(state: GraphState):

    if MOCK_LLM:

        state["answer"] = (
            "I can only answer questions about Zepto policies right now."
        )

        state["sources"] = []

        state["confidence"] = 1.0

    else:

        state["answer"] = (
            "Real LLM mode is not implemented."
        )

        state["sources"] = []

        state["confidence"] = 0.5

    return state


# ==========================================================
# Router
# ==========================================================

def router(state: GraphState):

    return state["intent"]


# ==========================================================
# Build LangGraph
# ==========================================================

builder = StateGraph(GraphState)

builder.add_node(
    "classify_intent",
    classify_intent
)

builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

builder.add_node(
    "direct_answer",
    direct_answer
)

builder.set_entry_point("classify_intent")

builder.add_conditional_edges(
    "classify_intent",
    router,
    {
        "policy_question": "retrieve_and_answer",
        "general_question": "direct_answer",
    },
)

builder.add_edge(
    "retrieve_and_answer",
    END
)

builder.add_edge(
    "direct_answer",
    END
)

graph = builder.compile()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Policy Question")
    print("=" * 60)

    result = graph.invoke({

        "query": "What is the delivery fee?",

        "intent": "",

        "retrieved_docs": [],

        "answer": "",

        "sources": [],

        "confidence": 0.0

    })

    print(result)

    print()

    print("=" * 60)
    print("General Question")
    print("=" * 60)

    result = graph.invoke({

        "query": "Who won the Cricket World Cup?",

        "intent": "",

        "retrieved_docs": [],

        "answer": "",

        "sources": [],

        "confidence": 0.0

    })

    print(result)