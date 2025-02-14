import requests

class Restai:
    def __init__(self, url, api_key, preload=False):
        self.url = url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }
        
        if preload == True:
            self.load_functions()
    
    def load_functions(self):
        self._create_functions_from_strings(self._get_projects_names())
        
    def _get_projects_names(self):
        project_names = []
        projects = self._get_projects()
        for project in projects:
            project_names.append(project['name'])
        return project_names

    def _get_projects(self):
        """Fetches projects from the API."""
        output = []
        try:
            response = requests.get(
                f'{self.url}/projects',
                headers=self.headers,
                timeout=60
            )

            if response.status_code == 200:
                response_data = response.json()
                return response_data.get('projects', [])
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
                timeout=120
            )

            if response.status_code == 200:
                response_data = response.json()
                return response_data.get('answer', "No answer returned")
            elif response.status_code == 404:
                raise Exception("Project not found")
            else:
                raise Exception(f"Failed: {response.status_code}, {response.text}")

        except requests.RequestException as e:
            print(f"Encountered an exception: {e}")
            return None

    def _create_functions_from_strings(self, strings):
        """Dynamically creates functions that call `call_project()` and attaches them as instance attributes."""
        for s in strings:
            func_name = s.lower().replace(' ', '_')  # Ensure valid function names
            
            def func(parameter=""):
                return self.call_project(func_name, parameter)

            # Attach function directly to the instance
            setattr(self, func_name, func)

    def call(self, func_name, parameter="Your default parameter"):
        """Calls a dynamically created function by name."""
        if hasattr(self, func_name):
            return getattr(self, func_name)(parameter)
        else:
            raise AttributeError(f"Function '{func_name}' not found")

    def __getattr__(self, name):
        """Dynamically create a function if it doesn't exist."""
        def method(parameter=""):
            return self.call_project(name, parameter)
        setattr(self, name, method)
        return method