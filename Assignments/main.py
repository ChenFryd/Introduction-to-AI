from search import search
from pancake_state import pancake_state
from heuristics import *
import timeit

if __name__ == '__main__':
    goal_state = "9,8,7,6,5,4,3,2,1"
    pancake_input = "5,2,1,9,7,6,3,4,8"
    pancake_state = pancake_state(pancake_input)

    # Measure execution time for base heuristic search
    start_time_base = timeit.default_timer()
    search_result = search(pancake_state, base_heuristic, goal_state)
    end_time_base = timeit.default_timer()
    print("Base Heuristic Search Time:", end_time_base - start_time_base)

    # Print base heuristic search results
    for i in search_result:
        print(i)


    # Measure execution time for advanced heuristic search
    start_time_adv = timeit.default_timer()
    search_resultAdv = search(pancake_state, advanced_heuristic, goal_state)
    end_time_adv = timeit.default_timer()
    print("Advanced Heuristic Search Time:", end_time_adv - start_time_adv)

    # Print advanced heuristic search results
    for i in search_resultAdv:
        print(i)
    print("----------")
