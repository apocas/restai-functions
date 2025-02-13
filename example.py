from restai_functions import Restai


restai = Restai(url='https://XXXXXXXXXXXXXX', api_key='XXXXXXXXXXXXXX')

print(restai.project1("What is the status?"))  # Assuming 'project1' exists
print(restai.another_project("Give me the latest update."))  # Another project

# Call function by name dynamically
print(restai.call("project1", "How is it performing?"))
print(restai.call("another_project", "What is the latest update?"))