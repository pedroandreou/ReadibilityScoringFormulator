import json

import autogen

from config import create_assistant_agent, create_user_proxy_agent, llm_config


def identify_the_industry(input_text: str):
    autogen.ChatCompletion.start_logging()

    student = create_user_proxy_agent(
        name="Admin",
    )

    industry_identifier_assistant = create_assistant_agent(
        name="IndustryIdentifierAssistant",
        system_message="""You are an assistant specialized in  identifying the industry of the given text. You can only choose from 'Education', 'Health Care', 'Military and Governmental Agencies' and 'Publishing'. You should only respond with the industry name and nothing else.""",
        llm_config=llm_config,
    )

    task = f"""A human admin. Interact with the Industry Identifier to identify the industry of the given text.
The text is provided delimited by three backticks.

```{input_text}```"""
    student.initiate_chat(
        industry_identifier_assistant,
        message=task,
    )

    logs = autogen.ChatCompletion.logged_history
    # autogen.ChatCompletion.print_usage_summary()
    autogen.ChatCompletion.stop_logging()

    key = next(iter(logs))
    entries = json.loads(key)
    identified_industry = next(
        (entry["content"] for entry in entries if entry["role"] == "assistant"), None
    )

    if identified_industry:
        return identified_industry
    else:
        raise ValueError("Could not identify the industry.")
