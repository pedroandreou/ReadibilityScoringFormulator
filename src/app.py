import sys
import io
import chats.industry_identification as industry_identification


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
    finally:
        # Restore stdout and stderr to their original values
        sys.stdout = original_stdout
        sys.stderr = original_stderr

    print(industry)


if __name__ == "__main__":
    main()