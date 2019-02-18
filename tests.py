"""
Модуль, содержащий тесты
"""
import configparser
import unittest
from readers import CSVReader
from writers import CSVWriter

CONFIG_PATH = 'settings.ini'


def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()

    config.add_section('')
    config.set('Settings', "file_name", "./test_csv.csv")
    config.set('Settings', "write_file_name", "./test_csv.csv")
    # config.add_section('fmtparams')


    with open(path, "w") as config_file:
        config.write(config_file)


class ReaderTestCase(unittest.TestCase):
    """ Тесты reader-объекта """
    def test_csv_reader(self):
        # test_file_name = './test_csv.csv'
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        reader = CSVReader(config)
        data = list(reader)
        self.assertEqual(len(data), 7)
        self.assertEqual(data[0][0], 'FirstName')
        self.assertEqual(data[6][5], '00123')


class WriterTestCase(unittest.TestCase):
    # """ Тесты writer-объекта """
    pass
    # def test_csv_writer(self):
    #     test_file_name = './test_write_csv.csv'
    #     writer = CSVWriter
    #
    #
    #     reader = CSVReader(test_file_name)
    #     data = list(reader)
    #     self.assertEqual(len(data), 7)
    #     self.assertEqual(data[0][0], 'FirstName')
    #     self.assertEqual(data[6][5], '00123')


class PipelineTestCase(unittest.TestCase):
    """ Тесты pipline-объекта """
    pass


if __name__ == '__main__':
    createConfig(CONFIG_PATH)
    unittest.main()