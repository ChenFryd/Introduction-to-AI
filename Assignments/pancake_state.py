import math

from heuristics import advanced_heuristic


class pancake_state:

    def __init__(self, state_str):
        self.state_str = state_str
        self.dict = {index: pancake for index, pancake in enumerate(state_str.split(","))}
        self.length = len(self.dict.keys())

    # returns an array of tuples of neighbor states and the cost to reach them: [(pancake_state1, cost1), (pancake _state2, cost2)...]
    def get_neighbors(self):
        """
        :rtype: list of tuples with the state and the cost
        """
        neighbors = list()
        for i in range(self.length - 1):  # minus 1 because we don't want self edge
            #the same values until i and reverse it
            list_of_pancakes_of_next_state = [self.dict[j] for j in range(i)] + [self.dict[self.length-1-k] for k in range(self.length - i)]
            neighbor_state = pancake_state(",".join(list_of_pancakes_of_next_state))
            neighbors.append((neighbor_state,1))
        return neighbors

    # you can change the body of the function if you want
    def __hash__(self):
        return hash(self.state_str)

    # you can change the body of the function if you want
    def __eq__(self, other):
        return self.state_str == other.state_str

    def get_state_str(self):
        return self.state_str

    def __str__(self):
        return self.state_str