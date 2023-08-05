import numpy as np
def svd (M):
    Q, s, Vt = np.linalg.svd(M, full_matrices=False)
    V = Vt.T
    S = np.diag(s)
    return Q,S
def diag (M):
    R = np.diag(M)
    return R
def size (M):
    return M.shape
def eps (M):
    return np.finfo(M).eps
def orth(A):
    Q,S=svd(A)
    S=diag(S)

    tol = max(size(A)) * S[0] * eps('double')
    r = sum(S > tol)

    Q = Q[:,0:r]
    return Q