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
    config['Settings'] = {}
    config['Settings']['file_name'] = "./test_csv.csv"
    config['Settings']['write_file_name'] = "./write_test_csv.csv"
    # config.add_section('fmtparams')
    # config['fmtparams']['encoding']='utf8'

    # config.add_section('Settings')
    # config.set('Settings', "file_name", "./test_csv.csv")
    # config.set('Settings', "write_file_name", "./write_test_csv.csv")
    # config.add_section('fmtparams')

    with open(path, "w") as config_file:
        config.write(config_file)


class ReaderTestCase(unittest.TestCase):
    """ Тесты reader-объекта """
    def test_csv_reader(self):
        # test_file_name = './test_csv.csv'
        # create config
        createConfig(CONFIG_PATH)

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        reader = CSVReader(config)
        data = list(reader)
        print('reader test')
        self.assertEqual(len(data), 7)
        self.assertEqual(data[0][0], 'FirstName')
        self.assertEqual(data[6][5], '00123')


class WriterTestCase(unittest.TestCase):
    """ Тесты writer-объекта """

    def test_csv_writer(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        reader = CSVReader(config)
        rows = list(reader)
        print('\n rows:')
        print(rows)
        writer = CSVWriter(config)
        writer.write(rows)
        config.set('Settings', "file_name", "./write_test_csv.csv")
        reader = CSVReader(config)
        data = list(reader.read())
        print('writer test')
        self.assertEqual(len(data), 7)
        self.assertEqual(data[0][0], 'FirstName')
        self.assertEqual(data[6][5], '00123')


class PipelineTestCase(unittest.TestCase):
    """ Тесты pipline-объекта """
    pass


if __name__ == '__main__':
    createConfig(CONFIG_PATH)
    unittest.main()
