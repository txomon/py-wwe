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


def test_records_will_not_be_added_twice():
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


def test_record_get_date():
    task = create_task()
    bank_holiday = create_bank_holiday()
    personal_holiday = create_personal_holiday()

    assert task.get_date is not None
    assert bank_holiday.get_date is not None
    assert personal_holiday.get_date is not None


def test_get_records_between_dates():
    start_date = datetime(2018, 1, 11)
    end_date = datetime(2018, 1, 14)
    bh1 = create_bank_holiday(date=datetime(2018, 1, 10))
    bh2 = create_bank_holiday(date=datetime(2018, 1, 12))
    bh3 = create_bank_holiday(date=datetime(2018, 1, 14))
    bh4 = create_bank_holiday(date=datetime(2018, 1, 16))
    r = Recorder()

    r.add(bh1, bh2, bh3, bh4)
    actual_result = r.records_between(start_date, end_date)
    expected_result = set()
    expected_result.add(bh2)
    expected_result.add(bh3)

    assert expected_result == actual_result


def test_no_personal_holidays_used():
    bh = create_bank_holiday(date=datetime(2018, 1, 10))
    r = Recorder()
    r.add(bh)
    actual_result = r.personal_holidays_used()
    expected_result = 0

    assert expected_result == actual_result


def test_personal_holidays_used():
    bh = create_bank_holiday(date=datetime(2018, 1, 10))
    ph1 = create_personal_holiday(date=datetime(2018, 1, 11))
    ph2 = create_personal_holiday(date=datetime(2018, 1, 12))
    r = Recorder()

    r.add(bh)
    r.add(ph1)
    r.add(ph2)
    actual_result = r.personal_holidays_used()
    expected_result = 2

    assert expected_result == actual_result


def test_personal_holidays_left_no_total_set():
    ph = create_personal_holiday(date=datetime(2018, 1, 11))
    r = Recorder()
    r.add(ph)

    with pytest.raises(Exception):
        r.personal_holidays_left()


def test_personal_holidays_left():
    ph1 = create_personal_holiday(date=datetime(2018, 1, 11))
    ph2 = create_personal_holiday(date=datetime(2018, 1, 12))
    r = Recorder()
    r.total_personal_holidays = 10

    r.add(ph1)
    r.add(ph2)
    actual_result = r.personal_holidays_left()
    expected_result = 8

    assert expected_result == actual_result


def test_total_worked_hours_without_record():
    start = datetime(2015, 1, 1)
    r = Recorder()

    with pytest.raises(Exception):
        r.total_worked_hours(start)


@pytest.mark.parametrize("start,end", [
    (None, datetime(2018, 1, 1)),
    (datetime(2018, 1, 1), None),
    (datetime(2018, 1, 3), datetime(2018, 1, 1)),
])
def test_total_worked_hours_with_null_arguments(start, end):
    t = create_task()
    r = Recorder()
    r.add(t)

    with pytest.raises(Exception):
        r.total_worked_hours(start, end)


def test_total_worked_hours_with_expected_date():
    start = datetime(2018, 1, 1)
    end = datetime(2018, 1, 3)
    t = create_task(start=datetime(2018, 1, 2, 8), end=datetime(2018, 1, 2, 9))
    r = Recorder()
    r.add(t)

    actual_result = r.total_worked_hours(start, end)
    expected_result = 1.0

    assert expected_result == actual_result


def test_total_hours_to_work_no_holidays_no_weekend():
    start = datetime(2018, 3, 6)
    end = datetime(2018, 3, 8)
    r = Recorder()

    actual_result = r.total_hours_to_work(start, end)
    expected_result = 3 * 7.5

    assert expected_result == actual_result


def test_total_hours_to_work_with_holidays_and_weekend():
    start = datetime(2018, 3, 28)
    end = datetime(2018, 4, 4)
    bh = create_bank_holiday(date=datetime(2018, 4, 2))  # Easter Monday
    ph = create_personal_holiday(date=datetime(2018, 4, 3))  # Easter Monday
    r = Recorder()

    r.add(bh)
    r.add(ph)
    actual_result = r.total_hours_to_work(start, end)
    # 8 real days - (2 weekend days + 1 bank holiday + 1 personal holiday)
    expected_result = (8 - (2 + 1 + 1)) * 7.5

    assert expected_result == actual_result


def test_hour_balance_on_end_no_date():
    pass

# def test_hour_balance_on_end():
#     start = datetime(2018, 4, 3)
#     end = datetime(2018, 4, 6)
#     r = Recorder()
#     actual_result = r.hour_balance_on_end(start, end)
#     expected_result = -4 * 7.5

#     assert expected_result == actual_result
#     pass
