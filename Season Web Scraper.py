import requests
import numpy as np
import pandas as pd

OCT = [str(x + 1) for x in range(20181015, 20181031)]  # Counts all games in October
NOV = [str(x + 1) for x in range(20181100, 20181130)]   # Counts all games in November
DEC1 = [str(x + 1) for x in range(20181200, 20181223)]  # Counts all games in December
# No game on December 24th
DEC2 = [str(x + 1) for x in range(20181225, 20181231)]  # Counts all games in December
JAN = [str(x + 1) for x in range(20190100, 20190131)]   # Counts all games in January
FEB = [str(x + 1) for x in range(20190200, 20190212)]   # Counts all games in February

months = OCT + NOV + DEC1 + DEC2 + JAN + FEB    # Adds all the months to make the season
OG_url = 'http://www.espn.com/nba/scoreboard/_/date/'  # The base url that will be edited for each day
all_urls = [OG_url + months[i] for i, x in enumerate(months)]  # Creates a list of all the urls for the season

all_teams = ['Hawks',
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

team_names_list = []    # List of teams played on a day

matchup_points_list = []    # List of match up points on a day

point_total = []    # List of total points scored for a matchup on a day

point_differential = []    # List of point differential for each team on a day


def find_teams(doc):    # Function that finds team names
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


def find_points(doc):   # Function that finds the points each team scored
    keyword = doc.find(
        '"name":"freeThrowsMade","abbreviation":"FTM"},{"displayValue":')  # Find the points in the source code
    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Start of the points
        end = start + 100  # Estimates the end of the points
        terminate = doc.find('</head>')  # Ends the search

        point_string = doc[start:end]  # Variable for the points
        point_list = point_string.split(',')  # Creates the list of html text
        points = point_list[2].strip('{"displayValue":"')  # Takes strips the not needed text
        matchup_points_list.append(int(points))
        # print(points)
        if end < terminate:  # Reruns function
            find_points(doc[end:])


def complete_list():  # Function that creats a complete list of the season
    for url in all_urls:
        r = requests.get(url)
        html = r.text
        find_teams(html)
        find_points(html)

complete_list()


team_names = np.asarray(team_names_list)    # Turns list into array
matchup_points = np.asarray(matchup_points_list)    # Turns list into array
home_point = matchup_points[::2]    # Organizes the array correctly
away_point = matchup_points[1::2]   # Organizes the array correctly
point_differential_home = home_point - away_point   # Creates point differential for home teams
point_differential_away = away_point - home_point   # Creates point differential for away teams
point_differential = np.empty((point_differential_home.size + point_differential_away.size,),
                              dtype=point_differential_home.dtype)
point_differential[0::2] = point_differential_home  # Combines the point differential arrays
point_differential[1::2] = point_differential_away  # Combines the point differential arrays
point_total_first = home_point + away_point     # Creates the  point total
point_total = np.empty((point_total_first.size + point_total_first.size), dtype=point_total_first.dtype)
point_total[0::2] = point_total_first
point_total[1::2] = point_total_first
points_allowed = point_total - matchup_points   # Creates the points allowed

data = {'Team': team_names, 'Points Scored': matchup_points, 'Points Allowed': points_allowed,
        'Total Points': point_total, 'Point Differential': point_differential}      # Organizes the data needed

df = pd.DataFrame(data)     # Creates the data frame

print(df)
