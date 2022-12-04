from typing import Optional
from fastapi import FastAPI
import scipy.stats as ss
import os
import json
from pydantic import BaseModel
from typing import Union

class PhysicalInfo(BaseModel):
    value: Union[float, None] = None
    height: Union[float, None] = None
    weight: Union[float, None] = None

class PhysicalPercentage(BaseModel):
    gender: str
    age: int
    physical_info: PhysicalInfo

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

basedir = os.path.abspath(os.path.dirname(__file__))
with open("{}/{}".format(basedir, "total_stats.json"), "r") as f:
    total_info=json.load(f)

class GetPercentage:
    def __init__(self, category):
        self.info=total_info[category]
        self.category=category

    def get_age_range(self, gender):
        return list(self.info["statistic_info"][gender].keys())

    def get_source(self):
        return self.info["source"]

    def get_percentage(self, age_range, gender, value):
        m=self.info["statistic_info"][gender][age_range]['average']
        s=self.info["statistic_info"][gender][age_range]['std']
        dif=ss.norm.cdf((value-m)/s)
        if self.category in ["height"]:
            return round(1-dif, 3)
        else:
            print(self.category,round(dif, 3), flush=True)
            return round(dif, 3)

def calculate_bmi(height, weight):
    return weight/((height/100)**2)

def get_age_range_from_age(age):
    if age < 24:
        age_range = '19~24세'
    elif 25<=age and age <30:
        age_range = '25~29세'
    elif 30<=age and age <35:
        age_range = '30~34세'
    elif 35<=age and age <40:
        age_range = '35~39세'
    elif 40<=age and age <45:
        age_range = '40~44세'
    elif 45<=age and age <50:
        age_range = '45~49세'
    elif 50<=age and age <55:
        age_range = '50~54세'
    elif 55<=age and age <60:
        age_range = '55~59세'
    elif 60<=age and age <65:
        age_range = '60~64세'
    elif 65<=age and age <70:
        age_range = '65~69세'
    elif 70<=age and age <75:
        age_range = '70~74세'
    elif 75<=age and age <80:
        age_range = '75~79세'
    else:
        age_range = '80세 이상'
    return age_range

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/stats/{category}")
async def create_percentage(category: str, item: PhysicalPercentage):
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
