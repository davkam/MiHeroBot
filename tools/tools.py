import re

class Bar():
    async def get_shortbar(act_val: int, max_val: int) -> str:
        """
        Return progress bar in string format based on percentage value of actual value to max value.
        """

        bar_val = max_val / 10
        bars = int(act_val / bar_val)
        bar_GUI = ["..........", 
                   "|.........", "||........", "|||.......", "||||......", "|||||.....",
                   "||||||....", "|||||||...", "||||||||..", "|||||||||.", "||||||||||",]

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
        else: ret_bars = bar_GUI[10]

        return ret_bars
    
    async def get_longbar(act_val: int, max_val: int) -> str:
        bar_val = max_val / 20
        bars = int(act_val / bar_val)
        bar_GUI = ["....................", 
                   "|...................", "||..................", "|||.................", "||||................", "|||||...............",
                   "||||||..............", "|||||||.............", "||||||||............", "|||||||||...........", "||||||||||..........",
                   "|||||||||||.........", "||||||||||||........", "|||||||||||||.......", "||||||||||||||......", "|||||||||||||||.....",
                   "||||||||||||||||....", "|||||||||||||||||...", "||||||||||||||||||..", "|||||||||||||||||||.", "||||||||||||||||||||"]

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
    
class StringManager():
    async def remove_special_characters(input_string: str) -> str:
        # Define a regular expression pattern for special characters
        # Keep only alphabetic characters and spaces
        pattern = r'[^a-zA-Z\s]'  

        # Substitute special characters with an empty string
        cleaned_string = re.sub(pattern, '', input_string)

        return cleaned_string