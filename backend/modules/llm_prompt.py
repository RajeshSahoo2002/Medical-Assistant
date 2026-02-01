from langchain.prompts import PromptTemplate # type: ignore
from langchain.chains import RetrievalQA # type: ignore
from langchain.groq import ChatGroq # type: ignore
import os
from langchain.vectorstores import Pinecone # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

#fUNCTION TO HANDLE THE LLM CHAIN

def get_llm_chain(retriever):
    llm=ChatGroq(
        model_name="llama3-70b-8192",
        groq_api_key=GROQ_API_KEY
    )
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are **AI Medical Assistant**, a RAG AI-powered assistant trained to help users understand medical documents and health-related questions and provide accurate information based on the trained data by understanding the given context.

        Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.

    ---

    🔍 **Context**:
    {context}

    🙋‍♂️ **User Question**:
    {question}

    ---

    💬 **Answer**:
    - Respond in a calm, factual, and respectful tone.
    - Use simple explanations when needed.
    - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents.Please consult a healthcare professional for accurate advice."
    - Always prioritize user safety and well-being.
    - Do NOT make up facts.
    - Do NOT give medical advice or diagnoses.
    """
    )
