import http.client, urllib.request, urllib.parse, urllib.error, base64
import xml.etree.ElementTree as ET

from firebase import firebase
f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)

#define to do different type of API pull
pullDefine = 3

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '14fe141643104501a0321bf3b55b4a65',
}
params = urllib.parse.urlencode({
})

if pullDefine == 0: # Curent games happening by week (2018: week1)
    try:
        conn = http.client.HTTPSConnection('api.fantasydata.net')
        conn.request("GET", "/v3/cfb/scores/xml/GamesByWeek/2018/1?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        with open('data.xml', 'wb') as f: 
            f.write(data)
        conn.close()
    except Exception as e:
        print("error in pull define 0")

    # No xml parse, currently no games live (as of 11/03/18, 1:27am)

elif pullDefine == 1:   # Schedules by season (2018)
    try:
        conn = http.client.HTTPSConnection('api.fantasydata.net')
        conn.request("GET", "/v3/cfb/scores/xml/Games/2018?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        with open('data.xml', 'wb') as f: 
            f.write(data)
        conn.close()
    except Exception as e:
        print("error in pull define 1")


    tree = ET.parse('data.xml')
    root = tree.getroot()
    n = len(root)

    # dicionary definitions
    # gameidList = []
    # daytime = {}
    # awayteam = {}
    # hometeam = {}
    # awayteamname = {}
    # hometeamname = {}
    # awayteamscore = {}
    # hometeamscore = {}


    # for x in range (n):
    #     gameidList.append(root[x][0].text) # append gameid to list
    #     daytime[root[x][0].text] = root[x][6].text # append day time
    #     awayteam[root[x][0].text] = root[x][7].text # append away team acronym
    #     hometeam[root[x][0].text] = root[x][8].text # append home team acronym
    #     awayteamname[root[x][0].text] = root[x][11].text # append away team full name
    #     hometeamname[root[x][0].text] = root[x][12].text # append home team full name
    #     awayteamscore[root[x][0].text] = root[x][13].text # append away team score
    #     hometeamscore[root[x][0].text] = root[x][14].text # append home team score

    # For testing purposes:
    # print(awayteamname['8989'])
    # print(hometeamscore['9255'])

    # Dictionary of dictionaries
    from firebase import firebase
    f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)
    for x in range(n):
        str1 = "Group/SchedulesBySeason/" + root[x][0].text
        f.patch(str1, {"Day time": root[x][6].text, "Away Team ID": root[x][7].text, "Home Team ID": root[x][8].text, "Away Team Name": root[x][11].text, "Home Team Name": root[x][12].text, "Away Team Score": root[x][13].text, "Home Team Score":root[x][14].text})

    from firebase import firebase
    f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)

#f.patch('/game_id/8578', {'home_team': 'yo', 'away_team':'yolo', 'winner':'me'})

