import numpy as np

MATRIX = '../data/matrix.txt'
COEFS = '../data/coefs.txt'

def main():
    matrix = np.loadtxt(MATRIX)
    print("matrix", matrix)
    det = np.linalg.det(matrix)
    print("determinant", det)
    inv = np.linalg.inv(matrix)
    print("inverse", inv)

    coeficients = np.loadtxt(COEFS)
    if len(coeficients) > 0:
        a1, a2 = np.hsplit(coeficients, [len(coeficients[0])-1])
        res = np.linalg.solve(a1, a2)
        print("result \n", res)
    else:
        print("not data")

if __name__ == "__main__":
    main()

