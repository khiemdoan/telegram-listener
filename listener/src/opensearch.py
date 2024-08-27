__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

from typing import Annotated, Any, AsyncGenerator, Self

from fast_depends import Depends
from opensearchpy import AsyncOpenSearch

from settings import OpenSearchSettings


class _OpenSearchClient:
    _instance: Self | None = None

    def __init__(self) -> None:
        settings = OpenSearchSettings()
        self._os = AsyncOpenSearch(
            hosts=[{'host': settings.host, 'port': settings.port}],
            http_compress=True,
            http_auth=(settings.user, settings.password),
            use_ssl=True,
            verify_certs=False,
        )

    @classmethod
    async def yield_instance(cls) -> AsyncGenerator[Self, Any]:
        if cls._instance is None:
            cls._instance = cls()
        yield cls._instance

    async def create_index(self, name: str, *, body: dict[str, Any]) -> Any:
        if await self._os.indices.exists(name):
            return

        return await self._os.indices.create(name, body)

    async def add_document(self, index: str, doc: Any) -> Any:
        return await self._os.index(index, doc)


OpenSearchClient = Annotated[_OpenSearchClient, Depends(_OpenSearchClient.yield_instance)]
