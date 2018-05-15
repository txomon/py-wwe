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

    def total_worked_hours(self, date: datetime.datetime):
        """Returns total hours worked from a given date"""
        pass

    def total_hours_to_work(self, start: datetime.datetime,
                            end: datetime.datetime):
        """Return total hours to be worked between two given dates"""
        pass

    def hours_today_on_end(self, end=datetime.datetime):
        """Return total hours to be worked/left until a given datetime"""
        pass

    def personal_holidays_used(self):
        """Return number of personal holidays used"""
        # Add the total personal holidays you can take in the config file
        result = 0
        for record in self.records:
            if isinstance(record, PersonalHoliday):
                result += 1
        return result

    def summary(self):
        """Return current work hours summary"""
        # {total: 37.5, worked: 28.5, left: 3.2}
        pass
