
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

Please analyse the following property and provide real, specific, data-backed insights.
Use only the data provided below. Do NOT make up prices, links, or facts.

Address: {address}

### Listing Information:
{listings_text}

### Suburb Market Context:
{suburb_text}

{format_comparables("Recent SOLD", sold_comps)}
{format_comparables("Currently FOR SALE", for_sale_comps)}

### Instructions:
- You MUST list at least 2-3 recent sold and for-sale properties as examples in your report.
- Use bullet points and markdown-style headers (## or **) for formatting.
- Never hallucinate or assume values that aren’t present in the data above.
- This report will be read by home buyers relying on factual insights.

Now write the report including:
1. Estimated market value (based on provided comparables)
2. Pricing red flags or negotiation considerations
3. Summary of property features (with agent/source details)
4. Comparable listings section with at least 3 actual examples
5. Mortgage impact estimate (20% deposit, 6.2% interest, 30-year term)
6. Buyer advice and recommended next steps
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a professional AI for Australian property buyers. You must not hallucinate or make up data." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
