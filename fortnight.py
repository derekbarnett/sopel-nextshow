"""
fortnight.py - Is it kpo or /dev/random's week
Author: Delwin
Licensed under the Eiffel Forum License 2

More info:
 * Sopel: https://github.com/sopel-irc
 * Jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/

This module checks whether it's an odd or even week
and displays which show is recording that weekend.
"""

import datetime, re
from sopel.module import commands, example

@commands('fortnight','f')
@example('.f YYYY/MM/DD, or simply .f to see if it is a KPO or /dev/random weekend')

def fortnight(sopel, input):
    """Is this a week for KPO or /dev/random?"""
    #if there's no argument given, check this week. if there is an argument,
    #see if it's a valid date string and calculate at that date
    check = input.group(2)

    if not check:
        weeknum = datetime.date.today().isocalendar()[1]
    else:
        gooddate = re.search('\/', check)
        if not gooddate:
            return sopel.reply("Please enter '.f YYYY/MM/DD' to check against a specific date.")
        if gooddate:
            parts = check.split("/")
            y, m, d = 0, 0, 0
            if len(parts) == 3:
                y, m, d = parts
                try:
                    y = int(y)
                    m = int(m)
                    d = int(d)
                except:
                    return sopel.reply("One of your date fields is mangled.")

                try:
                    weeknum = datetime.date(y,m,d).isocalendar()[1]
                except:
                    return sopel.reply("Something was off about the date you entered. I expect it in YYYY/MM/DD format.")

            else:
                return sopel.reply("Please enter the date in YYYY/MM/DD format.")


    #sopel.reply("Checking date now.")
    result = weeknum % 2
    #this was writtin in 2013, when KPO recorded on even weeks. If using this
    #in an odd week year, change the line below to read 'if result == 1:
    if result == 0:
        iresult = "KPO"
    else:
        iresult = "/dev/random"

    sopel.reply("It is " + iresult + "\'s weekend.")
#@fortnight.commands = ['fortnight', 'f']
#@fortnight.example = '.f YYYY/MM/DD, or simply .f to see if it is a KPO or /dev/random weekend'


if __name__ == '__main__':
    print(__doc__.strip())
