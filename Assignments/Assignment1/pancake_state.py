import math

from heuristics import advanced_heuristic


class pancake_state:

    def __init__(self, state_str):
        self._dict = None
        self._length = None
        self.state_str = state_str

    def setFields(self, dictInput, length):
        self._dict = dictInput
        self._length = length

    # returns an array of tuples of neighbor states and the cost to reach them: [(pancake_state1, cost1), (pancake _state2, cost2)...]
    def get_neighbors(self):
        """
        :rtype: list of tuples with the state and the cost
        """
        neighbors = list()

        for i in range(self._length - 1):  # minus 1 because we don't want self edge
            cost = 0
            length = self.get_state_length()
            dict = self.get_state_dict()
            neighbor_dict = self._dict.copy()  # the same values until i and reverse it
            for j in range((length - i) // 2):
                cost += neighbor_dict[i + j] + neighbor_dict[length - 1 - j]
                neighbor_dict[i + j], neighbor_dict[length - 1 - j] = neighbor_dict[length - 1 - j], \
                neighbor_dict[i + j]
            if (length - i) % 2 == 1:
                cost += neighbor_dict[i + (length - i) // 2]
            neighbor_state = pancake_state(",".join(map(str, neighbor_dict.values())))
            neighbor_state.setFields(neighbor_dict, length)
            neighbors.append((neighbor_state, cost))
        return neighbors

    # you can change the body of the function if you want
    def __hash__(self):
        return hash(self.state_str)

    # you can change the body of the function if you want
    def __eq__(self, other):
        return self.state_str == other.state_str

    def get_state_str(self):
        return self.state_str

    def get_state_dict(self):
        if not self._dict:
            self._dict = {index: int(pancake) for index, pancake in enumerate(self.state_str.split(","))}
        return self._dict

    def get_state_length(self):
        if not self._length:
            self._length = len(self.get_state_dict().keys())
        return self._length

    def __str__(self):
        return self.state_str