__author__ = 'dinal'

# InputData has the properties for the nodes in the search tree
# It has fields for considering parent and values
# Depending on its distance from its parents measures the worth
# Level stands for how many parent inputs it had eg:InA is level 0
class InputData(object):
    def __init__(self, name, parents, values, level, dist):
        self.name = name
        self.parent = parents
        self.values = values
        self.level = level
        self.dist = dist
