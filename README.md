# restai-functions

Call RESTai projects like functions in Python

## Usage

```python
from restai_functions import Restai


restai = Restai(url='https://XXXXXXXXXXXXXX', api_key='XXXXXXXXXXXXXX')

print(restai.func_project1("What is the status?"))  # Assuming 'project1' exists
print(restai.func_another_project("Give me the latest update."))  # Another project

# Call function by name dynamically
print(restai.call("func_project1", "How is it performing?"))
print(restai.call("func_another_project", "What is the latest update?"))
```
