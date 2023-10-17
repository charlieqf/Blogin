# date_utils.py
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def end_of_next_month(input_date):
    # First, add one month to the date
    next_month_date = input_date + relativedelta(months=1)

    # Then, find the first day of the subsequent month
    first_day_of_subsequent_month = next_month_date.replace(day=1) + relativedelta(months=1)

    # Finally, subtract one day from the first day of the subsequent month to get the end of the next month
    return first_day_of_subsequent_month - timedelta(days=1)