import asyncio
from typing import AsyncGenerator
import pytest_asyncio
from httpx import AsyncClient
from app import app

@pytest_asyncio.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac