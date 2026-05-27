import json
import pandas as pd

from openai import AzureOpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_DEPLOYMENT
)


def extract_user_intent(user_prompt):

    df = pd.read_csv(
        "dataset/styles.csv",
        on_bad_lines="skip"
    )

    article_types = sorted(
        df["articleType"]
        .dropna()
        .unique()
        .tolist()
    )

    usage_values = sorted(
        df["usage"]
        .dropna()
        .unique()
        .tolist()
    )

    gender_values = sorted(
        df["gender"]
        .dropna()
        .unique()
        .tolist()
    )

    colour_values = sorted(
        df["baseColour"]
        .dropna()
        .unique()
        .tolist()
    )

    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version="2024-02-15-preview"
    )

    system_prompt = f"""
You are an intent extraction assistant for a fashion recommendation system.

Extract the user's fashion request into valid JSON only.

The user may mention clothing they already own or are currently wearing.
Do NOT recommend the same existing item unless the user explicitly asks for it.

If the user explicitly requests a fashion item type,
focus article_types on that requested item category.

If the user does not explicitly request an item type,
infer 1 to 3 complementary fashion item categories.

Use natural semantic understanding.

Examples:
- "casual pants" → Trousers, Jeans, Track Pants
- "formal shoes" → Formal Shoes
- "winter jacket" → Jackets
- "sports outfit" → Sports Shoes, Track Pants
- "casual accessories" → Watches, Belts, Wallets

The usage field should represent the intended occasion or context.

Allowed article types:
{article_types}

Allowed usage values:
{usage_values}

Allowed gender values:
{gender_values}

Allowed colour values:
{colour_values}

Return ONLY valid JSON in this exact format:

{{
  "article_types": [],
  "usage": "",
  "gender": "",
  "preferred_colours": []
}}

Rules:
- article_types should contain 1 to 3 values.
- Use ONLY article types from the allowed list.
- The first article type should be the most relevant.
- preferred_colours should contain ONLY allowed colours.
- usage should contain ONLY allowed usage values.
- gender should contain ONLY allowed gender values.
- If the user says male, men, masculine → use "Men"
- If the user says female, women, feminine → use "Women"
- If the user requests darker tones, prefer colours like Black, Grey, Charcoal, Navy Blue, Brown
- If the user requests lighter tones, prefer colours like White, Beige, Cream, Off White
- If unknown, use empty string or empty list.
"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)

    except json.JSONDecodeError:

        return {
            "article_types": [],
            "usage": "",
            "gender": "",
            "preferred_colours": []
        }
    
def generate_recommendation_explanation(
    user_prompt,
    vision_context,
    user_intent,
    recommendations
):

    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version="2024-02-15-preview"
    )

    recommendation_summary = recommendations[
        [
            "productDisplayName",
            "articleType",
            "baseColour",
            "usage",
            "score"
        ]
    ].head(6).to_dict(orient="records")

    system_prompt = """
You are a fashion recommendation explanation assistant.

Explain why the recommended fashion products match the user's request and uploaded image.

Keep the explanation:
- short
- clear
- professional
- suitable for a university AI project demo

Do not mention internal implementation details such as dataframe filtering or scoring weights.
"""

    user_message = f"""
User request:
{user_prompt}

Azure Vision context:
{vision_context}

Extracted user intent:
{user_intent}

Top recommendations:
{recommendation_summary}

Write one concise paragraph explaining why these recommendations were selected.
"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content