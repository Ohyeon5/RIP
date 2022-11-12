import openai
import re
from api_secrets import API_KEY, ORGANIZATION

DEFAULT_IMG_URL = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-WUj2RT1EDW0dxp5pdZ1cixJz/user-VyFZAHxqEZ2X6M0XJ98C2zbc/img-XmAd24nVMBaHPeBoPzDNIen7.png?st=2022-11-12T13%3A55%3A31Z&se=2022-11-12T15%3A55%3A31Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2022-11-11T23%3A13%3A21Z&ske=2022-11-12T23%3A13%3A21Z&sks=b&skv=2021-08-06&sig=95hXSEujfXMDZ204VRhQTTQdv6tuc9e2L1ICzuYGQd8%3D"

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