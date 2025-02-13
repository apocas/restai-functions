import requests


class Restai:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }
        
        self.projects = self._get_projects()
        self._create_functions_from_strings(self.projects)

    def _get_projects(self):
        """Fetches project names from the API."""
        output = []
        try:
            response = requests.get(
                f'{self.url}/projects',
                headers=self.headers,
                timeout=60
            )

            if response.status_code == 200:
                response_data = response.json()
                projects = response_data.get('projects', [])
                for project in projects:
                    output.append(project['name'])
            else:
                print(f"Failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Failed: {e}")
        
        return output

    def call_project(self, function_name, parameter):
        """Calls the API endpoint with a given function name and parameter."""
        try:
            # Extract project name from function name (removing "func_")
            project_name = function_name
            
            response = requests.post(
                f'{self.url}/{project_name}/question',
                json={'question': parameter},
                headers=self.headers,
                timeout=60
            )

            if response.status_code == 200:
                response_data = response.json()
                return response_data.get('answer', "No answer returned")
            else:
                print(f"Failed: {response.status_code}, {response.text}")
                return None

        except requests.RequestException as e:
            print(f"Encountered an exception: {e}")
            return None

    def _create_functions_from_strings(self, strings):
        """Dynamically creates functions that call `call_project()` with their respective function name."""
        module_globals = globals()  # Get global scope of the module

        for s in strings:
            func_name = f"{s.lower().replace(' ', '_')}"  # Ensure valid function names
            
            def func(template_func_name=func_name):
                return self.call_project(template_func_name, "Your default parameter")

            module_globals[func_name] = func  # Attach function to module's namespace

    # Function to call a dynamically created function by name
    def call(self, func_name, parameter="Your default parameter"):
        """Calls a dynamically created function by name."""
        if func_name in globals():
            return globals()[func_name](parameter)
        else:
            raise AttributeError(f"Function '{func_name}' not found")
