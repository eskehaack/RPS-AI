from typing import DefaultDict
import numpy as np
import random
import matplotlib.pyplot as plt

'''
In this version of the code you can play against the AI yourself and se if you can beat it. Maybe try doing this before looking at the code too much.
When the game is quit some statistics will appear on the screen.
'''

# CONTROLS
# Tie point
tie_point = 0

# Propabiliy of random act
epsillon = 1.0

# Discount on epsillon
gamma = 0.9

# Learning rate
alpha = 0.1

# Reward
reward = 0.1

# Amount of games the AI looks back (in states), to make its decision
lookback_amount = 2

# INITIALIZATION
# Initializing points and game statistics 
AI_points,human_points,total_games,ties,count,game_val = 0,0,0,0,0,0
rest_actions = random.sample(range(3), 2)

# q-table initialization
q_values = DefaultDict(lambda: [0.33,0.33,0.33])

# Arrays to collect statistics for plots
x,y,y1 = np.array([]),np.array([]),np.array([])

# DICTIONARIES
# Translating number to common known action name
print_dict = {0 : "ROCK",
              1 : "PAPER",
              2 : "SCISSORS",
             -1 : "Quit"}

# Translate number to name for q_values-dictionary
rps_dict = {0 : "r",
            1 : "p",
            2 : "s"}

# Value for centering print-statements in console
center_val = 60

# Matrix for determine a win and a loss         
point_matrix = [[tie_point,-1,1],
                [1,tie_point,-1],
                [-1,1,tie_point]]

# Function to translate input numbers to string for q_values-dictionary
def get_row(old_inputs):
    input_list = []
    for action_sets in old_inputs:
        for action in action_sets:
            input_list.append(rps_dict[action])
    input_str = "".join(input_list)
    return input_str

# Function for updating the rows of the q-dictionary
def update_table(action1,action2,old_actions):
    global q_values
    value = q_values[get_row(old_actions)][action2]
    new_value = value + alpha * point_matrix[action2][action1] * ((reward) + gamma * np.max(state_row)-value)
    q_values[get_row(old_actions)][action2] = new_value

#Function for getting input from a human user
def human_input():
    print("- - - - - - - -")
    print("CHOOSE OPTION")
    print("(1) ROCK")
    print("(2) PAPER")
    print("(3) SCISSORS")
    print("(0) Quit")
    print("     ")
    
    # checking for valid input
    while True:
        try:
            # creating user input
            action = int(input("Choose an option: "))
            if action < 0 or action > 3:
                print("Please enter a integer between 0 and 3.")
                continue
        # checking if input is an integer
        except ValueError:
            print("Please enter an integer.")
            continue
        # breaking while loop if input is valid
        else:
            break
    action -= 1
    return action

# Starting with a random set of pre actions to initialize the update function
old_actions = []
for i in range(lookback_amount):
    old_actions.append(random.sample(range(3), 2))


#Function for getting the best AI-action (the brains of the beast)
def ai_input(): 
    #AI action
    number = random.random()
    #AI random action or rewardbased action
    if epsillon >= number:
        #random action
        action = random.randint(0,2)
    else:
        #finding the index om max-values
        state_row_saved = q_values[get_row(old_actions)]
        equal_max_val = [i for i, j in enumerate(state_row_saved) if j == max(state_row_saved)]
            
        #if the state has multiple max value actions
        if len(equal_max_val) > 1:
            action = random.choice(equal_max_val)
        else:
            action = equal_max_val[0]
    return action
        
#------------------------WHILE-LOOP-RUNNING-GAME----------------------------
while True:
    
    action1 = human_input()
    
    # if quit is chosen the while-loop ends
    if action1 == -1:
        break

    # Defining action2, usually the AI
    action2 = ai_input()

    # Updating epsillon (the probability of a random action from the AI)
    epsillon = epsillon * gamma
    
    # Point system (did the AI win or not?)
    game_val = point_matrix[action2][action1]
    
    # VALUE UPDATES
    # Saving a copy of the given state for further use
    state_row = np.copy(q_values[get_row(old_actions)])
    
    # Removing the actions the AI didnt make
    rest_actions = [0,1,2]
    rest_actions.pop(action2)
    
    # Update all three values of the table according to wether or not the AI won
    update_table(action1,action2,old_actions)
    update_table(action1,rest_actions[0],old_actions)
    update_table(action1,rest_actions[1],old_actions)
    
    # Saving the actions for this round for calculations in the next round
    old_actions.append([action2,action1])
    del old_actions[0] # Delete first element, so that we only look at a certain amount of previous games
    
    
    # PLOTTING AND STATISTICS
    
    # Prints for human players, and some statistics for the game (prints might be commented out)
    
    if game_val == 1:
        AI_points += 1
        print("-- AI wins --".center(center_val))
        
    elif game_val == -1:
        human_points += 1
        print("-- Human wins --".center(center_val))
    elif game_val == tie_point:
        ties += 1
        print("-- Tie --".center(center_val))
    total_games += 1
    
    print("*** Actions ***".center(center_val))
    
    text ="AI: " + print_dict[action2]
    print(text.center(center_val))
    text ="Human: " + print_dict[action1]
    print(text.center(center_val))
    print("       ")
    
    
    print("*** Score ***".center(center_val))
    text = "AI points: " + str(AI_points)
    print(text.center(center_val))
    text ="Human points: " + str(human_points)
    print(text.center(center_val))
    text ="Ties: " + str(ties)
    print(text.center(center_val))
    print("       ")
    text ="Total number of games: " + str(total_games)
    print(text.center(center_val))
    print("       ")
    # Calculations for the plots and statistics
    AI_x = AI_points/total_games
    human_x = human_points/total_games
    
    # Appending values to arrays
    y = np.append(y, AI_x)     
    y1 = np.append(y1, human_x)


x = np.linspace(0,total_games,total_games,endpoint=True)


# Formatting and printing q-table
q_table = np.array(list(q_values.items()), dtype = object)




# Exiting plots
plt.style.use('seaborn-deep')
fig,(ax1, ax2) = plt.subplots(2)
fig.suptitle('Subplots (1. AI, 2. Human)')
ax1.plot(x, y)    
ax2.plot(x,y1,'-.')
plt.show()

print("The game has been quit.")
