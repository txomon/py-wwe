from wwe.recorder import BankHoliday, PersonalHoliday, Recorder, Task
from datetime import datetime
import pytest


@pytest.fixture
def holiday_date():
    holiday_date = datetime(2018, 1, 10)
    return holiday_date


@pytest.fixture
def bank_holiday_date(holiday_date):
    bank_holiday_date = BankHoliday(holiday_date)
    return bank_holiday_date


@pytest.fixture
def personal_holiday_date(holiday_date):
    personal_holiday_date = PersonalHoliday(holiday_date)
    return personal_holiday_date


def test_bank_holiday(bank_holiday_date):
    bank_holiday = BankHoliday(bank_holiday_date)

    assert bank_holiday.category == 'bank holiday'
    assert bank_holiday.GetDuration() == 7.5
    assert bank_holiday.date == bank_holiday_date


def test_personal_holiday(personal_holiday_date):
    personal_holiday = PersonalHoliday(personal_holiday_date)

    assert personal_holiday.category == 'personal holiday'
    assert personal_holiday.GetDuration() == 7.5
    assert personal_holiday.date == personal_holiday_date


def test_task():
    project = "Bot Builder"
    task = "General"
    start = datetime(2018, 5, 12, 9, 0, 0)
    end = datetime(2018, 5, 12, 16, 0, 0)

    task_object = Task(start, end, project, task)

    assert task_object.category == "task"
    assert task_object.project == project
    assert task_object.task == task
    assert task_object.start == start
    assert task_object.end == end
    assert task_object.get_duration() == 7


def test_task_raises_exception_if_start_is_later_than_end():
    start = datetime(2018, 5, 12, 9, 0, 0)
    end = datetime(2018, 5, 12, 8, 0, 0)

    with pytest.raises(Exception):
        Task(start=start, end=end)


def create_task():
    task_start_date = datetime(2018, 1, 10, 16)
    task_end_date = datetime(2018, 1, 10, 17)
    task = Task(task_start_date, task_end_date)
    return task


def create_personal_holiday():
    personal_holiday_date = datetime(2018, 1, 11)
    personal_holiday = PersonalHoliday(personal_holiday_date)
    return personal_holiday


def create_bank_holiday():
    bank_holiday_date = datetime(2018, 1, 12)
    bank_holiday = BankHoliday(bank_holiday_date)
    return bank_holiday


def test_add_records():
    task = create_task()
    bank_holiday = create_bank_holiday()
    personal_holiday = create_personal_holiday()
    recorder = Recorder()

    recorder.add_record(task)
    recorder.add_record(bank_holiday)
    recorder.add_record(personal_holiday)

    assert len(recorder.records) == 3
