"""
nextshow.py - Is there a show this week?
Author: Delwin
Licensed under the Eiffel Forum License 2

More info:
 * Sopel: https://github.com/sopel-irc
 * Jenni: https://github.com/myano/jenni/
 * Phenny: http://inamidst.com/phenny/

This module was created for #linuxlugcast, which
hosts a show on the first and third friday of the month.
"""

import datetime, re
from sopel.module import commands, example

#ATTENTION - change schedule to the type of schedule appropriate
#            to the event you are using this to track.
#Valid options are:
# schedule = 1 - you are tracking specific weeks of the month
#                e.g. you are looking for something on the 1st and 3rd week every month
# schedule = 2 - you are tracking something so many weeks at a time
#                e.g. you want to track every other week, regardless of month
# a default of 1 is used simply because that was the original purpose of this plugin.

schedule = 1

@commands('nextshow', 'ns')
@example('.ns YYYY/MM/DD, or simply .ns to see if there is a show on this week')

def nextshow(sopel, input):
    """When is the next show?"""
    #if there's no argument given, check this week. if there is an argument,
    #see if it's a valid date string and calculate at that date
    if not schedule == 1 and not schedule == 2:
        return sopel.reply("The type of schedule to track is not properly set.")

    #look to see if a date has been given as an argument. if so, use that
    #as the date to check against. if no argument given, use today's date
    check = input.group(2)

    if not check:
        t = datetime.date.today()
        #the generic bool allows you to easily pick between two different
        #formats of showmessage
        generic = False
    else:
        generic = True
        #ensure that the date is in the format we expect, i.e. using slashes to seperate fields
        gooddate = re.search('\/', check)
        if not gooddate:
            return sopel.reply("Please enter '.ns YYYY/MM/DD' to check against a specific date.")
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
                    t = datetime.date(y, m, d)
                except:
                    return sopel.reply("Something was off about the date you entered. I expect it in YYYY/MM/DD format.")
            else:
                return sopel.reply("Please enter the date in YYYY/MM/DD format.")

    #send the date chosen to the correct function based upon what kind of cycle you
    #are looking for
    if schedule == 1:
        showmessage = weekcheck1(sopel, t, generic)
    elif schedule == 2:
        showmessage = weekcheck2(sopel, t, generic)

    return sopel.reply(showmessage)

def weekcheck1(sopel, t, generic):
    #this section assumes that the show in question records on the
    #Friday of the first and third week of the month, schedule = 1

    noshow = True
    #t is the date to check, either today's date or a user defined date

    #today is the integer corresponding to the day of the week.
    #Monday = 0, Friday = 4, Sunday = 6
    today = t.weekday()

    #use timedelta to find out the date of the Friday in the week being checked
    daydelta = 4 - today
    frcheck = t + datetime.timedelta(days=daydelta)

    #get the date string for the showdate. we'll rewrite this later if we have to
    #look into future weeks
    showdate = frcheck.strftime("%A, %B %d, %Y")
    showmessage = "Something went wrong"

    #look for first week
    if frcheck.day >= 1 and frcheck.day <= 7:
        #if it's Saturday or Sunday, go ahead and look for the next show date
        if today == 5 or today == 6:
            noshow = True
        #if it's Friday, the show is today
        elif today == 4:
            if generic:
                showmessage = "The next show is on " + showdate
            else:
                showmessage = "The next show (first week) is TODAY, " + showdate
            return showmessage
        #if it's Monday to Thursday, let them know the show is coming this week
        else:
            if generic:
                showmessage = "The next show is on " + showdate
            else:
                showmessage = "The next show (first week) is this week, " + showdate
            return showmessage

    #look for third week
    elif frcheck.day >= 15 and frcheck.day <= 21:
        if today == 5 or today == 6:
            noshow = True
        elif today == 4:
            if generic:
                showmessage = "The next show is on " + showdate
            else:
                showmessage = "The next show (third week) is TODAY, " + showdate
            return showmessage
        else:
            if generic:
                showmessage = "The next show is on " + showdate
            else:
                showmessage = "The next show (third week) is this week, " + showdate
            return showmessage

    #if noshow, look for next date of show
    if noshow:
        while noshow:
            #add 1 week timedelta to frcheck until the friday falls in proper date range
            frcheck = frcheck + datetime.timedelta(weeks=1)
            showdate = frcheck.strftime("%A, %B %d, %Y")
            if frcheck.day >= 1 and frcheck.day <= 7:
                if generic:
                    showmessage = "The next show is on " + showdate
                else:
                    showmessage = "The next show date (first week) is " + showdate
                return showmessage
            elif frcheck.day >= 15 and frcheck.day <= 21:
                if generic:
                    showmessage = "The next show is on " + showdate
                else:
                    showmessage = "The next show date (third week) is " + showdate
                return showmessage

    return showmessage

def weekcheck2(sopel, t, generic):
    #this section is written under the assumption that the show
    #takes place on a Saturday and occurs every other week
    #schedule = 2
    #
    #note: this will likely need rejiggered after a year with
    #an odd number of weeks in it

    noshow = True
    #t is the date to check, either today's date or a user defined date

    #today is the integer corresponding to the day of the week.
    #Monday = 0, Friday = 4, Sunday = 6
    today = t.weekday()

    #use timedelta to find out the date of the Saturday in the week being checked
    daydelta = 5 - today
    frcheck = t + datetime.timedelta(days=daydelta)
    weeknum = frcheck.isocalendar()[1]

    #get the date string for the showdate. we'll rewrite this later if we have to
    #look into future weeks
    showdate = frcheck.strftime("%A, %B %d, %Y")
    showmessage = "Something went wrong"

    #if even week
    if weeknum % 2 == 0:
        #if it is Sunday, kick the can
        if today == 6:
            noshow = True
        elif today == 5:
            #ATTENTION - uncomment the code for one of these two sections below
            #section 1 doesn't care about the time, only the date
            #section 2 will allow you to set a time you expect your event will be over,
            #and fail to the next valid date if it is later than the defined end time

            #section 1
            noshow = False
            showmessage = "The next show is (or was) TODAY " + showdate
            #end section 1

            ##begin section 2
            ##this would be the place to add a check for
            ##event ending time vs. current time if desirable
            ##if 8:30 p.m. was the cutoff time:
            #if t == datetime.date.today():
                #if datetime.datetime.now().time() > datetime.time(hour=20, minute=30):
                    #noshow = True
                #else:
                    #noshow = False
                    #showmessage = "The next show will be TODAY, " + showdate
            #else:
                #noshow = False
                #showmessage = "The next show will be " + showdate
            ##end section 2

        else:
            noshow = False
            showmessage = "The next show is " + showdate

        ##if we found a show this week, return the message, else kick it down the line
        if noshow == False:
            return showmessage

    #if odd week, kick the can
    else:
        noshow = True

    #if noshow, look for next date of show
    if noshow:
        while noshow:
            #add 1 week timedelta to frcheck and check the next week
            frcheck = frcheck + datetime.timedelta(weeks=1)
            showdate = frcheck.strftime("%A, %B %d, %Y")
            weeknum = frcheck.isocalendar()[1]

            if weeknum % 2 == 0:
                showmessage = "The next show is " + showdate
                return showmessage

    return showmessage

if __name__ == "__main__":
    print (__doc__.strip())
