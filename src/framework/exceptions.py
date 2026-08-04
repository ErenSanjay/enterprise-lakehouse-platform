"""
Custom exceptions for the Enterprise Lakehouse Platform.

All framework and pipeline exceptions should inherit from
PipelineException to provide consistent error handling.
"""


class PipelineException(Exception):
    """Base exception for all pipeline-related errors."""

    def __init__(self, message: str):
        super().__init__(message)


class ConfigurationError(PipelineException):
    """Raised when configuration is missing or invalid."""
    pass


class SourceReadError(PipelineException):
    """Raised when data cannot be read from the source."""
    pass


class ValidationError(PipelineException):
    """Raised when data quality or schema validation fails."""
    pass


class TransformationError(PipelineException):
    """Raised when a transformation step fails."""
    pass


class DeltaWriteError(PipelineException):
    """Raised when writing to Delta Lake fails."""
    pass


class MetadataUpdateError(PipelineException):
    """Raised when metadata update fails."""
    pass


class PipelineExecutionError(PipelineException):
    """Raised when an unexpected pipeline execution error occurs."""
    pass