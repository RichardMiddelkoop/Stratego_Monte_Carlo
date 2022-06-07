# from stratego_env import StrategoMultiAgentEnv, ObservationModes, GameVersions
import numpy as np
INT_DTYPE_NP = np.int64
# ======================================================
# komt uit stratego_procedural_impl
# owned_pieces = new_state[_player_index(player=player)]
# enemy_pieces = new_state[_player_index(player=-player)]

# owned_po_pieces = new_state[_player_po_index(player=player)]
# enemy_po_pieces = new_state[_player_po_index(player=-player)]

# owned_still_pieces = new_state[_player_still_pieces_index(player=player)]
# enemy_still_pieces = new_state[_player_still_pieces_index(player=-player)]

"""Internal State Breakdown:
shape = (layers, rows, columns)

state layers are defined by name in the StateLayers enum.

layers:
0: player 1 ground truth pieces (contents are SP enum types and CAN'T be UNKNOWN)
1: player 2 ground truth pieces (contents are SP enum types and CANT'T be UNKNOWN)
2: obstacle map (contents are 1 for 'obstacle at this space', 0 otherwise)

3: player 1 pieces from player 2's partially observable perspective (contents are SP enum types and CAN be UNKNOWN)
4: player 2 pieces from player 1's partially observable perspective (contents are SP enum types and CAN be UNKNOWN)

5: scalar data...
    state[3,0,0]: turn count (initial turn when no player has moved is 0, increments by 1 with each player action)
    state[3,0,1]: whether game is over (0 for False, 1 for True)
    state[3,0,2]: winner of the game if the game is over (0 for tie, 1 for player 1 won, -1 for player 2 won) (meaningless if game isn't over)
    state[3,1,0]: max turn count (after this many turns have happened, game is over and tied. We may or may not consider this kind of ending as invalid)
    state[3,1,1]: whether the game ending can be considered invalid (0 for False, 1 for True) (meaningless if game isn't over)

6: player 1 recent moves map for enforcing 2-squares rule against oscillating pieces back and forth (contents are RecentMoves enum types)
    This layer (and thus move tracking) is wiped to zeros anytime player 1 makes an attack.
    (0 for no move made here recently)
    (1 for the most recent piece to move came from here)
    (-1 for the most recent piece to move is now here)
    (-2 for the most recent piece to move is now here, and this is also the spot that it was in 2 turns ago.
       This piece cannot go to a spot marked as 1 and then return here.
    (-3 for the most recent piece to move is now here, and this is also the spot that it was in 2 turns ago.
       This piece cannot double back again (The piece here can't go to a spot marked with 1).

7: player 2 recent moves map (same rules apply)

8-19: player 1 captured pieces maps. Each piece is its own layer. (Layers are identified by _get_player_captured_piece_layer)
    These pieces were owned by player 1 but captured (and type revealed) by player 2.
    (0 for no piece of this type was ever captured at this location)
    (1 for 1 piece of the this type was captured at this location)
    (2 for 2 pieces of this type were captured at this location)
    etc.

20-31: player 2 captured pieces maps (same rules apply) (Layers are identified by _get_player_captured_piece_layer)

32: player 1 still pieces (from player 2's perspective), 1 for piece here that has never moved, 0 otherwise
33: player 2 still pieces (from player 1's perspective), 1 for piece here that has never moved, 0 otherwise

"""

# SPY = INT_DTYPE_NP(1)
# SCOUT = INT_DTYPE_NP(2)
# MINER = INT_DTYPE_NP(3)
# SERGEANT = INT_DTYPE_NP(4)
# LIEUTENANT = INT_DTYPE_NP(5)
# CAPTAIN = INT_DTYPE_NP(6)
# MAJOR = INT_DTYPE_NP(7)
# COLONEL = INT_DTYPE_NP(8)
# GENERAL = INT_DTYPE_NP(9)
# MARSHALL = INT_DTYPE_NP(10)
# FLAG = INT_DTYPE_NP(11)
# BOMB = INT_DTYPE_NP(12)
# UNKNOWN = INT_DTYPE_NP(13)

"""Stratego Pieces
    SPY (1) through Marshal (10) are defined by their rank.
    FLAG (11), BOMB (12), and UNKNOWN (13) are defined with special values.
[PIECE,     ID,     SCORE]
SPY         (1)     10 
SCOUT       (2)     8
MINER       (3)     5
SERGEANT    (4)     4
LIEUTENANT  (5)     5
CAPTAIN     (6)     6
MAJOR       (7)     7
COLONEL     (8)     8
GENERAL     (9)     12
MARSHALL    (10)    15
FLAG        (11)    0
BOMB        (12)    0

"""

NOPIECE = INT_DTYPE_NP(0)
SPY = INT_DTYPE_NP(1)
SCOUT = INT_DTYPE_NP(2)
MINER = INT_DTYPE_NP(3)
SERGEANT = INT_DTYPE_NP(4)
LIEUTENANT = INT_DTYPE_NP(5)
CAPTAIN = INT_DTYPE_NP(6)
MAJOR = INT_DTYPE_NP(7)
COLONEL = INT_DTYPE_NP(8)
GENERAL = INT_DTYPE_NP(9)
MARSHALL = INT_DTYPE_NP(10)
FLAG = INT_DTYPE_NP(11)
BOMB = INT_DTYPE_NP(12)
UNKNOWN = INT_DTYPE_NP(13)

def calc_score(state):
    score = 0
    for rows in state[0]:
        for index in rows:
            i = int(index)
            if(i == FLAG or i == BOMB): # Do not give points for bomb or flag
                continue
            elif(i == SPY):
                score += 10
            elif(i == SCOUT):
                score += 8
            elif(i == MINER):
                score += 5
            elif(i == SCOUT):
                score += 8
            elif(i == GENERAL):
                score += 12
            elif(i == MARSHALL):
                score += 15
            else:
                score += i
    return score

# RETURNS SCORE FOR END POSITION FOR BOTH PLAYERS IN FORMAT [SCORE PLAYER -1, SCORE PLAYER 1]
def eval_end_pos(env):
    # # print(env.base_env.action_size)
    # # print(env[1])
    # print(type(env))
    # # env.base_env.get_state_from_player_perspective()
    # # env.base_env.print_board_to_console(env)
    # print(env._get_current_obs)

    # player_id = list(obs.keys())[0]
    
    # print(player_id)
    # action_mask = obs[player_id]["partial_observation"]
    # print(len(action_mask), len(action_mask[0]), len(action_mask[0][0]))
    # print(env._get_current_obs(player=1))
    # print(env._get_current_obs(player=-1))
    # action_mask_1 = env._get_current_obs(player=1)["partial_observation"]
    # action_mask_2 = env._get_current_obs(player=-1)["partial_observation"]
    # print(action_mask_1[:][:][0])
    # state = env.state

    player_id = -1
    player_state = env.base_env.get_state_from_player_perspective(env.state, player_id)
    opp_state = env.base_env.get_state_from_player_perspective(env.state, -player_id)
    # full_obs = env.base_env.get_fully_observable_observation(env.state, player_id)

    # print(env.state)
    # print(np.shape(env.state))
    # print(player_state[0])

    # FIRST CALCULATE SCORE FOR PLAYER -1
    
    return([calc_score(player_state[0]), calc_score(opp_state[0])])
            
            
            
