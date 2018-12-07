import numpy as np

def get_policy(Q):
    """
    Return the optimal policy using the provided Q function (represented as a matrix).
    The optimal action a for a state s is the action that with the highest value for
    that state.

    Arguments:
        Q (np.array): 2D array of shape (|S|, |A|) where Q[s, a] is the value of being
            at a state s and taking action a

    Returns:
        policy (list): List of optimal actions, such that policy[i] is the action
            to be taken from state i
    """
    policy = np.argmax(Q, axis=1)
    return policy.tolist()



def get_policy_4D(Q):
    """
    Return the optimal policy using the provided Q function (represented as a matrix).
    The optimal action a for a state s is the action that with the highest value for
    that state.

    Arguments:
        Q (np.array): 4D array 
    Returns:
        policy: Matrix of optimal actions, such that optimal action of state (days left, demand level and tickets left) is given by policy[days_left-1, demand_level-100, tickets_left-1]
    """
    policy = np.argmax(Q, axis=3)
    return policy
