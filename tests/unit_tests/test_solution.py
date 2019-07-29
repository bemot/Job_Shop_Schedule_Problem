import os
import pickle
import shutil
import unittest

import numpy as np

from JSSP import solution
from JSSP.data import Data
from tests import project_root, tmp_dir

"""
Test the following: 

1. solution.solution.Solution equality
2. solution.solution.Solution inequality
3. solution.solution.Solution less than
4. solution.solution.Solution greater than 
5. sorting solution.solution.Solution objects
6. solution.InfeasibleSolutionException is raised when an infeasible operation list is passed to solution.solution.Solution()
7. solution.IncompleteSolutionException is raised when an incomplete operation list is passed to solution.solution.Solution()   
8. pickling a solution.solution.Solution object to a file

"""


class TestSolution(unittest.TestCase):

    def setUp(self) -> None:
        Data.initialize_data_from_csv(
            project_root + os.sep + 'data' + os.sep + 'given_data' + os.sep + 'sequenceDependencyMatrix.csv',
            project_root + os.sep + 'data' + os.sep + 'given_data' + os.sep + 'machineRunSpeed.csv',
            project_root + os.sep + 'data' + os.sep + 'given_data' + os.sep + 'jobTasks.csv')

    def test_solution_equality(self):
        solution_obj1 = solution.solution.SolutionFactory.get_solution()
        solution_obj2 = solution.Solution(solution_obj1.operation_2d_array)

        self.assertEqual(solution_obj1, solution_obj2, "These two solution.Solutions should be equal")

    def test_solution_inequality(self):
        solution_obj1 = solution.solution.SolutionFactory.get_solution()
        solution_obj2 = solution.solution.SolutionFactory.get_solution()

        self.assertNotEqual(solution_obj1, solution_obj2, "These two solution.Solutions should not be equal")

    def test_solution_less_than(self):
        solution_obj1 = solution.solution.SolutionFactory.get_solution()
        solution_obj2 = solution.Solution(solution_obj1.operation_2d_array)
        solution_obj2.makespan -= 1

        self.assertLess(solution_obj2, solution_obj1, "solution_obj2 should be less than solution_obj1")

        solution_obj2.makespan += 1
        solution_obj2.machine_makespans[0] -= 1

        self.assertLess(solution_obj2, solution_obj1, "solution_obj2 should be less than solution_obj1")

    def test_solution_greater_than(self):
        solution_obj1 = solution.solution.SolutionFactory.get_solution()
        solution_obj2 = solution.Solution(solution_obj1.operation_2d_array)
        solution_obj2.makespan -= 1

        self.assertGreater(solution_obj1, solution_obj2, "solution_obj2 should be greater than solution_obj1")

        solution_obj2.makespan += 1
        solution_obj2.machine_makespans[0] -= 1

        self.assertGreater(solution_obj1, solution_obj2, "solution_obj2 should be greater than solution_obj1")

    def test_sorting_solutions(self):
        lst = sorted(solution.solution.SolutionFactory.get_n_solutions(50))
        for i in range(1, len(lst)):
            self.assertLess(lst[i - 1], lst[i], "lst should be in sorted order")

    def test_solution_in_list(self):
        sol1 = solution.solution.SolutionFactory.get_solution()
        sol2 = solution.Solution(sol1.operation_2d_array)
        lst = [sol1]
        self.assertIn(sol2, lst)

    def test_infeasible_solution(self):
        try:

            solution_obj = solution.solution.SolutionFactory.get_solution()
            solution_obj.operation_2d_array[[0, 200]] = solution_obj.operation_2d_array[[200, 0]]
            solution.Solution(solution_obj.operation_2d_array)

            self.fail("Failed to raise solution.InfeasibleSolutionException")

        except solution.InfeasibleSolutionException:
            pass

    def test_incomplete_solution(self):
        try:

            solution_obj = solution.solution.SolutionFactory.get_solution()
            solution.Solution(np.delete(solution_obj.operation_2d_array, 0, axis=0))

            self.fail("Failed to raise solution.IncompleteSolutionException")

        except solution.IncompleteSolutionException:
            pass


class TestPicklingSolution(unittest.TestCase):

    def setUp(self) -> None:
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)

        Data.initialize_data_from_csv(
            project_root + os.sep + 'data' + os.sep + 'given_data' + os.sep + 'sequenceDependencyMatrix.csv',
            project_root + os.sep + 'data' + os.sep + 'given_data' + os.sep + 'machineRunSpeed.csv',
            project_root + os.sep + 'data' + os.sep + 'given_data' + os.sep + 'jobTasks.csv')

    def tearDown(self) -> None:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_pickle_to_file(self):
        solution_obj = solution.solution.SolutionFactory.get_solution()
        solution_obj.pickle_to_file(tmp_dir + os.sep + 'test_solution.pkl')

        self.assertTrue(os.path.exists(tmp_dir + os.sep + 'test_solution.pkl'), "The pickled solution does not exist")

        with open(tmp_dir + os.sep + 'test_solution.pkl', 'rb') as fin:
            solution_obj_pickled = pickle.load(fin)

        self.assertEqual(solution_obj, solution_obj_pickled, "The pickled solution should be equal to solution_obj")
        solution_obj.makespan -= 1
        self.assertNotEqual(solution_obj, solution_obj_pickled,
                            "The pickled solution should not be equal to solution_obj")


if __name__ == '__main__':
    unittest.main()