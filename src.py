import numpy as np

from mcts_bot import mcts_act
from rnd_bot import random_act
from stratego_env import StrategoMultiAgentEnv, ObservationModes, GameVersions
from evaluate_board import eval_end_pos
from save_load import load_state, save_state

if __name__ == '__main__':
    config = {
        'version': GameVersions.STANDARD,
        'random_player_assignment': False,
        'human_inits': True,
        'observation_mode': ObservationModes.PARTIALLY_OBSERVABLE,
    }
    print_board = False

    

    env = StrategoMultiAgentEnv(env_config=config)

    number_of_games = 1
    wons = [0, 0]
    for _ in range(number_of_games):
        print("New Game Started")
        obs = env.reset()
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
                current_player_action = random_act(obs)

            obs, rew, done, info = env.step(
                action_dict={current_player: current_player_action})
            
            if(print_board):
                print(f"Player {current_player} made move {current_player_action}")
            
            # print((obs["partial_observation"]))
            # time.sleep(599)

            if done["__all__"]:
                print(
                    f"Game Finished, player 1 rew: {rew[1]}, player -1 rew: {rew[-1]}")
                scores = eval_end_pos(env)
                save_state(env.state, "test.pickle")
                print(scores)
                if rew[1] == 1.0:
                    wons[0] += 1
                elif rew[-1] == 1.0:
                    wons[1] += 1
                break
            else:
                assert all(r == 0.0 for r in rew.values())
    print(wons)
