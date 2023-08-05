from pydantic import BaseModel, Field, validator
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

    # Additional validation to ensure that at least one of value, height, or weight is not None
    @validator('physical_info', pre=True, always=True)
    def check_physical_info(cls, v):
        if v['value'] is None and v['height'] is None and v['weight'] is None:
            raise ValueError("At least one of value, height, or weight must be provided")
        return v