import numpy as np


def convergence_matrix(spanning_matrix):
    grammian_matrix = spanning_matrix.T * spanning_matrix
    cm = (-1) * grammian_matrix
    np.fill_diagonal(cm, 1)
    return cm


def check_convergence(spanning_matrix):
    grammian_matrix = spanning_matrix.T * spanning_matrix
    convergence_matrix = (-1) * grammian_matrix
    np.fill_diagonal(convergence_matrix, 1)
    convergence_matrix_eigenvalues = np.linalg.eigvals(convergence_matrix)
    return min(convergence_matrix_eigenvalues) > 0
