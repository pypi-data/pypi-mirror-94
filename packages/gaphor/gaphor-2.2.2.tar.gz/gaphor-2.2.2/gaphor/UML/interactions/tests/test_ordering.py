from gaphor import UML
from gaphor.diagram.tests.fixtures import connect
from gaphor.UML.interactions.executionspecification import ExecutionSpecificationItem
from gaphor.UML.interactions.interactionsconnect import order_lifeline_covered_by
from gaphor.UML.interactions.lifeline import LifelineItem
from gaphor.UML.interactions.message import MessageItem


def test_ordering(diagram, element_factory):
    lifeline = diagram.create(
        LifelineItem, subject=element_factory.create(UML.Lifeline)
    )
    lifeline.lifetime.visible = True
    lifeline.lifetime.bottom.pos.y = 1000
    lifetime_top = lifeline.lifetime.top.pos

    exec_spec = diagram.create(ExecutionSpecificationItem)
    message1 = diagram.create(MessageItem)
    message2 = diagram.create(MessageItem)
    message3 = diagram.create(MessageItem)

    message1.head.pos.y = message1.tail.pos.y = lifetime_top.y + 300
    exec_spec.top.pos.y = lifetime_top.y + 400
    message2.head.pos.y = message2.tail.pos.y = lifetime_top.y + 500
    exec_spec.bottom.pos.y = lifetime_top.y + 600
    message3.head.pos.y = message3.tail.pos.y = lifetime_top.y + 700

    diagram.connections.solve()

    # Add in "random" order
    connect(exec_spec, exec_spec.handles()[0], lifeline)
    connect(message3, message3.tail, lifeline)
    connect(message1, message1.head, lifeline)
    connect(message2, message2.head, exec_spec)

    occurrences = [
        message1.subject.sendEvent,
        exec_spec.subject.start,
        message2.subject.sendEvent,
        exec_spec.subject.finish,
        message3.subject.receiveEvent,
    ]

    order_lifeline_covered_by(lifeline)

    assert list(lifeline.subject.coveredBy) == occurrences
