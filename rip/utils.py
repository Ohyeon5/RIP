import openai
import re
from api_secrets import API_KEY, ORGANIZATION
from typing import Dict, Any


DEFAULT_IMG_URL = "https://github.com/Ohyeon5/RIP/blob/ohyeon5/first_ui/figs/default_img.png"

""" for all possible parameters, see https://beta.openai.com/docs/api-reference/completions/create
Note that `best_of` >= `n` is required 
"""
_default_completion_parameters = {
    "temperature":0.7,
    "max_tokens":60,
    "top_p":1.0,
    "frequency_penalty":0.0,
    "presence_penalty":0.0,
    "n": 1,
    "best_of": 1,
    }


def initialize_openai_api():
    """initialize openai api's variables 
    """
    openai.api_key = API_KEY
    openai.organization = ORGANIZATION

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

def get_default_completion_params() -> Dict[str, Any]:
    return _default_completion_parameters

def set_completion_params(param_dict: Dict[str, Any]) -> Dict[str, Any]:
    params = get_default_completion_params()
    return {k:  param_dict[k] if k in param_dict.keys() else v for k,v in params.items()}