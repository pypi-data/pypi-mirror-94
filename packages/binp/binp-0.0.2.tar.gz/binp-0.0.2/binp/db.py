from asyncio import Lock
from functools import lru_cache
from logging import getLogger
from os import getenv
from pathlib import Path
from typing import Optional, Callable, Awaitable

from databases import Database


def ensure(db: Optional[Database] = None) -> Callable[[], Awaitable[Database]]:
    """
    Wraps database to async callable or inits
    default database defined in DB_URL environment. If not defined - sqlite in data.db will be used
    :return: awaitable with Database instance
    """
    if db is None:
        return __get_default_db()

    async def proxy() -> Database:
        return db

    return proxy


@lru_cache()
def __get_default_db():
    db = Database(getenv('DB_URL', 'sqlite:///data.db'))
    initialized = False
    lock = Lock()

    async def proxy() -> Database:
        nonlocal initialized
        if initialized:
            return db
        async with lock:
            if initialized:
                return db
            await migrate(db)
            initialized = True
            return db

    return proxy


async def migrate(db: Database,
                  src_dir: Path = Path(__file__).absolute().parent / 'migrations',
                  namespace: str = 'default'):
    """
    Apply forward migration on database.
    :param db: async database connection
    :param src_dir: source directory with *.sql files, ordered by name (ex: 0001_abc.sql, 0002_def.sql)
    :param namespace: migration namespace (useful if several projects are using same db)
    """
    logger = getLogger("db-migration")
    await db.execute(
        '''
        CREATE TABLE IF NOT EXISTS _migration (
            name TEXT NOT NULL, 
            namespace TEXT NOT NULL, 
            PRIMARY KEY(name,namespace)
        )''')
    row = await db.fetch_one(
        'SELECT name FROM _migration WHERE namespace = :namespace ORDER BY name DESC LIMIT 1', values={
            "namespace": namespace
        })
    for file in sorted(src_dir.glob("*.sql")):
        if row is not None and file.name <= row[0]:
            logger.info("skipping %s", file.name)
            continue
        async with db.transaction():
            logger.info("applying migration from %s", file.name)
            for statement in file.read_text().split(';'):
                logger.info("applying: %s", statement)
                await db.execute(statement)
            await db.execute('INSERT INTO _migration(name, namespace) VALUES(:name, :namespace)',
                             values={
                                 'name': file.name,
                                 'namespace': namespace
                             })
    logger.info("migration complete, namespace = %s", namespace)
