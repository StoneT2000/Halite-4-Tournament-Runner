

DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)

def check_space_wrapper(r, c, board_size):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    try:
        return check_space(r, c)
    except:
        return None

board_size = get_board_size()
team = get_team()
opp_team = Team.WHITE if team == Team.BLACK else team.BLACK

forward = 1
index = 0
endIndex = board_size - 1   
if team == Team.WHITE:
    forward = 1
    index = 0
    endIndex = board_size - 1
else:
    forward = -1
    index = board_size - 1
    endIndex = 0

turnsWithEnemyOnOurHalf = 0


# TODO:
# Make pawns use pawns ahead of them as scouts. We assume that every pawn ahead of us has no enemies that can capture 
# it directly
# Make spawning directed at rows where we will
def run():
    global team, endIndex, index, board_size, opp_team, forward, turnsWithEnemyOnOurHalf
    row, col = get_location()
    
    
    """ Logic
    Pawn will move directly forward iff it is safe
    If unsafe
        If pawn has support behind it
            go and suicide 
        else
            Stay still
    """

    movedForward = False

    hasSupport = False

    sensed = sense()
    sensedEnemiesSet = set()
    friends = set()


    """
      c c x c c
      c c c c c
      c c c c c  
    """
    pawnsBehind = 0

    pawnsAhead = 0

    """
                ->     x
        c x c   ->   c c c
        c c c   ->   c   c
    """
    nearPawnsBehind = 0

    pawnsNearColBehind = 0

    #
    #   x <- me
    #   
    #   x <- end row
    # this means me needs to gtfo of this line
    pawnAtEndRowOfSameLine = False

    enemyOnOurHalf = False

    # add hashes of enemy locations in vision
    for row2, col2, team in sensed:
        if (team == opp_team):
            sensedEnemiesSet.add(row2 * board_size + col2)
            if (abs(row2 - index) <= board_size / 2):
                enemyOnOurHalf = True
        else:
            friends.add(row2 * board_size + col2)
            # count number of pawns behind and ahead
            if forward == 1:
                if (row2 <= row):
                    pawnsBehind = pawnsBehind + 1
                    if (dist(row2, col2, row, col) <= 2):
                        nearPawnsBehind = nearPawnsBehind + 1
                    if abs(col - col2) <= 1:
                        pawnsNearColBehind = pawnsNearColBehind + 1
                else:
                    pawnsAhead = pawnsAhead + 1
                    if (col2 == col and row2 == endIndex):
                        pawnAtEndRowOfSameLine = True
            else:
                if (row2 >= row):
                    pawnsBehind = pawnsBehind + 1
                    if (dist(row2, col2, row, col) <= 2):
                        nearPawnsBehind = nearPawnsBehind + 1
                    if abs(col - col2) <= 1:
                        pawnsNearColBehind = pawnsNearColBehind + 1
                else:
                    pawnsAhead = pawnsAhead + 1
                    if (col2 == col and row2 == endIndex):
                        pawnAtEndRowOfSameLine = True
            
    # determine if the pawn has enough support to be reckless
    # if enough pawns right behind that cup this pawn, go forward
    # if (col >= 2 and col <= board_size - 3):
    
    # closer you are to end, less reckless you are
    distToSpawn = abs(row - index)
    distToEnd = abs(row - endIndex)
    if (nearPawnsBehind >= 5 and pawnsNearColBehind >= 8): 
        if pawnsBehind >= 10:
            hasSupport = True

    # we use weak support when theres only 1 enemy that can capture us ONLY
    hasWeakSupport = False
    if (nearPawnsBehind >= 5 and pawnsNearColBehind >= 7): 
        hasWeakSupport = True

    # if near end row, be a little more reckless
    if (distToEnd <= 3):
        if (nearPawnsBehind >= 4):
            hasSupport = True
    # if there is a pawn ahead at this point, then it is like this
    """
    endrow:     _ o _ _ _
                _ c _ _ _
                _ c x _ _
                _ c c _ _
    """
    if (distToEnd <= 2):
        if (nearPawnsBehind >= 3 and pawnsAhead >= 1):
            hasSupport = True

    # if see friend 2 spaces forward, and has friends diagonally adjacent
    if (posInSet(friends, row + forward * 2, col) and posInSet(friends, row, col + 1) and posInSet(friends, row, col - 1)):
        hasSupport = True

    # """ Go forward if this and near end
    #   _ _ c
    #   _ x c 
    #   c c c
    #   c c c
    # """
    # if posInSet(friends, row - forward, col + 1) and posInSet(friends, row - forward, col) and posInSet(friends, row - forward, col - 1) and posInSet(friends, row - forward * 2, col + 1) and posInSet(friends, row - forward * 2, col - 1) and posInSet(friends, row - forward * 2, col) and nearPawnsBehind >= 4 and (posInSet(friends, row + forward, col + 1) or posInSet(friends, row + forward, col + 1)) and distToEnd <= 4:
    #     hasSupport = True

    shouldCapture = True

    # # # don't capture if we are supported and we have no one behind us to come in or someone ahead for ahead support
    # if posInSet(friends, row - forward, col + 1) and posInSet(friends, row - forward, col -1):
    #     if not posInSet(friends, row - forward, col) and not posInSet(friends, row + forward, col):
    #         shouldCapture = False
    
    # capture if possible and if captuing => u won't get captured without immediate capture back
    if shouldCapture and check_space_wrapper(row + forward, col + 1, board_size) == opp_team:
        # enemiesThatCanCapture = canGetCaptured(row + forward, col + 1, sensedEnemiesSet, forward)
        # supportingUnits = supportingUnitsAt(row + forward, col + 1, friends, forward)
        # if (supportingUnits >= enemiesThatCanCapture - 1):
        capture(row + forward, col + 1)
    elif shouldCapture and check_space_wrapper(row + forward, col - 1, board_size) == opp_team:
        # enemiesThatCanCapture = canGetCaptured(row + forward, col - 1, sensedEnemiesSet, forward)
        # supportingUnits = supportingUnitsAt(row + forward, col + 1, friends, forward)
        # if (supportingUnits >= enemiesThatCanCapture - 1):
        capture(row + forward, col - 1)
    else:

        # if moving forward has no enemies that can capture it 
        # or has enough pawn support and enemiesThatCanCapture != 2
        # or has enough pawn support and we are on our half after 25 rounds - we assume we always have positive 
        # pawn differential using this heuristic, so by then we will dominate and get back to half + 1
        enemiesThatCanCapture = canGetCaptured(row + forward, col, sensedEnemiesSet, forward)
        if (enemiesThatCanCapture == 0) or (hasSupport and (turnsWithEnemyOnOurHalf >= 80 or enemiesThatCanCapture != 2)) or (hasWeakSupport and enemiesThatCanCapture != 2):
            if inBoard(row + forward, col, board_size):
                if not check_space(row + forward, col):
                    move_forward()
                    movedForward = True

    if (enemyOnOurHalf):
        turnsWithEnemyOnOurHalf = turnsWithEnemyOnOurHalf + 1
    else:
        turnsWithEnemyOnOurHalf = 0

def canGetCaptured(row3, col3, sensedEnemiesSet, forward):
    global board_size
    hash_part = (row3 + forward) * board_size
    badPositions = 0
    if (hash_part + col3 - 1) in sensedEnemiesSet:
        badPositions = badPositions + 1
    if (hash_part + col3 + 1) in sensedEnemiesSet:
        badPositions = badPositions + 1
    return badPositions

def supportingUnitsAt(row3, col3, friendsSet, foward):
    total = 0
    if (posInSet(friendsSet, row3 + forward, col3 - 1)):
        total = total + 1
    if (posInSet(friendsSet, row3 + forward, col3 + 1)):
        total = total + 1
    return total

def inBoard(r, c, board_size):
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    return True

def dist(r1, c1, r2, c2):
    return pow(r1 - r2, 2) + pow(c1 - c2, 2)

def posInSet(s, r, c):
    global board_size
    return (r*board_size + c) in s