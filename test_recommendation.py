from services.recommendation_engine import (
    load_dataset,
    filter_products
)

df = load_dataset()

results = filter_products(
    df,
    article_type="Shoes",
    usage="Formal",
    colors=["Black", "Brown"]
)

print(results[
    [
        "productDisplayName",
        "articleType",
        "baseColour",
        "usage"
    ]
].head(10))