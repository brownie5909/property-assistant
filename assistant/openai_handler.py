
import os
from openai import OpenAI

def generate_property_insights(address, page_data):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    summary = page_data.get("summary_text", "")
    listing_url = page_data.get("source_url", "")
    image = page_data.get("image_url", "")

    prompt = f"""You are a property advisor helping Australian home buyers.

Analyze the following listing data to:
1. Estimate a fair market value range
2. Identify any red flags
3. Suggest negotiation strategies
4. Estimate mortgage impact
5. Summarize the property details

ONLY use the data below. Do NOT hallucinate any facts.
This is for the property: {address}
Listing URL: {listing_url}

Listing content:
"""
{summary}
"""

Return your report in the following markdown format:

**1. Estimated Price Range and Justification**
**2. Red Flags or Negotiation Opportunities**
**3. Property Overview**
**4. Mortgage Impact Estimate**
**5. Negotiation Strategy & Buyer Advice**

Make it clear, professional, and helpful for a first-home buyer.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a smart assistant for Australian real estate buyers. Be honest, use only provided listing info." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
