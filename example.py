from restai_functions import Restai
import os
from dotenv import load_dotenv

load_dotenv()

restai = Restai(url=os.environ.get("RESTAI_URL"), api_key=os.environ.get("RESTAI_KEY"))

print(restai.yoda_speak("Hi I'm Pedro"))
