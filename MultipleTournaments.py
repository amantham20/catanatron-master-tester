from catanatron import Game, RandomPlayer, Color
from fortomm import PlayerE
from catanatron_core.catanatron.players.weighted_random import WeightedRandomPlayer
from collections import Counter

# import multiprocessing as mp
# import multiprocessing
# import threading
# import concurrent.futures

import csv
import logging

logging.basicConfig(filename='tournament.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

import pickle

tournament_results = []
best_players = []


# Static variables
NUMBER_OF_TOURNAMENTS = 1
NumberOfGames = 100
GENERATIONS = 50
ADDITIONALGAMES = 150


def PrintTheOrder(items: dict):
    """Prints out the players in order of their score

    :param items: Players and their scores
    """
    pos = 0
    for i in sorted(items, key=items.get, reverse=True):
        print(f"\033[1;32m  ({pos}) {i} : {items[i]} \033[00m")
        logging.info(f"  ({pos}) {i} : {items[i]}")
        pos += 1
        
def RunAgainstWeighted(players, NumberOfGames):
    """Runs a tournament against the weighted random player

    :param players: Players to be tested
    :param NumberOfGames: Number of games to be played
    """
    victory = []
    
    for __ in range(NumberOfGames):
        game = Game(players)
        val = game.play()
        victory.append(val)
    
    tempC = dict(Counter(victory))
    
    for key in tempC:
        tempC[key] = int(tempC[key] / NumberOfGames * 100)
    PrintTheOrder(tempC)

    
    
def SavePlayerScores(Scores):
    """Generates a csv file with the scores of the players

    :param Scores: Scores of the players
    """
    with open('player_scores.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Generation'] + [f'Player {i.color}' for i in players])
        for i in range(GENERATIONS):
            writer.writerow([i+1] + Scores[i])
            
            
def ComputeWinRate(Counter):
    """Computes the score of each player

    :param Counter: Couter for the wins of the players
    """
    for key in Counter:
        Counter[key] = int(Counter[key] / NumberOfGames * 100)
    

