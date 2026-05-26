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
    article_type=None,
    usage=None,
    colors=None,
    gender=None
):
    filtered_df = df.copy()

    if article_type:
        filtered_df = filtered_df[
            filtered_df["articleType"]
            .str.contains(article_type, case=False, na=False)
        ]

    if usage:
        filtered_df = filtered_df[
            filtered_df["usage"]
            .str.contains(usage, case=False, na=False)
        ]

    if colors:
        filtered_df = filtered_df[
            filtered_df["baseColour"]
            .isin(colors)
        ]

    if gender:
        filtered_df = filtered_df[
            filtered_df["gender"]
            .str.contains(gender, case=False, na=False)
        ]

    return filtered_df