import cplex

from functions_aux import multiply_vector_by_matrix

class SetCoveringLagrangeanProblem(object):
    def __init__(self, costs, incidence_matrix, columns, dual_lagrangean):
        self.costs = costs
        self.incidence_matrix = incidence_matrix
        self.columns = columns
        self.dual_lagrangean = dual_lagrangean
        self.num_variables = len(self.costs)
        self.names_variables = []

    def create_cplex_problem(self):
        self.c = cplex.Cplex()
        self.c.set_results_stream(None)
        self.c.set_log_stream(None)
        self.__add_variables()
        self.__add_function_objective()
        #self.c.set_problem_type(self.c.problem_type.LP)
        self.c.parameters.timelimit.set(2*3600)

    def __add_variables(self):
        self.names_variables = []
        for i in xrange(self.num_variables):
            self.names_variables.append('x%d' %(i+1))
        self.c.variables.add(names = self.names_variables, types = [self.c.variables.type.integer] * self.num_variables,
                            lb=[0]*self.num_variables,ub=[1]*self.num_variables)
        self.c.variables.add(names = ['pi'], types = [self.c.variables.type.continuous],
                            lb=[1],ub=[1])

    def __add_function_objective(self):
        objective = []
        news_costs = multiply_vector_by_matrix(self.dual_lagrangean, self.columns)
        for i in xrange(self.num_variables):
            objective.append((self.names_variables[i], self.costs[i] - news_costs[i]))
        sum_dual_lagrangean = 0
        for i in self.dual_lagrangean:
            sum_dual_lagrangean += i
        objective.append(('pi', sum_dual_lagrangean))
        self.c.objective.set_linear(objective)
        self.c.objective.set_sense(self.c.objective.sense.minimize)

class AuxProblem(object):
    def __init__(self, v, w, s, e1, e2):
        self.v = v
        self.w = w
        self.e1 = e1
        self.e2 = e2
        self.half_s = s * 0.5 

    def create_cplex_problem(self):
        self.c = cplex.Cplex()
        self.c.set_results_stream(None)
        self.c.set_log_stream(None)
        self.__add_variables()
        self.__add_function_objective()
        self.c.set_problem_type(self.c.problem_type.LP)
        self.c.parameters.timelimit.set(2*3600)

    def __add_variables(self):
        self.c.variables.add(names = ['alpha'], types = [self.c.variables.type.continuous],
                            lb=[0],ub=[1])
        self.c.variables.add(names = ['aux'], types = [self.c.variables.type.continuous],
                            lb=[1],ub=[1])

    def __add_function_objective(self):
        objective = []
        v_power_2 = []
        w_power_2 = []
        for i in xrange(len(self.v)):
            v_power_2.append(self.v[i]*self.v[i])
            w_power_2.append(self.w[i]*self.w[i])
        objective.append(('alpha', (-2*sum(w_power_2)+self.e1-self.e2)*self.half_s))
        objective.append(('aux', (sum(w_power_2)+self.e2)*self.half_s))
        self.c.objective.set_quadratic([(sum(v_power_2)+sum(w_power_2))*self.half_s, 0.0])
        self.c.objective.set_linear(objective)
        self.c.objective.set_sense(self.c.objective.sense.minimize) 
