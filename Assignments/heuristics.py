def base_heuristic(_pancake_state):
    """
    :param _pancake_state: gets as input a pancake_state and returns its base heuristic
    :rtype: int
    """
    pancake_state_str = _pancake_state.get_state_str()
    # calculate hueristics
    sorted_str = sorted(pancake_state_str.split(","), reverse=True)
    output = 0
    for index, pancake_sorted in enumerate(sorted_str):
        if pancake_sorted != pancake_state_str[2*index]:
            output += int(pancake_state_str[2*index])
    return output


def advanced_heuristic(_pancake_state):
    """
    :param _pancake_state: gets as input a pancake_state and returns its improved heuristic
    :rtype: int
    """
    pancake_state_list = [int(i) for i in (_pancake_state.get_state_str()).split(',')]
    output = 0
    if pancake_state_list[0] != len(pancake_state_list):
        output += 1

    for index in range(len(pancake_state_list)-1):
        if pancake_state_list[index] != pancake_state_list[index+1] + 1:
            output += 1

    return output
