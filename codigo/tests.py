import unittest

from functions_aux import product_dot, multiply_matrix_by_vector, subtract_two_vectors, multiply_vector_by_matrix, add_two_vectors, number_multiply_vector

class TestAuxFunction(unittest.TestCase):
    def test_product_dot(self):
        expect = 26
        self.assertEqual(expect, product_dot([1, 2, 3], [3, 4, 5]))
        
    def test_multiply_matrix_by_vector(self):
        incidence_matrix = [[1,0,1,0,0,1], [0,1,0,1,1,0], [1,1,1,0,0,0], [0,0,1,0,1,0]]
        vector = [2, 2, 2, 2, 2, 2]
        result = [6, 6, 6, 4]
        self.assertEqual(result, multiply_matrix_by_vector(incidence_matrix, vector))
        
    def test_multiply_vector_by_matrix(self):
        columns = [[1,0,1,0], [0,1,1,0],[1,0,1,1],[0,1,0,0],[0,1,0,1],[1,0,0,0]]
        vector = [2, 2, 2, 2]
        result = [4, 4, 6, 2, 4, 2]
        self.assertEqual(result, multiply_vector_by_matrix(vector, columns))
        
    def test_subtract_two_vectors(self):
        vector1 = [5, 4, 3, 2, 1]
        vector2 = [1, 2, 3, 4, 5]
        result = [4, 2, 0, -2, -4]
        self.assertEqual(result, subtract_two_vectors(vector1, vector2))
    
    def test_add_two_vectors(self):
        vector1 = [5, 4, 3, 2, 1]
        vector2 = [1, 2, 3, 4, 5]
        result = [6, 6, 6, 6, 6]
        self.assertEqual(result, add_two_vectors(vector1, vector2))
        
    def test_number_multiply_vector(self):
        vector1 = [5, 4, 3, 2, 1]
        result = [10, 8, 6, 4, 2]
        self.assertEqual(result, number_multiply_vector(2, vector1))
        
        
if __name__ == '__main__':
    unittest.main()