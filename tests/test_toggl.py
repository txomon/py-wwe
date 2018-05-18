# from wwe.toggl import TogglWrap
from tests.test_config import mock_config


def test_empty(mock_config):
    c = mock_config
    assert c.get("toggl").get("timezone") == "+00:00"
