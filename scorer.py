import numpy as np


def counting_pieces(obs_pre, obs_curr):
    values = np.array([4, 1, 3, 2, 2.5, 3, 3.5, 4, 4.5, 5, 0, 3])
    pieces_pre = obs_pre[:, :, :12]
    pieces_curr = obs_curr[:, :, :12]
    pieces_num_pre = np.array(
        [int(pieces_pre[:, :, i].sum()) for i in range(12)])
    pieces_num_curr = np.array(
        [int(pieces_curr[:, :, i].sum()) for i in range(12)])
    pieces_diff = pieces_num_curr - pieces_num_pre
    score = (pieces_diff * values).sum()
    return score


def capture_pieces(obs_pre, obs_curr):
    values = np.array([4, 1, 3, 2, 2.5, 3, 3.5, 4, 4.5, 5, 0, 3])
    pieces_pre = obs_pre[:, :, 53:65]
    pieces_curr = obs_curr[:, :, 53:65]
    pieces_num_pre = np.array(
        [int(pieces_pre[:, :, i].sum()) for i in range(12)])
    pieces_num_curr = np.array(
        [int(pieces_curr[:, :, i].sum()) for i in range(12)])
    pieces_diff = pieces_num_curr - pieces_num_pre
    score = (pieces_diff * values).sum()
    return score


def scouting_pieces(obs_pre, obs_curr):
    pass


def step_score(obs_pre, obs_curr):
    if type(obs_pre) == type(None):
        return 0
    score = 0
    score += counting_pieces(obs_pre, obs_curr)
    score += capture_pieces(obs_pre, obs_curr)
    return score
