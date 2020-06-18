import random
import math

DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)

SPAWN_WIDTH = 13 # Must be such that startSpawnIndex + SPAWN_WIDTH doesn't go past board_size=16
startSpawnIndex = 1
spawnIndex = startSpawnIndex
board_size = get_board_size()
team = get_team()
opp_team = Team.WHITE if team == Team.BLACK else team.BLACK

takenLanesSoFar = 0

index = 0
turn = 0
endIndex = board_size - 1
forward = 1
if team == Team.WHITE:
    forward = 1
    index = 0
    endIndex = board_size - 1
else:
    index = board_size - 1
    forward = -1
    endIndex = 0

firstSpawnOrderIndex = 0
firstSpawnOrder = [1, 13, 4, 7, 15, 10]
def run():
    global spawnIndex, board_size, opp_team, startSpawnIndex, SPAWN_WIDTH, forward, index, endIndex, team, takenLanesSoFar, turn, firstSpawnOrderIndex, firstSpawnOrder
    turn = turn + 1
    board = get_board()

    spawnRow = board[index]
    endRow = board[endIndex]
    
    # store what lanes/columns are not occupied by us already so we prioritize some other lanes with some buffer
    attackableLanes = set()
    # only lanes without our own unit
    strictAttackableLanes = set()

    # lanes we have lost to opponent
    lostLanes = set()

    # count how many of our pawns are in a col
    friendCountsPerCol = {}
    enemyCountsPerCol = {}

    # count the farthest up we are on a lane
    furthestRow = []
    closestDistToEnd = board_size

    lanesTaken = 0

    lowestTakenLane = board_size
    highestTakenLane = 0
    for i in range(board_size):
        friendCountsPerCol[str(i)] = 0
        enemyCountsPerCol[str(i)] = 0
        if forward == 1:
            furthestRow.append(-1)
        else:
            furthestRow.append(board_size)
        if not (endRow[i] == team):
            attackableLanes.add(i)
            strictAttackableLanes.add(i)
            if (i - 1 >= 0):
                attackableLanes.add(i - 1)
            if (i+1 <= board_size - 1):
                attackableLanes.add(i + 1)
        elif (endRow[i] == team):
            lanesTaken = lanesTaken + 1
            if (i > highestTakenLane):
                highestTakenLane = i
            if (i < lowestTakenLane):
                lowestTakenLane = i
        if (spawnRow[i] == opp_team):
            lostLanes.add(i)

    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == team:
                friendCountsPerCol[str(j)] = friendCountsPerCol[str(j)] + 1
                distToEnd = abs(i - endIndex)
                if (distToEnd < closestDistToEnd):
                    closestDistToEnd = distToEnd
                if (forward == 1):
                    if i > furthestRow[j]:
                        furthestRow[j] = i
                else:
                    if i < furthestRow[j]:
                        furthestRow[j] = i
            elif board[i][j] == opp_team:
                enemyCountsPerCol[str(j)] = enemyCountsPerCol[str(j)] + 1


    origAttackableLanes = attackableLanes.copy()

    # all counts of number of pawns per col in increasing order
    allminCols = sorted(friendCountsPerCol.items() , key=lambda x: (x[1]) )
    # above but without lanes we can't use
    minCols = []
    # remove from _minCols columns where lane is taken by opponent
    for i in range (len(allminCols)):
        if not int(allminCols[i][0]) in lostLanes:
            minCols.append(allminCols[i])

    # minEnemyCols[0][0] is col index with least enemies, minEnemeyCols[0][1] is number of enemy pawns on that col
    minEnemyCols = sorted(enemyCountsPerCol.items() , key=lambda x: (x[1]) )
    # above but cols where we haven't gotten control yet
    attackableMinEnemyCols = []
    # spawned already or not
    spawned = False

    # TODO: Consider going all out defence eventually
    # TODO: Consider just attacking like this xx_xx_xx. so those isolated areas we can target easily later
    

    # determine if all lanes are in our favor / we have more units than they could ever possibly have * constant
    atAdvantage = True
    if (minCols[0][1] < 2 and turn <= 100):
        atAdvantage = False
    if (minCols[0][1] < 3 and turn > 100):
        atAdvantage = False

    # if (closestDistToEnd <= 7 and minCols[0][1] < 4):
    #     atAdvantage = False

    # Old code that just checks if each column has enough pawns based on distance. wasn't good, we got spread out 
    # too much
    # if atAdvantage:
    #     for i in range(len(furthestRow)):
    #         pawnsOnLane = minCols[i][1]
    #         distToSpawn = abs(furthestRow[i] - index)
    #         distToEnd  = abs(endIndex - furthestRow[i])
    #         if distToSpawn > distToEnd:
    #             if pawnsOnLane < distToSpawn:
    #                 atAdvantage = False
    #                 dlog("Not enough pawns to defend on col " + str(i))
    #                 break
    #         else:
    #             if pawnsOnLane < distToEnd:
    #                 atAdvantage = False
    #                 dlog("Not enough pawns to attack on col " + str(i))
    #                 break


    dlog("Attackable: " + str(origAttackableLanes))
    dlog("minCols: " + str(minCols))
    dlog("minEnemyCols: " + str(attackableMinEnemyCols))
    dlog("High: " + str(highestTakenLane) + " | Low: " + str(lowestTakenLane) + " | Lanes Taken: " + str(lanesTaken))
    # if taken 6 lanes already, go all in on some lanes if other lanes have at least 2 pawns
    if (lanesTaken >= 6 and minCols[0][1] >= 2 and (highestTakenLane < board_size - 2 or lowestTakenLane > 2)):
        # calculate best place to go all in on
        # prefer edge of taken lanes that has 2 spaces available
        if (highestTakenLane < board_size - 2):
            attackableLanes.clear()
            attackableLanes.add(highestTakenLane)
            attackableLanes.add(highestTakenLane + 1)
            attackableLanes.add(highestTakenLane + 2)
        elif (lowestTakenLane > 2):
            attackableLanes.clear()
            attackableLanes.add(lowestTakenLane)
            attackableLanes.add(lowestTakenLane - 1)
            attackableLanes.add(lowestTakenLane - 2)

    # target some weak lanes as long as our other lanes have at least 2 pawns
    elif (turn >= 50 and atAdvantage):
        
        # target weak lanes of which we haven't won yet. Using strictlanes because we handle buffering here
        for i in range(len(minEnemyCols)):
            colIndex = int(minEnemyCols[i][0])
            if colIndex in strictAttackableLanes:
                attackableMinEnemyCols.append(minEnemyCols[i])
        
        dlog("Attackable min enemy cols: " + str(attackableMinEnemyCols))
        attackableLanes.clear()
        # target the lane where we have the most pawns and they have the least, calculate a delta
        weakIndex = int(attackableMinEnemyCols[0][0])
        # highestDifference = -1000
        # for i in range(board_size):
        #     diff = 0
        #     if (i < board_size - 3):
        #         diff = minCols[i][1] - minEnemyCols[i][1] + minCols[i+1][1] - minEnemyCols[i+1][1]+ minCols[i+2][1] - minEnemyCols[i+2][1]
        #     else:
        #         diff = minCols[i][1] - minEnemyCols[i][1] + minCols[i-1][1] - minEnemyCols[i-1][1]+ minCols[i-2][1] - minEnemyCols[i-2][1]
        #     if (diff > highestDifference):
        #         weakIndex = i

        # find which lanes have units not moving because they can get captured but its only 1 unit and so more support there will win us it

        for i in range(len(furthestRow)):
            rowNum = furthestRow[i]
            if (i > 0 and i < board_size - 1):
                # check rowNum + forward * 2, col +/- 1
                enemiesThatCanCapture = 0
                if check_space(rowNum + forward * 2, i - 1) == opp_team:
                    enemiesThatCanCapture = enemiesThatCanCapture + 1
                if check_space(rowNum + forward * 2, i + 1) == opp_team:
                    enemiesThatCanCapture = enemiesThatCanCapture + 1
                friendPawnsNearCol = friendCountsPerCol[str(i)] + friendCountsPerCol[str(i+1)] + friendCountsPerCol[str(i-1)]
                if (enemiesThatCanCapture == 1 and friendPawnsNearCol <= 15):
                    weakIndex = i
                    break


        if (weakIndex < board_size - 1 and weakIndex > 0):
            attackableLanes.add(weakIndex - 1)
            attackableLanes.add(weakIndex)
            attackableLanes.add(weakIndex + 1)
            # attackableLanes.add(weakIndex + 2)
        elif (weakIndex == 0):
            attackableLanes.add(weakIndex)
            attackableLanes.add(weakIndex+1)
            attackableLanes.add(weakIndex+2)
            # attackableLanes.add(weakIndex + 3)
        elif (weakIndex == board_size - 1):
            attackableLanes.add(weakIndex)
            attackableLanes.add(weakIndex-1)
            attackableLanes.add(weakIndex-2)
            # attackableLanes.add(weakIndex - 3)
    
    # Place pawns on the column with least units and is marked attackable
    for i in range(len(minCols)):
        spind = int(minCols[i][0])
        if (turn >= 16):
            if spind in attackableLanes:
                if (not check_space(index, spind) and not willGetCaptured(board, index, spind)):
                    
                    spawn(index, spind)
                    spawned = True
                    break
        else:
            spind = firstSpawnOrder[firstSpawnOrderIndex]
            firstSpawnOrderIndex = (firstSpawnOrderIndex + 1) % len(firstSpawnOrder)
            if (not check_space(index, spind) and not willGetCaptured(board, index, spind)):
                spawn(index, spind)
                spawned = True
                break


    if spawned:
        return

    # if haven't spawned yet, revert to line spawning to spawn anywhere we can that's atttackable
    # the index we are trying to start spawning on
    beginSpawn = spawnIndex
    while (True):
        
        sindex = getNextSpawnIndex()
        if sindex in origAttackableLanes:
            if (not check_space(index, sindex) and not willGetCaptured(board, index, sindex)):
                spawn(index, sindex)
                spawned = True
                break

        # if we wrapped around for spawn indexes, stop
        if sindex == beginSpawn:
            break
    
    # looped over and found no spawnindex in attackable lanes, just spawn anywhere
    if not spawned:
        while (True):
            sindex = getNextSpawnIndex()
            if (not check_space(index, sindex) and not willGetCaptured(board, index, sindex)):
                spawn(index, sindex)
                spawned = True
                break
        
            # if we wrapped around for spawn indexes, stop
            if sindex == beginSpawn:
                break

    # still no spawn? try all columns
    if not spawned:
        sindex = 0
        while (True):
            if (not check_space(index, sindex) and not willGetCaptured(board, index, sindex)):
                spawn(index, sindex)
                spawned = True
                break
            sindex = sindex + 1
            if (sindex == board_size):
                break
        
# get the next spawning index
def getNextSpawnIndex():
    global spawnIndex, SPAWN_WIDTH, board_size
    spawnIndex = (spawnIndex + 1) % board_size
    if spawnIndex > startSpawnIndex + SPAWN_WIDTH:
        spawnIndex = startSpawnIndex

    return spawnIndex

# if spawning on row col will get captured by a unit
def willGetCaptured(board, row, col):
    global forward, opp_team
    if (col >= 1 and board[row + forward][col - 1] == opp_team):
        return True
    if (col <= board_size - 2 and board[row + forward][col + 1] == opp_team):
        return True
    return False