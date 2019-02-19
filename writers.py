"""
Модуль содержит writer`ы библиотеки
Writer - объект, позволяющий записывать данные в определенный источник
"""

import csv
import sqlite3


class BaseWriter:
    """Базовый класс writer'а
    """

    def __init__(self, *args, **kwargs):
        """
        args[0] is config
        :param args:
        :param kwargs:
        """
        self._config = args[0]


    def write(self): ...



class CSVWriter(BaseWriter):
    """Запись файлов csv
    Внутри используется стандартная библиотека python csv

    config:
        file_name str: Название файла csv
        fmtparams {}: Параметры writer'а csv
    """

    def write(self, rows):
        with open(self._config.get('write_file_name'), mode='w') as csv_file:
            _writer = csv.writer(csv_file, newline='',
                                 **self._config.get('fmtparams', {}))
            for row in rows:
                print('\n a row', row)
                _writer.writerow(row)


class SQLiteWriter(BaseWriter):
    """
    Запись данных в базу данных SQLite

    config:
        db_name: имя базы данных

    """
    def write(self, rows):
        conn = sqlite3.connect(self._config['db_name'])
        cur = conn.cursor()
        table_name = self._config['table_name']

        #CREATE TABLE IF NOT EXISTS some_table (id INTEGER PRIMARY KEY AUTOINCREMENT, ...);
        # python to sqlite type mapping TODO
        try:

            if len(rows) == 0:
                print('EMPTY DATA')
                return
            else:
                query = 'INSERT INTO ' + table_name + ' VALUES (' + \
                        ('?,' * len(rows[0]))[:-1] + ')'
                print('Query ', query)
                cur.executemany(query, rows)
                conn.commit()

        except sqlite3.Error as e:
            print("An SQLite error occurred:", e.args[0])
        finally:
            cur.close()
            conn.close()






class WriterFactory:
    """Фабрика для создания writer-объектов
    Позволяет абстрагироваться от самого процесса создания и делегировать
    создание объекта в более декларативном виде

    TODO: необходимо обработать ситуацию, когда нет подходящего reader-класса
    для чтения.
    Выдать соответсвующую ошибку через WriterError
    Например: WriterFactory.create({'type': 'json'}) должен выдать корректную
    ошибку об отсутствии JSONWriter

    .. code:: python
        
        WriterFactory.create({'type': 'csv', 'file_name': './test_csv.csv'})

    """

    writers_mapping = {
        'csv': CSVWriter
    }

    @classmethod
    def create(cls, config: dict):
        """Основной метод класса, создающий конкретный writer-объект
        В конфигурации обязателен type (соотвествует cls.writers_mapping)
        """
        return cls.writers_mapping.get(config.get('type'), None)(config)