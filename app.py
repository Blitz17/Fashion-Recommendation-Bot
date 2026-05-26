import os
import streamlit as st

from services.recommendation_engine import (
    load_dataset,
    filter_products
)

st.set_page_config(
    page_title="StyleMate",
    layout="wide"
)

st.title("StyleMate")
st.subheader("Multimodal Fashion Recommendation Bot")

df = load_dataset()

st.sidebar.header("Recommendation Settings")

article_type = st.sidebar.selectbox(
    "Select Clothing Type",
    sorted(df["articleType"].dropna().unique())
)

usage = st.sidebar.selectbox(
    "Select Usage",
    sorted(df["usage"].dropna().unique())
)

gender = st.sidebar.selectbox(
    "Select Gender",
    sorted(df["gender"].dropna().unique())
)

color = st.sidebar.selectbox(
    "Select Colour",
    sorted(df["baseColour"].dropna().unique())
)

recommend_button = st.sidebar.button("Recommend")

if recommend_button:

    results = filter_products(
        df,
        article_type=article_type,
        usage=usage,
        colors=[color],
        gender=gender
    )

    st.write(f"Total Recommendations Found: {len(results)}")

    cols = st.columns(6)

    display_count = 0

    for _, row in results.iterrows():

        image_path = f"dataset/images/{row['id']}.jpg"

        if not os.path.exists(image_path):
            continue

        with cols[display_count % 6]:

            st.image(
                image_path,
                width=100
            )

            st.caption(row['productDisplayName'][:40])

            st.caption(
                f"{row['articleType']} | "
                f"{row['baseColour']} | "
                f"{row['usage']}"
            )
        display_count += 1

        if display_count >= 12:
            break