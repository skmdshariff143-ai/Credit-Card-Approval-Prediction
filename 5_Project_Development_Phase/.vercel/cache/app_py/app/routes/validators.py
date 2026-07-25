
from app.utils.exceptions import ValidationError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class InputValidator:
    """
    Validates input variables for the Credit Card Approval REST API and Flask UI.
    """

    @staticmethod
    def validate_predict_json(data: dict):
        """
        Validates API input request payload.
        """
        required = {
            "code_gender",
            "cnt_children",
            "cnt_fam_members",
            "age_years",
            "amt_income_total",
            "flag_own_car",
            "flag_own_realty",
            "name_income_type",
            "name_education_type",
            "name_family_status",
            "name_housing_type",
            "years_employed",
            "flag_unemployed",
        }

        # Check required fields
        missing = required - set(data.keys())
        if missing:
            raise ValidationError(f"Missing required parameters: {list(missing)}")

        # Validate value bounds
        try:
            age = float(data["age_years"])
            income = float(data["amt_income_total"])
            children = int(data["cnt_children"])
            family_members = int(data["cnt_fam_members"])
            years_employed = float(data["years_employed"])
        except ValueError as e:
            raise ValidationError(f"Invalid numeric type conversion: {str(e)}")

        if age < 18.0 or age > 120.0:
            raise ValidationError("Age must be between 18 and 120 years.")

        if income <= 0.0:
            raise ValidationError("Gross Annual Income must be greater than 0.")

        if children < 0:
            raise ValidationError("Number of children cannot be negative.")

        if family_members < 1:
            raise ValidationError("Family size must be at least 1.")

        if years_employed < 0.0 or years_employed > 80.0:
            raise ValidationError("Years employed must be between 0 and 80.")

        # Categorical choices check
        valid_genders = {"M", "F"}
        if data["code_gender"] not in valid_genders:
            raise ValidationError(f"Invalid Gender selection: {data['code_gender']}. Expected: M or F.")

        valid_assets = {"Y", "N"}
        if data["flag_own_car"] not in valid_assets or data["flag_own_realty"] not in valid_assets:
            raise ValidationError("Asset flags (car, realty) must be Y or N.")

        logger.info("Input prediction request validated successfully.")
        return True
