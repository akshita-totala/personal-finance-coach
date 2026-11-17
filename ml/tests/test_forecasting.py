
from ml.analytics.forecasting import (
    forecast_monthly_spending,
    forecast_from_database
)


def test_forecasting_with_sample_data():
    sample_data = {
        "2026-01": 5000,
        "2026-02": 6000,
        "2026-03": 7000,
        "2026-04": 8000,
        "2026-05": 9000,
        "2026-06": 10000
    }

    result = forecast_monthly_spending(sample_data)

    assert len(result["forecasts"]) == 1
    assert result["forecasts"][0]["month"] == "2026-07"
    assert result["forecasts"][0]["predicted_spending"] == 11000
    assert result["moving_average_baseline"] == 9000

    print("PASS: Linear regression forecasting works.")


def test_insufficient_data():
    sample_data = {
        "2026-07": 4950
    }

    try:
        forecast_monthly_spending(sample_data)
        assert False, "Expected ValueError"

    except ValueError as error:
        assert "At least 3 months" in str(error)

    print("PASS: Insufficient historical data handled.")


def test_missing_month():
    sample_data = {
        "2026-01": 5000,
        "2026-02": 6000,
        "2026-04": 8000
    }

    try:
        forecast_monthly_spending(sample_data)
        assert False, "Expected ValueError"

    except ValueError as error:
        assert "consecutive months" in str(error)

    print("PASS: Missing months handled.")


def test_database_forecast():
    try:
        result = forecast_from_database()
        print("Database forecast:", result)

    except ValueError as error:
        print("Database forecast unavailable:", error)


if __name__ == "__main__":
    test_forecasting_with_sample_data()
    test_insufficient_data()
    test_missing_month()
    test_database_forecast()

    print("\nForecasting tests completed!")
