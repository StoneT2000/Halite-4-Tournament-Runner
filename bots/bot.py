from kaggle_environments.envs.halite.helpers import *
from kaggle_environments.envs.halite import helpers
# from utils.log import Log
helpers.Configuration
class Log:
    def __init__(self, level = 3):
        self.level = level
    def info(self, msg):
        if (self.level >= 3):
            print("[INFO]", msg)
    def warn(self, msg):
        if (self.level >= 2):
            print("[INFO]", msg)

directions = [ShipAction.NORTH, ShipAction.EAST, ShipAction.SOUTH, ShipAction.WEST]
def getDirTo(fromPos, toPos, size):
    fromX, fromY = divmod(fromPos[0],size), divmod(fromPos[1],size)
    toX, toY = divmod(toPos[0],size), divmod(toPos[1],size)
    if fromY < toY: return ShipAction.NORTH
    if fromY > toY: return ShipAction.SOUTH
    if fromX < toX: return ShipAction.EAST
    if fromX > toX: return ShipAction.WEST
player_count = 2
ship_states = {}

log = Log(3)
def agent(obs, config):
    global player_count
    global ship_states

    size = config.size
    board = Board(obs, config)
    me = board.current_player

    if board.step == 0:
        log.info("Initializing")
        player_count = 1 + len(board.opponents)

    # edge cases, build ships if there is none
    if len(me.ships) == 0 and len(me.shipyards) > 0:
        me.shipyards[0].next_action = ShipyardAction.SPAWN
    
    # build shipyard if there is none
    if len(me.shipyards) == 0 and len(me.ships) > 0:
        me.ships[0].next_action = ShipAction.CONVERT
    
    for ship in me.ships:
        if ship.next_action == None:
            
            ### Part 1: Set the ship's state 
            if ship.halite < 200: # If cargo is too low, collect halite
                ship_states[ship.id] = "COLLECT"
            if ship.halite > 500: # If cargo gets very big, deposit halite
                ship_states[ship.id] = "DEPOSIT"
                
            ### Part 2: Use the ship's state to select an action
            if ship_states[ship.id] == "COLLECT":
                # If halite at current location running low, 
                # move to the adjacent square containing the most halite
                if ship.cell.halite < 100:
                    neighbors = [ship.cell.north.halite, ship.cell.east.halite, 
                                 ship.cell.south.halite, ship.cell.west.halite]
                    best = max(range(len(neighbors)), key=neighbors.__getitem__)
                    ship.next_action = directions[best]
            if ship_states[ship.id] == "DEPOSIT":
                # Move towards shipyard to deposit cargo
                direction = getDirTo(ship.position, me.shipyards[0].position, size)
                if direction: ship.next_action = direction
                
    return me.next_actions