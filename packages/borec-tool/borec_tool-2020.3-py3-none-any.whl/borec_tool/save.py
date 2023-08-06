import numpy as np
import scipy.io


def save_as_npz(new_data, name):
    new_file = open(name, "w")
    np.savez(new_file, new_data)
    new_file.close()


def save_as_mat(new_data, name):
    scipy.io.savemat('changed.mat', new_data)
