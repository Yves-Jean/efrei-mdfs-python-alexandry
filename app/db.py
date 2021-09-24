from app.clients import Client


class SingletonMeta(type):
    """ The Singleton """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self, client: Client) -> None:
        self._client = client

    def get_client(self) -> Client:
        return self._client
