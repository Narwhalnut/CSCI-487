import random

# Date edited in simulation.
# General
REWARD_PROBABILITIES = [0.1, 0.5, 0.8, 0.95];
CORRECT = 3;
STEP_SIZES = [0.1,0.05,0.02,0.01];
# For PLA
action_count = [0,0,0,0];
estimated_reward_probabilities = [0, 0, 0, 0];

# Simulates machine learning for the given parameters.
def simulate_reinforcement_learning(is_pla, step_size):
    # clear data.
    best_action = -1;
    keep_going = True;
    if is_pla:
        action_count = [0,0,0,0];
        estimated_reward_probabilities = [0, 0, 0, 0];

    # 1. The action probabilities are initialized to 1/n.
    action_probabilities = [0.25,0.25,0.25,0.25];

    while (keep_going):
        # Keep going until action proabilities converge.

        # 2. The agent randomly chooses an action by sampling the action rates.
        random_float = random.random();
        lower_bound = 0.0;
        action_index = -1;
        for i in range(len(action_probabilities)):
            lower_bound += action_probabilities[i];
            if random_float < lower_bound:
                action_index = i;
                break;

        # 3. Generate feedback by randomly sampling the reward probabilties.
            # if y (PRN) < d_i, the environment generates a feedback of 1.
        random_float = random.random();
        success_probability = REWARD_PROBABILITIES[action_index];
        success = (random_float < success_probability);

        # 4. Update the action proabilities based on the algorithm.
        if is_pla:
            count = action_count[action_index];
            # Track how many times each action has been chosen.
            action_count[action_index] += 1;
            # Set the estimated reward probability.
            e_r_p = estimated_reward_probabilities[action_index];
            estimated_reward_probabilities[action_index] = (count * e_r_p + success) / (count + 1);
            # Find the maximum reward probability estimate.
            index_of_maximum = 0;
            for i in range(len(estimated_reward_probabilities)):
                if i != 0:
                    if estimated_reward_probabilities[i] > estimated_reward_probabilities[index_of_maximum]:
                        index_of_maximum = i;
            # Reinforce the maximum reward probability estimate.
            for i in range(len(action_probabilities)):
                if i == index_of_maximum:
                    # Increase the action probility of the highest reward probability action.
                    action_probabilities[i] += step_size * (1 - action_probabilities[i]);
                else:
                    # Scale the other action proabilities to match.
                    action_probabilities[i] -= step_size * action_probabilities[i];
        else:
            if success:
                for i in range(len(action_probabilities)):
                    if i == action_index:
                        # Increase the action probility of the successful action.
                        action_probabilities[i] += step_size * (1 - action_probabilities[i]);
                    else:
                        # Scale the other action proabilities to match.
                        action_probabilities[i] -= step_size * action_probabilities[i];
        
        # 5. Continue until the action probabilites converge (some action reaches 0.9)
        for i in range(len(action_probabilities)):
            if action_probabilities[i] >= 0.9:
                best_action = i;
                keep_going = False;
                break;
    # Return the decision
    return best_action;

# Runs 100 instances of the simulation and returns accuracy percentage.
def trial(is_pla, step_size):
    accurate_trials = 0;
    for trials in range(100):
        best_action = simulate_reinforcement_learning(is_pla, step_size);
        if best_action == CORRECT:
            accurate_trials += 1;
    return (accurate_trials / 100);

def main():
    is_pla = False;
    step_size = STEP_SIZES[0];
    
    # Trial each step size and obtain accuracy.
    for i in range(len(STEP_SIZES)):
        step_size = STEP_SIZES[i];
        print("step size: " + str(step_size));
        accuracy = trial(False, step_size);
        print("  accuracy: " + str(accuracy));

if __name__ == "__main__":
    main();

