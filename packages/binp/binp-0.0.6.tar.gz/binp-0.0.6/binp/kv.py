from json import dumps, loads
from typing import Optional, Union, Type, TypeVar, List

from databases import Database
from pydantic.main import BaseModel

from binp.db import ensure

T = TypeVar('T', bound=BaseModel)


class KV:
    """
    Basic Key-Value storage with namespace.


    By default - 'default' namespace used. All values are serialized to JSON by standard JSON module or in case
    value is subclass of pydantic BaseMode - by pydantic ``.json()``.

    :Example:

    .. code-block:: python

        from binp import BINP

        binp = BINP()

        async def save_something():
            # save multiple values to storage
            await binp.kv.set(name="reddec", repo="binp", year=2020)
            # get single value
            name = await binp.kv.get('name')
            assert name == 'reddec'


    There is some optimization for saving/loading Pydantic classes when class name itself a key.

    :Example:

    .. code-block:: python

        from binp import BINP
        from pydantic.main import BaseModel

        binp = BINP()

        class Author(BaseModel):
            name: str
            repo: str
            year: int

        async def save_something():
            value = Author(name="reddec", repo="binp", year=2020)
            # save class with key name equal to fully-qualified class name
            await binp.kv.save(value)
            # restore
            saved_value = await binp.kv.load(Author)
            assert value == saved_value

    """

    def __init__(self, namespace: str = 'default', db: Optional[Database] = None):
        self.__db = ensure(db)
        self.__namespace = namespace

    async def save(self, value: BaseModel):
        """
        Save value with key name equal to class name (fqdn)
        """
        values = {
            value.__class__.__qualname__: value
        }
        return await self.set(**values)

    async def load(self, klass: Type[T]) -> Optional[T]:
        """
        Load and parse value by key name equal to class name (fqdn)

        :param klass: BaseModel inherited class to load and parse
        """
        db = await self.__db()
        value = await db.fetch_one('SELECT value FROM kv WHERE namespace = :ns AND key = :key', values={
            'ns': self.__namespace,
            'key': klass.__qualname__,
        })
        if value is None:
            return None
        return klass.parse_raw(value['value'])

    async def set(self, **values: Union[str, int, float, bool, BaseModel]):
        """
        Sav multiple values into storage. All values should be serializable to JSON.
        """
        db = await self.__db()
        await db.execute_many('INSERT OR REPLACE INTO kv(namespace, key, value) VALUES (:ns, :key, :value)', values=[
            {
                'ns': self.__namespace,
                'key': key,
                'value': (value.json() if isinstance(value, BaseModel) else dumps(value, ensure_ascii=False))
            } for key, value in values.items()
        ])

    async def remove(self, *names: str):
        """
        Remove multiple values by names
        """
        db = await self.__db()
        await db.execute_many('DELETE FROM kv WHERE namespace = :ns AND key = :key', values=[
            {'ns': self.__namespace, 'key': name} for name in names
        ])

    async def get(self, name: str) -> Optional[Union[str, int, float, bool, dict]]:
        """
        Get save value by name.
        """
        db = await self.__db()
        value = await db.fetch_one('SELECT value FROM kv WHERE namespace = :ns AND key = :key', values={
            'ns': self.__namespace,
            'key': name,
        })
        if value is None:
            return None
        return loads(value['value'])

    async def namespaces(self) -> List[str]:
        """
        Fetch all namespaces in selected database.
        """
        db = await self.__db()
        value = await db.fetch_all('SELECT namespace FROM kv GROUP BY namespace')
        if value is None:
            return []
        return [x['namespace'] for x in value]

    def select(self, namespace: str) -> 'KV':
        """
        Get accessor to another namespace in a same database
        """
        kv = KV(namespace=namespace, db=None)
        kv.__db = self.__db
        return kv
