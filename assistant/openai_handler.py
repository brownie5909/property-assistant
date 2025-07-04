
import os
from openai import OpenAI

def generate_property_insights(address, listing_data, suburb_data, sold_comps, for_sale_comps):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def format_comps(title, comps):
        section = f"\n### {title} Listings:\n"
        for c in comps:
            section += f"- {c.get('title', '')} | {c.get('price', '')} | {c.get('bedrooms', '')} bed / {c.get('bathrooms', '')} bath | {c.get('link', '')}\n"
        return section

    listings_text = "\n".join([f"- {i.get('title', '')}\n  {i.get('snippet', '')}\n  {i.get('link', '')}" for i in listing_data])
    suburb_text = "\n".join([f"- {i.get('title', '')}\n  {i.get('snippet', '')}\n  {i.get('link', '')}" for i in suburb_data])

    prompt = f"""You are an expert Australian property assistant. Based on the real data below, generate a price-based buyer report.

Address: {address}

### Current Listing:
{listings_text}

### Suburb Trends:
{suburb_text}

{format_comps("Sold Comparables", sold_comps)}
{format_comps("For-Sale Comparables", for_sale_comps)}

Instructions:
- Suggest a buyer offer range based on the comparables provided (e.g. "$1.08M–$1.12M").
- You may use judgement to estimate price confidence, but never invent properties or prices.
- Use **markdown-style bold headers** and bullet points.
- This will be part of a buyer’s PDF report.

Structure:
1. Estimated Price Range
2. Red Flags or Negotiation Notes
3. Summary of Features
4. Comparable Listings Summary
5. Mortgage Impact Estimate (20% deposit, 6.2% interest, 30 years)
6. Buyer Advice and Next Steps
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a reliable property insights assistant for Australian buyers. Use real data and estimate based on context. Do not make up listings." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
