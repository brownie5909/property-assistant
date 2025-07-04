
import os
from openai import OpenAI

def generate_property_insights(address, listing_data, suburb_data, sold_comps, for_sale_comps):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def format_comparables(label, comps):
        section = f"\n\n### {label} Listings:\n"
        for c in comps:
            section += f"- {c.get('title', '')}\n  {c.get('snippet', '')}\n  {c.get('link', '')}\n"
        return section

    listings_text = ""
    for item in listing_data:
        listings_text += f"- {item.get('title', '')}\n  {item.get('snippet', '')}\n  {item.get('link', '')}\n"

    suburb_text = ""
    for item in suburb_data:
        suburb_text += f"- {item.get('title', '')}\n  {item.get('snippet', '')}\n  {item.get('link', '')}\n"

    prompt = f"""You are an expert Australian property assistant.

Please analyse the following property report and provide real, specific and truthful insights ONLY based on the content below. Do NOT make up data or hallucinate facts.

Address: {address}

### Current Listing Information:
{listings_text}

### Suburb Trends and Market Data:
{suburb_text}

{format_comparables("Recent SOLD", sold_comps)}
{format_comparables("Current FOR SALE", for_sale_comps)}

Please provide a structured report with:

1. Estimated market value or range
2. Red flags or negotiation factors
3. Summary of features (bed/bath, land size, style, agent)
4. Comparable analysis referencing actual properties
5. Mortgage impact estimate (20% deposit, 6.2% interest, 30 years)
6. Buyer advice and next steps

Use markdown-style formatting: bold section headers, short bullet points, and no filler. Make this read like a sharp, data-driven buyer’s report.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a professional AI assistant for Australian home buyers. Do not invent facts. Only reference what you know from the user." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
