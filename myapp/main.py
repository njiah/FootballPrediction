import pandas as pd
from calendar import day_abbr, month
from optparse import check_builtin
from re import U
from tabnanny import check
#from time import clock_getres, strftime
from unicodedata import name
#from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from datetime import date, datetime, timedelta


from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash
import pandas as pd


app = Flask(__name__)
app.secret_key = 'Toasted Bun'

# /////////////////////////
# Main pages


@app.route('/')
def index():
    if session.get('df') is not None:
        return render_template('home.html', uploaded=True)
    else:
        session.clear()
        return render_template('home.html')
    
@app.route('/clear')
def clear():
    session.clear()
    return render_template('home.html', uploaded=False)








@app.route('/tables')
def tables():
    if session.get('df') is not None:
        
        dict=session['df']
        df = pd.DataFrame(dict)
        return render_template('tables.html', df=df)
    else:
        flash("Please upload CSV file.")
        return render_template('home.html')

@app.route('/profiles/<playername>')
def profiles(playername):
    dict = session['df']
    df = pd.DataFrame(dict)
    for index, row in df.iterrows():
        if row['PLAYER NAME'] == str(playername):
            playerInfo = row
            print(playerInfo)
    return render_template('profiles.html', playername=playername, playerInfo = playerInfo)



# /////////////////////////
# Functions & Classes


@app.route('/sort_win', methods=['GET', 'POST'])
def sort_win():
           
    dict=session['df']
    df = pd.DataFrame(dict)
    df.sort_values(by=['Win Percentage'], ascending=False, inplace=True)
    cols=session['cols']
    df = df[cols]
    return render_template('tables.html', df=df)
    

@app.route('/sort_value', methods=['GET', 'POST'])
def sort_value():
            
    dict=session['df']
    df = pd.DataFrame(dict)
    df.sort_values(by=['FG5 Value'], ascending=False, inplace=True)
    cols=session['cols']
    df = df[cols]
    return render_template('tables.html', df=df)
    



@app.route('/', methods=['GET', 'POST'])
def upload():
    

    if request.method=="POST":
        
        #df = dataframe
        df = pd.read_csv(request.files['fileSelect'], encoding='ISO-8859-1')
        df.encoding='ISO-8859-1'

        print(df.columns)
        win_percentage = df['GAMES WON'] / df['GAMES PLAYED THIS YEAR '] * 100

        # The CURRENT transfer value is multiplied by the current weekly salary x weeks left in the current contract x win percentage rate.
        current_value = (df['SALARY'] * df['CONTRACT DURATION'] * df['GAMES WON'] / df['GAMES PLAYED THIS YEAR '])
        df['Current Value']=round(current_value, 2)
        
        df['Win Percentage']=round(win_percentage, 2)
        print(round(win_percentage, 2))


        def calculate(game):
            df[game+' Value']=''

            for i in df.index:
                games_played=0
                games_won=0
                fg_number=int(game.split('G')[1])
                
                for j in range (fg_number, 0, -1):
                    games_played+=1
                    if df.loc[i, 'FG'+str(j)]=='W':
                        games_won+=1
                        
                    new_win_percentage=(df['GAMES WON'] + games_won) / (df['GAMES PLAYED THIS YEAR '] + games_played) * 100
                    new_value=(df.loc[i, 'SALARY'] * df.loc[i, 'CONTRACT DURATION'] * (df['GAMES WON'] + games_won) / (df['GAMES PLAYED THIS YEAR '] + games_played))
                    df.loc[i, [game+' Value']] = [round(new_value, 2)[i]]
                    df.loc[i, ['Win Rate after ' + game]] = [round(new_win_percentage, 2)[i]]

                    
                      
        calculate('FG1')
        calculate('FG2')
        calculate('FG3')
        calculate('FG4')
        calculate('FG5')

        
        # dict = df.to_dict();
        
        dictionaryObject = df.to_dict()
        session['df']=dictionaryObject
        cols = list(df.columns.values)
        session['cols']=cols

        result = df.to_html()
        
        return render_template('tables.html', df=df, uploaded=True)
    else:
        return render_template('home.html')
    
def store_dataframe(df):
    df = df
    return url_for ("home.html")
   
    

class Player:
    def __init__(self, playerName, salary, contract, played, won):
        self.playerName = playerName
        self.salary = salary
        self.contract = contract
        self.played = played
        self.won = won

    def __str__(self):
        return f"Player Name: {self.playerName} | Player Salary: £{self.salary }k/pw | Player Contract Length: {self.contract} | Matches Played: {self.played} | Matches Won: {self.won} | Market Value: {str(self.calculateMarketValue())}"

    def winRate(self):
        self.rate = float(self.won/self.played)
        return self.rate * 100

    def calculateMarketValue(self):
        self.marketValue = self.salary * self.contract * self.winRate()
        return '£' + str(int(self.marketValue))

    def updateWinRate(self, result):
        if result == 'W':
            self.won += 1
        else: 
            self.won = self.won
        self.played += 1

    
    






    
    
    
    

# /////////////////////////
# app.run (MUST STAY AT BOTTOM OF PAGE)

if __name__ == '__main__':
    for i in range(13000, 18000):
      try:
         app.run(debug = True, port = i)
         break
      except OSError as e:
         print("Port {i} not available".format(i))
