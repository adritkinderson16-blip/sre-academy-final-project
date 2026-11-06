"""Product catalog for the ShikyBox pet subscription service."""

PRODUCTS = {
    "dog-adventure": {
        "id": "dog-adventure",
        "name": "Dog Adventure Box",
        "pet_type": "dog",
        "price": 29.99,
        "icon": "\U0001F436",
        "description": (
            "A monthly collection of durable toys, training treats, "
            "and outdoor accessories for adventurous dogs."
        ),
        "items": [
            "Durable adventure toy",
            "Natural training treats",
            "Outdoor pet accessory",
            "Monthly care guide",
        ],
    },
    "cat-comfort": {
        "id": "cat-comfort",
        "name": "Cat Comfort Box",
        "pet_type": "cat",
        "price": 27.99,
        "icon": "\U0001F431",
        "description": (
            "A cozy selection of interactive toys, premium treats, "
            "and comfort accessories for curious cats."
        ),
        "items": [
            "Interactive cat toy",
            "Premium cat treats",
            "Comfort accessory",
            "Monthly enrichment guide",
        ],
    },
    "small-pet-discovery": {
        "id": "small-pet-discovery",
        "name": "Small Pet Discovery Box",
        "pet_type": "small-pet",
        "price": 24.99,
        "icon": "\U0001F430",
        "description": (
            "A discovery box containing enrichment toys, healthy snacks, "
            "and habitat accessories for small pets."
        ),
        "items": [
            "Enrichment toy",
            "Healthy small-pet snacks",
            "Habitat accessory",
            "Monthly care guide",
        ],
    },
}


def get_all_products():
    """Return all products sorted by product name."""
    return sorted(PRODUCTS.values(), key=lambda product: product["name"])


def get_product(product_id):
    """Return a product by ID or None when the product does not exist."""
    return PRODUCTS.get(product_id)
