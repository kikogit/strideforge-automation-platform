from typing import Any

import httpx

from common_utils.exceptions import ValidationError


class ResponseValidator:
    """
    Common API response validation helper.

    Responsibilities:
    - Validate status codes
    - Validate response JSON body
    - Validate required fields
    """

    @staticmethod
    def assert_status_code(response: httpx.Response, expected_status_code: int) -> None:
        actual_status_code = response.status_code

        if actual_status_code != expected_status_code:
            raise ValidationError(
                f"Expected status code {expected_status_code}, "
                f"but got {actual_status_code}. Response body: {response.text}"
            )

    @staticmethod
    def assert_json_body_is_dict(response: httpx.Response) -> dict[str, Any]:
        try:
            response_body = response.json()
        except ValueError as error:
            raise ValidationError("Response body is not valid JSON.") from error

        if not isinstance(response_body, dict):
            raise ValidationError(
                f"Expected response JSON to be a dictionary, "
                f"but got {type(response_body).__name__}."
            )

        return response_body

    @staticmethod
    def assert_json_body_is_list(response: httpx.Response) -> list[Any]:
        try:
            response_body = response.json()
        except ValueError as error:
            raise ValidationError("Response body is not valid JSON.") from error

        if not isinstance(response_body, list):
            raise ValidationError(
                f"Expected response JSON to be a list, "
                f"but got {type(response_body).__name__}."
            )

        return response_body

    @staticmethod
    def assert_field_exists(response_body: dict[str, Any], field_name: str) -> None:
        if field_name not in response_body:
            raise ValidationError(f"Expected field '{field_name}' was not found.")

    @staticmethod
    def assert_field_equals(
        response_body: dict[str, Any],
        field_name: str,
        expected_value: Any,
    ) -> None:
        ResponseValidator.assert_field_exists(response_body, field_name)

        actual_value = response_body[field_name]

        if actual_value != expected_value:
            raise ValidationError(
                f"Expected field '{field_name}' to be '{expected_value}', "
                f"but got '{actual_value}'."
            )