# # POC: import config
# from wwe.config import importConfig
# config = importConfig('./config.json')
# token = config['toggl']['token']
# print(token)

# # POC: Toggl API wrapper
# from tapioca_toggl import Toggl
# api = Toggl(access_token=token)
# me = api.me_with_related_data().get()
# print(me)

# # POC: UK bank holidays
# import requests
# bank_holiday_url = "https://www.gov.uk/bank-holidays.json"
# r = requests.get(bank_holiday_url)
# print(r.json())
from recorder import Task, Holiday, BankHoliday, PersonalHoliday, Recorder
from datetime import datetime


def create_task(
        start=datetime(2018, 1, 10, 16),
        end=datetime(2018, 1, 10, 17),
        project="no project", task="created with create_task"):
    task = Task(start, end, project, task)
    return task


def create_bank_holiday(date=datetime(2018, 1, 12)):
    bank_holiday = BankHoliday(date)
    return bank_holiday


def create_personal_holiday(date=datetime(2018, 1, 11)):
    personal_holiday = PersonalHoliday(date)
    return personal_holiday


task1 = Task(
    project="Bot Builder",
    task="General",
    start=datetime(2018, 5, 10, 9, 0, 0),
    end=datetime(2018, 5, 10, 9, 0, 25)
)

task2 = Task(
    project="Bot Builder",
    task="General",
    start=datetime(2018, 5, 12, 9, 0, 0),
    end=datetime(2018, 5, 12, 9, 0, 25)
)

holiday = Holiday(datetime(2018, 5, 11))
bank_holiday = BankHoliday(datetime(2018, 5, 13))
personal_holiday = PersonalHoliday(datetime(2018, 5, 14))


# start = datetime(2018, 3, 28)
# end = datetime(2018, 4, 4)
start = datetime(2018, 1, 10, 16)
end = datetime(2018, 1, 10, 17)
t = create_task()
r = Recorder()
r.add(t)
actual_result = r.total_worked_hours(start, end)
print(f"actual_result = {actual_result}")
