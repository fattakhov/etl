"""
Модуль, содержащий тесты
"""
import configparser
import unittest
from readers import CSVReader
from writers import CSVWriter


class ReaderTestCase(unittest.TestCase):
    """ Тесты reader-объекта """
    def test_csv_reader(self):
        # test_file_name = './test_csv.csv'

        config = {'type':'csv','file_name':'./test_csv.csv'}
        reader = CSVReader(config)
        data = list(reader)
        print('reader test')
        self.assertEqual(len(data), 7)
        self.assertEqual(data[0][0], 'FirstName')
        self.assertEqual(data[6][5], '00123')


class WriterTestCase(unittest.TestCase):
    """ Тесты writer-объекта """

    def test_csv_writer(self):
        config = {'type': 'csv', 'file_name': './test_csv.csv'}

        reader = CSVReader(config)
        rows = list(reader)
        print('\n rows:')
        print(rows)
        writer = CSVWriter(config={'type': 'csv', 'file_name': './write_test_csv.csv'})
        writer.write(rows)
        reader = CSVReader(config={'type': 'csv', 'file_name': './write_test_csv.csv'})
        data = list(reader.read())
        print('writer test')
        self.assertEqual(len(data), 7)
        self.assertEqual(data[0][0], 'FirstName')
        self.assertEqual(data[6][5], '00123')


class PipelineTestCase(unittest.TestCase):
    """ Тесты pipline-объекта """
    pass


if __name__ == '__main__':
    unittest.main()
