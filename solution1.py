# import numpy as np
import math

end_state = "123456780"

UP, DOWN, LEFT, RIGHT = 'up', 'down', 'left', 'right'



class Game:
    def __init__(self, state="012345678"):
        self.state = state
    def getrowcolumn(ind):
        return [math.floor(ind//3), ind%3]

class Node:
    def __init__(self, state="012345678", parent=None, cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.depth = depth
        self.solved = False
    def getPossibleMovesStates(self):
        moves = []
        zeroIndex = self.state.find("0")
        row, column = math.floor(zeroIndex/3), zeroIndex%3

        if column>0: moves.append([LEFT, self.makeNextMove(LEFT)])
        if column<2: moves.append([RIGHT, self.makeNextMove(RIGHT)])
        if row>0: moves.append([UP, self.makeNextMove(UP)])
        if row<2: moves.append([DOWN, self.makeNextMove(DOWN)])
        return moves
    def makeNextMove(self, action):
        zeroIndex = self.state.find('0')
        newIndex = None
        if action == LEFT:
            newIndex = zeroIndex - 1
        elif action == RIGHT:
            newIndex = zeroIndex + 1
        elif action == UP:
            newIndex = zeroIndex - 3
        elif action == DOWN:
            newIndex = zeroIndex + 3
        sparr = list(self.state)
        sparr[zeroIndex] = sparr[newIndex]
        sparr[newIndex] = "0"
        return ''.join(sparr)
    def isComplete(self):
        return self.state == end_state
    
    def getManhattan(self):
        distance = 0
        
        onepos = Game.getrowcolumn(self.state.index('1'))
        distance += abs(0-onepos[0]) + abs(0-onepos[1])
        
        twopos = Game.getrowcolumn(self.state.index('2'))
        distance += abs(0-twopos[0]) + abs(1-twopos[1])
        
        threepos = Game.getrowcolumn(self.state.index('3'))
        distance += abs(0-threepos[0]) + abs(2-threepos[1])
        
        fourpos = Game.getrowcolumn(self.state.index('4'))
        distance += abs(1-fourpos[0]) + abs(0-fourpos[1])
        
        fivepos = Game.getrowcolumn(self.state.index('5'))
        distance += abs(1-fivepos[0]) + abs(1-fivepos[1])

        sizpos = Game.getrowcolumn(self.state.index('6'))
        distance += abs(1-sizpos[0]) + abs(2-sizpos[1])

        sevenpos = Game.getrowcolumn(self.state.index('7'))
        distance += abs(2-sevenpos[0]) + abs(0-sevenpos[1])

        eightpos = Game.getrowcolumn(self.state.index('8'))
        distance += abs(2-eightpos[0]) + abs(1-eightpos[1])

        return distance
    def expand(self):
        result = []
        av_actions = self.getPossibleMovesStates()

        for ac in av_actions:
            enode = Node(ac[1], depth=self.depth+1, cost=self.cost+1)
            result.append({
                "node":enode,
                "state": ac[1],
                'heuristic': heuristic(enode),
                "parent":self,
                "for_move": ac[0]
            })
        
        return result

        print(av_actions)
    def printboard(self):
        print()
        print(self.state[:3])
        print(self.state[3:6])
        print(self.state[6:9])
        print()
    def backPropSolved(self):
        self.solved = True
        if self.parent:
            self.parent.backPropSovled()


MAX_DEPTH = 40

def heuristic(node:Node):
    return node.depth+node.getManhattan()

def solve(znode:Node, path=[], solved=False):
    
    # print({"state":znode.state, 'h':heuristic(znode)})
    if znode.solved:
        return
    if znode.isComplete():
        for p in path:
            Node(p).printboard()
        znode.printboard()
        znode.backPropSolved()
        print("Puzzle solved", "num of moves: ", len(path)+1)
        exit()
        return
    if znode.depth >= MAX_DEPTH:
        # print("MAX DEPTH")
        return 
    
    
    expandibleNodes = znode.expand()
    minmh = min([x['heuristic'] for x in expandibleNodes])
    min_nodes = list(filter(lambda x: (x['state'] not in path), expandibleNodes))
    min_nodes = [x['node'] for x in min_nodes]
    # print()
    # print([heuristic(x) for x in min_nodes], [x['heuristic'] for x in expandibleNodes], minmh)
    for newnode in min_nodes:
        # print(heuristic(newnode), newnode.state, dict(depth=newnode.depth))
        solve(newnode, path+[znode.state])
    pass

    




# g = Game("123056478")
g = Game("720153486")
solve(znode=Node(g.state))
