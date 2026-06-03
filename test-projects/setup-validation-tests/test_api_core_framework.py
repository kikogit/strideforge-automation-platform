from api_core.client import ApiClient
from api_core.services import PostsService
from api_core.validators import ResponseValidator

def test_api_client_can_be_created():
    api_client = ApiClient()

    assert api_client.base_url == "https://jsonplaceholder.typicode.com"

def test_posts_service_can_be_created():
    api_client = ApiClient()
    posts_service = PostsService(api_client)

    assert posts_service is not None

def test_response_validator_can_be_imported():
    assert ResponseValidator is not None
    