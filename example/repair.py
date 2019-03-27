"""
Automated program repair ::

    python repair.py ../sample/Triangle_bug
"""
import sys
import random
import argparse
from pyggi.base import Patch
from pyggi.line import LineProgram
from pyggi.base.atomic_operator import LineReplacement, LineInsertion
from pyggi.base.custom_operator import LineDeletion
from pyggi.algorithms import LocalSearch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PYGGI Bug Repair Example')
    parser.add_argument('project_path', type=str, default='../sample/Triangle_bug')
    parser.add_argument('--epoch', type=int, default=30,
        help='total epoch(default: 30)')
    parser.add_argument('--iter', type=int, default=10000,
        help='total iterations per epoch(default: 10000)')
    args = parser.parse_args()
    
    program = LineProgram(args.project_path)

    #program.set_modifcation_points = []
    class MyTabuSearch(LocalSearch):
        def setup(self):
            self.tabu = []

        def get_neighbour(self, patch):
            while True:
                temp_patch = patch.clone()
                if len(temp_patch) > 0 and random.random() < 0.5:
                    temp_patch.remove(random.randrange(0, len(temp_patch)))
                else:
                    edit_operator = random.choice([LineDeletion, LineInsertion, LineReplacement])
                    temp_patch.add(edit_operator.create(program, method="weighted"))
                if not any(item == temp_patch for item in self.tabu):
                    self.tabu.append(temp_patch)
                    break
            return temp_patch

        def get_fitness(self, patch):
            return int(patch.test_result.custom['failed'])

        def is_better_than_the_best(self, fitness, best_fitness):
            return fitness < best_fitness

        def stopping_criterion(self, iter, patch):
            if patch.fitness == 0:
                return True
            return False

    tabu_search = MyTabuSearch(program)
    result = tabu_search.run(warmup_reps=1, epoch=args.epoch, max_iter=args.iter)
    for epoch in result:
        print ("Epoch #{}".format(epoch))
        for key in result[epoch]:
            print ("- {}: {}".format(key, result[epoch][key]))
