import pytest

from api_core.client import ApiClient
from api_core.services import PostsService
from common_utils.test_data import TestDataManager

@pytest.fixture
def api_client() -> ApiClient:
    """Fixture to provide an instance of ApiClient."""
    return ApiClient() 

@pytest.fixture
def posts_service() -> PostsService:
    """Fixture to provide an instance of PostsService."""
    api_client = ApiClient()
    return PostsService(api_client) 

@pytest.fixture
def test_data_manager() -> TestDataManager:
    """Fixture to provide an instance of TestDataManager."""
    return TestDataManager()
