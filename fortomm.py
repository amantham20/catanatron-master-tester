from catanatron import Player
from catanatron_experimental.cli.cli_players import register_player

# from catanatron.models.player import Player
from catanatron.models.actions import ActionType

import random
import copy
# WEIGHTS_BY_ACTION_TYPE = {
#     ActionType.BUILD_CITY: random.randint(0,50000),
#     ActionType.BUILD_SETTLEMENT: random.randint(0,50000),
#     ActionType.BUY_DEVELOPMENT_CARD: random.randint(0,50000),
#     ActionType.BUILD_ROAD: random.randint(0,50000)
# }

# BUILD_ROAD = "BUILD_ROAD"  # value is edge_id
# BUILD_SETTLEMENT = "BUILD_SETTLEMENT"  # value is node_id
# BUILD_CITY = "BUILD_CITY"  # value is node_id
# BUY_DEVELOPMENT_CARD = "BUY_DEVELOPMENT_CARD",

# {<ActionType.BUILD_CITY: 'BUILD_CITY'>: 3655, 
# <ActionType.BUILD_SETTLEMENT: 'BUILD_SETTLEMENT'>: 5905, 
# <ActionType.BUY_DEVELOPMENT_CARD: 'BUY_DEVELOPMENT_CARD'>: 1854, 
# \<ActionType.BUILD_ROAD: 'BUILD_ROAD'>: 2669}

# @register_player("FOO")
class FooPlayer(Player):
  

  def __init__(self, color):
        super().__init__(color)
        self.WEIGHTS_BY_ACTION_TYPE = {ActionType.BUILD_CITY: 8730, 
        ActionType.BUILD_SETTLEMENT: 1661, 
        ActionType.BUY_DEVELOPMENT_CARD: 399, 
        ActionType.BUILD_ROAD: 6853}
        print(self.WEIGHTS_BY_ACTION_TYPE)

  def decide(self, game, playable_actions):
    """Should return one of the playable_actions.

    Args:
        game (Game): complete game state. read-only.
        playable_actions (Iterable[Action]): options to choose from
    Return:
        action (Action): Chosen element of playable_actions
    """


    if len(playable_actions) == 1:
        if self.analysis:
            self.analysis(playable_actions[0], self.color)
        return playable_actions[0]
    
    

    bloated_actions = []
    for action in playable_actions:
        weight = self.WEIGHTS_BY_ACTION_TYPE.get(action.action_type, 1)
        bloated_actions.extend([action] * weight)

    if len(bloated_actions) == 0:
        if self.analysis:
            self.analysis(playable_actions[0], self.color)

        return playable_actions[0]

    index = random.randrange(0, len(bloated_actions))
    if self.analysis:
        self.analysis(bloated_actions[index], self.color)

    return bloated_actions[index]


# @register_player("GP")
class PlayerE(Player):
  
  def __init__(self, color, printout=False):
        super().__init__(color)
        self.WEIGHTS_BY_ACTION_TYPE = {
            ActionType.BUILD_CITY: random.randint(0,10000),
            ActionType.BUILD_SETTLEMENT: random.randint(0,10000),
            ActionType.BUY_DEVELOPMENT_CARD: random.randint(0,10000),
            ActionType.BUILD_ROAD: random.randint(0,10000)
        }
        if printout:
            print(self.WEIGHTS_BY_ACTION_TYPE)

  def decide(self, game, playable_actions):
    """Should return one of the playable_actions.

    Args:
        game (Game): complete game state. read-only.
        playable_actions (Iterable[Action]): options to choose from
    Return:
        action (Action): Chosen element of playable_actions
    """


    if len(playable_actions) == 1:
        return playable_actions[0]
    
    

    bloated_actions = []
    for action in playable_actions:
        weight = self.WEIGHTS_BY_ACTION_TYPE.get(action.action_type, 1)
        bloated_actions.extend([action] * weight)

    if len(bloated_actions) == 0:
        if self.analysis:
            self.analysis(playable_actions[0], self.color)
        return playable_actions[0]

    index = random.randrange(0, len(bloated_actions))
    if self.analysis:
        self.analysis(bloated_actions[index], self.color)
    return bloated_actions[index]


  def mutate(self):
    keyR = random.choice(list(self.WEIGHTS_BY_ACTION_TYPE.keys()))
    self.WEIGHTS_BY_ACTION_TYPE[keyR] += random.randint(-1000,1000)

  def copyData(self):
    return copy.deepcopy(self.WEIGHTS_BY_ACTION_TYPE)
  
  def setData(self, data):
    self.WEIGHTS_BY_ACTION_TYPE = copy.deepcopy(data)



    
    
    
