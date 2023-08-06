import os
import tempfile
from unittest import TestCase

from gaphor.services.properties import FileBackend, Properties, get_config_dir


class MockEventManager(list):
    def handle(self, event):
        self.append(event)


class TestProperties(TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        backend = FileBackend(self.tmpdir)
        self.events = MockEventManager()
        self.properties = Properties(self.events, backend)

    def shutDown(self):
        self.properties.shutdown()
        os.remove(os.path.join(self.tmpdir, FileBackend.RESOURCE_FILE))
        os.rmdir(self.tmpdir)

    def test_properties(self):
        prop = self.properties

        prop.set("test1", 2)
        assert len(self.events) == 1, self.events
        event = self.events[0]
        assert "test1" == event.key
        assert None is event.old_value
        assert event.new_value == 2
        assert prop("test1") == 2

        prop.set("test1", 2)
        assert len(self.events) == 1

        prop.set("test1", "foo")
        assert len(self.events) == 2
        event = self.events[1]
        assert "test1" == event.key
        assert event.old_value == 2
        assert "foo" == event.new_value
        assert "foo" == prop("test1")

        assert prop("test2", 3) == 3
        assert prop("test2", 4) == 3


def test_config_dir():
    config_dir = get_config_dir()

    assert config_dir.endswith("gaphor")
