import pandas as pd

class MarketValue:
    def __init__(self, salary, contract, played, won):
        self.salary = salary
        self.contract = contract
        self.played = played
        self.won = won

    def winRate(self):
        self.rate = float(self.won/self.played)
        return str(self.rate * 100) + '%'

    def calculateMarketValue(self):
        self.marketValue = self.salary * self.contract * self.rate
        return str(int(self.marketValue)) + 'k'

    def updateWinRate(self, result):
        if result == 'W':
            self.won += 1
        else: 
            self.won = self.won
        self.played += 1
        
    
    def print(self):
        return 'Salary per week: ' + str(self.salary)



df = pd.read_csv('systems_development_project8/Football_players.csv')


for index, row in df.iterrows():
    #print(row.values)
    player = MarketValue(row['SALARY'], row['CONTRACT DURATION'], row['GAMES PLAYED THIS YEAR '], row['GAMES WON'])
    winPercentage = player.winRate()
    mv = player.calculateMarketValue()
    #print('Win Rate and Market Value before : ',winPercentage, mv)
    results = [row['FG1'], row['FG2'], row['FG3'], row['FG4'], row['FG5']]
    count = 0
    for i in results:
        player.updateWinRate(i)
        count += 1
        print('Win Rate and Market Value after game ', count, player.winRate(), player.calculateMarketValue())     
