import sys
import io
import chats.industry_identification as industry_identification
import chats.readability_test as readability_test
from config import text


def main():
    print("Please enter in text you want to analyze. If you just want to run the example text, press enter:\n")
    in_text = input()
    
    # Backup the original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    try:
        # Set stdout and stderr to "devnull"
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        # Call your function
        
        if in_text == "" or len(in_text) == 0:
            in_text = None
        industry = industry_identification.identify_the_industry(in_text)
        read_score = readability_test.score_readability_industry(industry, in_text)
    except Exception as err:
        raise err
    finally:
        # Restore stdout and stderr to their original values
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    print(f"Text: {text if in_text is None else in_text}\n")
    print(f"Industry\n{industry}\n\nReadability\n{read_score}")


if __name__ == "__main__":
    main()
