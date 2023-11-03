"""
Test readability with Flesch–Kincaid readability tests
"""
from config import llm_config, text, create_user_proxy_agent, create_assistant_agent
import autogen
import json

def score_readability_fk():
    autogen.ChatCompletion.start_logging()

    student = create_user_proxy_agent(
        name="Admin",
        llm_config=llm_config,
    )

    readability_assistant = create_assistant_agent(
        name="ReadabilityAssistant",
        system_message="""You are an assistant specialized in the Flesch-Kincaid readability tests. Give a score of the readability of the given text in school levels. You should only respond with the readability score and nothing else. Scores and school levels are as follows:
        Score           School Level
        100.00-90.00	5th grade
        90.0-80.0	    6th grade
        80.0-70.0	    7th grade
        70.0-60.0	    8th & 9th grade
        60.0-50.0	    10th to 12th grade
        50.0-30.0	    College
        30.0-10.0	    College graduate
        10.0-0.0	    Professional
        
        """,
        llm_config=llm_config,
    )

    task = f"""A human admin. Interact with the Readability Assistant to identify the readability score of the given text.
The text is provided delimited by three backticks.

```{text}```"""
    student.initiate_chat(
        readability_assistant,
        message=task,
    )

    logs = autogen.ChatCompletion.logged_history
    # autogen.ChatCompletion.print_usage_summary()
    autogen.ChatCompletion.stop_logging()

    key = next(iter(logs))
    entries = json.loads(key)
    identified_score = next(
        (entry["content"] for entry in entries if entry["role"] == "assistant"), None
    )

    if identified_score:
        return identified_score
    else:
        raise ValueError("Could not identify the readability score.")