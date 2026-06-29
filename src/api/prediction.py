import pandas as pd
from src.models.predict import InferenceEngine
from src.utils.logger import get_logger
from src.utils.exceptions import ModelTrainingError

logger = get_logger(__name__)

class PredictorAPI:
    """
    Scoring API interface connecting web request structures to the modeling InferenceEngine.
    """
    def __init__(self):
        self.engine = InferenceEngine()
        
    def process_and_predict(self, form_data: dict) -> dict:
        """
        Maps dictionary fields into raw DataFrame variables and executes inference.
        """
        logger.info("Parsing request data for prediction...")
        try:
            # Map Flask WTForms payload back to raw training features format
            raw_data = {
                'CODE_GENDER': form_data.get('code_gender'),
                'FLAG_OWN_CAR': form_data.get('flag_own_car'),
                'FLAG_OWN_REALTY': form_data.get('flag_own_realty'),
                'CNT_CHILDREN': int(form_data.get('cnt_children', 0)),
                'AMT_INCOME_TOTAL': float(form_data.get('amt_income_total', 0)),
                'NAME_INCOME_TYPE': form_data.get('name_income_type'),
                'NAME_EDUCATION_TYPE': form_data.get('name_education_type'),
                'NAME_FAMILY_STATUS': form_data.get('name_family_status'),
                'NAME_HOUSING_TYPE': form_data.get('name_housing_type'),
                'DAYS_BIRTH': -int(float(form_data.get('age_years', 0)) * 365.25),
                'DAYS_EMPLOYED': 365243 if form_data.get('flag_unemployed') else -int(float(form_data.get('years_employed', 0)) * 365.25),
                'FLAG_MOBIL': 1,
                'FLAG_WORK_PHONE': 1 if form_data.get('flag_work_phone') else 0,
                'FLAG_PHONE': 1 if form_data.get('flag_phone') else 0,
                'FLAG_EMAIL': 1 if form_data.get('flag_email') else 0,
                'OCCUPATION_TYPE': form_data.get('occupation_type', 'Unknown'),
                'CNT_FAM_MEMBERS': int(form_data.get('cnt_fam_members', 1))
            }
            
            input_df = pd.DataFrame([raw_data])
            result = self.engine.predict(input_df)
            return result
        except Exception as e:
            logger.error(f"Failed to process API prediction: {str(e)}")
            raise ModelTrainingError(f"Prediction failed: {str(e)}")
