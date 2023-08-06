"""Unit tests for AssociationItem."""

from gaphor import UML
from gaphor.tests import TestCase
from gaphor.UML.classes.association import AssociationItem
from gaphor.UML.classes.klass import ClassItem


class AssociationItemTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.assoc = self.create(AssociationItem)
        self.class1 = self.create(ClassItem, UML.Class)
        self.class2 = self.create(ClassItem, UML.Class)

    def test_create(self):
        """Test association creation and its basic properties."""
        self.connect(self.assoc, self.assoc.head, self.class1)
        self.connect(self.assoc, self.assoc.tail, self.class2)

        assert isinstance(self.assoc.subject, UML.Association)
        assert self.assoc.head_subject is not None
        assert self.assoc.tail_subject is not None

        assert not self.assoc.show_direction

        self.assoc.show_direction = True
        assert self.assoc.show_direction

    def test_direction(self):
        """Test association direction inverting."""
        self.connect(self.assoc, self.assoc.head, self.class1)
        self.connect(self.assoc, self.assoc.tail, self.class2)

        assert self.assoc.head_subject is self.assoc.subject.memberEnd[0]
        assert self.assoc.tail_subject is self.assoc.subject.memberEnd[1]

    def test_invert_direction(self):
        self.connect(self.assoc, self.assoc.head, self.class1)
        self.connect(self.assoc, self.assoc.tail, self.class2)

        self.assoc.invert_direction()

        assert self.assoc.subject.memberEnd
        assert self.assoc.head_subject is self.assoc.subject.memberEnd[1]
        assert self.assoc.tail_subject is self.assoc.subject.memberEnd[0]

    def test_association_end_updates(self):
        """Test association end navigability connected to a class."""
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)
        a = self.create(AssociationItem)

        self.connect(a, a.head, c1)
        c = self.get_connected(a.head)
        assert c is c1

        self.connect(a, a.tail, c2)
        c = self.get_connected(a.tail)
        assert c is c2

        assert a.subject.memberEnd, a.subject.memberEnd

        assert a.subject.memberEnd[0] is a.head_subject
        assert a.subject.memberEnd[1] is a.tail_subject
        assert a.subject.memberEnd[0].name is None

        a.subject.memberEnd[0].name = "blah"
        self.diagram.update_now((a,))

        assert a.head_end._name == "+ blah", a.head_end.get_name()

    def test_association_orthogonal(self):
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)
        a = self.create(AssociationItem)

        self.connect(a, a.head, c1)
        c = self.get_connected(a.head)
        assert c is c1

        a.matrix.translate(100, 100)
        self.connect(a, a.tail, c2)
        c = self.get_connected(a.tail)
        assert c is c2

        try:
            a.orthogonal = True
        except ValueError:
            pass  # Expected, hanve only 2 handles, need 3 or more
        else:
            assert False, "Can not set line to orthogonal with less than 3 handles"

    def test_association_end_owner_handles(self):
        assert self.assoc.head_end.owner_handle is self.assoc.head
        assert self.assoc.tail_end.owner_handle is self.assoc.tail
