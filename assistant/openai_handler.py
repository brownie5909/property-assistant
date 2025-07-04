
import os
from openai import OpenAI

def generate_property_insights(address, listing_data, suburb_data):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Format property listing data
    listings_text = ""
    for item in listing_data:
        listings_text += f"- {item.get('title', '')}\n  {item.get('snippet', '')}\n  {item.get('link', '')}\n\n"

    # Format suburb-level insights
    suburb_text = ""
    for item in suburb_data:
        suburb_text += f"- {item.get('title', '')}\n  {item.get('snippet', '')}\n  {item.get('link', '')}\n\n"

    prompt = f"""You are an expert Australian property assistant. Analyze this property and its surrounding market:

Address: {address}

### Property Listing Information:
{listings_text}

### Suburb Trends & Recent Sales:
{suburb_text}

Now create a buyer's report including:
1. Estimated price range and justification
2. Any pricing red flags or concerns
3. Summary of property features (bed, bath, layout, agent details)
4. Market trends and nearby sale comparisons
5. Mortgage impact estimate (20% deposit, 6.2% interest, 30-year loan)
6. Negotiation tips and red flags to be aware of

Write clearly, in a smart but friendly tone. Use **bold** section headers and markdown style formatting.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a professional AI assistant for Australian home buyers." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
