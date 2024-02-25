import logging
import os
import subprocess
import sys
from pathlib import Path

FAST_DOWNWARD_DIR_PATH = r"/mnt/c/Users/Chen/Desktop/hw3/fast-downward-22.06.1"  # fill the path to the location of the fast-downward directory on your machine


class FastDownwardSolver:
    """Class designated to use to activate the Fast Downward solver and parse its result."""

    logger: logging.Logger
    python_executable = sys.executable

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute_solver(
            self, problems_directory_path: Path, domain_file_path: Path) -> float:
        """Runs the Fast Downward solver on all the problems in the given directory.

        :param problems_directory_path: the path to the directory containing the problems.
        :param domain_file_path: the path to the domain file.
        :return: the percent of the problems solved by the solver.
        """
        num_problems_solved = 0
        os.chdir(FAST_DOWNWARD_DIR_PATH)
        self.logger.info("Starting to solve the input problems using Fast-Downward solver.")
        []
        if os.path.exists(problems_directory_path):
            print("Path exists.")
        else:
            print("Path does not exist.")
        for problem_file_path in problems_directory_path.glob(f"pfile*.pddl"):
            self.logger.debug(f"Starting to work on solving problem - {problem_file_path.stem}")
            solution_path = problems_directory_path / f"{problem_file_path.stem}.solution"
            running_options = ["--overall-time-limit", "60s",
                               "--plan-file", str(solution_path.absolute()),
                               str(domain_file_path.absolute()),
                               str(problem_file_path.absolute()),
                               "--evaluator", "'hcea=cea()'",
                               "--search", "'lazy_greedy([hcea], preferred=[hcea])'"]
            run_command = f"{self.python_executable} fast-downward.py {' '.join(running_options)}"
            try:
                subprocess.check_output(run_command, shell=True)
                self.logger.info(f"Solver succeeded in solving problem - {problem_file_path.stem}")
                num_problems_solved += 1

            except subprocess.CalledProcessError as e:
                self.logger.info(f"Solver failed to solve problem - {problem_file_path.stem}")
                self.logger.debug(f"Solver failed with error - {e}")
                continue

        final_score = (num_problems_solved / len(list(problems_directory_path.glob(f"pfile*.pddl")))) * 100
        print(f"Final score is {final_score}")


if __name__ == '__main__':
    args = sys.argv
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG)
    solver = FastDownwardSolver()
    solver.execute_solver(problems_directory_path=Path(args[1]),
                    domain_file_path=Path(args[2]))
