"""
Test readability
"""
from config import llm_config, text, create_user_proxy_agent, create_assistant_agent
import autogen
import json

def score_readability_industry(industry, in_text=None):
    industry = industry.lower()

    autogen.ChatCompletion.start_logging()

    student = create_user_proxy_agent(
        name="Admin",
        llm_config=llm_config,
    )

    if in_text:
        task = f"""A human admin. Interact with the Industry Identifier to identify the industry of the given text.
    The text is provided delimited by three backticks.

    ```{in_text}```"""
    else:
        task = f"""A human admin. Interact with the Industry Identifier to identify the industry of the given text.
    The text is provided delimited by three backticks.

    ```{text}```"""

    if industry == "education":
        # flesch–kincaid grade level
        flesch_reading_ease_assistant = create_assistant_agent(
            name="FleschEasyAssistant",
            system_message="You are an assistant specialized in calculating the Flesch Reading-Ease score for a given text. The formula for this score is: 206.835 - 1.015 * (Total Words/Total Sentences) - 84.6 * (Total Syllables/Total Words). A higher score indicates easier readability. This test focuses on the ease of reading, with polysyllabic words affecting the score significantly. It is a widely used formula and has even been integrated into popular word processing software.",
            llm_config=llm_config
        )
        
        # smog index
        smog_assistant = create_assistant_agent(
            name="SmogIndexAssistant",
            system_message="You are an assistant specialized in calculating the SMOG Grade for a given text. The SMOG Grade is a measure of readability designed to estimate the years of education a person needs to understand a particular piece of writing. It was developed by G. Harry McLaughlin in 1969 and is especially used for assessing health-related messages. To calculate the SMOG Grade using the standard formula, select three 10-sentence samples from the text, count the number of polysyllabic words (words with three or more syllables) in these samples, and use the formula: grade = 1.0430 * sqrt((number of polysyllabic words*30)/number of sentences) + 3.1291. There is also an approximate formula for mental calculation which involves counting the number of polysyllabic words in three samples of ten sentences each, finding the square root of the nearest perfect square to the count, and then adding 3 to the square root. It's important to note that while the SMOG Grade is precise for texts over 30 sentences, its accuracy diminishes for shorter texts.",
            llm_config=llm_config
        )
        
        groupchat = autogen.GroupChat(agents=[flesch_reading_ease_assistant, smog_assistant], messages=[], max_round=20)

        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        recepiant = manager

    elif industry == "healthcare":
        # gunning fox index
        gfi_assistant = create_assistant_agent(
            name="GunningFogIndexAssistant",
            system_message="""
    You are an assistant specialized in calculating the Gunning Fog Index for a given text. 
    The formula requires selecting a passage of around 100 words, including all sentences. Then, calculate the average sentence length (total words divided by total sentences) and count the complex words (those with three or more syllables, excluding proper nouns, familiar jargon, compound words, and common suffixes). Add the average sentence length to the percentage of complex words and multiply the result by 0.4. The Gunning Fog Index aims to estimate the years of formal education a person needs to understand a text on the first reading. An index of 12 suggests the reading level of a U.S. high school senior (around 18 years old). The index correlates with U.S. school grade levels and is used to ensure text readability for a specific audience. It has limitations, such as not considering word frequency or normal usage and changes in its calculation method over time.
    """,
            llm_config=llm_config
        )
        
        recepiant = gfi_assistant

    else:
        fk_grade_level_assistant = create_assistant_agent(
            name="FleschKincaidGradeLevelAssistant",
            system_message="You are an assistant specialized in calculating the Flesch-Kincaid Grade Level for a given text. The formula is: 0.39 * (Total Words/Total Sentences) + 11.8 * (Total Syllables/Total Words) - 15.59. The result represents a U.S. school grade level, indicating the level of education someone would need to easily understand the text. This test emphasizes sentence length over word length and can produce very high scores with long sentences of monosyllabic words. The test results are not directly comparable to the Reading-Ease score and do not have an upper bound.",
            llm_config=llm_config
        )
        
        recepiant = fk_grade_level_assistant

    student.initiate_chat(
        recepiant,
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