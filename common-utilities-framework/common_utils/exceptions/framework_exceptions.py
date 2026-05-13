class FrameworkError(Exception):
    """Base exception for all framework-level errors."""

class ConfigurationError(FrameworkError):
    """Raised when configuration is missing, invalid, or cannot be loaded."""


class EnvironmentError(FrameworkError):
    """Raised when the requested test environment is invalid or unavailable."""


class TestDataError(FrameworkError):
    """Raised when test data cannot be found or parsed."""


class ReportingError(FrameworkError):
    """Raised when report generation or artifact handling fails."""


class DriverInitializationError(FrameworkError):
    """Raised when browser, API client, or mobile driver initialization fails."""


class AuthenticationError(FrameworkError):
    """Raised when authentication or token handling fails."""


class ValidationError(FrameworkError):
    """Raised when framework-level validation fails."""

class RetryError(FrameworkError):
    """Raised when a retry operation fails after all retry attempts."""