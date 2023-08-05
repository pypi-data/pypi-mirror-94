
import textwrap
import os

from click.testing import CliRunner
from bash import bash

import szczypiorek as env
from szczypiorek.crypto import encrypt
from szczypiorek.constants import (
    ENCRYPTION_KEY_ENV_NAME,
    ENCRYPTION_KEY_FILE_ENV_NAME,
    ENVIRONMENT_ENV_NAME,
    ENVIRONMENT_FILE_ENV_NAME,
    # ENVIRONMENT_DEFAULT,
    # os.environ[ENVIRONMENT_FILE_ENV_NAME] = str(
    #     self.root_dir.join('e2e.szczyp'))
)
from szczypiorek.cli import cli
from szczypiorek.utils import load_yaml, dump_yaml
from tests import BaseTestCase


class MyEnvParser(env.EnvParser):

    a = env.CharField()


class SensitiveEnvParser(env.EnvParser):

    password = env.CharField()
    my_super_password = env.CharField()
    secret = env.CharField()
    some_secret = env.CharField()
    my_key = env.CharField()
    key = env.CharField()
    not_some_important = env.CharField()
    a = env.CharField()
    c = env.CharField()


my_env = None

sensitive_env = None


class CliTestCase(BaseTestCase):

    def setUp(self):
        super(CliTestCase, self).setUp()
        self.runner = CliRunner()

        try:
            self.root_dir.join('.szczypiorek_encryption_key').remove()

        except Exception:
            pass

        envs = [
            ENCRYPTION_KEY_ENV_NAME,
            ENCRYPTION_KEY_FILE_ENV_NAME,
            ENVIRONMENT_ENV_NAME,
            ENVIRONMENT_FILE_ENV_NAME,
        ]
        for e in envs:
            try:
                del os.environ[e]

            except KeyError:
                pass

        MyEnvParser._envs_gpg_cache = {}
        SensitiveEnvParser._envs_gpg_cache = {}
        env.EnvParser._envs_gpg_cache = {}

    #
    # PRINT_ENV
    #
    def test_print_env(self):

        content = encrypt(textwrap.dedent('''
            a: b
        '''))
        self.root_dir.join('env.szczyp').write(content, mode='w')

        global my_env
        my_env = MyEnvParser().parse()  # noqa

        result = self.runner.invoke(
            cli, ['print-env', 'tests.test_cli.my_env'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            a: b
        ''').strip()

    def test_print_env__hide_sensitive(self):

        content = encrypt(textwrap.dedent('''
            password: my.secret
            my_super_password: 123whatever
            secret: not tell anyone
            some_secret: not just any secret
            my_key: to open any doors
            key: yup
            not_some_important: just show it
            a: b
            c: '{"my_password": "yes hidden"}'
        '''))
        self.root_dir.join('env.szczyp').write(content, mode='w')

        global my_env
        my_env = SensitiveEnvParser().parse()  # noqa

        result = self.runner.invoke(
            cli, ['print-env', 'tests.test_cli.my_env'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            a: b
            c: {
                "my_password": "**********"
            }
            key: **********
            my_key: **********
            my_super_password: **********
            not_some_important: just show it
            password: **********
            secret: **********
            some_secret: **********
        ''').strip()

    #
    # ENCRYPT
    #
    def test_encrypt__no_yaml_files(self):

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    def test_encrypt__specific_file(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())
        bash('git init')
        self.root_dir.join('.gitignore').write(
            '.szczypiorek_encryption_key\n'
            'a.yml\n'
        )

        result = self.runner.invoke(
            cli, ['encrypt', str(self.root_dir.join('a.yml'))])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.git')),
            str(self.root_dir.join('.gitignore')),
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('a.szczyp')),
            str(self.root_dir.join('a.yml')),
        ]

    def test_encrypt__some_yaml_files(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())
        self.root_dir.join('b.yml').write(textwrap.dedent('''
            a: whatever
        ''').strip())
        bash('git init')
        self.root_dir.join('.gitignore').write(
            '.szczypiorek_encryption_key\n'
            'a.yml\n'
            'b.yml\n'
        )

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.git')),
            str(self.root_dir.join('.gitignore')),
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('a.szczyp')),
            str(self.root_dir.join('a.yml')),
            str(self.root_dir.join('b.szczyp')),
            str(self.root_dir.join('b.yml')),
        ]

    def test_encrypt__specific_file_and_custom_key_file(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())
        bash('git init')
        self.root_dir.join('.gitignore').write(
            '.development_encryption_key\n'
            'a.yml\n'
        )

        result = self.runner.invoke(
            cli,
            [
                'encrypt',
                '-k', '.development_encryption_key',
                str(self.root_dir.join('a.yml'))
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.development_encryption_key')),
            str(self.root_dir.join('.git')),
            str(self.root_dir.join('.gitignore')),
            str(self.root_dir.join('a.szczyp')),
            str(self.root_dir.join('a.yml')),
        ]

    def test_encrypt__some_error(self):

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert 'Error: Well it seems that the' in result.output.strip()

    def test_encrypt__some_error__do_not_overwrite_existing(self):

        self.root_dir.join('a.szczyp').write('hello gpg')

        self.root_dir.join('a.yml').write(textwrap.dedent('''
            a:
             b: true
             c: 12
        ''').strip())

        result = self.runner.invoke(cli, ['encrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert 'Error: Well it seems that the' in result.output.strip()
        assert self.root_dir.join('a.szczyp').read() == 'hello gpg'

    #
    # DECRYPT
    #
    def test_decrypt__no_gpg_files(self):

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    def test_decrypt__specific_gpg_file(self):

        content = encrypt(textwrap.dedent('''
            secret:
              key: secret.whatever
            is_important: true
            aws:
              url: {{ a.b.c }}

            number:
              of:
                workers: '113'
            a:
              b:
                c: http://hello.word.org
        '''))
        self.root_dir.join('e2e.szczyp').write(content, mode='w')

        result = self.runner.invoke(
            cli,
            ['decrypt', str(self.root_dir.join('e2e.szczyp'))])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('e2e.szczyp')),
            str(self.root_dir.join('e2e.yml')),
        ]

    def test_decrypt__some_gpg_files(self):

        content = encrypt(textwrap.dedent('''
            secret:
              key: secret.whatever
            is_important: true
            aws:
              url: {{ a.b.c }}

            number:
              of:
                workers: '113'
            a:
              b:
                c: http://hello.word.org
        '''))
        self.root_dir.join('env.szczyp').write(content, mode='w')

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])
        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('env.szczyp')),
            str(self.root_dir.join('env.yml')),
        ]

    def test_decrypt__specific_file_and_custom_key_file(self):

        content = encrypt(
            textwrap.dedent('''
                secret:
                  key: secret.whatever
                is_important: true
                aws:
                  url: {{ a.b.c }}

                number:
                  of:
                    workers: '113'
                a:
                  b:
                    c: http://hello.word.org
            '''),
            '.e2e_encryption_key')
        self.root_dir.join('e2e.szczyp').write(content, mode='w')

        result = self.runner.invoke(
            cli,
            [
                'decrypt',
                '-k', '.e2e_encryption_key',
                str(self.root_dir.join('e2e.szczyp'))
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.e2e_encryption_key')),
            str(self.root_dir.join('e2e.szczyp')),
            str(self.root_dir.join('e2e.yml')),
        ]

    def test_decrypt__some_error(self):

        self.root_dir.join('a.szczyp').write('whatever')

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert (
            "Something went wrong while attempting to decrypt" in
            result.output.strip())

    def test_decrypt__some_error__do_not_overwrite_existing(self):

        self.root_dir.join('a.szczyp').write('whatever')
        self.root_dir.join('a.yml').write('hello yml')

        result = self.runner.invoke(cli, ['decrypt', str(self.root_dir)])

        assert result.exit_code == 1
        assert (
            "Something went wrong while attempting to decrypt" in
            result.output.strip())
        assert self.root_dir.join('a.yml').read() == 'hello yml'

    #
    # REPLACE
    #
    def set_encrypted(self, json, filepath=None, key_filepath=None):
        content = encrypt(
            dump_yaml(json),
            key_filepath=key_filepath)
        filepath = filepath or 'env.szczyp'
        self.root_dir.join(filepath).write(content, mode='w')

    def get_decrypted(self, filepath, key_filepath=None):
        self.runner.invoke(
            cli,
            [
                'decrypt',
                str(self.root_dir.join(filepath))
            ])

        filepath = filepath.replace('.szczyp', '.yml')
        with open(self.root_dir.join(filepath)) as f:
            return load_yaml(f.read())

    def test_replace__no_replacements(self):

        result = self.runner.invoke(cli, ['replace'])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    def test_replace__default_env__single_replacement(self):

        env = {
            'secret': {
                'key': 'secret.whatever'
            },
            'is_important': True,
            'number': {
                'of': {
                    'workers': '113'
                }
            }
        }
        self.set_encrypted(env)

        result = self.runner.invoke(
            cli,
            [
                'replace',
                '-r', 'secret.key:known'
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('env.szczyp')),
        ]
        content = self.get_decrypted('env.szczyp')

        env['secret']['key'] = 'known'
        assert content == env

    def test_replace__default_env__multiple_replacements(self):

        env = {
            'secret': {
                'key': 'secret.whatever'
            },
            'is_important': True,
            'number': {
                'of': {
                    'workers': '113',
                    'bosses': 12,
                    'price': 19.21
                }
            }
        }
        self.set_encrypted(env)

        result = self.runner.invoke(
            cli,
            [
                'replace',
                '-r', 'secret.key:known',
                '-r', 'is_important:false',
                '-r', 'number.of.bosses:13',
                '-r', 'number.of.price:24.23',
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('env.szczyp')),
        ]
        content = self.get_decrypted('env.szczyp')

        env['secret']['key'] = 'known'
        env['is_important'] = False
        env['number']['of']['bosses'] = 13
        env['number']['of']['price'] = 24.23
        assert content == env

    def test_replace__default_env__only_one_env_changed(self):

        env0 = {
            'secret': {
                'key': 'secret.whatever'
            },
            'is_important': True,
        }
        env1 = {
            'secret': {
                'key': 'secret.whatever'
            },
            'is_important': True,
        }
        self.set_encrypted(env0, 'env0.szczyp')
        self.set_encrypted(env1, 'env1.szczyp')

        result = self.runner.invoke(
            cli,
            [
                'replace',
                '-p', 'env0.szczyp',
                '-r', 'secret.key:known'
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('env0.szczyp')),
            str(self.root_dir.join('env1.szczyp')),
        ]
        content0 = self.get_decrypted('env0.szczyp')
        content1 = self.get_decrypted('env1.szczyp')

        env0['secret']['key'] = 'known'
        assert content0 == env0
        assert content1 == env1

    def test_replace__env_given_by_env_var__single_replacement(self):

        env = {
            'secret': {
                'key': 'secret.whatever'
            },
            'is_important': True,
            'number': {
                'of': {
                    'workers': '113'
                }
            }
        }
        self.set_encrypted(env, 'my_env.szczyp')
        os.environ[ENVIRONMENT_FILE_ENV_NAME] = 'my_env.szczyp'

        result = self.runner.invoke(
            cli,
            [
                'replace',
                '-r', 'secret.key:known'
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('my_env.szczyp')),
        ]
        content = self.get_decrypted('my_env.szczyp')

        env['secret']['key'] = 'known'
        assert content == env

    def test_replace__env_given_as_argument__single_replacement(self):

        env = {
            'secret': {
                'key': 'secret.whatever'
            },
            'is_important': True,
            'number': {
                'of': {
                    'workers': '113'
                }
            }
        }
        self.set_encrypted(env, 'my_env.szczyp')

        result = self.runner.invoke(
            cli,
            [
                'replace',
                '-p', 'my_env.szczyp',
                '-r', 'secret.key:known'
            ])

        assert result.exit_code == 0
        assert sorted(self.root_dir.listdir()) == [
            str(self.root_dir.join('.szczypiorek_encryption_key')),
            str(self.root_dir.join('my_env.szczyp')),
        ]
        content = self.get_decrypted('my_env.szczyp')

        env['secret']['key'] = 'known'
        assert content == env

    def test_replace__env_given_as_argument__does_not_exist(self):
        env = {
            'secret': {
                'key': 'secret.whatever'
            },
            'is_important': True,
            'number': {
                'of': {
                    'workers': '113'
                }
            }
        }
        self.set_encrypted(env, 'my_env.szczyp')

        result = self.runner.invoke(
            cli,
            [
                'replace',
                '-r', 'secret.key:known'
            ])

        assert result.exit_code == 1
        assert result.output.strip() == (
            'Error: It seems that the file `env.szczyp` does not exist.')

    def test_replace__broken_replacement__syntax_error(self):

        broken_replacement = [
            'secret known',
            'secret.key known',
            'secret.key:',
            ':what',
            'a.c b:12',
            'a&b:12',
        ]

        for r in broken_replacement:
            result = self.runner.invoke(
                cli,
                [
                    'replace',
                    '-r', r
                ])

            assert result.exit_code == 1
            assert result.output.strip() == (
                f'Error: The replacement `{r}` does not follow '
                f'required syntax.')

    def test_replace__broken_replacement__keyerror(self):

        env = {
            'secret': {
                'key': 'secret.whatever'
            },
            'is_important': True,
            'number': {
                'of': {
                    'workers': '113'
                }
            }
        }
        self.set_encrypted(env)

        result = self.runner.invoke(
            cli,
            [
                'replace',
                '-r', 'a.b.what:known'
            ])

        assert result.exit_code == 1
        assert (
            'It seems that the path `a.b.what` does not exist. Check if '
            'it\'s\ncorrect.') in result.output
