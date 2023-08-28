# Static class containing methods involved in string management.
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

    # Centers string based on max length, returns a centered string.
    async def center_string(string: str, max_length: int) -> str:
        empty_space = " "
        str_length = len(string)

        if string.endswith("\u200B"):
            string = string[:-1]
            max_length -= 2

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

# Static class containing a progress bar method.
class Bar():
    # Returns a progress bar in string format based on percentage value of actual value to max value. 
    async def get_bar(act_val, max_val) -> str:
        bar_val = max_val / 20
        bars = round(act_val / bar_val)
        bar_GUI = ["....................", 
                   "I...................", "II..................", "III.................", "IIII................", "IIIII...............",
                   "IIIIII..............", "IIIIIII.............", "IIIIIIII............", "IIIIIIIII...........", "IIIIIIIIII..........",
                   "IIIIIIIIIII.........", "IIIIIIIIIIII........", "IIIIIIIIIIIII.......", "IIIIIIIIIIIIII......", "IIIIIIIIIIIIIII.....",
                   "IIIIIIIIIIIIIIII....", "IIIIIIIIIIIIIIIII...", "IIIIIIIIIIIIIIIIII..", "IIIIIIIIIIIIIIIIIII.", "IIIIIIIIIIIIIIIIIIII"]

        if bars <= 0: ret_bars = bar_GUI[0]
        elif bars == 1: ret_bars = bar_GUI[1]
        elif bars == 2: ret_bars = bar_GUI[2]
        elif bars == 3: ret_bars = bar_GUI[3]
        elif bars == 4: ret_bars = bar_GUI[4]
        elif bars == 5: ret_bars = bar_GUI[5]
        elif bars == 6: ret_bars = bar_GUI[6]
        elif bars == 7: ret_bars = bar_GUI[7]
        elif bars == 8: ret_bars = bar_GUI[8]
        elif bars == 9: ret_bars = bar_GUI[9]
        elif bars == 10: ret_bars = bar_GUI[10]
        elif bars == 11: ret_bars = bar_GUI[11]
        elif bars == 12: ret_bars = bar_GUI[12]
        elif bars == 13: ret_bars = bar_GUI[13]
        elif bars == 14: ret_bars = bar_GUI[14]
        elif bars == 15: ret_bars = bar_GUI[15]
        elif bars == 16: ret_bars = bar_GUI[16]
        elif bars == 17: ret_bars = bar_GUI[17]
        elif bars == 18: ret_bars = bar_GUI[18]
        elif bars == 19: ret_bars = bar_GUI[19]
        else: ret_bars = bar_GUI[20]

        return ret_bars