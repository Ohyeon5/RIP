import openai
import re
# from api_secrets import API_KEY, ORGANIZATION
from typing import Dict, Any


DEFAULT_IMG_URL = "https://raw.githubusercontent.com/Ohyeon5/RIP/main/figs/default_img.png"


# def initialize_openai_api():
#     """initialize openai api's variables 
#     """
#     openai.api_key = API_KEY
#     openai.organization = ORGANIZATION

def validate_url(url: str) -> bool:
    """validate if input str is a url, return bool

    Args:
        url (str): url to inspect

    Returns:
        bool: True when url is a valid url, otherwise False
    """
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None
