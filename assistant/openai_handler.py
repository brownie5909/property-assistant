import os
from openai import OpenAI

def generate_property_insights(address, listing_data, suburb_data, structured_comps_json):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    listings_text = "\n".join([f"- {i.get('title', '')}\n  {i.get('snippet', '')}\n  {i.get('link', '')}" for i in listing_data])
    suburb_text = "\n".join([f"- {i.get('title', '')}\n  {i.get('snippet', '')}\n  {i.get('link', '')}" for i in suburb_data])

    prompt = f"""You are an expert Australian property assistant. Based on verified data below, provide a full, buyer-focused report.

Address: {address}

### Listing Details:
{listings_text}

### Suburb Market Context:
{suburb_text}

### Structured Comparable Listings (already parsed):
{structured_comps_json}

Instructions:
- Estimate a price range (e.g. $1.08M–$1.12M) based on comps
- Never guess or invent data
- Use markdown headings and bullet formatting
- This is a PDF property report for a home buyer

Write your report in this format:
**1. Estimated Price Range and Justification**
**2. Red Flags or Negotiation Opportunities**
**3. Property Overview**
**4. Comparable Listings Summary**
**5. Mortgage Impact Estimate**
**6. Buyer Advice and Next Steps**
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a professional property AI for home buyers. Use only the structured data provided. No hallucinations." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
