def base_heuristic(_pancake_state):
    """
    :param _pancake_state: gets as input a pancake_state and returns its base heuristic
    :rtype: int
    """
    pancake_state_dict = _pancake_state.get_state_dict()
    output = 0
    panlength = _pancake_state.get_state_length()

    encounterMismatchNumber = False
    for index,num in pancake_state_dict.items():
        if num != panlength - index:
            encounterMismatchNumber = True
        if encounterMismatchNumber:
            output += num
    return output

def advanced_heuristic(_pancake_state):
    """
    :param _pancake_state: gets as input a pancake_state and returns its improved heuristic
    :rtype: int
    """
    pancake_state_dict = _pancake_state.get_state_dict()
    output = 0
    if pancake_state_dict[0] != _pancake_state.get_state_length():
        output += pancake_state_dict[0]

    for index in range(_pancake_state.get_state_length()-1):
        if abs(pancake_state_dict[index] - pancake_state_dict[index+1]) > 1:
            output += pancake_state_dict[index] + pancake_state_dict[index+1]

    return output

def zero_hueristics(_pancake_state):
    return 0