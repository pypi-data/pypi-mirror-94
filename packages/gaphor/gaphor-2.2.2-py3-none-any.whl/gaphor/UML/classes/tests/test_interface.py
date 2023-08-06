"""Test classes."""

from gaphor import UML
from gaphor.tests import TestCase
from gaphor.UML.classes.interface import Folded, InterfaceItem


class InterfaceTestCase(TestCase):
    def test_interface_creation(self):
        """Test interface creation."""
        iface = self.create(InterfaceItem, UML.Interface)
        assert isinstance(iface.subject, UML.Interface)

    def test_folded_interface_persistence(self):
        """Test folded interface saving/loading."""
        iface = self.create(InterfaceItem, UML.Interface)

        # note: assembly folded mode..
        iface.folded = Folded.REQUIRED

        data = self.save()
        self.load(data)

        interfaces = list(self.diagram.select(InterfaceItem))
        assert len(interfaces) == 1
        # ... gives provided folded mode on load;
        # correct folded mode is determined by connections, which will be
        # recreated later, i.e. required folded mode will be set when
        # implementation connects to the interface and Folded.PROVIDED
        # is equal to interfaces[0].folded
