import os
import streamlit as st

from services.recommendation_engine import (
    load_dataset,
    filter_products
)

from services.openai_service import (
    extract_user_intent,
    generate_recommendation_explanation
)

from services.vision_service import (
    analyze_image
)

from utils.vision_rules import (
    get_vision_preferences
)

st.set_page_config(
    page_title="StyleMate",
    layout="wide"
)

st.title("StyleMate")
st.subheader("Multimodal Fashion Recommendation Bot")

df = load_dataset()

uploaded_image = st.file_uploader(
    "Upload Clothing Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image is not None:

    st.image(
        uploaded_image,
        caption="Uploaded Clothing Image",
        width=250
    )

user_prompt = st.text_area(
    "Describe what you are looking for"
)

recommend_button = st.button(
    "Generate Recommendations"
)

if recommend_button:

    vision_context = {}
    vision_preferences = {}

    if uploaded_image is not None:

        image_bytes = uploaded_image.getvalue()

        with st.spinner(
            "Analyzing image..."
        ):

            vision_context = analyze_image(
                image_bytes
            )

            vision_preferences = get_vision_preferences(
                vision_context
            )

    with st.spinner(
        "Understanding user intent..."
    ):

        user_intent = extract_user_intent(
            user_prompt
        )

    with st.expander("View Azure Vision Output"):
        st.json(vision_context)

    with st.expander("View Azure OpenAI Intent"):
        st.json(user_intent)

    with st.expander("View Vision-Based Preferences"):
        st.json(vision_preferences)

    article_types = user_intent.get(
        "article_types",
        []
    )

    usage = user_intent.get(
        "usage",
        ""
    )

    gender = user_intent.get(
        "gender",
        ""
    )

    colors = user_intent.get(
        "preferred_colours",
        []
    )

    results = filter_products(
        df,
        article_types=article_types,
        usage=usage,
        colors=colors,
        gender=gender,
        vision_preferences=vision_preferences,
        top_n=30
    )

    if len(results) > 0:

        with st.spinner("Generating recommendation explanation..."):

            explanation = generate_recommendation_explanation(
                user_prompt=user_prompt,
                vision_context=vision_context,
                user_intent=user_intent,
                recommendations=results
            )

        st.subheader("Recommendation Explanation")
        st.write(explanation)

    st.subheader(
        f"Recommendations Found: {len(results)}"
    )

    cols = st.columns(6)

    display_count = 0

    for _, row in results.iterrows():

        image_path = (
            f"dataset/images/{row['id']}.jpg"
        )

        if not os.path.exists(image_path):
            continue

        with cols[display_count % 6]:

            st.image(
                image_path,
                width=100
            )

            st.caption(
                row["productDisplayName"][:40]
            )

            st.caption(
                f"{row['articleType']} | "
                f"{row['baseColour']} | "
                f"{row['usage']}"
            )

            st.caption(
                f"Match Score: {row['score']}"
            )

        display_count += 1
