"""Unittest the storage and parser modules."""

import re
from io import StringIO

import pytest

from gaphor import UML
from gaphor.application import distribution
from gaphor.core.modeling import StyleSheet
from gaphor.diagram.general import CommentItem
from gaphor.storage import storage
from gaphor.storage.xmlwriter import XMLWriter
from gaphor.tests.testcase import TestCase
from gaphor.UML.classes import AssociationItem, ClassItem, InterfaceItem


class PseudoFile:
    def __init__(self):
        self.data = ""

    def write(self, data):
        self.data += data

    def close(self):
        pass


class StorageTestCase(TestCase):
    def test_version_check(self):
        from gaphor.storage.storage import version_lower_than

        assert version_lower_than("0.3.0", (0, 15, 0))
        assert version_lower_than("0", (0, 15, 0))
        assert version_lower_than("0.14", (0, 15, 0))
        assert version_lower_than("0.14.1111", (0, 15, 0))
        assert not version_lower_than("0.15.0", (0, 15, 0))
        assert not version_lower_than("1.33.0", (0, 15, 0))
        assert not version_lower_than("0.15.0b123", (0, 15, 0))
        assert version_lower_than("0.14.0.b1", (0, 15, 0))
        assert not version_lower_than("0.15.b1", (0, 15, 0))
        assert not version_lower_than("0.16.b1", (0, 15, 0))
        assert not version_lower_than("0.15.0.b2", (0, 14, 99))
        assert not version_lower_than("1.2.0rc2-dev0+7fad31a0", (0, 17, 0))

    def test_save_uml(self):
        """Saving gaphor.UML model elements."""
        self.element_factory.create(UML.Package)
        self.element_factory.create(UML.Diagram)
        self.element_factory.create(UML.Comment)
        self.element_factory.create(UML.Class)

        out = PseudoFile()
        storage.save(XMLWriter(out), factory=self.element_factory)
        out.close()

        assert "<Package " in out.data
        assert "<Diagram " in out.data
        assert "<Comment " in out.data
        assert "<Class " in out.data

    def test_save_item(self):
        """Save a diagranm item too."""
        diagram = self.element_factory.create(UML.Diagram)
        diagram.create(CommentItem, subject=self.element_factory.create(UML.Comment))

        out = PseudoFile()
        storage.save(XMLWriter(out), factory=self.element_factory)
        out.close()

        assert "<Diagram " in out.data
        assert "<Comment " in out.data
        assert "<canvas>" in out.data
        assert ' type="CommentItem"' in out.data, out.data

    def test_load_uml(self):
        """Test loading of a freshly saved model."""
        self.element_factory.create(UML.Package)
        # diagram is created in TestCase.setUp
        self.element_factory.create(UML.Comment)
        self.element_factory.create(UML.Class)

        data = self.save()
        self.load(data)

        assert len(self.element_factory.lselect()) == 5
        assert len(self.element_factory.lselect(UML.Package)) == 1
        # diagram is created in TestCase.setUp
        assert len(self.element_factory.lselect(UML.Diagram)) == 1
        assert len(self.element_factory.lselect(UML.Comment)) == 1
        assert len(self.element_factory.lselect(UML.Class)) == 1
        assert len(self.element_factory.lselect(StyleSheet)) == 1

    def test_load_uml_2(self):
        """Test loading of a freshly saved model."""
        self.element_factory.create(UML.Package)
        self.create(CommentItem, UML.Comment)
        self.create(ClassItem, UML.Class)
        iface = self.create(InterfaceItem, UML.Interface)
        iface.subject.name = "Circus"
        iface.matrix.translate(10, 10)

        data = self.save()
        self.load(data)

        assert len(self.element_factory.lselect()) == 6
        assert len(self.element_factory.lselect(UML.Package)) == 1
        assert len(self.element_factory.lselect(UML.Diagram)) == 1
        d = self.element_factory.lselect(UML.Diagram)[0]
        assert len(self.element_factory.lselect(UML.Comment)) == 1
        assert len(self.element_factory.lselect(UML.Class)) == 1
        assert len(self.element_factory.lselect(UML.Interface)) == 1

        c = self.element_factory.lselect(UML.Class)[0]
        assert c.presentation
        assert c.presentation[0].subject is c

        iface = self.element_factory.lselect(UML.Interface)[0]
        assert iface.name == "Circus"
        assert len(iface.presentation) == 1
        assert tuple(iface.presentation[0].matrix) == (1, 0, 0, 1, 10, 10), tuple(
            iface.presentation[0].matrix
        )

        # Check load/save of other canvas items.
        assert len(list(d.get_all_items())) == 3
        for item in d.get_all_items():
            assert item.subject, f"No subject for {item}"
        d1 = next(d.select(lambda e: isinstance(e, ClassItem)))
        assert d1

    def test_load_with_whitespace_name(self):
        difficult_name = "    with space before and after  "
        diagram = self.element_factory.lselect()[0]
        diagram.name = difficult_name
        data = self.save()
        self.load(data)
        elements = self.element_factory.lselect()
        assert len(elements) == 2, elements
        assert elements[0].name == difficult_name, elements[0].name

    @pytest.mark.slow
    def test_load_uml_metamodel(self):
        path = distribution().locate_file("models/UML.gaphor")

        with open(path) as ifile:
            storage.load(
                ifile,
                factory=self.element_factory,
                modeling_language=self.modeling_language,
            )

    def test_save_and_load_model_with_relationships(self):
        self.element_factory.create(UML.Package)
        self.create(CommentItem, UML.Comment)
        self.create(ClassItem, UML.Class)

        a = self.diagram.create(AssociationItem)
        a.handles()[0].pos = (10, 20)
        a.handles()[1].pos = (50, 60)
        assert a.handles()[0].pos.x == 10, a.handles()[0].pos
        assert a.handles()[0].pos.y == 20, a.handles()[0].pos
        assert tuple(a.handles()[1].pos) == (50, 60), a.handles()[1].pos

        data = self.save()
        self.load(data)

        assert len(self.element_factory.lselect()) == 5
        assert len(self.element_factory.lselect(UML.Package)) == 1
        assert len(self.element_factory.lselect(UML.Diagram)) == 1
        d = self.element_factory.lselect(UML.Diagram)[0]
        assert len(self.element_factory.lselect(UML.Comment)) == 1
        assert len(self.element_factory.lselect(UML.Class)) == 1
        assert len(self.element_factory.lselect(UML.Association)) == 0

        # Check load/save of other canvas items.
        assert len(list(d.get_all_items())) == 3
        aa = next(
            item for item in d.get_all_items() if isinstance(item, AssociationItem)
        )
        assert aa
        assert list(map(float, aa.handles()[0].pos)) == [10, 20], aa.handles()[0].pos
        assert list(map(float, aa.handles()[1].pos)) == [50, 60], aa.handles()[1].pos
        d1 = next(d.select(lambda e: isinstance(e, ClassItem)))
        assert d1

    def test_save_and_load_of_association_with_two_connected_classes(self):
        c1 = self.create(ClassItem, UML.Class)
        c2 = self.create(ClassItem, UML.Class)
        c2.matrix.translate(200, 200)
        self.diagram.request_update(c2)
        self.diagram.update_now((c1, c2))
        assert tuple(c2.matrix_i2c) == (1, 0, 0, 1, 200, 200)

        a = self.create(AssociationItem)

        self.connect(a, a.head, c1)
        self.connect(a, a.tail, c2)

        self.diagram.update_now((c1, c2, a))

        assert a.head.pos.y == 0, a.head.pos
        assert a.tail.pos.x == 200, a.tail.pos
        assert a.tail.pos.y == 200, a.tail.pos
        assert a.subject

        fd = StringIO()
        storage.save(XMLWriter(fd), factory=self.element_factory)
        data = fd.getvalue()
        fd.close()

        old_a_subject_id = a.subject.id

        self.element_factory.flush()
        assert not list(self.element_factory.select())
        fd = StringIO(data)
        storage.load(
            fd, factory=self.element_factory, modeling_language=self.modeling_language
        )
        fd.close()

        diagrams = list(self.kindof(UML.Diagram))
        assert len(diagrams) == 1
        d = diagrams[0]
        a = next(d.select(lambda e: isinstance(e, AssociationItem)))
        assert a.subject is not None
        assert old_a_subject_id == a.subject.id
        cinfo_head = a.diagram.connections.get_connection(a.head)
        assert cinfo_head.connected is not None
        cinfo_tail = a.diagram.connections.get_connection(a.tail)
        assert cinfo_tail.connected is not None
        assert cinfo_head.connected is not cinfo_tail.connected

    def test_load_and_save_of_a_model(self):
        path = distribution().locate_file("test-models/simple-items.gaphor")

        with open(path, "r") as ifile:
            storage.load(
                ifile,
                factory=self.element_factory,
                modeling_language=self.modeling_language,
            )

        pf = PseudoFile()

        storage.save(XMLWriter(pf), factory=self.element_factory)

        with open(path, "r") as ifile:

            orig = ifile.read()

        copy = pf.data

        expr = re.compile('gaphor-version="[^"]*"')
        orig = expr.sub("%VER%", orig)
        copy = expr.sub("%VER%", copy)

        self.maxDiff = None
        assert copy == orig, "Saved model does not match copy"

    def test_can_not_load_models_older_that_0_17_0(self):

        path = distribution().locate_file("test-models/old-gaphor-version.gaphor")

        def load_old_model():
            with open(path, "r") as ifile:
                storage.load(
                    ifile,
                    factory=self.element_factory,
                    modeling_language=self.modeling_language,
                )

        self.assertRaises(ValueError, load_old_model)
