"""
Модуль содержит классы ошибок библиотеки 
"""


class BaseError(Error):
    """Базовый класс ошибки библиотеки
    """
    pass


class WriterError(BaseError):
    """Ошибка writer'а библиотеки
    """
    pass


class ReaderError(BaseError):
    """Ошибка reader'а библиотеки
    """
    pass


class PipelineError(BaseError):
    """Ошибка pipeline
    """
    pass