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
    assert bank_holiday.get_duration() == 7.5
    assert bank_holiday.date == bank_holiday_date


def test_personal_holiday(personal_holiday_date):
    personal_holiday = PersonalHoliday(personal_holiday_date)

    assert personal_holiday.category == 'personal holiday'
    assert personal_holiday.get_duration() == 7.5
    assert personal_holiday.date == personal_holiday_date


def test_task_is_created_with_required_properties():
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


def test_task_repr():
    task = create_task()

    actual_repr = repr(task)
    expected_repr = "Task instance: { project: no project, "
    expected_repr += "task: created with create_task, "
    expected_repr += "start: 2018-01-10 16:00:00, end: 2018-01-10 17:00:00, "
    expected_repr += "duration: 1:00:00 }"

    assert expected_repr == actual_repr


def test_bank_holiday_repr():
    bank_holiday = create_bank_holiday()

    actual_repr = repr(bank_holiday)
    expected_repr = "BankHoliday instance: { "
    expected_repr += "date: 2018-01-12 00:00:00 }"

    assert expected_repr == actual_repr


def test_personal_holiday_repr():
    personal_holiday = create_personal_holiday()

    actual_repr = repr(personal_holiday)
    expected_repr = "PersonalHoliday instance: { "
    expected_repr += "date: 2018-01-11 00:00:00 }"

    assert expected_repr == actual_repr


def test_records_cannot_be_added_twice():
    recorder = Recorder()
    task = create_task()
    bank_holiday = create_bank_holiday()
    personal_holiday = create_personal_holiday()

    recorder.add(task)
    recorder.add(task)
    recorder.add(bank_holiday)
    recorder.add(bank_holiday)
    recorder.add(personal_holiday)
    recorder.add(personal_holiday)

    assert len(recorder.records) == 3


def test_only_add_records_to_recorder():
    recorder = Recorder()
    random_object = {}
    task = create_task()

    recorder.add(random_object)
    assert len(recorder.records) == 0

    recorder.add(task)
    assert len(recorder.records) == 1
