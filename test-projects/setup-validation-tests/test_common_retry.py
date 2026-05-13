import pytest

from common_utils.exceptions import RetryError
from common_utils.retry import RetryHandler



def test_retry_handler_returns_successful_result():
    retry_handler = RetryHandler(max_attempts=3, delay_seconds=0)
    result = retry_handler.run(lambda: "success", operation_name="successful Operation")
    

def test_retry_handler_retries_until_success():
    retry_handler = RetryHandler(max_attempts=5, delay_seconds=0)
    attempts = {"count": 0}

    def unstable_operation():
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise ValueError("temporary failure")
        return "success after retry"
    result = retry_handler.run(unstable_operation,"unstable_operation")
    assert result == "success after retry"
    assert attempts["count"] == 2
    
def test_retry_handler_raises_retry_error_after_max_attempts():
    retry_handler = RetryHandler(max_attempts=3, delay_seconds=0)

    def always_fails():
        raise ValueError("permanent failure")   
    
    with pytest.raises(RetryError):
        retry_handler.run(always_fails, "always_fails_operation")

def test_retry_handler_validates_max_attempts():
    with pytest.raises(RetryError):
        RetryHandler(max_attempts=0, delay_seconds=0)


def test_retry_handler_validates_delay_seconds():
    with pytest.raises(RetryError):
        RetryHandler(max_attempts=3, delay_seconds=-1)

def test_retry_handler_only_retries_configured_exceptions():
    retry_handler = RetryHandler(
        max_attempts=3, 
        delay_seconds=0, 
        retry_exceptions=(ValueError,),
    )

    def raises_type_error():
        raise TypeError("not retryable")            

    with pytest.raises(TypeError):
        retry_handler.run(raises_type_error, "non_retryable_operation")