for tournament in range(NUMBER_OF_TOURNAMENTS):
    
    # map of players and their index
    playerDict = {
        Color.RED: 0,
        Color.BLUE: 1,
        Color.WHITE: 2,
        Color.ORANGE: 3,
    }

    # list of class of players
    players = [
        WeightedRandomPlayer(Color.RED),
        PlayerE(Color.BLUE, printout=True),
        PlayerE(Color.WHITE, printout=True),
        PlayerE(Color.ORANGE, printout=True),
    ]

    # copy of the first played players
    firstPlayersCopy = [None, players[1].copyData(), players[2].copyData(), players[3].copyData()]
    
    # Varaibles to store the best player
    BestPlayer = None
    BestScore = 0
    
    # stores the scores of the population
    player_scores = [[0]*len(players) for _ in range(GENERATIONS)]

    # loops for the number of generations
    for generations in range(GENERATIONS):
        
        victory = []

        # running the games for the current generation
        for games in range(NumberOfGames):
            game = Game(players)
            val = game.play()
            victory.append(val)
        
        c = dict(Counter(victory))
        print(generations)

        ComputeWinRate(c)

        print(c, " Score of weighted random:", c[Color.RED])
        
        # saving each player's score
        for _, player in enumerate(players):
            player_scores[generations][playerDict[player.color]] = c.get(player.color, 0)

        # find the best player
        logging.debug(f"Generation {generations}, tournament {tournament}: {c}  {c[Color.RED]}")
        for key in c:
            if c[key] > BestScore and key != Color.RED:
                BestScore = c[key]
                BestPlayer = players[playerDict[key]].copyData()
                
                # When the best Player is found then we can run it against the weighted random player
                print("New Best Player: ", BestPlayer, " with score: ", BestScore)
                logging.debug(f"New Best Player: {BestPlayer}, score: {BestScore}")
                print("********* The Best against WR *********")
                
                RunAgainstWeighted([ players[playerDict[key]], players[0]], NumberOfGames=NumberOfGames)
                
                print()
                print()
                
        # check each Weighted Random Player against the each player every 10 rounds
        # or when the WR is score is less than 25
        if generations % 10 == 0 or c[Color.RED] < 25: 
            print("********* 10th Turn or Less than 25 *********")
            for playerForTemp in c:
                if playerForTemp == Color.RED:
                    continue
                if playerForTemp == None:
                    continue
                RunAgainstWeighted([players[playerDict[playerForTemp]], players[0]], NumberOfGames=NumberOfGames)
                print("")
            
            
        # remove the weighted random player from the list
        # remove the None player from the list (Happens if there is a draw)
        temp = c.pop(Color.RED, None)
        temp = c.pop(None, None)
        # sort these players in order of their score
        st = sorted(c.items(), key=lambda x: x[1], reverse=True)
        
        # Mutate these players
        try:
            # copy over the best without changing it
            players[1].setData(players[playerDict[st[0][0]]].copyData())
            
            # copy over the best and mutate it
            players[2].setData(players[playerDict[st[0][0]]].copyData())
            players[2].mutate()
            
            # copy over the second best and mutate it
            players[3].setData(players[playerDict[st[1][0]]].copyData())
            players[3].mutate()
        except:
            print('An exception occurred')
            logging.warning('An exception occurred')

        # store best player
    best_players.append((BestPlayer, BestScore))
    logging.info(f"Tournament {tournament} results: {c}")
    # After all of the generations we Analyze
    print("\033[1;33m************************** ANALYSIS ************************** \033[00m")
    print()
    print()
    
    print("Running for the last generation of the bots againts Weighted Random")
    # Runs each last generation player withe the weighted random player
    for playerForTemp in c:
        if playerForTemp == Color.RED:
            continue
        if playerForTemp == None:
            continue
        print("Last Gen Bot: ", playerForTemp, " against Weighted Random")
        RunAgainstWeighted([players[playerDict[playerForTemp]], WeightedRandomPlayer(Color.RED)], NumberOfGames=NumberOfGames)
        print("")
    
    
    
    print("Running for the last generation of the bots againts the first gen bots")
    # save the scores of the last generation bots
    otherbots = {}
    for i in c:
        otherbots[i] = players[playerDict[i]].copyData()
        
    # use these bots to play against the first generation bots
    # replace the red bot with each of the last generation bots 
    #    # to see if there is an improvement
    for bot in otherbots:
        players[0] = PlayerE(Color.RED)
        players[0].setData(otherbots[bot])
        
        # replace the other bots with the first generation bots
        for i in range(1, len(players)):
            players[i].setData(firstPlayersCopy[i])
        
        # plays the games and stores the winner
        victory = []
        for games in range(NumberOfGames + ADDITIONALGAMES):
            game = Game(players)
            val = game.play()
            victory.append(val)
            
        c = dict(Counter(victory))
        
        # scores the winners
        for key in c:
            c[key] = int(c[key] / (NumberOfGames+ADDITIONALGAMES) * 100)
        print("\n\nFirst Gen bots vs  last gen BOT  *****", bot , " =>> RED bot (Red bot will use these weights)")
        logging.info(f"lFirst Gen bots vs ***** {bot} =>> RED bot (Red bot will use these weights)")
        PrintTheOrder(c)    


        
    logging.info(f"Best player's weights: {BestPlayer}, score: {BestScore}")
    
    print("Best player's weights: ", BestPlayer, " score: ", BestScore)
    print("Running the Best Player for all generations vs the First Gen bots")
    print("The Best Player's weights will be placed in the red bots")
    players[0] = PlayerE(Color.RED)
    players[0].setData(BestPlayer)

    for i in range(1, len(players)):
        players[i].setData(firstPlayersCopy[i])
        
    victory = []
    for games in range(NumberOfGames):
        game = Game(players)
        val = game.play()
        victory.append(val)
        
    c = dict(Counter(victory))
    ComputeWinRate(c)
    SavePlayerScores(player_scores)
    
    # printing the results form the tournament
    PrintTheOrder(c)
    tournament_results.append(c)





# Saving the file data
with open("SavedData/tournament_results.pkl", "wb") as f:
    pickle.dump(tournament_results, f)

with open("SavedData/best_players.pkl", "wb") as f:
    pickle.dump(best_players, f)


