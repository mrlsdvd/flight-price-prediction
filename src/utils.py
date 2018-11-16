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
