class ProjectBaseException(Exception):
    """Base exception class for all custom project exceptions."""
    def __init__(self, message="A credit card approval prediction system error occurred."):
        self.message = message
        super().__init__(self.message)


class ConfigurationError(ProjectBaseException):
    """Raised when configuration values are missing, invalid, or misconfigured."""
    def __init__(self, message="Invalid or missing project configuration."):
        super().__init__(message)


class DataLoadingError(ProjectBaseException):
    """Raised when there is an issue reading, downloading, or parsing data files."""
    def __init__(self, message="Failed to load input data files."):
        super().__init__(message)


class DataValidationError(ProjectBaseException):
    """Raised when input data schema, values, or formats violate validation checks."""
    def __init__(self, message="Data validation checks failed."):
        super().__init__(message)


class DataCleaningError(ProjectBaseException):
    """Raised when cleaning or merging operations fail."""
    def __init__(self, message="Data cleaning operations failed."):
        super().__init__(message)


class FeatureEngineeringError(ProjectBaseException):
    """Raised when engineering new features or preprocessing fails."""
    def __init__(self, message="Feature engineering operations failed."):
        super().__init__(message)


class ModelTrainingError(ProjectBaseException):
    """Raised when model training, tuning, or saving fails."""
    def __init__(self, message="Model training process encountered an error."):
        super().__init__(message)


class ModelEvaluationError(ProjectBaseException):
    """Raised when model evaluation metric computations or chart plotting fails."""
    def __init__(self, message="Model evaluation process failed."):
        super().__init__(message)


class CloudDeploymentError(ProjectBaseException):
    """Raised when deploying models or scoring requests via IBM Watson Machine Learning fails."""
    def __init__(self, message="IBM Cloud Watson Machine Learning operation failed."):
        super().__init__(message)
