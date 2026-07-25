class CreditCardApprovalException(Exception):
    """Base exception for all system modules."""

    def __init__(self, message="A credit card approval prediction system error occurred."):
        self.message = message
        super().__init__(self.message)


class DataLoadingError(CreditCardApprovalException):
    """Raised when data reading or ingestion fails."""

    pass


class DataValidationError(CreditCardApprovalException):
    """Raised when schema validation rules fail."""

    pass


class ValidationError(DataValidationError):
    """Raised when API input validation checks fail."""

    pass


class DataPreprocessingError(CreditCardApprovalException):
    """Raised when cleaning, imputing, outlier correction, or pipeline transforms fail."""

    pass


class FeatureEngineeringError(CreditCardApprovalException):
    """Raised when generating custom indicators or selecting features fails."""

    pass


class ModelTrainingError(CreditCardApprovalException):
    """Raised when training, tuning, or serialization operations fail."""

    pass


class ModelEvaluationError(CreditCardApprovalException):
    """Raised when scoring metrics or plotting operations fail."""

    pass


class CloudDeploymentError(CreditCardApprovalException):
    """Raised when interacting with IBM Watson ML endpoints fails."""

    pass
