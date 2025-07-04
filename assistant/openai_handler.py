
import os
from openai import OpenAI

def generate_property_insights(address, listing_data):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Format listing data into readable prompt parts
    listings_text = ""
    for item in listing_data:
        title = item.get('title', '')
        link = item.get('link', '')
        snippet = item.get('snippet', '')
        listings_text += f"- Title: {title}\n  Snippet: {snippet}\n  Link: {link}\n\n"

    prompt = f"""You are a smart Australian property buying assistant. A user is researching a property at:

Address: {address}

Below is what we found online about the property:
{listings_text}

Based on this, generate a clear, professional report including:
- Estimated market value or range (if data suggests it)
- Any pricing red flags or negotiation leverage
- Summary of features (e.g., bedrooms, bathrooms, layout, agent notes)
- Mortgage impact estimate (assume 30-year loan at 6.2% interest, 20% deposit)
- Strategic advice for the buyer

Keep it smart, helpful, and suited to a first-home buyer audience. Use markdown-style **bold** headers.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a professional property assistant for Australian buyers." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
