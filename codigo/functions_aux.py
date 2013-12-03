def product_dot(vector1, vector2):
    result = 0
    for i in xrange(len(vector1)):
        result += vector1[i] * vector2[i]
    return result

def multiply_matrix_by_vector(matrix, vector):
    result = []
    for line in matrix:
        item = product_dot(line, vector)
        result.append(item)
    return result

def multiply_vector_by_matrix(vector, matrix):
    result = []
    for column in matrix:
        multiply = 0
        for i in xrange(len(vector)):
            multiply += vector[i] * column[i]
        result.append(multiply)
    return result

def subtract_two_vectors(vector1, vector2):
    result = []
    for i in xrange(len(vector1)):
        result.append(vector1[i] - vector2[i])
    return result

def add_two_vectors(vector1, vector2):
    result = []
    for i in xrange(len(vector1)):
        result.append(vector1[i] + vector2[i])
    return result

def number_multiply_vector(number, vector):
    result = []
    for i in xrange(len(vector)):
        result.append(vector[i] * number)
    return result

def transform_incidence2column(incidence_matrix):
    numbers_column = len(incidence_matrix[0])
    columns = []
    for i in xrange(numbers_column):
        column = []
        for item in incidence_matrix:
            column.append(item[i])
        columns.append(column)
    return columns 
