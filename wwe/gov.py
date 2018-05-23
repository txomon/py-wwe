import requests
import datetime


def gov_uk_bank_holidays() -> set:
    url = 'https://www.gov.uk/bank-holidays.json'
    r = requests.get(url)
    data = r.json()
    england_data = data.get('england-and-wales')
    events = england_data.get('events')
    result = set()
    for event in events:
        date_str = event.get('date')
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        result.add(date)
    return result


def gov_uk_bank_holidays_between(start: datetime.datetime, end: datetime.datetime) -> set:
    bank_holidays = gov_uk_bank_holidays()
    result = set()
    for day in bank_holidays:
        if start <= day and day <= end:
            result.add(day)
    return result
