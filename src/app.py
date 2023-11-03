import sys
import io
import chats.industry_identification as industry_identification
import chats.readability_test as readability_test
from config import text


def main():
    # Backup the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        # Set stdout and stderr to "devnull"
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        # Call your function
        industry = industry_identification.identify_the_industry()
        read_score = readability_test.score_readability_fk()
    except Exception as err:
        raise err
    finally:
        # Restore stdout and stderr to their original values
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    print(f"Text: {text}\n")
    print(f"Industry: {industry}\nReadability Score: {read_score}")


if __name__ == "__main__":
    main()
