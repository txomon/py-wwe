from tapioca_toggl import Toggl
from datetime import datetime
from config import import_config

# api = Toggl(access_token="b0769e321caa66ba4cdb946598ba6e88")
# me = api.me_with_related_data().get().data()
# print(me)


class TogglWrap:
    def __init__(self, token=""):
        if token != "" and token is not None:
            print("jey! token received! :D")
            self.toggl = Toggl(access_token=token)
            print("Toggl client wrapper created!")

    def get_tasks(self, start: datetime, end: datetime, client: str):
        """Return tasks from Toggl between two given dates for a client"""
        if self.toggl is not None:

            print("fetching your tasks!")


cfg = import_config('./config.json')
t = TogglWrap(token=cfg['toggl']['token'])
start_date = datetime(2018, 2, 5)
end_date = datetime(2018, 2, 7)
client = "Software Imaging"
t.get_tasks(start_date, end_date, client)
