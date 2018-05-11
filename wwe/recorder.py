import datetime


class Record:
    def GetDuration(self):
        return self.duration


class Task(Record):
    category = "task"

    # Allow weekends

    def __init__(self, start: datetime.datetime, end: datetime.datetime,
                 project="no project", task="no task description"):
        if start > end:
            raise Exception("start cannot be later than end")
        self.project = project
        self.task = task
        self.start = start
        self.end = end
        self.duration = end-start

    def __repr__(self):
        result = f"Task instance: {{ "
        result += f"project: {self.project}, task: {self.task},"
        result += f"date: {self.start}, duration: {self.duration}"
        result += f" }}"
        return result

    def GetDuration(self):
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


class PersonalHoliday(Holiday):
    category = "personal holiday"

    def __init__(self, date):
        self.date = date


class Recorder:
    def __init__(self):
        self.records = []

    def AddRecord(self, record: Record):
        self.records.append(record)

    def ValidateRecord(self, record: Record):
        # Do the depp validation when you create the record, but
        # not when you add it. Later you only need to validate
        # that the created record is a Task, a BankHoliday or a
        # PersonalHoliday type.
        pass

    # def ValidateTask(self, record: Task):
    #     pass

    # def ValidateBankHoliday(self, record: BankHoliday):
    #     pass

    # def ValidatePersonalHoliday(self, record: PersonalHoliday):
    #     pass

    def RemoveDuplicatedRecords(self):
        # Ensure there are not records duplicated in self.records
        pass

    def GetRecordsBetweenDateTimes(self, start: datetime.datetime,
                                   end: datetime.datetime):
        # Is not point to get is only **from** one date, as you want to
        # exclude the future holiday days

        # Filter records in self.records array based on the dates
        # Think about how to filter the return from this method to get
        # the holidays in a separate array and the working days in a
        # separate array
        pass
