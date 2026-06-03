from typing import Any

import httpx

from common_utils.config import EnvironmentManager
from common_utils.logging import FrameworkLogger
from common_utils.retry import RetryHandler


class ApiClient:
    """
    Base API client for framework-level HTTP communication.

    Responsibilities:
    - Read API base URL from environment config
    - Execute HTTP requests
    - Apply timeout
    - Log request and response details
    - Support retry for transient request failures
    """

    def __init__(self) -> None:
        environment_manager = EnvironmentManager()
        api_config = environment_manager.get_api_config()

        self.base_url = api_config["base_url"].rstrip("/")
        self.timeout = api_config.get("timeout", 30)
        retry_count = api_config.get("retry_count", 1)

        self.logger = FrameworkLogger.get_logger("api_client")
        self.retry_handler = RetryHandler(
            max_attempts=retry_count,
            delay_seconds=0,
            retry_exceptions=(httpx.RequestError,),
        )

    def get(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        return self._request(
            method="GET",
            endpoint=endpoint,
            headers=headers,
            params=params,
        )

    def post(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> httpx.Response:
        return self._request(
            method="POST",
            endpoint=endpoint,
            headers=headers,
            json_body=json_body,
        )

    def put(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> httpx.Response:
        return self._request(
            method="PUT",
            endpoint=endpoint,
            headers=headers,
            json_body=json_body,
        )

    def patch(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> httpx.Response:
        return self._request(
            method="PATCH",
            endpoint=endpoint,
            headers=headers,
            json_body=json_body,
        )

    def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        return self._request(
            method="DELETE",
            endpoint=endpoint,
            headers=headers,
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> httpx.Response:
        url = self._build_url(endpoint)

        def execute_request() -> httpx.Response:
            self.logger.info("API Request: %s %s", method, url)

            response = httpx.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=self.timeout,
            )

            self.logger.info(
                "API Response: %s %s -> Status %s",
                method,
                url,
                response.status_code,
            )

            return response

        return self.retry_handler.run(
            execute_request,
            operation_name=f"{method} {endpoint}",
        )

    def _build_url(self, endpoint: str) -> str:
        clean_endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{clean_endpoint}"