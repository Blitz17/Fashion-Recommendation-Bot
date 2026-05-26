import pandas as pd


def load_dataset():

    df = pd.read_csv(
        "dataset/styles.csv",
        on_bad_lines="skip"
    )

    df = df.dropna(
        subset=[
            "id",
            "articleType",
            "baseColour",
            "usage"
        ]
    )

    df["id"] = df["id"].astype(str)

    return df


def filter_products(
    df,
    article_types=None,
    usage=None,
    colors=None,
    gender=None,
    vision_preferences=None,
    top_n=18
):

    scored_products = []

    for _, row in df.iterrows():

        score = 0

        article_type = str(row["articleType"])
        product_usage = str(row["usage"])
        product_colour = str(row["baseColour"])
        product_gender = str(row["gender"])

        if article_types:

            for requested_type in article_types:

                if requested_type.lower() in article_type.lower():

                    score += 5
                    break

        if usage:

            if usage.lower() in product_usage.lower():

                score += 3

        if colors:

            if product_colour in colors:

                score += 2

        if gender:

            if gender.lower() in product_gender.lower():

                score += 1

        if vision_preferences:

            preferred_types = vision_preferences.get(
                "preferred_article_types",
                []
            )

            avoided_types = vision_preferences.get(
                "avoided_article_types",
                []
            )

            preferred_colours = vision_preferences.get(
                "preferred_colours",
                []
            )

            for preferred in preferred_types:

                if preferred.lower() in article_type.lower():

                    score += 4

            for avoided in avoided_types:

                if avoided.lower() in article_type.lower():

                    score -= 8

            if product_colour in preferred_colours:

                score += 2

        if score > 0:

            row_data = row.to_dict()

            row_data["score"] = score

            scored_products.append(row_data)

    scored_df = pd.DataFrame(scored_products)

    if len(scored_df) == 0:
        return scored_df

    scored_df = scored_df.sort_values(
        by="score",
        ascending=False
    )

    return scored_df.head(top_n)
