import pandas as pd
import tensorflow as tf


df = pd.read_csv('NBAStatsFinalcsv.csv')

del df['index']

Hawks = df.loc[df['Team'] == 'Hawks']
Celtics = df.loc[df['Team'] == 'Celtics']
Nets = df.loc[df['Team'] == 'Nets']
Hornets = df.loc[df['Team'] == 'Hornets']
Bulls = df.loc[df['Team'] == 'Bulls']
Cavaliers = df.loc[df['Team'] == 'Cavaliers']
Mavericks = df.loc[df['Team'] == 'Mavericks']
Nuggets = df.loc[df['Team'] == 'Nuggets']
Pistons = df.loc[df['Team'] == 'Pistons']
Warriors = df.loc[df['Team'] == 'Warriors']
Rockets = df.loc[df['Team'] == 'Rockets']
Pacers = df.loc[df['Team'] == 'Pacers']
Clippers = df.loc[df['Team'] == 'Clippers']
Lakers = df.loc[df['Team'] == 'Lakers']
Grizzlies = df.loc[df['Team'] == 'Grizzlies']
Heat = df.loc[df['Team'] == 'Heat']
Bucks = df.loc[df['Team'] == 'Bucks']
Timberwolves = df.loc[df['Team'] == 'Timberwolves']
Pelicans = df.loc[df['Team'] == 'Pelicans']
Knicks = df.loc[df['Team'] == 'Knicks']
Thunder = df.loc[df['Team'] == 'Thunder']
Magic = df.loc[df['Team'] == 'Magic']
A76ers = df.loc[df['Team'] == '76ers']
Suns = df.loc[df['Team'] == 'Suns']
Trail_Blazers = df.loc[df['Team'] == 'Trail Blazers']
Kings = df.loc[df['Team'] == 'Kings']
Spurs = df.loc[df['Team'] == 'Spurs']
Raptors = df.loc[df['Team'] == 'Raptors']
Jazz = df.loc[df['Team'] == 'Jazz']
Wizards = df.loc[df['Team'] == 'Wizards']

#print(Hawks, Celtics,Nets, Hornets, Bulls, Cavaliers, Mavericks, Nuggets, Pistons, Warriors, Rockets, Pacers, Clippers, Lakers, Grizzlies, Heat, Bucks, Timberwolves, Pelicans, Knicks, Thunder, Magic, A76ers, Suns, Trail_Blazers, Kings, Spurs, Raptors, Jazz, Wizards)

