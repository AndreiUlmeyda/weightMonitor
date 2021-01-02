import unittest
from unittest import result
from unittest.mock import MagicMock, patch
from src.ocr import Ocr


class TestOcr(unittest.TestCase):
    @patch('src.ocr.subprocess')
    def testReturnSubprocessOutput(self, SubprocessMock):
        subprocess_result = MagicMock()
        subprocess_result.stdout = 'some result'
        subprocess_result.stderr = 'some error'
        SubprocessMock.run.return_value = subprocess_result

        image = MagicMock()
        image.save.return_value = None
        actual = Ocr.read(image)

        expected = (subprocess_result.stdout, subprocess_result.stderr)
        self.assertEqual(actual, expected)
