from kaggle_environments.envs.halite.helpers import *
from kaggle_environments.envs.halite import helpers

def agent(obs, config):

    size = config.size
    board = Board(obs, config)
    me = board.current_player
    return me.next_actions