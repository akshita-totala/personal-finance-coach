
from ml.analytics.spending_analysis import (
    get_spending_summary,
    get_category_breakdown,
    get_monthly_spending
)


def main():
    print("\n--- SPENDING SUMMARY ---")
    print(get_spending_summary())

    print("\n--- CATEGORY BREAKDOWN ---")
    print(get_category_breakdown())

    print("\n--- MONTHLY SPENDING ---")
    print(get_monthly_spending())


if __name__ == "__main__":
    main()
