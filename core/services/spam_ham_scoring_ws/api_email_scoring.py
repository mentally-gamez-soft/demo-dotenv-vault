import requests
from core import env_loader

def get_payload_spam_ham(email:str) -> dict:
    payload = {"email":email}
    response = requests.post("http://{}:{}/spam-email-refine/api/v1.0/my_email_is_spam_or_ham".format(env_loader.get("WS_HOSTNAME"),env_loader.get("WS_PORT")), json=payload)
    return response.json()