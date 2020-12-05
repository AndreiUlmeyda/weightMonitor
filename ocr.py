import subprocess


class Ocr:
    @staticmethod
    def read(image):
        filePath = 'ready_for_ocr.jpg'
        image.save(filePath)

        completed = subprocess.run(
            [
                "ssocr",
                "invert",
                "-D",  # write a debug file to current directory
                "-T",  # use iteratice thresholding
                "-C",  # omit decimal points
                "-d",  # number of digits in the image, see next parameter
                "-1",  # refers to parameter '-d', -1 stands for 'auto'
                "-c",  # select recognized characters, see next parameter
                "digit",  # refers to parameter '-c', only read digits
                "-t",  # specify threshold, see next parameter
                "25",  # refers to parameter '-t', threshold in %
                filePath
            ],
            stdout=subprocess.PIPE)

        readout = completed.stdout
        error = completed.stderr
        return (readout, error)
