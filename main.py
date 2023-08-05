from typing import Optional
from fastapi import FastAPI, HTTPException
import scipy.stats as ss
import os
import json
from pydantic import BaseModel, Field
from typing import Union

# Define models to handle the input data.
class PhysicalInfo(BaseModel):
    value: Union[float, None] = None
    height: Union[float, None] = None
    weight: Union[float, None] = None

class PhysicalPercentage(BaseModel):
    gender: str = Field(..., regex="^(male|female)$") # Validate that gender is either 'male' or 'female'
    age: int = Field(..., ge=0) # Validate that age is a positive integer
    physical_info: PhysicalInfo

# Create the FastAPI application
app = FastAPI()

"""
{
    "height": {
        "statistic_info": {
            "male":{
                "19~24세": {
                    "average":174.4,
                    "std":5.75
                },
                ...
            },
            "female":{
                ...
            }
        }
    }
}
"""

# Load the statistics data from a json file
basedir = os.path.abspath(os.path.dirname(__file__))
with open("{}/{}".format(basedir, "total_stats.json"), "r") as f:
    total_info=json.load(f)

# Define a class to calculate the percentile based on the user's physical information and the statistics data
class GetPercentage:
    def __init__(self, category):
        self.info=total_info[category]
        self.category=category

    # Get the age ranges for a specific gender
    def get_age_range(self, gender):
        return list(self.info["statistic_info"][gender].keys())

    # Get the source of the statistics data
    def get_source(self):
        return self.info["source"]

    # Calculate the percentile
    def get_percentage(self, age_range, gender, value):
        m=self.info["statistic_info"][gender][age_range]['average']
        s=self.info["statistic_info"][gender][age_range]['std']
        dif=ss.norm.cdf((value-m)/s)
        if self.category in ["height"]:
            return round(1-dif, 3)
        else:
            print(self.category,round(dif, 3), flush=True)
            return round(dif, 3)

# Function to calculate the Body Mass Index (BMI)
def calculate_bmi(height, weight):
    return weight/((height/100)**2)

def get_age_range_from_age(age: int) -> str:
    if age < 19:
        raise ValueError("Age should be at least 19")
    age_ranges = ['19~24세', '25~29세', '30~34세', '35~39세', '40~44세', '45~49세', '50~54세', '55~59세', '60~64세', '65~69세', '70~74세', '75~79세']
    index = min((age - 19) // 5, len(age_ranges) - 1)
    return age_ranges[index] if age < 80 else '80세 이상'


# Define the API endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/stats/{category}")
async def create_percentage(category: str, item: PhysicalPercentage):
    """
    Calculate and return the percentile of the user's physical information in a specific category.
    
    This endpoint accepts a POST request with a JSON body containing the user's gender, age, and physical information.
    The category is specified as a path parameter and should be one of the categories available in the statistics data.

    The physical information includes height, weight, and a value, but the value used in the calculation depends on the category.
    For the 'bmi' category, the value is calculated from the height and weight.
    For other categories, the value is used directly.

    The percentile is calculated based on the statistics data for the user's age range and gender.

    Args:
        category (str): The category of the statistics. This should be one of the categories available in the statistics data.
        item (PhysicalPercentage): The user's physical information.

    Returns:
        dict: A dictionary with a single key 'percent_result', and the value is the calculated percentile.
    """
    try:
        percentage = GetPercentage
        item_dict = item.dict()
        age_range = get_age_range_from_age(item_dict["age"])
        physical_info = item_dict["physical_info"]
        gender = item_dict["gender"]
        if category =='bmi':
            value = calculate_bmi(physical_info["height"], physical_info["weight"])
        else:
            value = physical_info["value"]
        percent_result=percentage(category).get_percentage(age_range, gender, value)
        return {"percent_result": percent_result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))