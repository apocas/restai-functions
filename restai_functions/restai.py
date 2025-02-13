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

    def call_project(self, project_name, parameter):
        """Calls the API endpoint with a given project name and parameter."""
        try:
            response = requests.post(
                f'{self.url}/projects/{project_name}/question',
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
        """Dynamically creates functions that call `call_project()` and attaches them as instance attributes."""
        for s in strings:
            func_name = s.lower().replace(' ', '_')  # Ensure valid function names
            
            def func(template_func_name=s):
                return self.call_project(template_func_name, "Your default parameter")

            # Attach function directly to the instance
            setattr(self, func_name, func)

    def call(self, func_name, parameter="Your default parameter"):
        """Calls a dynamically created function by name."""
        if hasattr(self, func_name):
            return getattr(self, func_name)(parameter)
        else:
            raise AttributeError(f"Function '{func_name}' not found")
