import pytest
import mongomock
from motor.motor_asyncio import AsyncIOMotorClient
from model import Todo
from database import fetch_all_todos  # Adjust the import based on your project structure
from unittest.mock import patch

@pytest.fixture
def mock_mongo():
    mock_client = mongomock.MongoClient()
    db = mock_client.TodoList
    collection = db.todo

    # Insert test data
    collection.insert_many([
        {"title": "Test Todo 1", "description": "Description 1"},
        {"title": "Test Todo 2", "description": "Description 2"},
        {"title": "Test Todo 3", "description": "Description 3"}
    ])

    # Patch the AsyncIOMotorClient to return the mock client
    with patch('motor.motor_asyncio.AsyncIOMotorClient', return_value=mock_client):
        yield db.todo

@pytest.mark.asyncio
async def test_fetch_all_todos(mock_mongo):
    todos = await fetch_all_todos()
    assert len(todos) == 3
    assert todos[0].title == "Test Todo 1"
    assert todos[1].title == "Test Todo 2"
    assert todos[2].title == "Test Todo 3"
