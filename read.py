import csv
with open('PROJECT/systems_development_project8/players.csv', newline='', encoding='ISO-8859-1') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)


import pandas as pd
#df = dataframe
df = pd.read_csv('PROJECT/systems_development_project8/players.csv', encoding ='ISO-8859-1')
win_percentage = df['GAMES WON'] / df['GAMES PLAYED THIS YEAR '] * 100

# The CURRENT transfer value is multiplied by the current weekly salary x weeks left in the current contract x win percentage rate.
current_value = (df['SALARY (ï¿½k/Week)'] * df['CONTRACT DURATION'] * win_percentage)
df['Current Value']=current_value
df['Win Percentage']=win_percentage
print(df)

def game_win_percentage(game):
    df[game+'value']=''
    for i in df.index:
        print(df)
        if df.loc[i, game]=='W':

            new_win_percentage=(df['GAMES WON'] + 1) / df['GAMES PLAYED THIS YEAR '] * 100
            new_value=(df.loc[i, 'SALARY (ï¿½k/Week)'] * df.loc[i, 'CONTRACT DURATION'] * new_win_percentage)
            df.loc[i, [game+'value']] = [new_value[i]]
game_win_percentage('FG1')
print(df)
