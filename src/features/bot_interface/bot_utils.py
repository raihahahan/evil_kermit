import re

def extract_telegram_handle(input_string):
    # Define a regular expression pattern to match the Telegram handle without the @ symbol
    pattern = r'/clone @(\w+)'

    # Use re.match to search for the pattern in the input string
    match = re.match(pattern, input_string)

    # Check if a match is found
    if match:
        # Extract the Telegram handle from the matched group
        telegram_handle = match.group(1)
        return telegram_handle
    else:
        # Return None if no match is found
        return None