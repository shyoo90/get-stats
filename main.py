from typing import Optional
from fastapi import FastAPI, HTTPException
from models import PhysicalPercentage
from utils import calculate_bmi, get_age_range_from_age
from percentage import GetPercentage
from fastapi import Depends

def get_percentage(category: str):
    return GetPercentage(category)

# Create the FastAPI application
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/stats/{category}")
async def create_percentage(category: str, item: PhysicalPercentage, percentage: GetPercentage = Depends(get_percentage)):
    """
    Calculate and return the percentile of the user's physical information in a specific category.
    
    This endpoint accepts a POST request with a JSON body containing the user's gender, age, and physical information.
    The category is specified as a path parameter and should be one of the categories available in the statistics data.

    The physical information includes height, weight, and a value, but the value used in the calculation depends on the category.
    For the 'bmi' category, the value is calculated from the height and weight.
    For other categories, the value is used directly.

    The percentile is calculated based on the statistics data for the user's age range and gender.

    Args:
        category (str): The category of the statistics. height, bmi, fattness, waist_size.
        item (PhysicalPercentage): The user's physical information.

    Returns:
        dict: A dictionary with a single key 'percent_result', and the value is the calculated percentile.
    """
    try:
        item_dict = item.dict()
        age_range = get_age_range_from_age(item_dict["age"])
        physical_info = item_dict["physical_info"]
        gender = item_dict["gender"]
        if category =='bmi':
            value = calculate_bmi(physical_info["height"], physical_info["weight"])
        else:
            value = physical_info["value"]
        percent_result = percentage.get_percentage(age_range, gender, value)
        return {"percent_result": percent_result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
