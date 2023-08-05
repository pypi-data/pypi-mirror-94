
from unittest import TestCase

from szczypiorek.fields import (
    BooleanField,
    CharField,
    FloatField,
    IntegerField,
    URLField,
)
from szczypiorek.exceptions import ValidatorError


class BooleanFieldTestCase(TestCase):

    def test_to_python(self):

        assert BooleanField().to_python('X', 'True') is True
        assert BooleanField().to_python('X', 'TRUE') is True
        assert BooleanField().to_python('X', 'False') is False
        assert BooleanField().to_python('X', 'FALse') is False

    def test_to_python__allow_null(self):

        f = BooleanField(allow_null=True)

        assert f.to_python('X', None) is None

    def test_to_python__not_allow_null(self):

        f = BooleanField(allow_null=False)

        try:
            f.to_python('X', None)

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Null value are not allowed'

        else:
            raise AssertionError('should raise error')

    def test_to_python__not_valid(self):

        f = BooleanField()

        try:
            f.to_python('X', 'WHAT')

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Cannot cast WHAT to boolean'

        else:
            raise AssertionError('should raise error')


class CharFieldTestCase(TestCase):

    def test_to_python(self):

        assert CharField().to_python('X', 'Hi there') == 'Hi there'
        assert CharField().to_python('X', 'cześć') == 'cześć'

    def test_to_python__allow_null(self):

        f = CharField(allow_null=True)

        assert f.to_python('X', None) is None

    def test_to_python__not_allow_null(self):

        f = CharField(allow_null=False)

        try:
            f.to_python('X', None)

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Null value are not allowed'

        else:
            raise AssertionError('should raise error')

    def test_to_python__not_valid(self):

        cases = [
            (
                CharField(min_length=2),
                'h',
                'env.X: Text "h" is too short. min length: 2',
            ),
            (
                CharField(max_length=4),
                'hello',
                'env.X: Text "hello" is too long. max length: 4',
            ),
            (
                CharField(min_length=3, max_length=4),
                'hi',
                'env.X: Text "hi" is too short. min length: 3',
            ),
        ]

        for f, text, message in cases:
            try:
                f.to_python('X', text)

            except ValidatorError as e:
                assert e.args[0] == message

            else:
                raise AssertionError('should raise error')


class FloatFieldTestCase(TestCase):

    def test_to_python(self):

        assert FloatField().to_python('X', '12') == 12.0
        assert FloatField().to_python('X', '14.5') == 14.5

    def test_to_python__allow_null(self):

        f = FloatField(allow_null=True)

        assert f.to_python('X', None) is None

    def test_to_python__not_allow_null(self):

        f = FloatField(allow_null=False)

        try:
            f.to_python('X', None)

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Null value are not allowed'

        else:
            raise AssertionError('should raise error')

    def test_to_python__not_valid(self):

        f = FloatField()

        try:
            f.to_python('X', 'WHAT')

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Cannot cast WHAT to float'

        else:
            raise AssertionError('should raise error')


class IntegerFieldTestCase(TestCase):

    def test_to_python(self):

        assert IntegerField().to_python('X', '12') == 12
        assert IntegerField().to_python('X', '14.5') == 14

    def test_to_python__allow_null(self):

        f = IntegerField(allow_null=True)

        assert f.to_python('X', None) is None

    def test_to_python__not_allow_null(self):

        f = IntegerField(allow_null=False)

        try:
            f.to_python('X', None)

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Null value are not allowed'

        else:
            raise AssertionError('should raise error')

    def test_to_python__not_valid(self):

        f = IntegerField()

        try:
            f.to_python('X', 'WHAT')

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Cannot cast WHAT to integer'

        else:
            raise AssertionError('should raise error')


class URLFieldTestCase(TestCase):

    def test_to_python(self):

        assert URLField().to_python(
            'X', 'http://127.0.0.1') == 'http://127.0.0.1'
        assert URLField().to_python(
            'X', 'ws://hi.org:123') == 'ws://hi.org:123'
        assert URLField().to_python(
            'X', 'ftp://hi.org') == 'ftp://hi.org'

    def test_to_python__allow_null(self):

        f = URLField(allow_null=True)

        assert f.to_python('X', None) is None

    def test_to_python__not_allow_null(self):

        f = URLField(allow_null=False)

        try:
            f.to_python('X', None)

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Null value are not allowed'

        else:
            raise AssertionError('should raise error')

    def test_to_python__not_valid(self):

        f = URLField()

        try:
            f.to_python('X', 'WHAT')

        except ValidatorError as e:
            assert e.args[0] == 'env.X: Text "WHAT" is not valid URL'

        else:
            raise AssertionError('should raise error')
