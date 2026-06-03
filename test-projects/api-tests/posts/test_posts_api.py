import pytest

from api_core.services import PostsService
from api_core.validators import ResponseValidator
from common_utils.test_data import TestDataManager

@pytest.mark.api
@pytest.mark.smoke
def test_get_post_by_id(posts_service: PostsService):
    response  = posts_service.get_post_by_id(1)

    ResponseValidator.assert_status_code(response,200)
    response_body = ResponseValidator.assert_json_body_is_dict(response)

    ResponseValidator.assert_field_equals(response_body, "id",1)
    ResponseValidator.assert_field_exists(response_body, "title")
    ResponseValidator.assert_field_exists(response_body, "body")
    ResponseValidator.assert_field_exists(response_body, "userId")

@pytest.mark.api
@pytest.mark.response
def test_get_all_posts(posts_service: PostsService):
    response = posts_service.get_all_posts()

    ResponseValidator.assert_status_code(response,200)
    response_body = ResponseValidator.assert_json_body_is_list(response)

    assert len(response_body) > 0



def test_create_post(
    posts_service: PostsService, 
    test_data_manager: TestDataManager,
):
    payload = test_data_manager.get_json_record("api/positive/posts.json", "create_post")
    response = posts_service.create_post(payload)

    ResponseValidator.assert_status_code(response,201)
    response_body = ResponseValidator.assert_json_body_is_dict(response)
    
    ResponseValidator.assert_field_equals(response_body, "title", payload["title"])
    ResponseValidator.assert_field_equals(response_body, "body", payload["body"])
    ResponseValidator.assert_field_equals(response_body, "userId", payload["userId"])
