import numpy as np
import more_itertools as mit
def seq2list(sdna, q):
    sdna=list(sdna)
    b = np.array(sdna)
    b = np.array(list(mit.windowed(b.ravel(), n=q)))
    return np.array(b)