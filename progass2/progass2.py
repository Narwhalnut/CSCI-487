import random # Used for random float generation.
import matplotlib.pyplot as plt # Used only for generating the plots seen in the paper.

# Date edited in simulation.
# General
REWARD_PROBABILITIES = [0.19,0.2,0.21,0.59,0.6,0.61,0.72,0.41,0.39,0.4];
CORRECT = 6;
STEP_SIZES = [0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5];
RESULT = 0;
ITERATIONS = 1;
# For PLA
action_count = [0,0,0,0,0,0,0,0,0,0];
estimated_reward_probabilities = [0,0,0,0,0,0,0,0,0,0];

# Simulates machine learning for the given parameters. Returns a tuple [result, iterations].
def simulate_reinforcement_learning(is_pla, step_size):
    # clear data.
    iterations = 0;
    best_action = -1;
    keep_going = True;
    if is_pla:
        action_count = [0,0,0,0,0,0,0,0,0,0];
        estimated_reward_probabilities = [0,0,0,0,0,0,0,0,0,0];

    # 1. The action probabilities are initialized to 1/n.
    action_probabilities = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1];

    while (keep_going):
        # Keep going until action proabilities converge.
        iterations = iterations + 1;

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
    return (best_action, iterations);

# Runs 100 simulations. Returns a tuple [accuracy, iterations].
def trial(is_pla, step_size):
    accurate_trials = 0;
    iteration_total = 0;
    for trials in range(100):
        results = simulate_reinforcement_learning(is_pla, step_size);
        # Add to the accuracy count if the conclusion was correct.
        if results[RESULT] == CORRECT:
            accurate_trials += 1;
        # Track the number of iterations required.
        iteration_total += results[ITERATIONS];
    return (accurate_trials / 100, iteration_total / 100);

# Trials L-RI and PLA for various different step sizes.
def main():
    # Randomize the environment.
    random.seed()

    is_pla = False;
    step_size = STEP_SIZES[0];
    
    # L-RI
    print("L-RI");
    iterations_lri = [];
    accuracy_lri = [];
    # Trial each step size.
    for j in range(len(STEP_SIZES)):
        step_size = STEP_SIZES[j];
        results = trial(is_pla, step_size);
        print("  [" + str(step_size) + "] accuracy: " + str(results[RESULT]) + " iterations: " + str(results[ITERATIONS]));
        # Track points for the plots later.
        iterations_lri.append(results[ITERATIONS]);
        accuracy_lri.append(results[RESULT]);
    
    # PLA
    print("PLA");
    is_pla = True;
    iterations_pla = [];
    accuracy_pla = [];
    # Trial each step size.
    for j in range(len(STEP_SIZES)):
        step_size = STEP_SIZES[j];
        results= trial(is_pla, step_size);
        print("  [" + str(step_size) + "] accuracy: " + str(results[RESULT]) + " iterations: " + str(results[ITERATIONS]));
        # Track points for the plots later.
        iterations_pla.append(results[ITERATIONS]);
        accuracy_pla.append(results[RESULT]);
        
    # Make Plots
    # Accuracy
    plt.plot(STEP_SIZES, accuracy_lri, label = "L-RI");
    plt.plot(STEP_SIZES, accuracy_pla, label = "PLA");
    plt.legend();
    plt.title("Accuracy");
    plt.xlabel("Step Size");
    plt.ylabel("Accuracy");
    plt.show();
    plt.clf();
    # Speed
    plt.plot(STEP_SIZES, iterations_lri, label = "L-RI");
    plt.plot(STEP_SIZES, iterations_pla, label = "PLA");
    plt.legend();
    plt.title("Iteration Count");
    plt.xlabel("Step Size");
    plt.ylabel("Speed");
    plt.show();
        

# Execute main.
if __name__ == "__main__":
    main();