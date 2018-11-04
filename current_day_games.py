# Define todays date and run the code to populate the data base.

TODAYS_DATE = "2018-09-22"

############################################################################################3

from firebase import firebase

# input: date "YYYY-MM-DD"
def games_today(date):
    f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)

    games = f.get('Group/SchedulesBySeason/', None)
    for game in games:
        getString = 'Group/SchedulesBySeason/' + game
        gameDate = f.get(getString, "Day time")

        try:
            if gameDate[0:10] == date:
                HomeName = f.get('Group/SchedulesBySeason/' + game , "Home Team ID")
                AwayName = f.get('Group/SchedulesBySeason/' + game, "Away Team ID")
                pushString = HomeName + " vs. " + AwayName # ex. 'ARZST vs. WASH'

                f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)
                f.patch("TodaysGame/", {game : pushString})
        except: 
            print("Skipped missing piece of data")
    return 0

# For populating database:
games_today(TODAYS_DATE)
