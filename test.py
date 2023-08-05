from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is defined in a file named main.py
import json

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_percentage():
    # Example data
    data = {
        "gender": "male",
        "age": 25,
        "physical_info": {
            "height": 180,
            "weight": 75
        }
    }
    response = client.post("/stats/bmi", data=json.dumps(data))
    assert response.status_code == 200
    # Add additional assertions here to check the response data