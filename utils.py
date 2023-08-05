# Function to calculate the Body Mass Index (BMI)
def calculate_bmi(height, weight):
    return weight/((height/100)**2)

def get_age_range_from_age(age: int) -> str:
    if age < 19:
        raise ValueError("Age should be at least 19")
    age_ranges = ['19~24세', '25~29세', '30~34세', '35~39세', '40~44세', '45~49세', '50~54세', '55~59세', '60~64세', '65~69세', '70~74세', '75~79세']
    index = min((age - 19) // 5, len(age_ranges) - 1)
    return age_ranges[index] if age < 80 else '80세 이상'