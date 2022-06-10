import numpy as np

from mcts_bot import mcts_act
from rnd_bot import random_act
from stratego_env import StrategoMultiAgentEnv, ObservationModes, GameVersions
from evaluate_board import eval_end_pos
from save_load import load_state, save_state

def mcGame(env, obs, config):
    
    print_board = False
    wons = [0, 0]
    
    print("New Game Started")
    
    # env.base_env.print_board_to_console(env.state)
    save_state(env.state, "start_test.pickle")
    while True:
        assert len(obs.keys()) == 1
        current_player = list(obs.keys())[0]
        assert current_player == 1 or current_player == -1
        if(print_board):
            env.base_env.print_board_to_console(env.state)

        if current_player == 1:
            current_player_action = mcts_act(config, env, obs)
        else:
            current_player_action = mcts_act(config, env, obs)

        obs, rew, done, info = env.step(
            action_dict={current_player: current_player_action})
        
        # if(print_board):
        # print(f"Player {current_player} made move {current_player_action}")
        
        # print((obs["partial_observation"]))
        # time.sleep(599)

        if done["__all__"]:
            print(
                f"Game Finished, player 1 rew: {rew[1]}, player -1 rew: {rew[-1]}")
            # scores = eval_end_pos(env)
            # save_state(env.state, "test.pickle")
            if rew[1] == 1.0:
                wons[0] += 1
            elif rew[-1] == 1.0:
                wons[1] += 1
            break
        else:
            assert all(r == 0.0 for r in rew.values())
    # print(wons)
    if(wons[0] == 1):
        return 1
    else:
        return -1