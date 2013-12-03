import sys

import my_io
from functions_aux import product_dot, multiply_matrix_by_vector, multiply_vector_by_matrix, subtract_two_vectors, \
                          add_two_vectors,number_multiply_vector,transform_incidence2column
import colect_time
from models import SetCoveringLagrangeanProblem, AuxProblem

def resolve_sub_problem_lagrangean(costs, incidence_matrix,columns, dual_lagrangean):
    set_covering = SetCoveringLagrangeanProblem(costs=costs, incidence_matrix=incidence_matrix,columns=columns, dual_lagrangean=dual_lagrangean)
    set_covering.create_cplex_problem()
    set_covering.c.solve()
    x = set_covering.c.solution.get_values(set_covering.names_variables)
    objective = set_covering.c.solution.get_objective_value()
    return objective, x

def resolve_problem_aux(v, w, s, e1, e2):
    aux_problem = AuxProblem(v, w, s, e1, e2)
    aux_problem.create_cplex_problem()
    aux_problem.c.solve()
    solution = aux_problem.c.solution
    alpha = solution.get_values('alpha')
    return alpha

def stop(w,dual_lagrangean_aux,p):
    epsilon1 = 0.00001
    epsilon2 = 0.00001
    return product_dot(w, w) <= epsilon1*epsilon1 and abs(product_dot(w, subtract_two_vectors(dual_lagrangean_aux,p)))+epsilon <= epsilon2
    
def main(name_file, UB):
    MAX_ITER = 500000
    MAX_TIME_SEC = 7200
    costs, incidence_matrix = my_io.read_file_format_or_library(name_file)
    columns = transform_incidence2column(incidence_matrix)
    #passo0
    dual_lagrangean = [1]*len(incidence_matrix)
    start = colect_time.cpu_time()
    set_covering = SetCoveringLagrangeanProblem(costs=costs, incidence_matrix=incidence_matrix,columns=columns, dual_lagrangean=dual_lagrangean)
    set_covering.create_cplex_problem()
    set_covering.c.solve()
    m1 = 0.001
    x = set_covering.c.solution.get_values(set_covering.names_variables)
    v = subtract_two_vectors([1]*len(incidence_matrix), multiply_matrix_by_vector(incidence_matrix, x))
    z = x[:]
    dual_lagrangean_aux = dual_lagrangean[:]
    w = v[:]
    p = dual_lagrangean[:]
    epsilon = 0
    t = 1
    k = 1
    s = 0.1
    objective = 0
    while True:
        #passo1
        dual_lagrangean = add_two_vectors(dual_lagrangean_aux, number_multiply_vector(s, w))
        ro = s * product_dot(w, w) + abs(product_dot(w, subtract_two_vectors(dual_lagrangean_aux,p))) + epsilon
        if stop(w,dual_lagrangean_aux,p) or UB-objective < 1 or colect_time.cpu_time() - start > MAX_TIME_SEC or t > MAX_ITER:
            end = colect_time.cpu_time()
            break
        #passo2:
        objective, x = resolve_sub_problem_lagrangean(costs=costs, incidence_matrix=incidence_matrix,columns=columns, dual_lagrangean=dual_lagrangean)
        v = subtract_two_vectors([1]*len(incidence_matrix), multiply_matrix_by_vector(incidence_matrix, x))
        
        #passo3
        objective_aux, x_aux = resolve_sub_problem_lagrangean(costs=costs, incidence_matrix=incidence_matrix,columns=columns, dual_lagrangean=dual_lagrangean_aux)
        if objective >= objective_aux + m1 * ro:
            dual_lagrangean_aux = dual_lagrangean[:]
            k = k + 1
        #passo4
        s = 0.5*((UB-objective)/product_dot(w,w))
        alpha = resolve_problem_aux(v, w, s, product_dot(v, subtract_two_vectors(dual_lagrangean_aux,dual_lagrangean)), product_dot(w, subtract_two_vectors(dual_lagrangean_aux, p))+epsilon)
        z = add_two_vectors(number_multiply_vector(alpha, x),number_multiply_vector(1-alpha, z))
        w = add_two_vectors(number_multiply_vector(alpha, v),number_multiply_vector(1-alpha, w))
        p = add_two_vectors(number_multiply_vector(alpha, dual_lagrangean),number_multiply_vector(1-alpha, p))
        aux = 1-alpha * product_dot(subtract_two_vectors(v, w), subtract_two_vectors(p, dual_lagrangean))
        epsilon = alpha * aux + (1 - alpha) * epsilon
        t = t + 1
    print name_file, objective, t, end
    
if __name__ == '__main__':
    if len(sys.argv) == 3:
        name_file = sys.argv[1]
        UB = int(sys.argv[2])
        main(name_file, UB)