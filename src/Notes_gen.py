from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
def notes_generator(clusters):
    context = ""
    for topic in clusters:
        context+= f"===== Topic {topic['Topic_id']} =====\n"

        for c in topic["Conversations"]:
            context += (
            f"[Question: {c["Question"]} | Answer: {c["Answer"]} | Retrieved_chunks: {c["Retrieved_chunks"]}]\n"
            f"Faithfulness: {c["Faithfulness"]}\n\n"
            )
    response= client.models.generate_content(
        model= "gemini-flash-lite-latest",
        config= {
            "system_instruction":'''You are an AI study assistant.

            The input consists of grouped conversations, where each group
            represents one topic.

            Generate clean study notes.

            Requirements:
            - Merge repeated concepts.
            - Do not repeat information.
            - Give a relevant document title. (starting with "*")
            - Use headings (starting with "#") and subheadings (starting with "##") and no punctuation for body text.
            - Use bullet points (specifically: "-")
            -Mention formulas if present.
            - Keep notes concise.
            - Only use the supplied context.
            - DO NOT include the question answers with Faithfullness - "Hallucinated"
            If a topic has multiple explanations, combine them into one.
            '''
        },
        contents= context
    )
    return response.text
    