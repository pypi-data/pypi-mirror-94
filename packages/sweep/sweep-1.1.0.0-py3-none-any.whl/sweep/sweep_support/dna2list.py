import more_itertools as mit
import numpy as np
def dna2list(sdna, q):
    b = np.array(sdna)
    b = np.array(list(mit.windowed(b.ravel(), n=q)))
    return np.array(b)