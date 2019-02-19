import requests
import numpy as np
import pandas as pd
import sqlite3 as sql
import sqlalchemy as alc

OG_url = 'http://www.espn.com/nba/matchup?gameId='

games1 = [str(x + 1) for x in range(401070212, 401070223)]
games2 = [str(x + 1) for x in range(401070692, 401071177)]
games3 = [str(x + 1) for x in range(401070232, 401070237)]
games4 = [str(x + 1) for x in range(401071177, 401071374)]
games5 = [str(x + 1) for x in range(401070237, 401070240)]
games6 = [str(x + 1) for x in range(401071374, 401071539)]
all_games = games1 + games2 + games3 + games4 + games5 + games6
all_urls = [OG_url + all_games[i] for i, x in enumerate(all_games)]

team_names_list = []  # List of teams played on a day

score_list = []

opp_score_list = []

fieldgoal_percentage_list = []  # List of match up points on a day

fieldgoal3_percentage_list = []  # List of total points scored for a matchup on a day

fieldgoalft_percentage_list = []  # List of point differential for each team on a day

rebounds_list = []

off_rebounds_list = []

assists_list = []

steals_list = []

blocks_list = []

turnovers_list = []

fastbreak_list = []

pointsinpaint_list = []

foul_list = []


def find_teams(doc):  # Function that finds team names
    keyword = doc.find('<title>')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword + 7  # Finds the start of the team name
        end = start + 40  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split(' ')  # Creates the list of the taken html text
        team1 = name_list[2]  # Takes strips the not needed text
        team2 = name_list[0]
        team_names_list.append(team1)
        team_names_list.append(team2)  # Adds team names to a list


