import autogen

from config import llm_config

# Scoring agents
# flesch–kincaid grade level
flesch_reading_ease_assistant = autogen.AssistantAgent(
    name="FleschEasyAssistant",
    system_message="You are an assistant specialized in calculating the Flesch Reading-Ease score for a given text. The formula for this score is: 206.835 - 1.015 * (Total Words/Total Sentences) - 84.6 * (Total Syllables/Total Words). A higher score indicates easier readability. This test focuses on the ease of reading, with polysyllabic words affecting the score significantly. It is a widely used formula and has even been integrated into popular word processing software.",
    llm_config=llm_config,
)

# smog index
smog_assistant = autogen.AssistantAgent(
    name="SmogIndexAssistant",
    system_message="You are an assistant specialized in calculating the SMOG Grade for a given text. The SMOG Grade is a measure of readability designed to estimate the years of education a person needs to understand a particular piece of writing. It was developed by G. Harry McLaughlin in 1969 and is especially used for assessing health-related messages. To calculate the SMOG Grade using the standard formula, select three 10-sentence samples from the text, count the number of polysyllabic words (words with three or more syllables) in these samples, and use the formula: grade = 1.0430 * sqrt((number of polysyllabic words*30)/number of sentences) + 3.1291. There is also an approximate formula for mental calculation which involves counting the number of polysyllabic words in three samples of ten sentences each, finding the square root of the nearest perfect square to the count, and then adding 3 to the square root. It's important to note that while the SMOG Grade is precise for texts over 30 sentences, its accuracy diminishes for shorter texts.",
    llm_config=llm_config,
)

# gunning fox index
gfi_assistant = autogen.AssistantAgent(
    name="GunningFogIndexAssistant",
    system_message="""
You are an assistant specialized in calculating the Gunning Fog Index for a given text.
The formula requires selecting a passage of around 100 words, including all sentences. Then, calculate the average sentence length (total words divided by total sentences) and count the complex words (those with three or more syllables, excluding proper nouns, familiar jargon, compound words, and common suffixes). Add the average sentence length to the percentage of complex words and multiply the result by 0.4. The Gunning Fog Index aims to estimate the years of formal education a person needs to understand a text on the first reading. An index of 12 suggests the reading level of a U.S. high school senior (around 18 years old). The index correlates with U.S. school grade levels and is used to ensure text readability for a specific audience. It has limitations, such as not considering word frequency or normal usage and changes in its calculation method over time.
""",
    llm_config=llm_config,
)

Automated_readability_index_expert = autogen.AssistantAgent(
            name="Automated_readability_index_expert",
            llm_config=llm_config,
            system_message="""You are a very smart expert in calculating the Automated readability Index from a given text. \
The automated readability index (ARI) is a readability test for English texts, designed to gauge the understandability of a text.\

        """
        )

Coleman_Liau_index_expert = autogen.AssistantAgent(
            name="Coleman_Liau_index_expert",
            llm_config=llm_config,
            system_message="""You are a very smart expert in calculating the Coleman-Liau Index from a given text. \
Coleman–Liau relies on characters instead of syllables per word. Its Formula is CLI= 0.0588*L - 0.296*S-15.8. \
where L is the average number of letters per 100 words and S is the average number of sentences per 100 words.
        """
        )

def prepare_scoring_formulas(industry):
    if industry == "education":
        groupchat = autogen.GroupChat(
            agents=[flesch_reading_ease_assistant, smog_assistant, Coleman_Liau_index_expert],
            messages=[],
            max_round=5,
        )

    elif industry == "healthcare":
        groupchat = autogen.GroupChat(agents=[gfi_assistant, Automated_readability_index_expert, flesch_reading_ease_assistant],
                                      messages=[],
                                      max_round=5)

    elif industry == "military and governmental agencies":
        groupchat = autogen.GroupChat(agents=[Automated_readability_index_expert, Coleman_Liau_index_expert, smog_assistant],
                                      messages=[],
                                      max_round=5)

    elif industry == "publishing":
        groupchat = autogen.GroupChat(agents=[Coleman_Liau_index_expert, flesch_reading_ease_assistant, Automated_readability_index_expert],
                                      messages=[],
                                      max_round=5)

    else:
        raise ValueError(
            "The extracted industry is not part of the pre-defined ones for setting up the scoring formulas."
        )

    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    return manager
