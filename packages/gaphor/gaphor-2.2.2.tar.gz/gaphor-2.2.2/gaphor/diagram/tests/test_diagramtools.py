import logging

from gi.repository import Gdk

from gaphor import UML
from gaphor.tests import TestCase
from gaphor.ui.abc import UIComponent
from gaphor.ui.event import DiagramOpened
from gaphor.UML.classes import AssociationItem, ClassItem

logging.basicConfig(level=logging.DEBUG)


class DiagramItemConnectorTestCase(TestCase):
    services = TestCase.services + [
        "main_window",
        "properties",
        "namespace",
        "diagrams",
        "toolbox",
        "export_menu",
        "tools_menu",
        "elementeditor",
    ]

    def setUp(self):
        super().setUp()
        self.component_registry = self.get_service("component_registry")
        self.event_manager = self.get_service("event_manager")
        mw = self.get_service("main_window")
        mw.open()
        self.main_window = mw
        self.event_manager.handle(DiagramOpened(self.diagram))

    def test_item_reconnect(self):
        # Setting the stage:
        ci1 = self.create(ClassItem, UML.Class)
        ci2 = self.create(ClassItem, UML.Class)
        a = self.create(AssociationItem)

        self.connect(a, a.head, ci1)
        self.connect(a, a.tail, ci2)

        assert a.subject
        assert a.head_subject
        assert a.tail_subject

        the_association = a.subject

        # The act: perform button press event and button release
        view = self.component_registry.get(UIComponent, "diagrams").get_current_view()

        assert self.diagram is view.model

        p = view.get_matrix_i2v(a).transform_point(*a.head.pos)

        event = Gdk.Event()
        event.x, event.y, event.type, event.state = (
            p[0],
            p[1],
            Gdk.EventType.BUTTON_PRESS,
            0,
        )

        view.event(event)

        assert the_association is a.subject

        event = Gdk.Event()
        event.x, event.y, event.type, event.state = (
            p[0],
            p[1],
            Gdk.EventType.BUTTON_RELEASE,
            0,
        )

        view.event(event)

        assert the_association is a.subject
