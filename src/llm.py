from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_response(prompt, retrieved_chunks):
    context = ""
    for chunk in retrieved_chunks:
        context += (
        f"[Source: {chunk['source']} | Page: {chunk['page']} | Chunk: {chunk['chunk_id']}]\n"
        f"{chunk['text']}\n\n"
        )
    user_prompt = f"""
    The following context was retrieved from the uploaded PDF.
    Use ONLY this information to answer the question.
        Context:
        {context}

        Question:
        {prompt}
        """
    response= client.models.generate_content(
        model= "gemini-flash-lite-latest",
        config= {
            "system_instruction":'''You are an AI study assistant.
            Answer using the provided context.
            
            Keep answers factual and explanatory with proper formatting'''
        },
        contents= user_prompt
    )
    return response.text

