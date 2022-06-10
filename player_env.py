import argparse
from copy import deepcopy
from math import inf
from pve import pve
from pvp_2 import pvp
from src import mcGame
from stratego_env import StrategoMultiAgentEnv, ObservationModes, GameVersions
from evaluate_board import eval_end_pos
import numpy as np

# TODO make an actual function which plays the games.
def playGame(player1, player2, score, startingDifference):
    config = {
        'version': GameVersions.STANDARD,
        'random_player_assignment': False,
        'human_inits': True,
        'observation_mode': ObservationModes.PARTIALLY_OBSERVABLE,
    }

    # Ugly if statement, sorry
    if(player1 != "human" and player2 != "human"):
        pass
    else:
        config['vs_human'] = True
        config['human_player_num'] = 1
        config['human_web_gui_port'] = 7000
    best_env = StrategoMultiAgentEnv(env_config=config)
    best_obs = best_env.reset()

    # closest_score = -9999999
    # best_env = None
    # best_obs = None
    # print("Creating boards for comeback score, this may take a while...")
    # for i in range(5):
    #     print(f"Calculating {i+1} out of 5")
    #     env = StrategoMultiAgentEnv(env_config=config)
    #     obs = env.reset()
    #     save_env = deepcopy(env)
    #     save_obs = deepcopy(obs)
    #     end_board_scores = [[0],[0]]
    #     avg_games = 2
    #     winner = 0
    #     for i in range(avg_games):
    #         print(f"Sub calculating {i+1} out of {avg_games}")
    #         env = deepcopy(save_env)
    #         # env.base_env.print_board_to_console(env.state)
    #         # obs = env.reset()

    #         # env.base_env.print_board_to_console(env.state)
    #         # obs = deepcopy(save_obs)

    #         # env.base_env.print_board_to_console(env.state)
    #         winner_id = mcGame(env, obs, config)
    #         winner += winner_id
    #         temp_scores = eval_end_pos(env)
    #         end_board_scores[0] += [temp_scores[0]]
    #         end_board_scores[1] += [temp_scores[1]]
    #     print(np.shape(end_board_scores))
    #     comeback_score = winner + (end_board_scores[0][0] - end_board_scores[1][0]) + (end_board_scores[0][1] - end_board_scores[1][1])
    #     print(winner, end_board_scores)
    #     print(comeback_score)
    #     if(abs(startingDifference-comeback_score) < abs(startingDifference-closest_score)):
    #         closest_score = comeback_score
    #         best_env = deepcopy(save_env)
    #         best_obs = deepcopy(save_obs)

    if(player1 != "human" and player2 == "human"):
        temp = pve(1, best_env, config, best_obs)
        if(temp == 1):
            score[0] += 1
        elif(temp == -1):
            score[1] += 1
        return score
    elif(player1 == "human" and player2 != "human"):
        temp = pve(-1, best_env, config, best_obs)
        if(temp == 1):
            score[0] += 1
        elif(temp == -1):
            score[1] += 1
    elif(player1 == "human" and player2 == "human"):
        temp = pvp(best_env)
        if(temp == 1):
            score[0] += 1
        elif(temp == -1):
            score[1] += 1
    else:
        temp = mcGame(best_env, best_obs, config)
        if(temp == 1):
            score[0] += 1
        elif(temp == -1):
            score[1] += 1

    return score

def startGame(player1, player2, nrOfGames, comeback, score=[0,0]):
    
    # The checks if a player has won the entire section
    if nrOfGames == "bo3" and max(score) >= 2:
        
        if score.index(max(score)) == 0:
            print("player1: {} has won with score {}-{}, exiting the program".format(player1, score[0], score[1]))
            return
        else:
            print("player2: {} has won with score {}-{}, exiting the program".format(player2, score[0], score[1]))
            return

    if nrOfGames == "bo5" and max(score) >= 3:
        if score.index(max(score)) == 0:
            print("player1: {} has won with score {}-{}, exiting the program".format(player1, score[0], score[1]))
            return
        else:
            print("player2: {} has won with score {}-{}, exiting the program".format(player2, score[0], score[1]))
            return

    # Checking if the players want to continue playing
    print("{} v {} is currently {}-{}".format(player1, player2, score[0], score[1]))
    wait = "-"
    while not (wait=="" or wait=="q"):
        wait = input("Press enter to begin game {} or type q to stop playing: ".format(sum(score)+1))
    if wait == "q":
        return

    # Starting a new game
    ## If comeback is active calculate the starting difference.
    startingDifference = 0.0
    if comeback:
        
        pass
    ## With the difference setup the playing screens for the players
    startGame(player1, player2, nrOfGames, comeback, playGame(player1, player2, score, startingDifference))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-M","--mode", default="", help="Would you like to play player versus player or player versus bot?, options are pvp or pve")
    parser.add_argument("-B","--bot", default="", help="Against what bot would you like to play?, options are easy or hard")
    parser.add_argument("-N","--nrofgames", default="", help="How many games would you like to play?, options are bo3, bo5 or freeplay")
    parser.add_argument("-C","--comeback", action="store_true", help="Adding this option turns on the comeback mechanic between the rounds")
    parser.add_argument("-T","--testing", action="store_true", help="Adding this options lets the games be played between two bots, generally only used for testing purposes.")
    args = parser.parse_args()
    test = args.mode
    player2 = args.bot
    nrofgames = args.nrofgames
    useComeback = args.comeback
    while not (test == "pvp" or test == "pve" or test == "eve"):
        print("Would you like to play player versus player or player versus bot or watch two bots compete?") 
        test = input("Enter pvp or pve or eve: ")

    if test == "pve":
        # while not (player2 == "hardBot" or player2 == "easyBot"): 
        #     print("Against what bot would you like to play?")
        #     player2 = input("Enter hard or easy: ") + "Bot"
        player1 = "human"
        player2 = "easyBot"
    elif test == "eve":
        player1 = "easyBot"
        player2 = "easyBot"
    else:
        player1 = "human"
        player2 = "human"

    while not (nrofgames == "bo3" or nrofgames == "bo5" or nrofgames == "freeplay"):
        print("How many games would you like to play?")
        print("The options are best of 3, best of 5 or freeplay")
        nrofgames = input("Enter bo3, bo5 or freeplay: ")

    if not useComeback:
        print("Do you want to include a comeback mechanic between the rounds?")
        temp = ""
        while not(temp == "yes" or temp == "no"):
            temp = input("Enter yes or no: ")
        useComeback = (temp == "yes")

    # The parameters are:
    ## player1 = "hardBot" if testing else "human" 
    ## player2 = "human" if "pve" else "hardBot" or "easyBot"
    ## nrOfGames: nr of rounds to be played
    ## useComeback: whenether the comeback mechanic is active or not
    # player1 = "hardBot" if args.testing else "human" 
    startGame(player1, player2, nrofgames, useComeback)