elif pullDefine == 2:   # Pre-Game Odds By Week
    try:
        conn = http.client.HTTPSConnection('api.fantasydata.net')
        conn.request("GET", "/v3/cfb/odds/xml/GameOddsByWeek/2018/1?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        with open('data.xml', 'wb') as f: 
            f.write(data)
        conn.close()
    except Exception as e:
        print("error in Group 2")

    tree = ET.parse('data.xml')
    root = tree.getroot()
    n = len(root)

    # dicionary definitions
    # gameidList = []
    # datetime = {}
    # awayteamid = {}
    # hometeamid = {}
    # awayteamname = {}
    # hometeamname = {}
    awaymoneyline = {}
    homemoneyline = {}
    # awaypointspread = {}
    # homepointspread = {}
    # awaypointspreadypayout = {}
    # homepointspreadpayout = {}
    # overunder = {}
    # overpayout = {}
    # underpayout = {}

    odds = {}

    from firebase import firebase
    f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)
    for x in range (n):
    #     gameidList.append(root[x][0].text) # append gameid to list
    #     datetime[root[x][0].text] = root[x][5].text # append date time
    #     awayteamid[root[x][0].text] = root[x][7].text # append away team id
    #     hometeamid[root[x][0].text] = root[x][8].text # append home team id
    #     awayteamname[root[x][0].text] = root[x][9].text # append away team name
    #     hometeamname[root[x][0].text] = root[x][10].text # append home team name
        try:
            awaymoneyline[root[x][0].text] = root[x][14][0][6].text # append away money line
            homemoneyline[root[x][0].text] = root[x][14][0][5].text # append home money line
            # awaypointspread[root[x][0].text] = root[x][14][0][9].text # append away point spread
            # homepointspread[root[x][0].text] = root[x][14][0][8].text # append home point spread
            # awaypointspreadypayout[root[x][0].text] = root[x][14][0][11].text # append away point spread payout
            # homepointspreadpayout[root[x][0].text] = root[x][14][0][10].text # append home point spread payout
            # overunder[root[x][0].text] = root[x][14][0][12].text # append over under
            # overpayout[root[x][0].text] = root[x][14][0][13].text # append over payout
            # underpayout[root[x][0].text] = root[x][14][0][14].text # append under payout

            strx = "Group/PreGameOddsByWeek/" + root[x][0].text
            f.patch(strx, {"Away Money Line" : root[x][14][0][6].text, "Home Money Line": root[x][14][0][5].text, "Away Points Spread": root[x][14][0][9].text, "Home Points Spread": root[x][14][0][8].text, "Away Point Spread Payout": root[x][14][0][11].text, "Home Point Spread Payout": root[x][14][0][10].text, "Over Under": root[x][14][0][12].text, "Over Payout": root[x][14][0][13].text, "Under Payout" : root[x][14][0][14].text})
            data_2[root[x][0].text] = {"Away Money Line" : root[x][14][0][6].text, "Home Money Line": root[x][14][0][5].text, "Away Points Spread": root[x][14][0][9].text, "Home Points Spread": root[x][14][0][8].text, "Away Point Spread Payout": root[x][14][0][11].text, "Home Point Spread Payout": root[x][14][0][10].text, "Over Under": root[x][14][0][12].text, "Over Payout": root[x][14][0][13].text, "Under Payout" : root[x][14][0][14].text}
            #use money lines to generate game odds (Home:Away)
            #place under Group == 2 section
            AML = float(awaymoneyline[root[x][0].text])
            HML = float(homemoneyline[root[x][0].text])
            if HML > 0:
                odds[root[x][0].text] = (100/(100+HML))/(100/(100+HML)-AML/(100-AML))
            elif AML > 0:
                odds[root[x][0].text] = (-HML/(100-HML))/(-HML/(100-HML)+100/(100+AML))
            else:
                pass
        except:
            print("For game %s, moneyline does not exist." % root[x][0].text)

    for key in odds:
        strx = "Group/PreGameOddsByWeek/" + key
        f.patch(strx, {"Odds": odds[key]})

    # Dictionary of dictionaries
    from firebase import firebase
    f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)
    for x in range(n):
        str2 = "Group/PreGameOddsByWeek/" + root[x][0].text
        f.patch(str2, {"Date Time":root[x][5].text, "Away Team ID" : root[x][7].text, "Home Team ID": root[x][8].text, "Away Team Name":root[x][9].text, "Home Team Name":root[x][10].text})

    


    # print(datetime["8989"])
    # print(hometeamname["8989"])

elif pullDefine == 3:   # Team Stats
    try:
        conn = http.client.HTTPSConnection('api.fantasydata.net')
        conn.request("GET", "/v3/cfb/stats/xml/Teams?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        with open('data.xml', 'wb') as f: 
            f.write(data)
        conn.close()
    except Exception as e:
        print("error in Group 3")

    tree = ET.parse('data.xml')
    root = tree.getroot()
    n = len(root)

    # dicionary definitions
    # teamidList = []
    # wins = {}
    # losses = {}
    
    # for x in range (n):
    #     teamidList.append(root[x][0].text) # append gameid to list
    #     wins[root[x][0].text] = root[x][7].text # append wins
    #     losses[root[x][0].text] = root[x][8].text # append losses

    # Dictionary of dictionaries

    from firebase import firebase
    f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)

    for x in range(n):
        str3 = "Group/TeamStats/" + root[x][0].text
        f.patch(str3, {"wins" : root[x][7].text, "losses": root[x][8].text})

    # for testing
    # print(wins["5"])
    # print(losses["5"])


elif pullDefine == 4:   # Player states by team

    from firebase import firebase
    f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)

    # iterate the teams
    try:
        conn = http.client.HTTPSConnection('api.fantasydata.net')
        conn.request("GET", "/v3/cfb/stats/xml/Teams?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        with open('data.xml', 'wb') as f: 
            f.write(data)
        conn.close()
    except:
        print("error")

    tree = ET.parse('data.xml')
    root = tree.getroot()
    n = len(root)

    from firebase import firebase
    f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)

    for x in range(n):
        location = "Group/Teams/" + root[x][1].text
        f.patch(location, {"wins" : root[x][7].text, "losses": root[x][8].text, "team name": root[x][4].text})



# # iterate through teams and add all the players
#     try:
#         conn = http.client.HTTPSConnection('api.fantasydata.net')
#         conn.request("GET", "/v3/cfb/stats/xml/Players/%s?%s" % team, params, "{body}", headers)
#         response = conn.getresponse()
#         data = response.read()
#         with open('data.xml', 'wb') as f: 
#             f.write(data)
#         conn.close()
#     except: 
#         print("error")

#     tree = ET.parse('data.xml')
#     root = tree.getroot()
#     n = len(root)

#     for x in range(n):
#         location = "Group/Teams/" + root[x][1].text
