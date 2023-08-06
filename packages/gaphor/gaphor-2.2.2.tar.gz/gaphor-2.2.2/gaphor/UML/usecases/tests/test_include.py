"""Test include item connections."""

from gaphor import UML
from gaphor.tests import TestCase
from gaphor.UML.usecases.include import IncludeItem
from gaphor.UML.usecases.usecase import UseCaseItem


class IncludeItemTestCase(TestCase):
    def test_use_case_glue(self):
        """Test "include" gluing to use cases."""

        uc1 = self.create(UseCaseItem, UML.UseCase)
        include = self.create(IncludeItem)

        glued = self.allow(include, include.head, uc1)
        assert glued

    def test_use_case_connect(self):
        """Test connecting "include" to use cases."""
        uc1 = self.create(UseCaseItem, UML.UseCase)
        uc2 = self.create(UseCaseItem, UML.UseCase)
        include = self.create(IncludeItem)

        self.connect(include, include.head, uc1)
        assert self.get_connected(include.head), uc1

        self.connect(include, include.tail, uc2)
        assert self.get_connected(include.tail), uc2

    def test_use_case_reconnect(self):
        """Test reconnecting use cases with "include"."""
        uc1 = self.create(UseCaseItem, UML.UseCase)
        uc2 = self.create(UseCaseItem, UML.UseCase)
        uc3 = self.create(UseCaseItem, UML.UseCase)
        include = self.create(IncludeItem)

        # connect: uc1 -> uc2
        self.connect(include, include.head, uc1)
        self.connect(include, include.tail, uc2)
        e = include.subject

        # reconnect: uc1 -> uc2
        self.connect(include, include.tail, uc3)

        assert e is include.subject
        assert include.subject.addition is uc1.subject
        assert include.subject.includingCase is uc3.subject

    def test_use_case_disconnect(self):
        """Test disconnecting "include" from use cases."""
        uc1 = self.create(UseCaseItem, UML.UseCase)
        uc2 = self.create(UseCaseItem, UML.UseCase)
        include = self.create(IncludeItem)

        self.connect(include, include.head, uc1)
        self.connect(include, include.tail, uc2)

        self.disconnect(include, include.head)
        assert self.get_connected(include.head) is None
        assert include.subject is None

        self.disconnect(include, include.tail)
        assert self.get_connected(include.tail) is None
