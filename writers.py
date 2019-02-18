"""
Модуль содержит writer`ы библиотеки
Writer - объект, позволяющиq записывать данные в определенный источник
"""

class BaseWriter:
    """Базовый класс writer'а
    """

    def __init__(self, *arsg, **kwargs): ...

    def write(): ...


class WriterFactory:
    """Фабрика для создания writer-объектов
    Позволяет абстрагироваться от самого процесса создание и делегировать
    создание объекта в более декларативном виде

    TODO: необходимо обработать ситуацию, когда нет подходящего reader-класса для чтения.
    Выдать соответсвующую ошибку через WriterError
    Например: WriterFactory.create({'type': 'json'}) должен выдать корректную ошибку об отсутствии JSONWriter

    .. code:: python
        
        WriterFactory.create({'type': 'csv', 'file_name': './test_csv.csv'})

    """

    writers_mapping = {
        'csv': CSVReader
    }

    @classmethod
    def create(cls, config: dict):
        """Основной метод класса, создающий конкретный writer-объект
        В конфигурации обязателен type (соотвествует cls.writers_mapping)
        """
        return cls.writers_mapping.get(config.get('type'), None)(config)