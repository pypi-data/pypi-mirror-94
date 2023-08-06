import csv
import itertools
import os


class TxtToCsv:
    """
    Converter script.
    Put your txt-files in `input_files` dir and run the script.
    CSV-files will be generated in `output_files`.
    """

    def __init__(self, input_dir='../input_files/', output_dir='../output_files/'):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run_converter(self):
        for file in os.listdir(self.input_dir):
            self.convert_file(file)

    def convert_file(self, file):
        with open(self.input_dir + file, 'r') as in_file:
            lines = in_file.read().splitlines()
            stripped = [line.replace(",", " ").split() for line in lines]
            grouped = itertools.izip(*[stripped]*1)
            with open(self.output_dir + os.path.splitext(file)[0] + '.csv', 'w') as out_file:
                writer = csv.writer(out_file)
                for group in grouped:
                    writer.writerows(group)
