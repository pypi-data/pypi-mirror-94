import random
import numpy as np
from moead_framework.core.genetic_operator.abstract_operator import GeneticOperator


class Crossover(GeneticOperator):
    """
    Multi-point crossover.

    Require 2 solutions, run a crossover according to the number of points crossover_points.
    """

    def __init__(self, solutions, **kwargs):
        super().__init__(solutions, **kwargs)
        if kwargs.get("crossover_points") is None:
            self.crossover_points = 1
        else:
            self.crossover_points = int(kwargs.get("crossover_points"))

    def run(self):
        self.number_of_solution_is_correct(n=2)
        solution1 = self.solutions[0]
        solution2 = self.solutions[1]

        list_of_points = set()
        while len(list_of_points) < self.crossover_points:
            int_rand = random.randint(1, len(solution1) - 1)
            list_of_points.add(int_rand)

        list_of_points = sorted(list(list_of_points))

        current = 0
        last_i = 0
        child = []
        for i in range(self.crossover_points):
            last_i = i
            if i % 2 == 0:
                child = np.append(child, solution1[current:list_of_points[i]])
            else:
                child = np.append(child, solution2[current:list_of_points[i]])

            current = list_of_points[i]

        if last_i % 2 == 0:
            child = np.append(child, solution2[list_of_points[-1]:])
        else:
            child = np.append(child, solution1[list_of_points[-1]:])

        return child
