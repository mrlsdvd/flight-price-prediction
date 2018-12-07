import math
import numpy as np
import pickle
from custom_flight_revenue_simulator import simulate_single_action as take_action
from make_state_features import create_state
from make_state_features import zero_Q, demand_level_Q

def q_learning(num_states=1000000, num_actions=201, discount=0.95, lr=0.1,
               epsilon_threshold=0.1, num_iter=1000, Q=None, default_val=0,
               print_every=100000):
    """
    Performs Q-learning

    Arguments:
        num_states (int): Size of state space
        num_actions (int): Size of action space
        discount (float): Discount factor
        lr (float): Learning rate
        epsilon_threshold (float): Max epsilon thrshold to explore over exploit.
            if 0 <= epsilon <= epsilon_threshold -> explore
            if epsilon_threshold < epsilon <= 1 -> exploit
        num_iter (int): Number of iterations to run Q-learning for
        Q (np.array): Optional 2D array of shape (|S|, |A|) where Q[s, a] is
            the value of being at a state s and taking action a
        default_val (float): Optional fill value for Q
        print_every (int): Parameter detailing what iteration to report at

    Returns:
        Q_new (np.array): Updated Q
    """
    if Q is None:
        Q = np.empty((num_states, num_actions))
        Q.fill(default_val)
    epsilon_threshold = 0.3

    days_left = 100  # Begin max days_left at 100
    tickets_to_sell = 100  # Begin max tickets_to_sell at 100
    demand_level = int(math.floor(np.random.uniform(100, 200)))  # Demand level is uniformly random

    for i in range(num_iter):
        if i % print_every == 0:
            print("At iteration: {}".format(i))
        #  If end of round reached, reset days_left and tickets_to_sell
        if days_left == 0 or tickets_to_sell == 0:
            days_left = 100
            tickets_to_sell = 100

        s = create_state(days_left, demand_level, tickets_to_sell)

        epsilon = np.random.random()  # Sample random epsilon
        if epsilon > epsilon_threshold:
            a = np.argmax(Q[s])
        else:
            # Randomly choose price action between 0 and demand level
            a = int(math.floor(np.random.uniform(0, demand_level)))

        # Simlulate taking action with current state
        r, tickets_left = take_action(days_left, demand_level, tickets_to_sell, a)

        # Create next state
        demand_level = int(math.floor(np.random.uniform(100, 200)))
        days_left = days_left - 1
        tickets_to_sell = tickets_left

        if tickets_left == 0 or days_left == 1:
            # No more tickets or no more days in next state
            # Q[next_state, a] -> 0
            Q[s, a] = Q[s, a] + lr*(r - Q[s, a])
        else:
            sp = create_state(days_left, demand_level, tickets_to_sell)
            Q[s, a] = Q[s, a] + lr*(r + discount*np.max(Q[sp]) - Q[s, a])

    return Q


def q_learning_all_demand_levels(num_states=1000000, num_actions=201, discount=0.95, lr=0.1,
               epsilon_threshold=0.1, num_iter=1000, Q=None, default_val=0,
               print_every=100000):
    """
    Performs Q-learning

    Arguments:
        num_states (int): Size of state space
        num_actions (int): Size of action space
        discount (float): Discount factor
        lr (float): Learning rate
        epsilon_threshold (float): Max epsilon thrshold to explore over exploit.
            if 0 <= epsilon <= epsilon_threshold -> explore
            if epsilon_threshold < epsilon <= 1 -> exploit
        num_iter (int): Number of iterations to run Q-learning for
        Q (np.array): Optional 2D array of shape (|S|, |A|) where Q[s, a] is
            the value of being at a state s and taking action a
        default_val (float): Optional fill value for Q
        print_every (int): Parameter detailing what iteration to report at

    Returns:
        Q_new (np.array): Updated Q
    """
    if Q is None:
        Q = np.empty((num_states, num_actions))
        Q.fill(default_val)



    epsilon_threshold = 0.3

    days_left = 100  # Begin max days_left at 100
    tickets_to_sell = 100  # Begin max tickets_to_sell at 100

    for i in range(num_iter):
        if i % print_every == 0:
            print("At iteration: {}".format(i))
        #  If end of round reached, reset days_left and tickets_to_sell
        if days_left == 0 or tickets_to_sell == 0:
            days_left = 100
            tickets_to_sell = 100

        # Simlulate taking action with current state
        for demand_level in range(100, 200):
            s = create_state(days_left, demand_level, tickets_to_sell)
            epsilon = np.random.random()  # Sample random epsilon
            if epsilon > epsilon_threshold:
                a = np.argmax(Q[s])
                if np.max(Q[s]) == 0:
                    a = demand_level-1
            else:
                # Randomly choose price action
                a = int(math.floor(np.random.uniform(0, demand_level)))

            r, tickets_left = take_action(days_left, demand_level, tickets_to_sell, a)

            if tickets_left == 0 or days_left == 1:
                # No more tickets or no more days in next state
                # Q[next_state, a] -> 0
                Q[s, a] = Q[s, a] + lr*(r - Q[s, a])
            else:
                sp = create_state(days_left, demand_level, tickets_to_sell)
                Q[s, a] = Q[s, a] + lr*(r + discount*np.max(Q[sp]) - Q[s, a])

        # Create next state
        days_left = days_left - 1
        tickets_to_sell = tickets_left

    return Q


def dynamic_programming(Q=None, discount=0.95, lr=0.1, epsilon_threshold=0.1,
                        num_iter=1000, default_val=0, print_every=100000):
    for days_left in range(1, 101):
        print("days_left: {}".format(days_left))
        for demand_level in range(100, 200):
            for tickets_to_sell in range(1, 101):
                for action in range(201):

                    r, tickets_left = take_action(days_left, demand_level, tickets_to_sell, action)

                    if days_left == 1 or tickets_left == 0:
                        Q[days_left-1, demand_level-100, tickets_left-1, action] = r

                    else:
                        prev_state_avg = np.amax(Q[days_left-1, : , tickets_left-1, :], axis=1).mean()
                        Q[days_left-1, demand_level-100, tickets_left-1, action] = r + prev_state_avg


def train(num_states=1000000, num_actions=201, discount=0.95, lr=0.1,
          epsilon_threshold=0.1, num_iter=1000, Q=None, save_q=True,
    q_outfile_name="Q-5.pickle"):
#     Q = q_learning_all_demand_levels(num_iter=10000000)
    Q = q_learning(num_iter=10000000)
    # Initialize Q
    # Q = zero_Q((100, 100, 100, 201))
    # Q = demand_level_Q((100, 100, 100, 201))
    # Q = dynamic_programming(Q)
    if save_q:
        with open(q_outfile_name, 'wb') as q_f:
            pickle.dump(Q, q_f)

if __name__ == '__main__':
    train()
