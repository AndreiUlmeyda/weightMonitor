"""
Unit tests for the class Ocr
"""

import unittest
from unittest.mock import MagicMock, patch
from src.ocr import Ocr


class TestOcr(unittest.TestCase):
    """
    Test simply forwarding the output of a subprocess call
    """
    @patch('src.ocr.subprocess')
    def test_return_subprocess_output(self, subprocess_mock):
        """
        The output should be a tuple containing stderr and stdout
        of the subprocess call.
        """
        subprocess_result = MagicMock()
        subprocess_result.stdout = 'some result'
        subprocess_result.stderr = 'some error'
        subprocess_mock.run.return_value = subprocess_result

        image = MagicMock()
        image.save.return_value = None
        actual = Ocr.read(image)

        expected = (subprocess_result.stdout, subprocess_result.stderr)
        self.assertEqual(actual, expected)
