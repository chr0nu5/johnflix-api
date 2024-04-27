import glob
import pep8

from django.test import TestCase


class Pep8TestCase(TestCase):

    """Test all the files for PEP8

    Attributes:
        path (str): the base path for the files
        pep8style (pep8): the checker
    """

    def setUp(self):
        """Initialize the vars for the test
        """
        self.path = '/app/'
        self.pep8style = pep8.StyleGuide(quiet=True)

    def test_pep8(self):
        """Should not show any errors"""
        for file in glob.glob('/app/' + '/**/*.py', recursive=True):
            if "migrations" not in file:
                fchecker = pep8.Checker(file, show_source=True)
                file_errors = fchecker.check_all()
                self.assertEqual(file_errors, 0)
