from time import sleep
from mcts_bot import mcts_act
from stratego_env import StrategoMultiAgentEnv, ObservationModes, GameVersions



def pve(human_player_num_, env, config, obs):

    # config['vs_human'] = True
    # config['human_player_num'] = 1
    # config['human_web_gui_port'] = 7000


    # env = StrategoMultiAgentEnv(env_config=config)

    print(
        f"Visit \nhttp://localhost:{config['human_web_gui_port']}?player={config['human_player_num']} on a web browser")
    env_agent_player_num = config['human_player_num'] * -1

    number_of_games = 1
    for _ in range(number_of_games):
        print("New Game Started")
        obs = env.reset()
        while True:

            assert len(obs.keys()) == 1
            current_player = list(obs.keys())[0]
            assert current_player == env_agent_player_num

            current_player_action = mcts_act(config, env, obs)

            obs, rew, done, info = env.step(
                action_dict={current_player: current_player_action})
            print(f"Player {current_player} made move {current_player_action}")

            if done["__all__"]:
                print(
                    f"Game Finished, player {env_agent_player_num} rew: {rew[env_agent_player_num]}")
                break
            else:
                assert all(r == 0.0 for r in rew.values())
    if(rew[env_agent_player_num] > 0.5):
        return -1
    else:
        return 1
