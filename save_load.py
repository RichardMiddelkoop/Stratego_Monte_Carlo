# SAVE AND LOAD ENVIRONMENTS IN WHICH THE BOARDS ARE SAVED

from cmath import e
import pickle

def save_env(env, filename):
    assert filename.endswith(".pickle") or filename.endswith(".pkl"), "Error: file exetension is not '.pickle' or '.pkl'"
    with open(filename, 'wb') as output:
        pickle.dump(env, output, pickle.HIGHEST_PROTOCOL)

def load_env(filename):
    try:
        with open(filename, 'rb') as output:
            return pickle.load(output)
    except e:
        print(e)