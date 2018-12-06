import json
from numpy.random import uniform, seed
from numpy import floor
from collections import namedtuple

def _tickets_sold(p, demand_level, max_qty):
        quantity_demanded = floor(max(0, demand_level - p))
        return min(quantity_demanded, max_qty)

def simulate_single_action(days_left, demand_level, tickets_to_sell, price, verbose=False):
    """
    Simulates the action of setting the flight price to p for the current
    state of days left, tickets left, and demand level.

    Arguments:
        days_left (int): Number of days left before flight (in range [0, 100])
        demand_level (int): Arbitrary level of flight demand (in range [100, 200])
        tickets_to_sell (int): Tickets left to sell
        price (int): Price set based on state (action)
        verbose (bool): Whether to print simulation output or not

    Returns:
        revenue (int): Revenue made based on state and action (reward)
        tickets_left (int): Number of tickets left to sell after action (new state)
    """
    if (days_left == 0) or (tickets_to_sell == 0):
        if verbose:
            if (days_left == 0):
                print("The flight took off today. ")
            if (tickets_to_sell == 0):
                print("This flight is booked full.")
            print("Total Revenue: ${:.0f}".format(rev_to_date))
        return 0
    else:
        tickets_sold = _tickets_sold(price, demand_level, tickets_to_sell)
        if verbose:
            print("{:.0f} days before flight: "
                  "Started with {:.0f} seats. "
                  "Demand level: {:.0f}. "
                  "Price set to ${:.0f}. "
                  "Sold {:.0f} tickets. "
                  "Daily revenue is {:.0f}. Total revenue-to-date is {:.0f}. "
                  "{:.0f} seats remaining".format(days_left, tickets_to_sell, demand_level, p, tickets_sold, p*tickets_sold, p*tickets_sold+rev_to_date, tickets_to_sell-tickets_sold))

        revenue = tickets_sold * price
        tickets_left = tickets_to_sell - tickets_sold
        return (revenue, tickets_left)

def _save_score(score):
    message = {
        'jupyterEvent': 'custom.exercise_interaction',
        'data': {
            'learnTutorialId': 0,
            'interactionType': "check",
            'questionId': 'Aug31OptimizationChallenge',
            'outcomeType': 'Pass',
            'valueTowardsCompletion': score/10000,
            'failureMessage': None,
            'learnToolsVersion': "Testing"
        }
    }
    js = 'parent.postMessage(%s, "*")' % json.dumps(message)
    display(Javascript(js))

def score_me(pricing_function, sims_per_scenario=200):
    seed(0)
    Scenario = namedtuple('Scenario', 'n_days n_tickets')
    scenarios = [Scenario(n_days=100, n_tickets=100),
                 Scenario(n_days=14, n_tickets=50),
                 Scenario(n_days=2, n_tickets=20),
                Scenario(n_days=1, n_tickets=3),
                 ]
    scenario_scores = []
    for s in scenarios:
        scenario_score = sum(simulate_revenue(s.n_days, s.n_tickets, pricing_function)
                                     for _ in range(sims_per_scenario)) / sims_per_scenario
        print("Ran {:.0f} flights starting {:.0f} days before flight with {:.0f} tickets. "
              "Average revenue: ${:.0f}".format(sims_per_scenario,
                                                s.n_days,
                                                s.n_tickets,
                                                scenario_score))
        scenario_scores.append(scenario_score)
    score = sum(scenario_scores) / len(scenario_scores)
    try:
        _save_score(score)
    except:
        pass
    print("Average revenue across all flights is ${:.0f}".format(score))
