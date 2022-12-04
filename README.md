# Get Percentage
This is a simple python fast-api API script to get your physical percentage.  
The statistic is based on KOSIS(KOrean Statistical Information Service).

## Getting Started
1. Install dependencies
```zsh
pip install -r requirements.txt
```
2. Start FastAPI process
```zsh
uvicorn main:app --reload --host=[HOST] --port=[PORT]
```
3. Open local API docs [http://[HOST]:[PORT]/docs](http://localhost:5000/docs)

## Input
- example
  ```zsh
  curl --location --request POST 'http://localhost:5000/stats/height' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "gender": "male",
    "age": 25,
    "physical_info": {
        "value":174
    }
  }'
  ```
- category: height, bmi, fattness, waist_size

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
