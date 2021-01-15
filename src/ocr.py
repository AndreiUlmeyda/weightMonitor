# pylint: disable=R0903
"""
Provide a class to perform optical character recognition
on an image of a seven segment display.
"""

import subprocess


class Ocr:
    """
    SSOCR (https://github.com/auerswal/ssocr) is used for this task.
    """
    @staticmethod
    def read(image):
        """
        Take an image, save it, then call SSOCR using that file.
        A few parameters are set in order to be able to recover from
        common errors during OCR. For instance, wrong placement of the
        decimal point is avoided by suppressing the output of decimal points
        and inserting them later under the assumption the the digits are correct
        and in order.
        """
        file_path = 'ready_for_ocr.jpg'
        image.save(file_path)

        completed = subprocess.run(
            [
                "ssocr",
                "invert",
                "-D",  # write a debug file to current directory
                "-T",  # use iterative thresholding
                "-C",  # omit decimal points
                "-d",  # number of digits in the image, see next parameter
                "-1",  # refers to parameter '-d', -1 stands for 'auto'
                "-c",  # select recognized characters, see next parameter
                "digit",  # refers to parameter '-c', only read digits
                "-t",  # specify threshold, see next parameter
                "25",  # refers to parameter '-t', threshold in %
                file_path
            ],
            stdout=subprocess.PIPE,
            check=True)

        readout = completed.stdout
        error = completed.stderr
        return (readout, error)
