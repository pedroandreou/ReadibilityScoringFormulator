import autogen
from config import (
    llm_config,
    config_list,
    create_user_proxy_agent,
    create_assistant_agent,
)


def ask_summary_generator(message):
    summary_generator = create_assistant_agent(
        name="summary_generator",
        system_message="""You are a smart summarizer AI assistant. \
    Another AI assistant will send you a text and you will generate a clear, accurate, concise and informative summary that highlights \
    the main points and the overall message.""",
    )

    summary_user = create_user_proxy_agent(
        name="summary_user",
    )

    summary_user.initiate_chat(summary_generator, message=message)
    return summary_user.last_message()["content"]


def ask_simplification_expert(message):
    simplification_expert = create_assistant_agent(
        name="simplification_expert",
        system_message="""You are a smart simplification expert AI assistant. \
    You will be provided with text. Your task is to simplify the vocabulary within the text, making it easily comprehensible for a five-year-old child.""",
    )

    simplification_user = create_user_proxy_agent(
        name="simplification_user",
    )

    simplification_user.initiate_chat(simplification_expert, message=message)
    return simplification_user.last_message()["content"]


def ask_complexity_expert(message):
    complexity_expert = create_assistant_agent(
        name="complexity_expert",
        system_message="""You are a smart sophistication expert AI assistant. \
    You will be provided with text. Your task is to elevate the complexity of the vocabulary within the text, \
    ensuring it is suitable for a highly specialized audience.""",
    )

    complexity_user = create_user_proxy_agent(
        name="complexity_user",
    )

    complexity_user.initiate_chat(complexity_expert, message=message)
    return complexity_user.last_message()["content"]


def generate_summary(input_text: str, easy_summary: bool = True):
    if easy_summary:

        task = f"""Summarize this text delimited between triple backticks. Then convert the vocabulary of the generated summary \
        to a basic vocabulary that a 5-years-old child could understand.

    text: ```{input_text}```
    """

    else:
        task = f"""Summarize this text delimited between triple backticks. Then transform the vocabulary of the generated summary \
        into an advanced vocabulary appropriate for experts or specialized audiences.

        text: ```{input_text}```
        """

    user_proxy = create_user_proxy_agent(
        name="user_proxy",
        max_consecutive_auto_reply=5,
        is_termination_msg=lambda x: "content" in x
        and x["content"] is not None
        and x["content"].rstrip().endswith("TERMINATE"),
        function_map={
            "ask_summary_generator": ask_summary_generator,
            "ask_simplification_expert": ask_simplification_expert,
            "ask_complexity_expert": ask_complexity_expert,
        },
    )

    assistant = create_assistant_agent(
        name="assistant",
        llm_config={
            "temperature": 0,
            "request_timeout": 600,
            "seed": 42,
            "model": "gpt-4",
            "config_list": config_list,
            "functions": [
                {
                    "name": "ask_summary_generator",
                    "description": "ask ask_summary_generator to summarize a given text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "The text provided to summarize.",
                            },
                        },
                        "required": ["message"],
                    },
                },
                {
                    "name": "ask_simplification_expert",
                    "description": "ask simplification_expert to simplify the vocabulary of a given text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "The text provided to simplify.",
                            },
                        },
                        "required": ["message"],
                    },
                },
                {
                    "name": "ask_complexity_expert",
                    "description": "ask complexity_expert to transform the vocabulary of a given text into an advanced vocabulary appropriate for experts or specialized audiences.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "The text provided to transform into an advanced vocabulary.",
                            },
                        },
                        "required": ["message"],
                    },
                },
            ],
        },
    )

    user_proxy.initiate_chat(
        assistant,
        message=task,
    )
    generated_summary = user_proxy.last_message()["content"].replace("TERMINATE", "")

    return generated_summary
