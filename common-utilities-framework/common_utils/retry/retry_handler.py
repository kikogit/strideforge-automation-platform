import time
from collections.abc import Callable
from typing import TypeVar

from common_utils.exceptions import RetryError
from common_utils.logging import FrameworkLogger

T = TypeVar("T")


class RetryHandler:
    """
    Common retry utility for framework operations.

    Responsibilities:
    - Retry a callable operation
    - Log each failed attempt
    - Wait between attempts
    - Raise RetryError after all attempts fail
    """

    def __init__(
        self,
        max_attempts: int = 3,
        delay_seconds: float = 1.0,
        retry_exceptions: tuple[type[Exception], ...] = (Exception,),
    ) -> None:
        if max_attempts < 1:
            raise RetryError("max_attempts must be at least 1.")

        if delay_seconds < 0:
            raise RetryError("delay_seconds cannot be negative.")

        self.max_attempts = max_attempts
        self.delay_seconds = delay_seconds
        self.retry_exceptions = retry_exceptions
        self.logger = FrameworkLogger.get_logger("retry_handler")

    def run(
        self,
        operation: Callable[[], T],
        operation_name: str = "operation",
    ) -> T:
        last_error: Exception | None = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                self.logger.info(
                    "Executing %s. Attempt %s of %s.",
                    operation_name,
                    attempt,
                    self.max_attempts,
                )
                return operation()

            except self.retry_exceptions as error:
                last_error = error

                if attempt == self.max_attempts:
                    break

                self.logger.warning(
                    "%s failed on attempt %s of %s. Error: %s. Retrying in %s seconds.",
                    operation_name,
                    attempt,
                    self.max_attempts,
                    error,
                    self.delay_seconds,
                )

                time.sleep(self.delay_seconds)

        raise RetryError(
            f"{operation_name} failed after {self.max_attempts} attempt(s). "
            f"Last error: {last_error}"
        ) from last_error