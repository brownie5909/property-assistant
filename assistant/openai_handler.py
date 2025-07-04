
import os
from openai import OpenAI
from datetime import datetime

def generate_property_insights(address, listing_data, suburb_data, sold_comps, for_sale_comps):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    current_year = 2025

    def format_comps(title, comps):
        section = f"\n### {title} Listings:\n"
        for c in comps:
            # Skip old data if year appears too far back
            year = c.get("year", "")
            try:
                if year and int(year) < current_year - 1:
                    continue
            except:
                pass
            section += f"- {c.get('title', '')} | {c.get('price', '')} | {c.get('bedrooms', '')} bed / {c.get('bathrooms', '')} bath | {c.get('link', '')}\n"
        return section

    listings_text = "\n".join([f"- {i.get('title', '')}\n  {i.get('snippet', '')}\n  {i.get('link', '')}" for i in listing_data])
    suburb_text = "\n".join([f"- {i.get('title', '')}\n  {i.get('snippet', '')}\n  {i.get('link', '')}" for i in suburb_data])

    prompt = f"""You are an expert Australian property assistant. Based on verified data below, provide a full, buyer-focused report. 
DO NOT include sales from before 2024 unless clearly noted as outdated. DO NOT make up any data. Use a confident, clear tone like a professional advisor. This will be part of a PDF given to property buyers.

Address: {address}

### Listing Details:
{listings_text}

### Suburb Market Context:
{suburb_text}

{format_comps("Recent SOLD", sold_comps)}
{format_comps("Currently FOR SALE", for_sale_comps)}

### Please write the report in the following format:

**1. Estimated Price Range and Justification**
- Give a price range (e.g., $1.08M–$1.12M)
- Base this ONLY on valid comparables above

**2. Pricing Red Flags or Negotiation Opportunities**
- Identify red flags, e.g., aggressive price vs. same-building sale

**3. Property Overview**
- Bullet point summary: bed, bath, parking, lot size, building name, renovation clues

**4. Comparable Listings Summary**
- List 2–3 recent sold and for-sale properties with context

**5. Mortgage Impact Estimate**
- Monthly repayment at 6.2%, 20% deposit, 30-year loan at lower and upper range

**6. Buyer Advice and Next Steps**
- Strategic advice: what to check, what to offer, what to confirm

Keep formatting clean with **markdown headings** and spacing. Use only facts provided above.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            { "role": "system", "content": "You are a senior AI advisor for Australian home buyers. Use only real data. Do not hallucinate." },
            { "role": "user", "content": prompt }
        ]
    )

    return response.choices[0].message.content
