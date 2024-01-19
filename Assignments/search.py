from search_node import search_node
import heapq


def create_open_set():
    new_heapq=[]
    return new_heapq


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
    heapq.heappush(open_set, vn)


def open_not_empty(open_set):
    """
    :param open_set: the open_set that getting
    :return: boolean if the set is empty
    """
    return open_set


def get_best(open_set):
    return heapq.heappop(open_set)


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
    if vn not in open_set:
        return False
    for element in open_set:
        if element == vn:
            return element.g <= vn.g
    return False


# returns False if curr_neighbor state not in closed_set or has a lower g from the node in closed_set
# remove the node with the higher g from closed_set (if exists)
def duplicate_in_closed(vn, closed_set):
    if vn not in closed_set:
        return False
    search_node = closed_set.get(vn, None)
    return search_node.g <= vn.g



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
