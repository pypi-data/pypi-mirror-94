
import json
import base64
import os

import pytest

from szczypiorek.crypto import (
    encrypt,
    decrypt,
    get_encryption_key,
    create_encryption_key_if_not_exist,
)
from szczypiorek.exceptions import (
    normalize,
    DecryptionError,
    EncryptionKeyBrokenBase64Error,
    EncryptionKeyBrokenJsonError,
    EncryptionKeyFileMissingError,
    EncryptionKeyTooShortError,
    FileNotIgnoredError,
)
from tests import BaseTestCase


def read_encrypted(content):
    content = base64.b64decode(content).decode('utf8')
    content = json.loads(content)

    return content


def write_encrypted(gpg_content, key_hash):

    content = {
        'key_hash': key_hash,
        'gpg': gpg_content,
    }
    content = json.dumps(content)
    content = content.encode('utf8')
    content = base64.b64encode(content)

    return content


class CryptoTestCase(BaseTestCase):

    def setUp(self):
        super(CryptoTestCase, self).setUp()
        try:
            del os.environ['SZCZYPIOREK_ENCRYPTION_KEY']

        except KeyError:
            pass

    #
    # ENCRYPT
    #
    def test_encrypt__empty_content__success(self):

        self.mocker.patch(
            'szczypiorek.crypto.get_encryption_key'
        ).return_value = ('secret', 'hash')

        encrypted = encrypt('').strip()

        content = read_encrypted(encrypted)
        assert content['key_hash'] == 'hash'
        assert content['gpg'].startswith('-----BEGIN PGP MESSAGE-----')
        assert content['gpg'].endswith('-----END PGP MESSAGE-----')
        assert decrypt(encrypted) == ''

    def test_encrypt__no_encryption_key__success(self):

        assert self.root_dir.join(
            '.szczypiorek_encryption_key').exists() is False

        encrypted = encrypt('hello world').strip()

        content = read_encrypted(encrypted)
        assert content['key_hash'] is not None
        assert content['gpg'].startswith('-----BEGIN PGP MESSAGE-----')
        assert content['gpg'].endswith('-----END PGP MESSAGE-----')
        assert decrypt(encrypted) == 'hello world'
        assert self.root_dir.join(
            '.szczypiorek_encryption_key').exists() is True

    def test_encrypt__encryption_key_exists__success(self):

        create_encryption_key_if_not_exist()

        encrypted = encrypt('hello world').strip()

        content = read_encrypted(encrypted)
        assert content['key_hash'] is not None
        assert content['gpg'].startswith('-----BEGIN PGP MESSAGE-----')
        assert content['gpg'].endswith('-----END PGP MESSAGE-----')
        assert decrypt(encrypted) == 'hello world'
        assert len(self.root_dir.join(
            '.szczypiorek_encryption_key').read()) > 128

    #
    # DECRYPT
    #
    def test_decrypt__empty_gpg_content__success(self):

        assert decrypt(encrypt('')) == ''

    def test_decrypt__wrong_content__error(self):

        self.mocker.patch(
            'szczypiorek.crypto.get_encryption_key'
        ).return_value = ('secret', 'hash')

        with pytest.raises(DecryptionError) as e:
            decrypt('what is it')

        assert e.value.args[0] == normalize("""
            Something went wrong while attempting to decrypt. The big chance
            is that you've messed around with the payload.

            Therefore if you see this message it means that you're trying to
            do something bad. Stop doing that.
        """)

    def test_decrypt__broken_gpg__error(self):

        self.mocker.patch(
            'szczypiorek.crypto.get_encryption_key'
        ).return_value = ('secret', 'hash')

        with pytest.raises(DecryptionError) as e:
            decrypt(write_encrypted('what is it', 'hash'))

        assert e.value.args[0] == normalize("""
            Something went wrong while attempting to decrypt. The big chance
            is that you've used broken encryption key.

            Therefore if you see this message it means that you're trying to
            do something bad. Stop doing that.
        """)

    def test_decrypt__key_changed__error(self):

        self.mocker.patch(
            'szczypiorek.crypto.get_encryption_key'
        ).return_value = ('secret', 'hash0')

        with pytest.raises(DecryptionError) as e:
            decrypt(write_encrypted('what is it', 'hash1'))

        assert e.value.args[0] == normalize("""
            It seems that different key was used for encryption and decryption.
        """)

    def test_decrypt__wrong_passphrase__error(self):

        self.mocker.patch(
            'szczypiorek.crypto.get_encryption_key'
        ).side_effect = [('secret.0', 'hash'), ('secret.1', 'hash')]

        encrypted = encrypt('what is it')

        with pytest.raises(DecryptionError) as e:
            decrypt(encrypted)

        assert e.value.args[0] == normalize("""
            Something went wrong while attempting to decrypt. The big chance
            is that you've used broken encryption key.

            Therefore if you see this message it means that you're trying to
            do something bad. Stop doing that.
        """)

    #
    # GET_ENCRYPTION_KEY
    #
    def test_get_encryption_key__all_good__success(self):

        key = 10 * 'd8s9s8c9s8s9ds8d98sd9s89cs8c9s8d'
        self.root_dir.join('.szczypiorek_encryption_key').write(
            base64.b64encode(json.dumps({
                'key': key,
                'hash': 'hash',
            }).encode('utf8')),
            mode='wb')

        assert get_encryption_key() == (key, 'hash')

    def test_get_encryption_key__custom_file__success(self):

        key = 10 * 'd8s9s8c9s8s9ds8d98sd9s89cs8c9s8d'
        self.root_dir.join('.development_encryption_key').write(
            base64.b64encode(json.dumps({
                'key': key,
                'hash': 'hash',
            }).encode('utf8')),
            mode='wb')

        assert get_encryption_key(
            '.development_encryption_key') == (key, 'hash')

    def test_get_encryption_key__file_does_not_exist__error(self):

        with pytest.raises(EncryptionKeyFileMissingError) as e:
            get_encryption_key()

        assert e.value.args[0] == normalize("""
            Couldn't find the '.szczypiorek_encryption_key' file. It is required
            for the correct functioning of the encryption and decryption
            phases.

            If you see this message while performing 'decrypt' then
            simply request the file from fellow code contributor.
            In the 'encrypt' scenario the file is created automatically.
        """)  # noqa

    def test_get_encryption_key__env_var__not_base64__error(self):

        os.environ['SZCZYPIOREK_ENCRYPTION_KEY'] = json.dumps({'key': 'key'})

        with pytest.raises(EncryptionKeyBrokenBase64Error) as e:
            get_encryption_key()

        assert e.value.args[0] == normalize("""
            The content of the 'SZCZYPIOREK_ENCRYPTION_KEY' environment variable was automatically
            encoded with base64 so that noone tries to mess around with it.
            So if you see this message that means that someone tried just that.

            Try to get access to the not broken version of the
            'SZCZYPIOREK_ENCRYPTION_KEY' environment variable or if you have access to the not
            encrypted version you environment files simply remove the broken
            file and run 'decrypt' phase one more time.
        """)  # noqa

    def test_get_encryption_key__file__not_base64__error(self):

        self.root_dir.join('.szczypiorek_encryption_key').write(
            json.dumps({'key': 'key'}).encode('utf8'),
            mode='wb')

        with pytest.raises(EncryptionKeyBrokenBase64Error) as e:
            get_encryption_key()

        assert e.value.args[0] == normalize("""
            The content of the '.szczypiorek_encryption_key' file was automatically
            encoded with base64 so that noone tries to mess around with it.
            So if you see this message that means that someone tried just that.

            Try to get access to the not broken version of the
            '.szczypiorek_encryption_key' file or if you have access to the not
            encrypted version you environment files simply remove the broken
            file and run 'decrypt' phase one more time.
        """)  # noqa

    def test_get_encryption_key__not_json__error(self):

        self.root_dir.join('.szczypiorek_encryption_key').write(
            base64.b64encode(b'"key": "whatever"'),
            mode='wb')

        with pytest.raises(EncryptionKeyBrokenJsonError) as e:
            get_encryption_key()

        assert e.value.args[0] == normalize("""
            The content of the '.szczypiorek_encryption_key' file must be a valid
            json file encoded with base64. It takes the following shape:

            {
                "key": <automatically generated secret>,
                "hash": <automatically generated secret's hash>,
                "created_datetime": <iso datetime of the key creation>
            }
        """)  # noqa

    def test_get_encryption_key__missing_json_fields__error(self):

        self.root_dir.join('.szczypiorek_encryption_key').write(
            base64.b64encode(json.dumps({'not.key': 'what'}).encode('utf8')),
            mode='wb')

        with pytest.raises(EncryptionKeyBrokenJsonError) as e:
            get_encryption_key()

        assert e.value.args[0] == normalize("""
            The content of the '.szczypiorek_encryption_key' file must be a valid
            json file encoded with base64. It takes the following shape:

            {
                "key": <automatically generated secret>,
                "hash": <automatically generated secret's hash>,
                "created_datetime": <iso datetime of the key creation>
            }
        """)  # noqa

    def test_get_encryption_key__file_not_gitignored__error(self):

        key = 'd8s9s8c9s8s9ds8d98sd9s89cs8c9s8d'
        self.root_dir.join('.szczypiorek_encryption_key').write(
            base64.b64encode(json.dumps({
                'key': key,
                'hash': 'hash',
            }).encode('utf8')),
            mode='wb')

        self.mocker.patch(
            'szczypiorek.crypto.assert_is_git_repository'
        ).return_value = True
        self.mocker.patch(
            'szczypiorek.crypto.assert_is_git_ignored'
        ).side_effect = FileNotIgnoredError('not ignored')

        with pytest.raises(FileNotIgnoredError) as e:
            get_encryption_key()

        assert e.value.args[0] == normalize('not ignored')

    def test_get_encryption_key__to_short__error(self):

        key = 'abc123'
        self.root_dir.join('.szczypiorek_encryption_key').write(
            base64.b64encode(json.dumps({
                'key': key,
                'hash': 'hash',
            }).encode('utf8')),
            mode='wb')

        with pytest.raises(EncryptionKeyTooShortError) as e:
            get_encryption_key()

        assert e.value.args[0] == normalize("""
            So it seems that the key used for encryption hidden in
            the '.szczypiorek_encryption_key' file is too short.

            Which means that because of some reason you've decided to mess
            around with the built-in generator of the secured key.

            Try to get access to the not broken version of the
            '.szczypiorek_encryption_key' file or if you have access to the not
            encrypted version you environment files simply remove the broken
            file and run 'decrypt' phase one more time.
        """)

    #
    # CREATE_ENCRYPTION_KEY_IF_NOT_EXIST
    #
    def test_create_encryption_key_if_not_exist__exists__success(self):

        key = 'd8s9s8c9s8s9ds8d98sd9s89cs8c9s8d'
        content = base64.b64encode(json.dumps({'key': key}).encode('utf8'))
        self.root_dir.join('.szczypiorek_encryption_key').write(
            content, mode='wb')

        assert create_encryption_key_if_not_exist() is False
        assert self.root_dir.join(
            '.szczypiorek_encryption_key').read('rb') == content

    def test_create_encryption_key_if_not_exist__does_not_exist__success(self):

        assert create_encryption_key_if_not_exist() is True
        content = self.root_dir.join('.szczypiorek_encryption_key').read('rb')
        content = json.loads(base64.b64decode(content).decode('utf8'))

        assert len(content['key']) == 128
        assert len(set(content['key'])) > 20
