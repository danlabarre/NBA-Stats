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

team_names_list = []  # Lists of all the data from each day

score_list = []

opp_score_list = []

fieldgoal_percentage_list = []

fieldgoal3_percentage_list = []

fieldgoalft_percentage_list = []

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


def find_score(doc):    # Function that finds score
    keyword = doc.find('td class="final-score">')

    if keyword != -1:
        start = keyword + 23
        end = start + 3
        terminate = doc.find(
            '</td></tr></tbody></table></div></div><div class="team home"><div class="team__content"><div class="team__banner"')

        score = doc[start:end]
        # name_list = name.split(',')
        scores = score.strip('<')
        score_list.append(scores)
        opp_score_list.append(scores)
        # print(teams)
        if end < terminate:
            find_score(doc[end:])


def find_FG_per(doc):  # Function that finds FG%
    keyword = doc.find('Field Goal %')

    if keyword != -1:
        start = keyword + 137
        end = start + 30

        name = doc[start:end]
        name_list = name.split('"')
        fgp1 = name_list[0]
        fgp2 = name_list[2]
        fieldgoal_percentage_list.append(float(fgp1))
        fieldgoal_percentage_list.append(float(fgp2))


def find_3FG_per(doc):  # Function that finds 3 point FG%
    keyword = doc.find('Three Point %')

    if keyword != -1:
        start = keyword + 138
        end = start + 30

        name = doc[start:end]
        name_list = name.split('"')
        fg3p1 = name_list[0]
        fg3p2 = name_list[2]
        fieldgoal3_percentage_list.append(float(fg3p1))
        fieldgoal3_percentage_list.append(float(fg3p2))


def find_ft_per(doc):  # Function that finds free throw %
    keyword = doc.find('<tr class="highlight" data-stat-attr="freeThrowPct">')  # Find the match ups in the source code

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        ftp1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        ftp2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        fieldgoalft_percentage_list.append(float(ftp1))
        fieldgoalft_percentage_list.append(float(ftp2))


def find_rebounds(doc):  # Function that finds rebounds
    keyword = doc.find('rebounds"><h3>Rebounds')

    if keyword != -1:
        start = keyword + 147
        end = start + 30

        name = doc[start:end]
        name_list = name.split('"')
        rbs1 = name_list[0]
        rbs2 = name_list[2]
        rebounds_list.append(int(rbs1))
        rebounds_list.append(int(rbs2))


def find_off_rebounds(doc):  # Function that finds offensive rebounds
    keyword = doc.find(
        '<tr class="indent" data-stat-attr="offensiveRebounds">')

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        orbs1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        orbs2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        off_rebounds_list.append(int(orbs1))
        off_rebounds_list.append(int(orbs2))


def find_assists(doc):  # Function that finds assists
    keyword = doc.find('<tr class="highlight" data-stat-attr="assists">')  # Find the match ups in the source code

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        ast1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        ast2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        assists_list.append(int(ast1))
        assists_list.append(int(ast2))


def find_steals(doc):  # Function that finds steals
    keyword = doc.find('<tr class="highlight" data-stat-attr="steals">')

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        stl1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        stl2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        steals_list.append(int(stl1))
        steals_list.append(int(stl2))


def find_blocks(doc):  # Function that finds blocks
    keyword = doc.find('<tr class="highlight" data-stat-attr="blocks">')

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        blk1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        blk2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        blocks_list.append(int(blk1))
        blocks_list.append(int(blk2))


def find_turnovers(doc):  # Function that finds turnovers
    keyword = doc.find(
        '<tr class="highlight" data-stat-attr="totalTurnovers">')

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        to1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        to2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        turnovers_list.append(int(to1))
        turnovers_list.append(int(to2))


def find_fastbreak(doc):  # Function that finds fastbreak points
    keyword = doc.find(
        '<tr class="highlight" data-stat-attr="fastBreakPoints">')

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        fb1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        fb2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        fastbreak_list.append(int(fb1))
        fastbreak_list.append(int(fb2))


def find_paint(doc):  # Function that finds points in the paint
    keyword = doc.find('<tr class="highlight" data-stat-attr="pointsInPaint">')

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        pt1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        pt2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        pointsinpaint_list.append(int(pt1))
        pointsinpaint_list.append(int(pt2))


def find_fouls(doc):  # Function that finds fouls
    keyword = doc.find('<tr class="highlight" data-stat-attr="fouls">')

    if keyword != -1:
        start = keyword
        end = start + 400

        name = doc[start:end]
        name_list = name.split('td>')
        fl1 = name_list[5].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        fl2 = name_list[3].strip('\n\t\t\t\t\t\t\t\t\t, \n\t\t\t\t\t\t\t\t</')
        foul_list.append(int(fl1))
        foul_list.append(int(fl2))


def complete_list(): # Function that runs all the other functions to create the lists
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
scores1_list = score_list[::2]  # Manipulates the scores list to be used to find point points allowed
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

point_allowed = np.empty((scores1.size + scores2.size,), dtype=scores1.dtype)   # Creates the points allowed array
point_allowed[0::2] = scores2
point_allowed[1::2] = scores1

data = {"Team": team_names, "Points Scored": point_allowed, "Points Allowed": opp_score, "FG%": fg_per, "3p FG%": fg3_per,
        "Ft%": ft_per, 'Rebounds': rbs, "Offensive Rebounds": off_reb, "Assists": ast, "Steals": steals,
        "Blocks": blocks, "Turnovers:": turnovers, "Fastbreak Points": fastbreak, "Points in Paint": paint,
        "Fouls": fouls} # Puts all the arrays into columns with a header for each column

df = pd.DataFrame(data)  # Creates the data frame

print(df)

db = '2018-2019_NBA_Stats_Database'  # Names the db


def make_db():  # Downloads the database to import into mysql
    name = 'NBA_2018-2019'
    con = sql.connect(db)
    df.to_sql(name, con)


make_db()
