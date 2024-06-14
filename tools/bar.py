class Bar():
    async def get_bar(act_val: int, max_val: int) -> str:
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