class StringManager():
    # Checks lengths of string and caps it to max length.
    async def cap_string(string: str, max_length: int) -> str:
        if string.endswith("\u200B"):
            string = string[:-1]

        str_length = len(string)

        if str_length > max_length:
            length_diff = str_length - max_length
            rem_chars = length_diff + 3
            return f"{string[:-rem_chars]}..."
        else:
            return string

    # Centers string based on max length, returns centered string.
    async def center_string(string: str, max_length: int) -> str:
        empty_space = " "
        str_length = len(string)

        if string.endswith("\u200B"):
            string = string[:-1]
            str_length += 3

        if str_length >= max_length - 2:
            str_result = await StringManager.cap_string(string = string, max_length = max_length - 2)
        else:
            str_result = string

        str_length = len(str_result)
        length_diff = max_length - str_length - 2
        if length_diff > 0:
            left_spaces = int(length_diff / 2)
            right_spaces = length_diff - left_spaces
        else:
            left_spaces = 0; right_spaces = 0

        return f"-{left_spaces * empty_space}{str_result}{right_spaces * empty_space}-"