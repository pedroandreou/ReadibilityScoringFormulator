import io
import sys

import chats.industry_identifier as industry_identifier
import chats.scoring_formulas as scoring_formulas
import chats.summarizer as summarizer
from config import create_user_proxy_agent, text


def main(input_text: str):
    # Backup the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        # Set stdout and stderr to "devnull"
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        # Get the industry of the given text
        industry = industry_identifier.identify_the_industry(input_text)
    finally:
        # Restore stdout and stderr to their original values
        sys.stdout = original_stdout
        sys.stderr = original_stderr
    print("The industry is: ", industry)

    # Get the Groupchat of Scoring Formula Agents
    industry = industry.lower()
    manager = scoring_formulas.prepare_scoring_formulas(industry)

    # Generate summary
    easy_summary = True  # This should be a button on the UI or sth
    summary = summarizer.generate_summary(input_text, easy_summary)
    print("The summary is: ", summary)

    task = f"""Decide which scoring formula you should follow by calling the right assistant.
Each assistant represents a different readibility scoring formula.
Doing so, the assistant should calculate the readability level and return the result based on the given text delimited by three backticks.

```{summary}```
"""

    student = create_user_proxy_agent(name="Admin")

    student.initiate_chat(manager, message=task)


if __name__ == "__main__":
    main(text)
