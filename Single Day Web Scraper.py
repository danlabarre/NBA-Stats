import requests
import numpy as np
import pandas as pd

url = 'http://www.espn.com/nba/scoreboard/_/date/20190211'

r = requests.get(url)

teams = ['Hawks',
         'Celtics',
         'Nets',
         'Bobcats',
         'Bulls',
         'Cavaliers',
         'Mavericks',
         'Nuggets',
         'Pistons',
         'Warriors',
         'Rockets',
         'Pacers',
         'Clippers',
         'Lakers',
         'Grizzlies',
         'Heat',
         'Bucks',
         'Timberwolves',
         'Hornets',
         'Knicks',
         'Thunder',
         'Magic',
         'Sixers',
         'Suns',
         'Trail Blazers',
         'Kings',
         'Spurs',
         'Raptors',
         'Jazz',
         'Wizards']

html_doc = r.text

team_names_list = []

matchup_points_list = []


def find_teams(doc):
    keyword = doc.find(':true,"shortDisplayName":')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword + 24  # Finds the start of the team name
        end = start + 50  # Estimates the end of the team name
        terminate = doc.find('</head>')  # Ends the search

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split(',')  # Creates the list of the taken html text
        teams = name_list[0].strip(':"')  # Takes strips the not needed text
        team_names_list.append(teams)  # Adds team names to a list
        # print(teams)
        if end < terminate:  # Reruns function
            find_teams(doc[end:])


find_teams(html_doc)  # Runs find_teams for the html link

team_names = np.asarray(team_names_list)  # Converts the list into an array

#print(team_names)


def find_points(doc):
    keyword = doc.find(
        '"name":"freeThrowsMade","abbreviation":"FTM"},{"displayValue":')  # Find the points in the source code
    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Start of the points
        end = start + 100  # Estimates the end of the points
        terminate = doc.find('</head>')  # Ends the search

        point_string = doc[start:end]  # Variable for the points
        point_list = point_string.split(',')  # Creates the list of html text
        points = point_list[2].strip('{"displayValue":"')  # Takes strips the not needed text
        matchup_points_list.append(int(points))  # Adds the points to a list
        # print(points)
        if end < terminate:  # Reruns function
            find_points(doc[end:])


find_points(html_doc)  # Runs find_points for the html link

matchup_points = np.asarray(matchup_points_list)  # Converts the list into an array
#print(matchup_points)

home_point = matchup_points[::2]
away_point = matchup_points[1::2]
point_differential_home = home_point - away_point
point_differential_away = away_point - home_point

point_differential = np.empty((point_differential_home.size + point_differential_away.size,),
                              dtype=point_differential_home.dtype)
point_differential[0::2] = point_differential_home
point_differential[1::2] = point_differential_away

point_total_first = home_point + away_point
point_total = np.empty((point_total_first.size + point_total_first.size), dtype=point_total_first.dtype)
point_total[0::2] = point_total_first
point_total[1::2] = point_total_first
#print(point_total)
#np.array(point_total).tolist()

#print(point_differential)
#np.array(point_differential).tolist()

data = {'Team': team_names, 'Points Scored': matchup_points,
        'Total Points': point_total, 'Point Differential': point_differential}

df = pd.DataFrame(data)

print(df)