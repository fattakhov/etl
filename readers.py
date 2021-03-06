"""
Модуль содержит reader`ы библиотеки
Reader - объект, позволяющий считывать данные из определенного источника
"""

import csv
import sqlite3

class BaseReader:
    """Базовый класс reader'а
    """

    def __init__(self, config):
        self._config = config

    def read(self): ...


class CSVReader(BaseReader):
    """Чтение файлов csv
    Внутри используется стандартная библиотека python csv

    config: 
        file_name str: Название файла csv
        fmtparams {}: Параметры reader'а csv
    """

    def __iter__(self):
        with open(self._config.get('Settings', 'file_name')) as csv_file:
            _reader = csv.reader(csv_file, **self._config.get('fmtparams', {}))
            for row in _reader:
                yield row

    def read(self):
        return list(self)


class SQLiteReader(BaseReader):
    """
    Запись данных в базу данных SQLite

    config:
        db_name: имя базы данных

    """
    def __iter__(self):
        conn = sqlite3.connect(self._config['db_name'])
        cur = conn.cursor()
        table_name = self._config['table_name']

        try:
            for row in cur.execute('SELECT * FROM '+table_name):
                yield(row)
        except sqlite3.Error as e:
            print("An SQLite error occurred:", e.args[0])
        finally:
            cur.close()
            conn.close()

    def read(self):
        conn = sqlite3.connect(self._config['db_name'])
        cur = conn.cursor()
        table_name = self._config['table_name']
        rows = None
        try:
            cur.execute('SELECT * FROM ' + table_name)
            rows = cur.fetchall()
        except sqlite3.Error as e:
            print("An SQLite error occurred:", e.args[0])
        finally:
            cur.close()
            conn.close()
        return rows

class ReaderFactory:
    """Фабрика для создания reader-объектов
    Позволяет абстрагироваться от самого процесса создание и делегировать
    создание объекта в более декларативном виде

    TODO: необходимо обработать ситуацию, когда нет подходящего reader-класса для чтения.
    Выдать соответсвующую ошибку через ReaderError
    Например: ReaderFactory.create({'type': 'json'}) должен выдать корректную ошибку об отсутствии JSONReader

    .. code:: python
        
        ReaderFactory.create({'type': 'csv', 'file_name': './test_csv.csv'})

    """

    readers_mapping = {
        'csv': CSVReader,
        'sqlite': SQLiteReader
    }

    @classmethod
    def create(cls, config: dict):
        """Основной метод класса, создающий конкретный reader-объект
        В конфигурации обязателен type (соотвествует cls.readers_mapping)
        """
        return cls.readers_mapping.get(config.get('type'))(config)