from search_node import search_node
import heapq


def create_open_set():
    class open_set():
        def __init__(self):
            self.heap = []
            self.dict = {}

        def add(self, vn):
            heapq.heappush(self.heap, vn)
            self.dict[vn.state] = vn.g

        def getG(self, vn):
            return self.dict[vn.state]

        def getBest(self):
            item = heapq.heappop(self.heap)
            #del self.dict[item.state]
            return item
        def __contains__(self, vn):
            return vn.state in self.dict

        def __bool__(self):
            return bool(self.heap)

        def __len__(self):
            return len(self.heap)
    return open_set()


def create_closed_set():
    """
    creates a set for the closed nodes
    :rtype: set
    """
    return set()


def add_to_open(vn, open_set):
    """
    adds a node to the open set
    :param vn: a node to be added
    :param open_set: the open_set that getting added the new node
    """
    open_set.add(vn)


def open_not_empty(open_set):
    """
    :param open_set: the open_set that getting
    :return: boolean if the set is empty
    """
    return bool(open_set)


def get_best(open_set):
    return open_set.getBest()



def add_to_closed(vn, closed_set):
    """
    adds a node to the closed set
    :param vn: a node
    :param closed_set: a set of nodes
    """
    closed_set.add(vn)


# returns False if curr_neighbor state not in open_set or has a lower g from the node in open_set
# remove the node with the higher g from open_set (if exists)
def duplicate_in_open(vn, open_set):
    if not open_set.__contains__(vn):
        return False
    return open_set.getG(vn) <= vn.g


# returns False if curr_neighbor state not in closed_set or has a lower g from the node in closed_set
# remove the node with the higher g from closed_set (if exists)
def duplicate_in_closed(vn, closed_set):
    if not closed_set.__contains__(vn):
        return False
    return closed_set.getG(vn) <= vn.g

def print_path(path):
    for i in range(len(path) - 1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.state_str)


def search(start_state, heuristic, goal_state):

    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)

        if current.state.get_state_str() == goal_state:
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)

        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_open(curr_neighbor, open_set) and not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set)

    return None