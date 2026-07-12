from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def judge_faithfullness(prompt, top_chunks, response):
    context=""
    for chunk in top_chunks:
        context += (
        f"[Source: {chunk['source']} | Page: {chunk['page']} | Chunk: {chunk['chunk_id']}]\n"
        f"{chunk['text']}\n\n"
        )
    feedback_prompt= f"""
    Context: {context} \n
    Question: {prompt} \n
    Answer: {response}\n
    """
    feedback_report= client.models.generate_content(
        model= "gemini-flash-lite-latest",
        config= {
            "system_instruction":''' You are evaluating a Retrieval-Augmented Generation (RAG) system.
                Only use the retrieved context.
        
                If any claim appears in the answer but cannot be found in the context,
                mark it as Hallucinated.
                Return JSON only.
                {
                "label":"Faithful | Partially Faithful | Hallucinated",
                "reason":"One sentence"
                }'''
        },
        contents= feedback_prompt
    )

    return feedback_report
