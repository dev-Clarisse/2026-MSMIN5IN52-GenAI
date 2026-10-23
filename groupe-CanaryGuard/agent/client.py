from openai import OpenAI
from agent.config import MODEL_API_KEY, API_BASE_URL, MODEL_NAME

client = OpenAI(api_key=MODEL_API_KEY, base_url=API_BASE_URL)


def appeler_modele(messages: list, outils: list | None = None):
    """Un appel au modèle. Mêmes réglages pour toutes les configurations."""
    kwargs = dict(
        model=MODEL_NAME,
        messages=messages,
        temperature=0,  
        extra_body={"enable_thinking": False},  
    )
    if outils:
        kwargs["tools"] = outils
        kwargs["tool_choice"] = "auto"
    return client.chat.completions.create(**kwargs)