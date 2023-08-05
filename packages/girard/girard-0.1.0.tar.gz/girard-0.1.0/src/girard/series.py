import numpy as np

from math import pi, sqrt, exp
from functools import reduce
from numpy import matrix, arccos
from numpy.linalg import inv, det
from decimal import *

from girard import linear_algebra as la, memoize as mem, utils, series_convergence as sc

#term of the hypergeometric series in dimension \binom{n}{k}.
# a and alpha are vectors in dimension \binom{n}{k}
def series_term(m_tuple, alpha, n):
    alpha_to_the_m = la.vector_vetor_exp(alpha, m_tuple)
    sum_entries = sum(m_tuple)
    sign = (-1) ** sum_entries
    power = mem.power_of_two(sum_entries)
    fact = reduce(lambda a,b: a*b, map(mem.factorial, m_tuple))
    gamma_prod = utils.gamma_product(m_tuple, n)
    return (alpha_to_the_m * sign * power * gamma_prod) / fact

# function that puts together all previous components to implement Ribando"s formula for the solid angle
def solid_angle(spanning_matrix, eps, max_weight=50):
    cone_vectors = list(map(la.normalize, spanning_matrix.T.tolist()))

    dimension = len(cone_vectors)

    alpha = la.pairwise_dot_products(cone_vectors)
    normalized_spanning_matrix = np.matrix(cone_vectors).T

    series_will_converge = sc.check_convergence(normalized_spanning_matrix)

    if not series_will_converge:
        raise ValueError("The cone inputed is not within the region of convergence of the hypergeometric series. Use the monte_carlo module instead.")

    det_V = abs(np.linalg.det(normalized_spanning_matrix))

    pi_term = (4*np.pi)**(dimension/2.0)
    constant_term = Decimal(det_V / pi_term)

    series_dimension = int(dimension*(dimension-1)/2)
    inputs = utils.tuple_generator(series_dimension)
    number_of_tuples = utils.number_of_d_tuples_with_max_weight_k(series_dimension, max_weight)

    approx = 0
    its = 0
    while its < number_of_tuples:
        term = series_term(next(inputs), alpha, dimension)
        approx += term
        its += 1
        if abs(term) < eps:
            break

    return constant_term * approx
