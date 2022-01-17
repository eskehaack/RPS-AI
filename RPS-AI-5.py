from typing import DefaultDict
import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm import tqdm


#random.seed(10) #AHHHHHHHHHHHHHHHHHHHHHHHHHHHH

# CONTROLS
# Tie point
tie_point = 0 #-0.5

# Propabiliy of random act
epsillon = 1.0 #1.0

# Discount on epsillon
gamma = 0.9 #0.9

# Learning rate
alpha = 0.1 #0.1

# Reward
reward = 0.1 #0.5

# Amount of games the AI looks back, to make its decision
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

# Starting with a random set of pre actions to initialize the update function
old_actions = []
for i in range(lookback_amount):
    old_actions.append(random.sample(range(3), 2))


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

# BOTS FOR GATHERING STATISTICS
# A super dumb bot for early testing
def super_dumb_bot():
    return 1

def bot_i(old_actions):
    move = old_actions[-1][0]
    return move

def bot_ii(game_val, rest_actions):
    if game_val == -1:
        move = old_actions[-1][1]
    elif game_val == 1:
        move = old_actions[-1][0]
    else:
        move = random.choice(rest_actions)
    return move

def bot_iii(game_val, rest_actions):
    if game_val == -1:
        move = old_actions[-1][0]
    elif game_val == 1:
        move = old_actions[-1][1]
    else:
        move = random.choice(rest_actions)
    return move

def bot_iv(i,game_val, rest_actions):
    global count
    if count > 149:
        count = 0
    if count < 50:
        move = bot_v(i)
    elif count < 100:
        move = bot_ii(game_val, rest_actions)
    elif count < 150:
        move = bot_iii(game_val, rest_actions)
    count += 1
    return move

# A human like bot for testing the AI
dummy_moves =[random.randint(0,2),random.randint(0,2)]

def bot_v(i):
    global dummy_moves
    
    if i > 0 and i % 5 == 0:
        dummy_moves = random.sample(range(0,3),2)
    if i == 0 or (i > 0 and i % 2 == 0):
        current_move = dummy_moves[0]
    else:
        current_move = dummy_moves[1]
    return current_move

def bot_vi(i):
    global dummy_moves
    
    if i == 0:
        current_move = random.choice([0,1,2])
    elif AI_points-human_points <= 5 and game_val == -1:
        current_move = old_actions[1][1]
    elif AI_points-human_points > 5 and game_val == -1:
        current_move = old_actions[1][0]
    elif AI_points-human_points > 5 and game_val == 1:
        current_move = old_actions[0][random.choice([0,1])]
    elif game_val == -0.5:
        current_move = old_actions[0][1]
    elif game_val == 1:
        current_move = old_actions[random.choice([0,1])][0]
    else:
        current_move = random.choice([0,1,2])
    return current_move


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

for i in range(400):
    AI_points,human_points,total_games,ties,count,game_val = 0,0,0,0,0,0
    rest_actions = random.sample(range(3), 2)

    # q-table initialization
    q_values = DefaultDict(lambda: [0.33,0.33,0.33])         
#------------------------WHILE-LOOP-RUNNING-GAME----------------------------
    while total_games < 150:
        
        #Defining action1, could be a human input or one of the bots
        # if i == 0:
        #     action1 = bot_i(old_actions)
        # if i == 1:
        #     action1 = bot_ii(game_val,rest_actions)
        # if i == 2:
        #     action1 = bot_iii(game_val,rest_actions)
        # if i == 3:
        #     action1 = bot_iv(total_games,game_val,rest_actions)
        # if i == 4:
        #     action1 = bot_v(total_games)
        # if i == 5:
        #     action1 = bot_vi(total_games)           
        # if i == 6:
        #     action1 = super_dumb_bot()
        
        action1 = super_dumb_bot()
        
        #action1 = human_input()
        
        #if quit is chosen the while-loop ends
        # if action1 == -1:
        #     break

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
        #print("AI-played:", print_dict[action2])
        #print("Game nr.", total_games)
        if game_val == 1:
            AI_points += 1
            #print("-- AI wins --")
        elif game_val == -1:
            human_points += 1
            #print("-- Human wins --")
        elif game_val == tie_point:
            ties += 1
            #print("-- Tie --")
        #if total_games > 148:
            #print("SSSSSTTTTTOOOOOOOOPPPPPPPPP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            
        total_games += 1
        
        # Calculations for the plots and statistics
        AI_x = AI_points/total_games
        human_x = human_points/total_games
        
        # Appending values to arrays
        #x = np.append(x, total_games)
        #if game_val == 1:
        #y = np.append(y, AI_x)
        #else:
            #y = np.append(y, 0)        
            
        # if game_val == -1:
        #     y1 = np.append(y1, 100)
        # else:
        #     y1 = np.append(y1, 0)

    print(AI_points,human_points,ties)
    # if i == 0:
    #     bot_i_wins = np.copy(y)
    #     y = np.array([])
    # if i == 1:
    #     bot_ii_wins = np.copy(y)
    #     y = np.array([])
    # if i == 2:
    #     bot_iii_wins = np.copy(y)
    #     y = np.array([])
    # if i == 3:
    #     bot_iv_wins = np.copy(y)
    #     y = np.array([])
    # if i == 4:
    #     bot_v_wins = np.copy(y)
    #     y = np.array([])
    # if i == 5:
    #     bot_vi_wins = np.copy(y)
    #     y = np.array([])
    # if i == 6:
    #     super_dumb_bot_wins = np.copy(y)
    #     y = np.array([])

