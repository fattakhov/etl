"""
Модуль содержит основной объект потока данных pipeline
"""
from typing import Callable
from errors import PipelineError
from readers import ReaderFactory
from writers import WriterFactory


class Pipeline:
    """
    Основной класс потока данных, который содержит в себе reader, writer и обработчики данных

    .. code:: python

    # На примере test_csv.csv можно отфильтровать данные только по резидентам NJ

    def filter_for_nj_rezidents(data):
        return [row for row in data if row[4].strip().lower() == 'nj']

    pipeline = Pipeline({'type': 'csv', 'file_name': 'in.csv'}, {'type': 'sqlite', 'db_file_name': 'out.sqlite'})
    pipeline.register(filter_for_nj_rezidents)
    pipeline.run()

    """

    def __init__(self, reader_config: dict, writer_config: dict):
        self._callbacks = [] # здесь хранятся все регистрируемые обработчики 
        self._reader = ReaderFactory.create(reader_config)
        self._writer = WriterFactory.create(writer_config)

    def register(self, caller):
        """Регистрация обработчика в текущей цепочке.
        """
        if callable(caller):
            self._callbacks.append(caller)
        else:
            raise PipelineError('Попытка регистрации не вызываемого объекта в цепочке обработчиков.')

    def __iter__(self):
        """Итерация по списку обработчиков
        """
        for caller in self._callbacks:
            yield caller

    def run(self):
        """Основной публичный метод объекта pipeline
        Открывает поток на чтение, проводит все зарегистрированные обработчики и записывает данные в хранилище
        """
        data = self._reader.read()
        for caller in self._callbacks:
            data = caller.__call__(data)
        self._writer.write(data)