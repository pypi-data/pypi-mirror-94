
from unittest import TestCase

from szczypiorek.fields_validators import url, length, ValidatorError


class UrlTestCase(TestCase):

    def test_success(self):
        assert url('Y', 'http://hi.io') is True

    def test_not_valid(self):

        try:
            url('Y', 'hi.io')

        except ValidatorError as e:
            assert e.args[0] == 'env.Y: Text "hi.io" is not valid URL'

        else:
            raise AssertionError('should raise error')


class LengthTestCase(TestCase):

    def test_success(self):
        assert length('Y', 'hello world') is True

    def test_not_valid(self):

        try:
            length('Y', 'hello', min_length=10)

        except ValidatorError as e:
            assert e.args[0] == (
                'env.Y: Text "hello" is too short. min length: 10')

        else:
            raise AssertionError('should raise error')
