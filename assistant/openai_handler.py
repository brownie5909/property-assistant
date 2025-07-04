import os
from openai import OpenAI

def generate_property_insights(address):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""Generate a brief analysis of the property at {address}, including:
    - Estimated price range
    - Red flags
    - Negotiation tips
    - Mortgage impact summary
    Use a clear, smart tone suitable for first home buyers."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a helpful AI property assistant for Australian home buyers." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
