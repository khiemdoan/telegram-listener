__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'
__url__ = 'https://github.com/khiemdoan/clean-architecture-python-boilerplate/blob/main/src/settings/__init__.py'

__all__ = [
    'OpenSearchSettings',
    'TelegramSettings',
]


from .opensearch import OpenSearchSettings
from .telegram import TelegramSettings
