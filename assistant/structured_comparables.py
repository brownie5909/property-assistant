import os
from openai import OpenAI

def generate_structured_comparables(address, sold_comps, for_sale_comps):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def format_raw_data(comps):
        return "\n".join([
            f"- {c.get('title')} | {c.get('price')} | {c.get('bedrooms')} bed / {c.get('bathrooms')} bath | {c.get('year')} | {c.get('snippet')}"
            for c in comps
        ])

    prompt = f"""You are a data extraction expert for Australian real estate. Your job is to extract 4–6 valid comparable properties based on raw snippets.

Address being analysed: {address}

ONLY use properties sold in 2024 or listed now. Ignore anything too old or vague.

Format your output exactly like this:

[
  {{
    "title": "...",
    "type": "sold",
    "price": "$980,000",
    "bedrooms": 3,
    "bathrooms": 2,
    "comment": "Sold 3 months ago in same complex",
    "confidence": "high"
  }},
  ...
]

Here are the SOLD properties:
{format_raw_data(sold_comps)}

Here are the FOR SALE properties:
{format_raw_data(for_sale_comps)}

Use only the best 3–4 from each, and structure the JSON exactly.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        response_format="json",
        messages=[
            { "role": "system", "content": "You are a real estate data formatter for buyer intelligence reports." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
