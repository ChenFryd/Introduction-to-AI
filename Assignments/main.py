import time

from search import search
from pancake_state import pancake_state
from heuristics import *

if __name__ == '__main__':
    # goal_state = "4,3,2,1"
    # pancake_input = "4,2,3,1"
    # pancake_state = pancake_state(pancake_input)
    # search_result = search(pancake_state, advanced_heuristic, goal_state)
    #
    # for node in search_result:
    #     print(node)
    start_time = time.time()
    pancake_input = "6,4,2,7,5,3,8,1"
    goal_state = "8,7,6,5,4,3,2,1"
    pancake_state = pancake_state(pancake_input)
    search_result = search(pancake_state, advanced_heuristic, goal_state)

    for node in search_result:
        print(node)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

