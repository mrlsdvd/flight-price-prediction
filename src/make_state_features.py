

def create_state(days_left, demand_level, tickets_to_sell):
    """
    Creates an integer-value state from flight information

    Arguments:
        days_left (int): Number of days left before flight (in range [1, 100])
        demand_level (int): Arbitrary level of flight demand (in range [100, 199])
        tickets_to_sell (int): Tickets left to sell (in range [1,100])

    Returns:
        state (int): Integer representing the state (in range [0, 999999])
    """
    days_left = (days_left - 1)  # Put in range [0, 99]
    demand_level = (demand_level - 100) * 100  # put in range [100, 9900]
    tickets_to_sell = (tickets_to_sell - 1) * 10000  # put in range [10000, 990000]
    state = int(days_left + demand_level + tickets_to_sell)

    return state
