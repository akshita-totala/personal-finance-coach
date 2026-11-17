
from sklearn.linear_model import LinearRegression
import numpy as np

from ml.analytics.spending_analysis import get_monthly_spending


MIN_MONTHS_REQUIRED = 3


def validate_months(monthly_spending):
    """Ensure monthly data is sufficient and consecutive."""

    if len(monthly_spending) < MIN_MONTHS_REQUIRED:
        raise ValueError(
            f"At least {MIN_MONTHS_REQUIRED} months of data "
            "are required for forecasting."
        )

    months = sorted(monthly_spending.keys())

    month_numbers = []

    for month in months:
        year, month_number = map(int, month.split("-"))

        if not 1 <= month_number <= 12:
            raise ValueError(f"Invalid month: {month}")

        month_numbers.append(year * 12 + month_number)

    if any(
        month_numbers[i] - month_numbers[i - 1] != 1
        for i in range(1, len(month_numbers))
    ):
        raise ValueError("Monthly data must contain consecutive months.")

    return months


def forecast_monthly_spending(monthly_spending, periods=1):
    """
    Forecast future expenditure using linear regression.

    Input:
        {"2026-01": 5000, "2026-02": 6000, ...}

    Returns forecast values and a moving-average baseline.
    """

    if not isinstance(periods, int) or isinstance(periods, bool) or periods < 1:
        raise ValueError("Periods must be a positive integer.")

    if any(
        not np.isfinite(float(value)) or float(value) < 0
        for value in monthly_spending.values()
    ):
        raise ValueError("Spending values must be finite and non-negative.")

    months = validate_months(monthly_spending)

    values = np.array(
        [float(monthly_spending[month]) for month in months]
    )

    # Time indices for historical observations
    X = np.arange(len(values)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, values)

    # Predict future months
    future_X = np.arange(
        len(values),
        len(values) + periods
    ).reshape(-1, 1)

    predictions = model.predict(future_X)

    # Expenditure cannot be negative
    predictions = np.maximum(predictions, 0)

    moving_average = float(np.mean(values[-3:]))

    last_year, last_month = map(int, months[-1].split("-"))

    forecasts = []

    for index, prediction in enumerate(predictions, start=1):
        month_index = last_year * 12 + last_month - 1 + index
        year = month_index // 12
        month = month_index % 12 + 1

        forecasts.append({
            "month": f"{year:04d}-{month:02d}",
            "predicted_spending": round(float(prediction), 2)
        })

    return {
        "historical_months": len(values),
        "moving_average_baseline": round(moving_average, 2),
        "forecasts": forecasts
    }


def forecast_from_database(periods=1):
    """Forecast using actual PostgreSQL transaction history."""

    monthly_spending = get_monthly_spending()

    return forecast_monthly_spending(
        monthly_spending,
        periods=periods
    )
