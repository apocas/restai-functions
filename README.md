# restai-functions

Call RESTai projects like functions in Python

## Usage

```python
from restai_functions import Restai

restai = Restai(url=os.environ.get("RESTAI_URL"), api_key=os.environ.get("RESTAI_KEY"), auto_load=True)

print(restai.yoda_speak("Hi I'm Pedro"))

```
