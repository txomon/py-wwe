import datetime


class Record:

    def __repr__(self):
        result = self.__class__.__name__ + " instance: { "

        props = self.__dict__
        print(self.__class__.__dict__.keys())
        keys = props.keys()

        for i, key in enumerate(keys):
            result += f"{key}: {props[key]}"
            if i < len(props) - 1:
                result += ", "

        result += " }"

        return result

    def get_duration(self):
        """Return record duration"""
        return self.duration

    def get_date(self):
        """Return record date"""
        class_name = self.__class__.__name__
        if class_name == 'Task':
            return self.start
        else:
            return self.date


class Task(Record):
    category = "task"

    # Allow weekend days

    def __init__(self, start: datetime.datetime, end: datetime.datetime,
                 project="no project", task="no task description"):
        if start > end:
            raise Exception("start cannot be later than end")
        self.project = project
        self.task = task
        self.start = start
        self.end = end
        self.duration = end-start

    def __hash__(self):
        result = hash(self.category)
        result += hash(self.project)
        result += hash(self.task)
        result += hash(self.start) ^ hash(self.end)
        return result

    def get_duration(self) -> float:
        """Return record duration"""
        total_hours = self.duration.total_seconds() / 3600
        return total_hours


class Holiday(Record):
    duration = 7.5

    def __init__(self, date):
        self.date = date


class BankHoliday(Holiday):
    category = "bank holiday"

    def __init__(self, date):
        self.date = date

    def __hash__(self):
        return hash(self.category) + hash(self.date)


class PersonalHoliday(Holiday):
    category = "personal holiday"

    def __init__(self, date):
        self.date = date

    def __hash__(self):
        return hash(self.category) + hash(self.date)


class Recorder:
    def __init__(self):
        self.records = set()

        # TODO pass this in the constructor.
        # Implement a factory for the tests
        self.work_day = 7.5

    def _bank_holidays(self, start: datetime.datetime, end: datetime.datetime):
        """Return total bank holidays between to given dates"""
        result = 0
        if self.records is not None:
            for record in self.records:
                if isinstance(record, Holiday):
                    print(f"holiday found! >> {record}")
                    result += 1

        return result

    def _weekend_days(self, start: datetime.datetime, end: datetime.datetime):
        # Calculate number of weekend days between start and end dates
        day_generator = (start + datetime.timedelta(x+1)
                         for x in range((end - start).days))
        result = sum(1 for day in day_generator if day.weekday() > 4)
        return result

    def add(self, *args):
        """Add one or more records"""
        for record in args:
            if isinstance(record, Record):
                self.records.add(record)

    def records_between(self, start: datetime.datetime,
                        end: datetime.datetime):
        """Return records between start and end dates, both included"""
        result = set()
        for record in self.records:
            date = record.get_date()
            if start <= date and date <= end:
                result.add(record)
        return result

    def total_worked_hours(self, start: datetime.datetime,
                           end: datetime.datetime):
        """Returns total hours worked from a given date"""
        # TODO (BUG):
        # You need an end date, otherwise, the future holidays will be also
        # added to the days off, and they shouldn't. Add a unit test to cover
        # this case.
        if len(self.records) == 0:
            raise Exception("no records in recorder")
        if start is None:
            raise TypeError("start cannot be None")
        if end is None:
            raise TypeError("end cannot be None")
        if start > end:
            raise Exception("start date cannot be later than end")

        result = 0
        records_subset = self.records_between(start, end)
        for record in records_subset:
            if isinstance(record, Task):
                duration = record.get_duration()
                result += duration
        return result

    def total_hours_to_work(self, start: datetime.datetime,
                            end: datetime.datetime):
        """Return total hours to be worked between two given dates"""
        total_days = (end.date() - start.date()).days + 1

        days_off = 0
        days_off += self._bank_holidays(start, end)
        days_off += self._weekend_days(start, end)

        work_days = total_days - days_off
        work_hours = work_days * self.work_day
        return work_hours

    def hour_balance_on_end(self, start: datetime.datetime,
                            end: datetime.datetime):
        """Return total hours to be worked/left between two given datetimes"""
        result = 0
        to_work = self.total_hours_to_work(start, end)
        worked = self.total_worked_hours(start, end)
        pass

    def personal_holidays_left(self):
        """Return number of personal holidays left"""
        total = self.total_personal_holidays
        if total is None:
            raise Exception("no total_personal_holidays set")
        used = self.personal_holidays_used()
        return total - used

    def personal_holidays_used(self):
        """Return number of personal holidays used"""
        # TODO: Add the total personal holidays you can take in the config file
        result = 0
        for record in self.records:
            if isinstance(record, PersonalHoliday):
                result += 1
        return result

    def summary(self):
        """Return current work hours summary"""
        # {total: 37.5, worked: 28.5, left: 3.2}
        pass
