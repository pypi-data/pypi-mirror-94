
import textwrap

import pytest

from szczypiorek.utils import (
    fix_yaml,
    dump_yaml,
    load_yaml,
    flatten,
    substitute,
)
from szczypiorek.exceptions import (
    BrokenYamlError,
    MissingSubstitutionKeyError,
    normalize,
)
from tests import BaseTestCase


def n(t):
    return textwrap.dedent(t)


class UtilsTestCase(BaseTestCase):

    #
    # DUMP_YAML
    #
    def test_dump_yaml__is_valid(self):

        assert dump_yaml({
            'a': {'b': 'whatever'},
            'c': True,
        }).strip() == n('''
            a:
              b: whatever
            c: true
        ''').strip()

    #
    # LOAD_YAML
    #
    def test_load_yaml__is_valid(self):

        assert load_yaml(n('''
            a:
              b: 'whatever'
            c: true
        ''')) == {
            'a': {'b': 'whatever'},
            'c': True,
        }

    def test_load_yaml__is_not_valid(self):

        with pytest.raises(BrokenYamlError) as e:
            assert load_yaml(n('''
                a: {{what}
            ''')) is True

        assert e.value.args[0] == normalize("""
            It seems that you're yaml file is broken.

            Run in through some online validators to find the reason behind it.
        """)

    #
    # FIX_YAML
    #
    def test_fix_yaml__nothing_to_fix__success(self):

        assert fix_yaml(n('''
            a:
              b: 'whatever'
            c: true
        ''')) == n('''
            a:
              b: 'whatever'
            c: true
        ''')

    def test_fix_yaml__one_thing_to_fix__success(self):

        assert fix_yaml(n('''
            a:
              b: {{ whatever }}
            c: true
        ''')) == n('''
            a:
              b: '{{whatever}}'
            c: true
        ''')

    def test_fix_yaml__many_things_to_fix__success(self):

        assert fix_yaml(n('''
            a:
              b: {{ whatever }}
            c: true
            d: {{g.b.g}}.example.pl
            f: {{ ff }}/payments/success?session_id={CHECKOUT_SESSION_ID}
        ''')) == n('''
            a:
              b: '{{whatever}}'
            c: true
            d: '{{g.b.g}}.example.pl'
            f: '{{ff}}/payments/success?session_id={CHECKOUT_SESSION_ID}'
        ''')

    def test_fix_yaml__do_not_fix_is_already_fixed(self):

        assert fix_yaml(n('''
            a:
              b: '{{whatever}}'
            c: true
            d: '{{g.b.g}}.example.pl'
            f: '{{ ff }}/payments/success?session_id={CHECKOUT_SESSION_ID}'
        ''')) == n('''
            a:
              b: '{{whatever}}'
            c: true
            d: '{{g.b.g}}.example.pl'
            f: '{{ ff }}/payments/success?session_id={CHECKOUT_SESSION_ID}'
        ''')

    #
    # FLATTEN
    #
    def test_flatten__already_flat__success(self):

        assert flatten(
            {'a': 1, 'b': True, 'c': 'whatever'}
        ) == {'a': 1, 'b': True, 'c': 'whatever'}

    def test_flatten__one_level_nested__success(self):

        assert flatten(
            {
                'a': 1,
                'b': {
                    'c': 'hi there',
                },
                'c': 'whatever',
            }
        ) == {
            'a': 1,
            'b_c': 'hi there',
            'c': 'whatever',
        }

    def test_flatten__many_levels_nested__success(self):

        assert flatten(
            {
                'a': 1,
                'b': {
                    'c': {
                        'what': {
                            'ty': 67,
                            'x': 13,
                        },
                    },
                    'd': 12
                },
                'c': 'whatever',
            }
        ) == {
            'a': 1,
            'b_c_what_ty': 67,
            'b_c_what_x': 13,
            'b_d': 12,
            'c': 'whatever',
        }

    #
    # SUBSTITUTE
    #
    def test_substitute__nothing_to_substitute__success(self):

        assert substitute({
            'hi': 'what',
            'a_b': True,
        }) == {
            'hi': 'what',
            'a_b': True,
        }

    def test_substitute__one_thing_to_substitute__success(self):

        assert substitute({
            'hi': '{{ a.b }} what',
            'a_b': 'why',
        }) == {
            'hi': 'why what',
            'a_b': 'why',
        }

    def test_substitute__many_things_to_substitute__success(self):

        assert substitute({
            'hi': '{{ a.b }} what',
            'a_b': 'why',
            'hello': '{{ c.d.ex }} what',
            'c_d_ex': 'sanatorium',
        }) == {
            'hi': 'why what',
            'a_b': 'why',
            'hello': 'sanatorium what',
            'c_d_ex': 'sanatorium',
        }

    def test_substitute__missing_key__error(self):

        with pytest.raises(MissingSubstitutionKeyError) as e:
            substitute({
                'hi': '{{ a.b }} what',
                'c_d_ex': 'sanatorium',
            })

        assert e.value.args[0] == normalize("""
            Your template variable is referring non-existent value under
            the 'a.b' key.
        """)
