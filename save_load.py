# SAVE AND LOAD ENVIRONMENTS IN WHICH THE BOARDS ARE SAVED

from cmath import e
import pickle

def save_state(state, filename):
    assert filename.endswith(".pickle") or filename.endswith(".pkl"), "Error: file exetension is not '.pickle' or '.pkl'"
    with open(filename, 'wb') as output:
        pickle.dump(state, output, pickle.HIGHEST_PROTOCOL)

def load_state(filename):
    try:
        with open(filename, 'rb') as output:
            return pickle.load(output)
    except e:
        print(e)