def find_score(doc):
    keyword = doc.find('td class="final-score">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword + 23  # Finds the start of the team name
        end = start + 3  # Estimates the end of the team name
        terminate = doc.find(
            '</td></tr></tbody></table></div></div><div class="team home"><div class="team__content"><div class="team__banner"')  # Ends the search

        score = doc[start:end]  # Variable for the teams names
        # name_list = name.split(',')  # Creates the list of the taken html text
        scores = score.strip('<')  # Takes strips the not needed text
        score_list.append(scores)  # Adds team names to a list
        opp_score_list.append(scores)
        # print(teams)
        if end < terminate:  # Reruns function
            find_score(doc[end:])


def find_FG_per(doc):  # Function that finds team names
    keyword = doc.find('Field Goal %')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword + 137  # Finds the start of the team name
        end = start + 30  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('"')  # Creates the list of the taken html text
        fgp1 = name_list[0]  # Takes strips the not needed text
        fgp2 = name_list[2]
        fieldgoal_percentage_list.append(float(fgp1))
        fieldgoal_percentage_list.append(float(fgp2))  # Adds team names to a list


def find_3FG_per(doc):  # Function that finds team names
    keyword = doc.find('Three Point %')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword + 138  # Finds the start of the team name
        end = start + 30  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('"')  # Creates the list of the taken html text
        fg3p1 = name_list[0]  # Takes strips the not needed text
        fg3p2 = name_list[2]
        fieldgoal3_percentage_list.append(float(fg3p1))
        fieldgoal3_percentage_list.append(float(fg3p2))  # Adds team names to a list


def find_ft_per(doc):  # Function that finds team names
    keyword = doc.find('<tr class="highlight" data-stat-attr="freeThrowPct">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        ftp1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        ftp2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        fieldgoalft_percentage_list.append(float(ftp1))
        fieldgoalft_percentage_list.append(float(ftp2))  # Adds team names to a list


def find_rebounds(doc):  # Function that finds team names
    keyword = doc.find('rebounds"><h3>Rebounds')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword + 147  # Finds the start of the team name
        end = start + 30  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('"')  # Creates the list of the taken html text
        rbs1 = name_list[0]  # Takes strips the not needed text
        rbs2 = name_list[2]
        rebounds_list.append(int(rbs1))
        rebounds_list.append(int(rbs2))  # Adds team names to a list


def find_off_rebounds(doc):  # Function that finds team names
    keyword = doc.find(
        '<tr class="indent" data-stat-attr="offensiveRebounds">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        orbs1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        orbs2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        off_rebounds_list.append(int(orbs1))
        off_rebounds_list.append(int(orbs2))  # Adds team names to a list


def find_assists(doc):  # Function that finds team names
    keyword = doc.find('<tr class="highlight" data-stat-attr="assists">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        ast1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        ast2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        assists_list.append(int(ast1))
        assists_list.append(int(ast2))  # Adds team names to a list


def find_steals(doc):  # Function that finds team names
    keyword = doc.find('<tr class="highlight" data-stat-attr="steals">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        stl1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        stl2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        steals_list.append(int(stl1))
        steals_list.append(int(stl2))  # Adds team names to a list


def find_blocks(doc):  # Function that finds team names
    keyword = doc.find('<tr class="highlight" data-stat-attr="blocks">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        blk1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        blk2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        blocks_list.append(int(blk1))
        blocks_list.append(int(blk2))  # Adds team names to a list


def find_turnovers(doc):  # Function that finds team names
    keyword = doc.find(
        '<tr class="highlight" data-stat-attr="totalTurnovers">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        to1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        to2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        turnovers_list.append(int(to1))
        turnovers_list.append(int(to2))  # Adds team names to a list


def find_fastbreak(doc):  # Function that finds team names
    keyword = doc.find(
        '<tr class="highlight" data-stat-attr="fastBreakPoints">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        fb1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        fb2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        fastbreak_list.append(int(fb1))
        fastbreak_list.append(int(fb2))  # Adds team names to a list


def find_paint(doc):  # Function that finds team names
    keyword = doc.find('<tr class="highlight" data-stat-attr="pointsInPaint">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        pt1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        pt2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        pointsinpaint_list.append(int(pt1))
        pointsinpaint_list.append(int(pt2))  # Adds team names to a list


def find_fouls(doc):  # Function that finds team names
    keyword = doc.find('<tr class="highlight" data-stat-attr="fouls">')  # Find the match ups in the source code

    if keyword != -1:  # Ends function if no more teams exists
        start = keyword  # Finds the start of the team name
        end = start + 400  # Estimates the end of the team name

        name = doc[start:end]  # Variable for the teams names
        name_list = name.split('td>')  # Creates the list of the taken html text
        fl1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')  # Takes strips the not needed text
        fl2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        foul_list.append(int(fl1))
        foul_list.append(int(fl2))  # Adds team names to a list


def complete_list():
    for url in all_urls:
        r = requests.get(url)
        html = r.text
        find_teams(html)
        find_score(html)
        find_FG_per(html)
        find_3FG_per(html)
        find_ft_per(html)
        find_rebounds(html)
        find_off_rebounds(html)
        find_assists(html)
        find_steals(html)
        find_blocks(html)
        find_turnovers(html)
        find_fastbreak(html)
        find_paint(html)
        find_fouls(html)


complete_list()

team_names = np.asarray(team_names_list)  # Converts the list into an array
scores1_list = score_list[::2]
scores2_list = score_list[1::2]
scores1 = np.asarray(scores1_list)
scores2 = np.asarray(scores2_list)
opp_score = np.asarray(opp_score_list)
fg_per = np.asarray(fieldgoal_percentage_list)
fg3_per = np.asarray(fieldgoal3_percentage_list)
ft_per = np.asarray(fieldgoalft_percentage_list)
rbs = np.asarray(rebounds_list)
off_reb = np.asarray(off_rebounds_list)
ast = np.asarray(assists_list)
steals = np.asarray(steals_list)
blocks = np.asarray(blocks_list)
turnovers = np.asarray(turnovers_list)
fastbreak = np.asarray(fastbreak_list)
paint = np.asarray(pointsinpaint_list)
fouls = np.asarray(foul_list)

point_allowed = np.empty((scores1.size + scores2.size,), dtype=scores1.dtype)
point_allowed[0::2] = scores2
point_allowed[1::2] = scores1

data = {"Team": team_names, "Points Scored": point_allowed, "Points Allowed": opp_score, "FG%": fg_per, "3p FG%": fg3_per,
        "Ft%": ft_per, 'Rebounds': rbs, "Offensive Rebounds": off_reb, "Assists": ast, "Steals": steals,
        "Blocks": blocks, "Turnovers:": turnovers, "Fastbreak Points": fastbreak, "Points in Paint": paint,
        "Fouls": fouls}

df = pd.DataFrame(data)  # Creates the data frame

print(df)

db = '2018-2019_NBA_Stats_Database'


def make_db():  # Downloads the database to import into mysql
    name = 'NBA_2018-2019'
    con = sql.connect(db)
    df.to_sql(name, con)


make_db()
