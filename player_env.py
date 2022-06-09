import argparse
from pve import pve
from pvp_2 import pvp
from src import mcGame

# TODO make an actual function which plays the games.
def playGame(player1, player2, score, startingDifference):
    # score[0] += 1
    if(player1 != "human" and player2 == "human"):
        temp = pve(1)
        if(temp == 1):
            score[0] += 1
        elif(temp == -1):
            score[1] += 1
        return score
    elif(player1 == "human" and player2 != "human"):
        temp = pve(-1)
        if(temp == 1):
            score[0] += 1
        elif(temp == -1):
            score[1] += 1
    elif(player1 == "human" and player2 == "human"):
        temp = pvp()
        if(temp == 1):
            score[0] += 1
        elif(temp == -1):
            score[1] += 1
    else:
        temp = mcGame()
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
        # Function by Luuk
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
        while not (player2 == "hardBot" or player2 == "easyBot"): 
            print("Against what bot would you like to play?")
            player2 = input("Enter hard or easy: ") + "Bot"
    elif test == "eve":
        player1 = "easyBot"
        player2 = "easyBot"
    else:
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
    player1 = "hardBot" if args.testing else "human" 
    startGame(player1, player2, nrofgames, useComeback)