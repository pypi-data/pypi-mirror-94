import numpy as np

def min(A, B):
    if A.shape[0] != B.shape[0]:
        print("Error: size of A does not equal size of B")
        return 0
    print(A, B, '\n')
    C = np.zeros((A.shape[0], B.shape[0]))
    for i in range(A.shape[0]):
        for j in range(B.shape[0]):
            if A[i] < B[j]:
                C[i][j] = A[i]
            if A[i] >= B[j]:
                C[i][j] = B[j]
        print(C[i])
    return C

def max(A, B):
    if A.shape[0] != B.shape[0]:
        print("Error: size of A does not equal size of B")
        return 0
    print(A, B, '\n')
    C = np.zeros((A.shape[0], B.shape[0]))
    for i in range(A.shape[0]):
        for j in range(B.shape[0]):
            if A[i] > B[j]:
                C[i][j] = A[i]
            if A[i] <= B[j]:
                C[i][j] = B[j]
        print(C[i])
    return C

def min_max(A, B):
    C = np.zeros(A.shape[0])
    for i in range(A.shape[0]):
        for j in range(B.shape[0]):
            if A[i] < B[i][j]:
                B[j][i] = A[i]
            if A[i] >= B[i][j]:
                continue
    B = np.rot90(B, 3)
    for i in range (C.shape[0]):
        print(B[i])
        C[i] = np.amax(B[i])
    print(C)
    return C


A = np.array([0.2, 0.8, 0.1])
B = np.array([[0.2, 0.2, 0.2], [0.3, 0.6, 0.4], [0.1, 0.1, 0.1]])

min_max(A, B)
