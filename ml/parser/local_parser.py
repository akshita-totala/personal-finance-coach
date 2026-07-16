import re


def parse_transactions(text):
    """
    Converts extracted PDF text into structured transactions.
    """

    transactions = []

    # Remove empty lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    i = 0

    while i < len(lines):

        # Expect:
        # Date
        # Description
        # Amount
        # Debit/Credit

        if i + 3 < len(lines):

            date = lines[i]
            description = lines[i + 1]
            amount = lines[i + 2]
            txn_type = lines[i + 3]

            # Remove ₹ and commas
            amount = re.sub(r"[₹,]", "", amount)

            try:
                amount = float(amount)

                transactions.append({
                    "date": date,
                    "description": description,
                    "amount": amount,
                    "type": txn_type
                })

            except ValueError:
                pass

            i += 4

        else:
            break

    return transactions