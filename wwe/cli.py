from pprint import pprint as print
from wwe.toggl import TogglWrap
from wwe.config import import_config
from datetime import datetime


def main():
    c = import_config('./config.json')
    t = TogglWrap(token=c['toggl_token'])
    print(t.get_today())
    start = datetime(2018, 2, 5)
    end = datetime.today()
