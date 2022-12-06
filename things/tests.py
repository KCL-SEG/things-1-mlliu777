from django.test import TestCase
from .models import Thing
from django.core.exceptions import ValidationError

# Create your tests here.
class unitTestCase(TestCase):
    def setUp(self):
        self.thing = Thing(name="Foobar", description="Foobar thing", quantity=2)


    def test_valid_thing(self):
        self._assert_thing_is_valid

    def test_name_must_be_unique(self):
        other_thing = Thing(name="Baz", description="Baz thing", quantity=1)
        other_thing.save()
        self.thing.name = other_thing.name
        self._assert_thing_is_invalid(message="Name must be unique")

    def test_name_must_not_be_blank(self):
        self.thing.name = ''
        self._assert_thing_is_invalid()

    def test_name_may_have_30_characters(self):
        self.thing.name = 'x' * 30
        self._assert_thing_is_valid()

    def test_name_must_not_have_more_than_30_characters(self):
        self.thing.name = 'x' * 31
        self._assert_thing_is_invalid()

    def test_description_may_be_blank(self):
        self.thing.description = ''
        self._assert_thing_is_valid()

    def test_description_may_have_120_characters(self):
        self.thing.description = 'x' * 120
        self._assert_thing_is_valid()

    def test_description_must_not_have_more_than_120_characters(self):
        self.thing.description = 'x' * 121
        self._assert_thing_is_invalid()

    def test_description_need_not_be_unique(self):
        other_thing = Thing(name="Baz", description="Baz thing", quantity=1)
        other_thing.save()
        self.thing.description = other_thing.description
        self._assert_thing_is_valid()

    def test_quantity_need_not_be_unique(self):
        other_thing = Thing(name="Baz", description="Baz thing", quantity=1)
        other_thing.save()
        self.thing.quantity = other_thing.quantity
        self._assert_thing_is_valid()

    def test_quantity_may_be_0(self):
        self.thing.quantity = 0
        self._assert_thing_is_valid()

    def test_quantity_must_not_be_negative(self):
        self.thing.quantity = -1
        self._assert_thing_is_invalid()

    def test_quantity_may_be_100(self):
        self.thing.quantity = 100
        self._assert_thing_is_valid()

    def test_quantity_must_not_be_greater_than_100(self):
        self.thing.quantity = 101
        self._assert_thing_is_invalid()

    def _assert_thing_is_valid(self):
        try:
            self.thing.full_clean()
        except (ValidationError):
            self.fail("Test thing supposed to be valid")

    def _assert_thing_is_invalid(self):
        try:
            self.thing.full_clean()
            self.fail("Test was supposed to be invalid")
        except (ValidationError):
            pass
