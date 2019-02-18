"""
Модуль, содержащий тесты
"""

import unittest
from readers import CSVReader


class ReaderTestCase(unittest.TestCase):
    """ Тесты reader-объекта """
    def test_csv_reader(self):
        test_file_name = './test_csv.csv'
        reader = CSVReader(test_file_name)
        data = list(reader)
        self.assertEqual(len(data), 7)
        self.assertEqual(data[0][0], 'FirstName')
        self.assertEqual(data[6][5], '00123')


class WriterTestCase(unittest.TestCase):
    """ Тесты writer-объекта """
    pass


class PipelineTestCase(unittest.TestCase):
    """ Тесты pipline-объекта """
    pass


if __name__ == '__main__':
    unittest.main()