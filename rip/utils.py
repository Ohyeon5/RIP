import openai
from api_secrets import API_KEY, ORGANIZATION

def initialize_openai_api():
    """initialize openai api's variables 
    """
    openai.api_key = API_KEY
    openai.organization = ORGANIZATION
