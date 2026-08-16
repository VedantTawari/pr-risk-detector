import json
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="pr_risk_history"
)


def create_document(pr):
    return f"""
Pull Request #{pr["number"]}

Title:
{pr["title"]}

AI Risk Score:
{pr["risk_score"]}

AI Risk Level:
{pr["risk_level"]}

AI Risk Factors:
{", ".join(pr["risk_factors"])}

Rule Score:
{pr["rule_score"]}

Rule Factors:
{", ".join(pr["rule_factors"])}

Final Score:
{pr["final_score"]}

Final Risk Level:
{pr["final_level"]}

Recommendation:
{pr["recommendation"]}
""".strip()


def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT"
        )
    )

    return response.embeddings[0].values


def retrieve_similar_prs(query, k=3, exclude_pr=None):

    embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY"
        )
    ).embeddings[0].values

    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        where={
            "pr_number": {
                "$ne": exclude_pr
            }
        } if exclude_pr is not None else None
    )
    return results

def add_pr_to_knowledge_base(pr):

    document = create_document(pr)

    embedding = get_embedding(document)

    collection.upsert(
        ids=[f"pr_{pr['number']}"],
        documents=[document],
        embeddings=[embedding],
        metadatas=[{
            "pr_number": pr["number"],
            "title": pr["title"],
            "final_score": pr["final_score"],
            "final_level": pr["final_level"]
        }]
    )

    print(f"Added PR #{pr['number']} to RAG knowledge base")