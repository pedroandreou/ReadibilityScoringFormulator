import sys
import io
import chats.industry_identifier as industry_identifier
import chats.scoring_formulas as scoring_formulas
import autogen
from config import text


def main(input_text: str):
    # Backup the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        # Set stdout and stderr to "devnull"
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        # Call your function
        industry = industry_identifier.identify_the_industry(input_text)
    finally:
        # Restore stdout and stderr to their original values
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    print(industry)

    industry = industry.lower()
    manager = scoring_formulas.prepare_scoring_formulas(industry)
    print("The manager is ", manager)


if __name__ == "__main__":
    main(text)
