"""
Neuron Connectivity Matrix
Date: December 2020
"""
import numpy as np

numneurons = 10
c_matrix = np.zeros((numneurons,numneurons))
c_matrix[0][1] = -205
c_matrix[1][3] = 120
c_matrix[3][4] = -50
c_matrix[3][5] = 200
c_matrix[5][9] = -1000
c_matrix[1][9] = 6.089
c_matrix[5][5] = -200
c_matrix[8][8] = -200

c_matrix[0][2] = 207
c_matrix[2][6] = 100
c_matrix[6][7] = -50
c_matrix[6][8] = 200
c_matrix[8][9] = -1000
c_matrix[2][9] = 6.755
c_matrix[9][9] = -800

def getMatrix():
    return c_matrix

def accessWeights(n1,n2):
    return c_matrix[n1-1][n2-1]
    