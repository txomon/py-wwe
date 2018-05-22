# Credit to Mosab Ibrahim <mosab.a.ibrahim@gmail.com>

import requests
import datetime

from requests.auth import HTTPBasicAuth

TOGGL_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'


def toggl_format(ts: datetime.datetime):
    if not ts:
        return ''
    tz = ts.strftime('%z')
    if tz:
        tz = f'{tz[:2]}:{tz[3:]}'
    else:
        tz = '+00:00'
    return ts.strftime(TOGGL_TIMESTAMP_FORMAT) + tz


class TogglAPI(object):
    """A wrapper for Toggl Api"""

    def __init__(self, api_token):
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(api_token, 'api_token')
        self.session.headers = {'content-type': 'application/json'}

    def get(self, section, params):
        response = self.session.get(
            f'https://www.toggl.com/api/v8/{section}', params=params)
        return response.json()

    def clients(self, workspace_id=''):
        """Get Projects by Workspace ID"""
        section = f'workspaces/{workspace_id}/clients'
        return self.get(section=section)

    def get_time_entries(self, start_date: datetime.datetime='', end_date: datetime.datetime =''):
        """Get Time Entries JSON object from Toggl within a given start_date
        and an end_date with a given timezone"""
        p = {
            'start_date': toggl_format(start_date),
            'end_date': toggl_format(end_date)
        }
        return self.get(section='time_entries', params=p)

    def projects(self, workspace_id=''):
        """Get Projects by Workspace ID"""
        section = f'workspaces/{workspace_id}/projects'
        return self.get(section=section)

    def workspaces(self):
        """Get Workspaces"""
        section = f'workspaces'
        return self.get(section=section)
