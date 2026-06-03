from typing import Any

import httpx

from api_core.client import ApiClient

class PostsService:
    """
    Service layer for /posts API operations.

    Responsibilities:
    - Provide business-readable methods
    - Hide endpoint details from test cases
    - Use ApiClient for low-level HTTP communication
    """

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    def get_all_posts(self) -> httpx.Response:
        return self.api_client.get("/posts")

    def get_post_by_id(self, post_id: int) -> httpx.Response:
        return self.api_client.get(f"/posts/{post_id}")

    def create_post(self, payload: dict[str, Any]) -> httpx.Response:
        return self.api_client.post("/posts", json_body=payload)

    def update_post(self, post_id: int, payload: dict[str, Any]) -> httpx.Response:
        return self.api_client.put(f"/posts/{post_id}", json_body=payload)

    def delete_post(self, post_id: int) -> httpx.Response:
        return self.api_client.delete(f"/posts/{post_id}")