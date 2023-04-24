from catanatron import Game, RandomPlayer, Color
from fortomm import PlayerE

from catanatron_core.catanatron.players.weighted_random import WeightedRandomPlayer

from collections import Counter

import random

# import multiprocessing as mp
import multiprocessing
import threading
import concurrent.futures

import logging

playerDict = {
    Color.RED: 0,
    Color.BLUE: 1,
    Color.WHITE: 2,
    Color.ORANGE: 3,
}

NumberOfGames = 100
GENERATIONS = 10


players = [
    WeightedRandomPlayer(Color.RED),
    PlayerE(Color.BLUE, printout=True),
    PlayerE(Color.WHITE, printout=True),
    PlayerE(Color.ORANGE, printout=True),
]

firstPlayersCopy = [None, players[1].copyData(), players[2].copyData(), players[3].copyData()]

BestPlayer = None
BestScore = 0

for generations in range(GENERATIONS):
    
    victory = []

    for games in range(NumberOfGames):
    
        game = Game(players)
        val = game.play()
        victory.append(val)
        
    c = dict(Counter(victory))
    print(generations)

    for key in c:
        c[key] = int(c[key] / NumberOfGames * 100)

    print(c)

    # find the best player
    for key in c:
        if c[key] > BestScore and key != Color.RED:
            BestScore = c[key]
            BestPlayer = players[playerDict[key]]
            print("New Best Player: ", BestPlayer, " with score: ", BestScore)

    # mutate the best player
    temp = c.pop(Color.RED, None)
    temp = c.pop(None, None)
    st = sorted(c.items(), key=lambda x: x[1], reverse=True)
    try:
      players[1].setData(players[playerDict[st[0][0]]].copyData())
      players[2].setData(players[playerDict[st[0][0]]].copyData())
      players[2].mutate()
      players[3].setData(players[playerDict[st[1][0]]].copyData())
      players[3].mutate()
    except:
      print('An exception occurred')



# save the scores of other players
otherbots = {}
for i in c:
    # otherbots[i] = c[i]
    otherbots[i] = players[playerDict[i]].copyData()
    
additionalGames = 150
for bot in otherbots:
    players[0] = PlayerE(Color.RED)
    players[0].setData(otherbots[bot])

    for i in range(1, len(players)):
        players[i].setData(firstPlayersCopy[i])
        
    victory = []
    for games in range(NumberOfGames + additionalGames):
        game = Game(players)
        val = game.play()
        victory.append(val)
        
    c = dict(Counter(victory))
    for key in c:
        c[key] = int(c[key] / (NumberOfGames+additionalGames) * 100)


    print("\n\nbest from last session tournament", bot)
    for i in sorted(c, key=c.get, reverse=True):
        print(i, c[i])
    
print("\n\n\n ----------------------------------- best victor from the tournament ----------------------------------- ")

print(BestPlayer.WEIGHTS_BY_ACTION_TYPE)
print(BestScore)

players[0] = PlayerE(Color.RED)
players[0].setData(BestPlayer.copyData())

for i in range(1, len(players)):
    players[i].setData(firstPlayersCopy[i])
    
victory = []
for games in range(NumberOfGames):
    game = Game(players)
    val = game.play()
    victory.append(val)
    
c = dict(Counter(victory))
for key in c:
    c[key] = int(c[key] / NumberOfGames * 100)


print("best For this tournament")
for i in sorted(c, key=c.get, reverse=True):
    print(i, c[i])





