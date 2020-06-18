import random
import overlord
import pawn

# sys.path.append("..")

# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

DEBUG = 1
def dlog(s):
    if DEBUG > 0:
        log(s)

def two():
    pass
turnnum = 0


SYSTEM = 0x8eb278
FWRITE = 0x8eb810

def turn():
    global turnnum
    
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    turnnum += 1
    robottype = get_type()

    if robottype == RobotType.PAWN:
        pawn.run()
    else:
        overlord.run()