def get_vision_preferences(vision_context):
    tags = [
        tag.lower()
        for tag in vision_context.get("tags", [])
    ]

    caption = vision_context.get("caption", "").lower()

    combined_text = " ".join(tags) + " " + caption

    preferred_article_types = []
    avoided_article_types = []
    preferred_colours = []
    preferred_usage = ""
    style_type = ""

    def add_unique(target_list, values):
        for value in values:
            if value not in target_list:
                target_list.append(value)

    # -------------------------
    # Colour extraction
    # -------------------------

    colour_map = {
        "black": "Black",
        "white": "White",
        "blue": "Blue",
        "navy": "Navy Blue",
        "navy blue": "Navy Blue",
        "grey": "Grey",
        "gray": "Grey",
        "brown": "Brown",
        "tan": "Tan",
        "beige": "Beige",
        "cream": "Cream",
        "green": "Green",
        "olive": "Olive",
        "red": "Red",
        "maroon": "Maroon",
        "pink": "Pink",
        "purple": "Purple",
        "yellow": "Yellow",
        "orange": "Orange",
        "gold": "Gold",
        "silver": "Silver"
    }

    for key, dataset_colour in colour_map.items():
        if key in combined_text:
            add_unique(preferred_colours, [dataset_colour])

    # -------------------------
    # Existing topwear detected
    # -------------------------

    if (
        "shirt" in combined_text
        or "t-shirt" in combined_text
        or "tshirt" in combined_text
        or "tee" in combined_text
        or "top" in combined_text
        or "hoodie" in combined_text
        or "sweatshirt" in combined_text
        or "blouse" in combined_text
    ):
        add_unique(
            avoided_article_types,
            [
                "Shirts",
                "Tshirts",
                "Tops",
                "Sweatshirts"
            ]
        )

        add_unique(
            preferred_article_types,
            [
                "Jeans",
                "Trousers",
                "Shorts",
                "Casual Shoes",
                "Watches",
                "Backpacks",
                "Handbags"
            ]
        )

        style_type = "casual"
        preferred_usage = "Casual"

    # -------------------------
    # Hoodie / streetwear
    # -------------------------

    if (
        "hoodie" in combined_text
        or "sweatshirt" in combined_text
    ):
        add_unique(
            preferred_article_types,
            [
                "Casual Shoes",
                "Sports Shoes",
                "Jackets",
                "Caps",
                "Backpacks",
                "Track Pants"
            ]
        )

        add_unique(
            avoided_article_types,
            [
                "Formal Shoes",
                "Suits",
                "Blazers",
                "Ties",
                "Ties and Cufflinks"
            ]
        )

        style_type = "streetwear"
        preferred_usage = "Casual"

    # -------------------------
    # Formal upperwear detected
    # -------------------------

    if (
        "blazer" in combined_text
        or "suit" in combined_text
        or "formal" in combined_text
    ):
        add_unique(
            avoided_article_types,
            [
                "Blazers",
                "Suits",
                "Shirts"
            ]
        )

        add_unique(
            preferred_article_types,
            [
                "Formal Shoes",
                "Trousers",
                "Watches",
                "Ties",
                "Belts",
                "Wallets"
            ]
        )

        style_type = "formal"
        preferred_usage = "Formal"

    # -------------------------
    # Dress detected
    # -------------------------

    if (
        "dress" in combined_text
        or "gown" in combined_text
    ):
        add_unique(
            avoided_article_types,
            [
                "Dresses"
            ]
        )

        add_unique(
            preferred_article_types,
            [
                "Heels",
                "Handbags",
                "Clutches",
                "Earrings",
                "Necklace and Chains",
                "Bracelet",
                "Watches"
            ]
        )

        style_type = "party"
        preferred_usage = "Party"

    # -------------------------
    # Jeans / bottomwear detected
    # -------------------------

    if (
        "jeans" in combined_text
        or "trousers" in combined_text
        or "pants" in combined_text
        or "shorts" in combined_text
        or "skirt" in combined_text
    ):
        add_unique(
            avoided_article_types,
            [
                "Jeans",
                "Trousers",
                "Shorts",
                "Skirts",
                "Track Pants"
            ]
        )

        add_unique(
            preferred_article_types,
            [
                "Shirts",
                "Tshirts",
                "Tops",
                "Jackets",
                "Casual Shoes",
                "Formal Shoes",
                "Watches"
            ]
        )

    # -------------------------
    # Shoes detected
    # -------------------------

    if (
        "shoe" in combined_text
        or "shoes" in combined_text
        or "sneaker" in combined_text
        or "sneakers" in combined_text
        or "footwear" in combined_text
    ):
        add_unique(
            avoided_article_types,
            [
                "Casual Shoes",
                "Formal Shoes",
                "Sports Shoes",
                "Flats",
                "Heels",
                "Sandals",
                "Flip Flops"
            ]
        )

        add_unique(
            preferred_article_types,
            [
                "Jeans",
                "Trousers",
                "Shirts",
                "Tshirts",
                "Tops",
                "Jackets",
                "Watches",
                "Backpacks",
                "Handbags"
            ]
        )

    # -------------------------
    # Sportswear detected
    # -------------------------

    if (
        "sports" in combined_text
        or "sport" in combined_text
        or "gym" in combined_text
        or "fitness" in combined_text
        or "active" in combined_text
    ):
        add_unique(
            preferred_article_types,
            [
                "Sports Shoes",
                "Track Pants",
                "Tracksuits",
                "Tshirts",
                "Caps",
                "Wristbands",
                "Water Bottle"
            ]
        )

        add_unique(
            avoided_article_types,
            [
                "Formal Shoes",
                "Suits",
                "Blazers",
                "Ties"
            ]
        )

        style_type = "sports"
        preferred_usage = "Sports"

    # -------------------------
    # Bag detected
    # -------------------------

    if (
        "bag" in combined_text
        or "backpack" in combined_text
        or "handbag" in combined_text
        or "clutch" in combined_text
        or "purse" in combined_text
    ):
        add_unique(
            avoided_article_types,
            [
                "Backpacks",
                "Handbags",
                "Clutches",
                "Duffel Bag",
                "Messenger Bag",
                "Laptop Bag",
                "Trolley Bag"
            ]
        )

        add_unique(
            preferred_article_types,
            [
                "Casual Shoes",
                "Formal Shoes",
                "Watches",
                "Sunglasses",
                "Wallets",
                "Belts"
            ]
        )

    # -------------------------
    # Accessories detected
    # -------------------------

    if (
        "watch" in combined_text
        or "jewellery" in combined_text
        or "jewelry" in combined_text
        or "necklace" in combined_text
        or "earring" in combined_text
        or "bracelet" in combined_text
        or "ring" in combined_text
    ):
        add_unique(
            avoided_article_types,
            [
                "Watches",
                "Jewellery Set",
                "Necklace and Chains",
                "Earrings",
                "Bracelet",
                "Ring"
            ]
        )

        add_unique(
            preferred_article_types,
            [
                "Dresses",
                "Tops",
                "Shirts",
                "Formal Shoes",
                "Heels",
                "Handbags"
            ]
        )

    # -------------------------
    # Weather / outerwear clues
    # -------------------------

    if (
        "winter" in combined_text
        or "cold" in combined_text
        or "coat" in combined_text
    ):
        add_unique(
            preferred_article_types,
            [
                "Jackets",
                "Sweaters",
                "Sweatshirts",
                "Scarves",
                "Mufflers",
                "Gloves"
            ]
        )

    if (
        "rain" in combined_text
        or "raincoat" in combined_text
        or "umbrella" in combined_text
    ):
        add_unique(
            preferred_article_types,
            [
                "Rain Jacket",
                "Rain Trousers",
                "Umbrellas"
            ]
        )

    return {
        "style_type": style_type,
        "preferred_usage": preferred_usage,
        "preferred_article_types": preferred_article_types,
        "avoided_article_types": avoided_article_types,
        "preferred_colours": preferred_colours
    }