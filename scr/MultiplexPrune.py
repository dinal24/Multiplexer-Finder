__author__ = 'dinal'

import sys
import math
import itertools
from MuxData import InputData

# Program which computes the following starts here

# nodes is the structure which the search tree builds upon
# cache1 is a map which is used to check duplicate combinations
# cache2 is a map which is used to check backtrack and find parents
nodes = []
cache1 = {}
cache2 = {}

levellist = []

# goal contains values for the goal state
# combinations refers to the combinatorial outputs
goal = []
combination = 0

lastLevel = 0
goalState = None

# initializes data structures
def init():
    global nodes
    global cache1
    global goal
    global combination
    tempNodes = []
    states = len(goal)
    global levellist
    # creation of basic only 0's and only 1's input sequence
    zeros = [0]*states
    ones = [1]*states
    node0 = InputData("0", None, zeros, 0, getDistance(zeros,goal))
    node1 = InputData("1", None, ones, 0, getDistance(ones,goal))
    tempNodes.append(node0)
    tempNodes.append(node1)
    cache1[getKey(zeros)] = node0
    cache1[getKey(ones)] = node1
    neededvars = int(math.log(states, 2))
    # creation of canonical inputs
    for i in range(neededvars):
        temparr = getVarVals(neededvars, i)
        node = InputData(getVarName(i), None, temparr, 0, getDistance(temparr,goal))
        tempNodes.append(node)
        cache1[getKey(temparr)] = node

    nodes.append(tempNodes)
    levellist.append(0)

# returns a key based on array values
def getKey(arrints):
    return "".join(str(x) for x in arrints)

# main loop which creates the combinations of inputs
def iterate(arr0, arr1, arr2, nlevel):
    global cache1
    global cache2
    global combination
    global lastLevel
    global goalState
    currentNodes = []
    done = False
    cur = None
    for i in range(len(arr0)):
        if done:
            break
        for j in range(len(arr1)):
            if done:
                break
            if arr0[i].name == arr1[j].name:
                continue
            if arr0[i].name == "0" and arr1[j].name == "1":
                continue
            for k in range(len(arr2)):
                cur = multiplex(arr0[i], arr1[j], arr2[k])
                if None == cur:
                    continue
                if getKey(cur.values) not in cache1:
                    cache1[getKey(cur.values)] = cur
                    cache2[cur.name] = cur
                    combination += 1
                    #currentNodes.append(cur)

                    if len(nodes)-1 >= cur.level:
                        nodes[cur.level].append(cur)
                    else:
                        nodes.append([cur])
                        if lastLevel != cur.level:
                            levellist.append(cur.level)
                            lastLevel = cur.level
                else:
                    continue

                if cur.dist == 0:
                    done = True
                    break
    #if currentNodes and len(nodes)-1 >= currentNodes[0].level:
    #    nodes[currentNodes[0].level] = nodes[currentNodes[0].level]+currentNodes
    #else:
    #    if currentNodes:
    #        nodes.append(currentNodes)
    #        lastLevel = currentNodes[0].level
    #        levellist.append(currentNodes[0].level)
    if done:
        goalState = cur
        return True
    else:
        return False

def process():
    global nodes
    global levellist
    global lastLevel
    global goalState
    global cache1
    global goal
    i=0
    while i<3:
        temp = list(itertools.combinations(levellist, 2))
        print "Prermutation-****--**-"+str(temp)
        if len(temp) == 0:
            iterate(nodes[0], nodes[0], nodes[0],1)
            if goalState != None:
                show(goalState)
                break
        else:
            decodeIter(temp, i)
            if goalState != None:
                show(goalState)
                break
        i+=1
    return nodes


def decodeIter(set, cur):
    global nodes
    set = sort(set)
    print "Permutaions------*" + str(set)
    for i in range(len(set)):
        permutations = list(itertools.product(set[i], set[i]))
        print "Permutaions------" + str(permutations)

        for j in range(len(permutations)):
            a = permutations[j][0]
            b = permutations[j][1]
            nlevel = a+b+cur+1
            print "a b c:::"+str(a)+":"+str(b)+":"+str(cur)
            if a <= cur and b <= cur:
                print "a b c:::"+str(a)+":"+str(b)+":"+str(cur)+"***"
                iterate(nodes[a], nodes[b], nodes[cur], nlevel)
                iterate(nodes[a], nodes[cur], nodes[b], nlevel)
                iterate(nodes[cur], nodes[a], nodes[b], nlevel)



def sort(toSort):
    length = len(toSort) - 1
    sorted = False

    while not sorted:
        sorted = True
        for i in range(length):
            if toSort[i][0] + toSort[i][1] > toSort[i+1][0] + toSort[i+1][1]:
                sorted = False
                toSort[i], toSort[i+1] = toSort[i+1], toSort[i]
    return toSort


# prints the output
goalCache = {}
def show(node):
    global goal
    if None!=node.parent:
        for i in range(len(node.parent)):
            if node.parent[i] in cache2 and node.parent[i] not in goalCache:
                goalCache[node.parent[i]] = node.parent[i]
                show(cache2[node.parent[i]])
        print node.name+" :"+node.parent[0]+","+node.parent[1]+","+node.parent[2]+"::"+str(node.level)+"--"+str(getDistance(node.values,goal))

# sets the goal
def setGoal(vgoal):
    global goal
    goal = vgoal
    return 0

# generates variable names for the inputs
def getVarName(index):
    return "In"+chr(ord('A')+index)

# returns names for the states created by the inputs
def getStateName():
    global  combination
    return "Q"+str(combination)

# generates the values for the inputs in their canonical order
def getVarVals(vcount, index):
    arr = []
    combins = pow(2, vcount)
    dif = pow(2, index+1)
    shift = combins/dif
    zero = False
    # creates an array of bits in canonical order
    for i in range(combins):
        if 0==i%shift:
            zero = not zero
        if zero:
            arr.append(0)
        else:
            arr.append(1)
    return arr

# multiplexes the given sequence of bit values
def multiplex(first, second, switch):
    global nodes
    global goal
    arr = []
    worth = True
    change = True
    # simply the multiplexing logic
    for i in range(len(switch.values)):
        if(0 == switch.values[i]):
            arr.append(first.values[i])
        else:
            arr.append(second.values[i])

    if getKey(arr) in cache1:
        return  None

    level = first.level + second.level + switch.level + 1

    return InputData(getStateName(), [first.name, second.name, switch.name], arr, level, getDistance(arr,goal))

# checks the change (distance) between given sequence of bits
def getDistance(current, base):
    dist = 0;
    for i in range(len(current)):
        if current[i]!= base[i]:
            dist+=1
    return dist


