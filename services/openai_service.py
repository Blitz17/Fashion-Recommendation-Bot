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

Extract the user's shopping intent into valid JSON only.

The user may mention clothing they already own, wear, or currently have.
Do NOT recommend those same items unless explicitly requested.

The system should recommend NEW complementary fashion items.

If the user clearly asks for a specific item type,
include that item type first.

If the user does not clearly specify an item type,
infer 1 to 3 useful complementary fashion item categories.

Examples:
- blazer/shirt/top mentioned → recommend Formal Shoes, Trousers, Watches
- shoes mentioned → recommend Shirts, Tops, Jackets
- dress mentioned → recommend Heels, Handbags, Jewellery Set
- casual outfit mentioned → recommend Casual Shoes
- sports outfit mentioned → recommend Sports Shoes

The usage should represent the occasion or context,
NOT the existing clothing item.

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
- Use ONLY allowed article types.
- The first article type should be the most relevant.
- preferred_colours should contain ONLY allowed colours.
- usage should contain ONLY allowed usage values.
- gender should contain ONLY allowed gender values.
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