# pylint:disable=(missing-function-docstring)
import typing as tp

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError


BASE_URL = 'https://api.zoom.us/v2'

class Client:
    """
    Async client for making requests
    """

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url

    async def get(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        async with ClientSession() as session:
            async with session.get(f'{self.base_url}/{method}', *args, **kwargs) as response:
                try:
                    data = await response.json()
                    return data
                except ContentTypeError as error:
                    raise ClientException('Error: ', error)

    async def post(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        async with ClientSession() as session:
            async with session.post(f"{self.base_url}/{method}", *args, **kwargs) as response:
                try:
                    data = await response.json()
                    return data
                except ContentTypeError as error:
                    raise ClientException('Error: ', error)

    async def put(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        async with ClientSession() as session:
            async with session.put(f"{self.base_url}/{method}", *args, **kwargs) as response:
                try:
                    data = await response.json()
                    return data
                except ContentTypeError as error:
                    raise ClientException('Error: ', error)

    async def patch(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        async with ClientSession() as session:
            async with session.patch(f"{self.base_url}/{method}", *args, **kwargs) as response:
                try:
                    data = await response.json()
                    return data
                except ContentTypeError as error:
                    raise ClientException('Error: ', error)

    async def delete(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        async with ClientSession() as session:
            async with session.delete(f"{self.base_url}/{method}", *args, **kwargs) as response:
                try:
                    data = await response.json()
                    return data
                except ContentTypeError as error:
                    raise ClientException('Error: ', error)

client = Client()


class ClientException(Exception):
    pass
