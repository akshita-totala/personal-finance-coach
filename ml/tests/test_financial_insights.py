
from ml.analytics.financial_insights import generate_financial_insights


def main():
    insights = generate_financial_insights()

    print("\n--- PERSONAL FINANCE INSIGHTS ---\n")

    for index, insight in enumerate(insights, start=1):
        print(f"{index}. {insight}")

    print("\nFinancial insights generated successfully!")


if __name__ == "__main__":
    main()
