
from unittest import TestCase
import os

import pytest


class BaseTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker, tmpdir):
        self.mocker = mocker
        self.tmpdir = tmpdir

    def setUp(self):

        self.root_dir = self.tmpdir.mkdir('root')

        os.chdir(str(self.root_dir))
