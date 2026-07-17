def categorize_transaction(description):
    description = description.upper()

    categories = {
        "Food": [
            "SWIGGY",
            "ZOMATO",
            "DOMINOS",
            "PIZZA",
            "MCDONALD",
            "BURGER KING",
            "CAFE"
        ],

        "Shopping": [
            "AMAZON",
            "FLIPKART",
            "MYNTRA",
            "AJIO",
            "NYKAA"
        ],

        "Travel": [
            "UBER",
            "OLA",
            "RAPIDO",
            "IRCTC"
        ],

        "Entertainment": [
            "NETFLIX",
            "SPOTIFY",
            "HOTSTAR",
            "PRIME VIDEO"
        ],

        "Income": [
            "SALARY",
            "CREDIT INTEREST"
        ],

        "Utilities": [
            "ELECTRICITY",
            "WATER",
            "GAS",
            "AIRTEL",
            "JIO",
            "VI"
        ]
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                return category

    return "Others"