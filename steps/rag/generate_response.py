# steps/rag/generate_response.py
from zenml import step
from openai import OpenAI
from llm_engineering.settings import settings

@step
def generate_response(context: str, query: str = "Aziz Sancar kimdir?"):
    """
    Generates a response using the retrieved context and OpenAI model.
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    messages = [
        {"role": "system", "content": "You are a helpful assistant who knows a lot about Aziz Sancar."},
        {"role": "user", "content": f"Kontekst: {context}\n\nSoru: {query}"}
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    answer = completion.choices[0].message.content
    print("\n💬 Yanıt:\n", answer)
    return answer