# x = np.linspace(0,total_games,total_games,endpoint=True)
# bundlinje = np.full(total_games,1/3)

# cumsumlen = round(total_games/100)

# def move_avg_bot(bot):
#     move_avg_bot = np.convolve(bot, np.ones(cumsumlen), mode='same')/cumsumlen
#     move_avg_bot = np.delete(move_avg_bot, np.s_[len(move_avg_bot)-cumsumlen:])
#     move_avg_bot = np.delete(move_avg_bot, np.s_[:cumsumlen])
#     return move_avg_bot


# move_avg_bot_i = move_avg_bot(bot_i_wins)
# move_avg_bot_ii = move_avg_bot(bot_ii_wins)
# move_avg_bot_iii = move_avg_bot(bot_iii_wins)
# move_avg_bot_iv = move_avg_bot(bot_iv_wins)
# move_avg_bot_v = move_avg_bot(bot_v_wins)
# move_avg_bot_vi = move_avg_bot(bot_vi_wins)
# move_avg_super_dumb_bot = move_avg_bot(super_dumb_bot_wins)
# x = np.delete(x, np.s_[len(x)-cumsumlen:])
# x = np.delete(x, np.s_[:cumsumlen])
# bundlinje = np.delete(bundlinje, np.s_[len(bundlinje)-cumsumlen:])
# bundlinje = np.delete(bundlinje, np.s_[:cumsumlen])

# Exiting prints for score and statistics    
#printing actions
# print("*** Actions ***".center(center_val))
# text ="AI: " + print_dict[action2]
# print(text.center(center_val))
# text ="Human: " + print_dict[action1]
# print(text.center(center_val))
# print("       ")


# print("*** Score ***".center(center_val))
# text = "AI points: " + str(AI_points)
# print(text.center(center_val))
# text ="Human points: " + str(human_points)
# print(text.center(center_val))
# text ="Ties: " + str(ties)
# print(text.center(center_val))
# print("       ")
# text ="Total number of games: " + str(total_games)
# print(text.center(center_val))
# print("       ")
#print(q_values)
#print(reward,alpha)
#print("Max value:", max_value, optimized_value)

# Exiting plots
# fig,(ax1, ax2) = plt.subplots(2)
# fig.suptitle('Subplots (1. AI, 2. Human), human trials' )
# plt.style.use('seaborn-deep')
# plt.plot(x, move_avg_bot_i, label = "bot_i")  
# plt.plot(x, move_avg_bot_ii, label = "bot_ii") 
# plt.plot(x, move_avg_bot_iii, label = "bot_iii") 
# plt.plot(x, move_avg_bot_iv, label = "bot_iv") 
# plt.plot(x, move_avg_bot_v, label = "bot_v") 
# plt.plot(x, move_avg_bot_vi, label = "bot_vi")
# plt.plot(x, move_avg_super_dumb_bot,'g', label = "super_dumb_bot")
# plt.plot(x, bundlinje,'r', label = "Bundlinje")
# plt.legend()
# plt.legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)
# plt.subplots_adjust(right=0.7)
# plt.title("Winrate for AI against human-like bots\nRolling average")
# plt.xlabel("Games played")
# plt.ylabel("Percentage won")
# plt.show()

print("The game has been quit.")