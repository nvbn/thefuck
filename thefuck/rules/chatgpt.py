import platform
import openai
import re
import os
from thefuck import logs
from thefuck.conf import settings


def _check_chatgpt(api_key: str = None) -> bool:
    openai.api_key = os.getenv("THEFUCK_OPENAI_TOKEN") or os.getenv("OPENAI_API_KEY")
    if settings["chatgpt"] > 0 and (api_key or openai.api_key):
        return True
    return False


enabled_by_default = _check_chatgpt()
logs.debug(f"ChatGPT enabled: {enabled_by_default}")

MAX_NUMBER = settings["chatgpt"] or 1
MAX_TOKENS = settings["chatgpt_token"] or 400
MODEL = settings["chatgpt_model"] or "gpt-3.5-turbo"


def match(command):
    return _check_chatgpt()


def get_new_command(command):
    result = _query_chatgpt(
        command=command.script,
        error=command.output,
        explanation=False,
    )
    logs.debug(f"chatgpt result: {result}")
    return result


def _query_chatgpt(
    command: str,
    error: str,
    explanation: bool,  # can be used to include explanations but not used yet
    number: int = MAX_NUMBER,
    model: str = MODEL,
    max_tokens: int = MAX_TOKENS,
    api_key: str = None,
):
    if api_key:
        openai.api_key = api_key
    elif openai.api_key is None:
        return []

    os_env = f"{platform.platform()}"
    prompt = f"""
OS: `{os_env}`
Command: `{command}`
Error: `{error}`
Suggest {"one command" if number == 1 else f"{number} commands"} {"with" if explanation else "without"} explanation.
Commands:"""

    logs.debug("chatgpt: " + prompt)

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
        )
        content = response["choices"][0]["message"]["content"]
        contents = [item.strip() for item in content.split("\n") if item.strip() != ""]
        pattern = re.compile(r"^\d+\.\ *")
        cleaned_contents = [re.sub(pattern, "", item).strip('`') for item in contents]
        return cleaned_contents
    except Exception as e:
        logs.debug(f"chatgpt error: {e}")
        return []
