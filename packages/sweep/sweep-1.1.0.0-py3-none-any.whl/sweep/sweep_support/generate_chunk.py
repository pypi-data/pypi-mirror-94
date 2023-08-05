from .matlab_like import floor,repmat,zeros,ones
import numpy as np
def generate_chunk(chunks, file_len):
    z = floor(file_len/chunks)
    idxMat = repmat(z, chunks, 2) * np.array([list(range(0,chunks)),list(range(1,chunks+1))]).T + np.concatenate((ones(chunks,1),zeros(chunks,1)),axis=1)
    idxMat[-1,1] = file_len
    return idxMat