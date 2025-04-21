from datetime import date, timedelta

def format_week_range(reference_date=None):
    today = reference_date or date.today()

    # Get the most recent Sunday (week end)
    days_since_sunday = (today.weekday() + 1) % 7
    week_end = today - timedelta(days=days_since_sunday)
    print(f"Week end (Sunday): {week_end}")

    # Start of the week is 6 days before Sunday
    week_start = week_end - timedelta(days=6)
    print(f"Week start (Monday): {week_start}")

    start_day = week_start.day
    start_month = week_start.strftime('%b').upper()
    end_day = week_end.day
    end_month = week_end.strftime('%b').upper()

    if start_month != end_month:
        formatted = f"{start_day:02}{start_month}–{end_day:02}{end_month}"
    else:
        formatted = f"{start_day:02}–{end_day:02}{end_month}"

    print(f"Formatted range: {formatted}")
    return formatted



if __name__ == "__main__":
    # test_date = date(2025, 4, 6)  # April 2, 2025
    format_week_range()
