
from bash import bash
import pytest

from szczypiorek.git import assert_is_git_ignored, assert_is_git_repository
from szczypiorek.exceptions import FileNotIgnoredError, normalize
from tests import BaseTestCase


class GitTestCase(BaseTestCase):

    #
    # ASSERT_IS_GIT_IGNORED
    #
    def test_assert_is_git_ignored__is_ignored(self):

        bash('git init')
        self.root_dir.join('.gitignore').write('file.txt\n')
        f = self.root_dir.join('file.txt')
        f.write('whatever')

        assert assert_is_git_ignored(str(f)) is True

    def test_assert_is_git_ignored__is_ignored__no_file(self):

        bash('git init')

        assert assert_is_git_ignored(None) is True

    def test_assert_is_git_ignored__is_not_ignored(self):

        bash('git init')
        self.root_dir.join('.gitignore').write('')
        f = self.root_dir.join('file.txt')
        f.write('whatever')

        with pytest.raises(FileNotIgnoredError) as e:
            assert_is_git_ignored('file.txt')

        assert e.value.args[0] == normalize("""
            Well it seems that the 'file.txt' is not git ignored. Since it
            appears in the context there's a big chance that it contains some
            sensitive data.

            Please add it to the '.gitignore' and stop tracking it.
        """)

    #
    # ASSERT_IS_GIT_REPOSITORY
    #
    def test_assert_is_git_repository__is_repository(self):

        bash('git init')

        assert assert_is_git_repository() is True

    def test_assert_is_git_repository__is_not_repository(self):

        assert assert_is_git_repository() is False
