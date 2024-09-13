import math
import random
import sys
import time
from itertools import permutations


class Puzzle(object):
    """ The puzzle config. """

    def __init__(self, secret: str):
        self.secret = secret
        self.guessed = 0
        self.correct_pattern = Puzzle.diff_pattern(self.secret, self.secret)

    def guess(self, candidate: str) -> str:
        """ Get the pattern by diffing the given candidate from the secret.
    Args:
        candidate (str): The candidate string.
    Returns:
        str: pattern string.
    """
        self.guessed += 1
        return Puzzle.diff_pattern(self.secret, candidate)

    def is_correct(self, result: str) -> bool:
        return result == self.correct_pattern

    @staticmethod
    def diff_pattern(secret: str, candidate: str) -> str:
        a = b = 0
        for i in range(len(secret)):
            if secret[i] == candidate[i]:
                a += 1
            if candidate[i] in secret:
                b += 1
        return '{}A{}B'.format(a, b - a)


class Solver(object):
    """ The base class of solvers. """

    def __init__(self, name: str, digits: list[str], secret_len: int):
        self.name = name
        self.digits = digits
        self.secret_len = secret_len
        self.all_candidates = list(permutations(digits, secret_len))

    def choose(self, candidates: list[str]) -> str:
        """ Choose next candidate, which must be implemented by derived classes.
    Args:
        candidates (list[str]): The list of candidates.
    Returns:
        str: chosen candidate.
    """
        raise NotImplementedError('Not implemented in base class')

    def run_with_stats(self):
        """ Run solver over all candidates with stats. """
        print(
            '=== {} (DigitSize={}, SecretLen={}, CandidateSize={}) ==='.format(
                self.name, len(self.digits), self.secret_len,
                len(self.all_candidates)),
            file=sys.stderr)
        max_guessed = 0
        sum_guessed = 0
        total_start_time = time.time()
        # Enumerate all candidates and solve the corresponding puzzle.
        for secret in self.all_candidates:
            # Create a puzzle with given secret.
            puzzle = Puzzle(secret)
            candidates = list(self.all_candidates)
            while True:
                candidate = self.choose(candidates)
                pattern = puzzle.guess(candidate)
                if puzzle.is_correct(pattern):
                    break
                # Filter candidates.
                candidates = [
                    x for x in candidates
                    if Puzzle.diff_pattern(x, candidate) == pattern
                ]
            assert secret == candidate
            # Update stats.
            max_guessed = max(max_guessed, puzzle.guessed)
            sum_guessed += puzzle.guessed
        total_time = time.time() - total_start_time
        print(
            'Solver={},DigitSize={},SecretLen={},CandidateSize={},MaxGuess={},AveGuess={},TotalTime={}'
            .format(self.name, len(self.digits), self.secret_len,
                    len(self.all_candidates), max_guessed,
                    sum_guessed / len(self.all_candidates), total_time))


class SimpleSolver(Solver):
    """ The simple solver that always choose the first candidate. """

    def __init__(self, digits: list[str], length: int):
        super().__init__('Simple', digits, length)

    def choose(self, candidates: list[str]) -> str:
        return candidates[0]


class RandomSolver(Solver):
    """ The solver based on random selection. """

    def __init__(self, digits: list[str], length: int):
        super().__init__('Random', digits, length)

    def choose(self, candidates: list[str]) -> str:
        return random.choice(candidates)


class SmartSolver(Solver):
    """ The solver based on max-entropy selection. """

    def __init__(self, digits: list[str], length: int):
        super().__init__('Smart', digits, length)

    def choose(self, candidates: list[str]) -> str:
        # Initial guess.
        if candidates[0] == self.all_candidates[0]:
            return candidates[0]
        # Pick the candidate with max entropy over the rest candidates.
        best_candidate = candidates[0]
        best_entropy = 0.0
        for candidate in candidates:
            # Probability distribution.
            dist = dict()
            for expected in candidates:
                r = Puzzle.diff_pattern(expected, candidate)
                dist[r] = 1 + dist.get(r, 0)
            entropy = 0.0
            norm = sum(dist.values())
            for r in dist:
                p = dist[r] / norm
                entropy += -p * math.log(p)
            if entropy > best_entropy:
                best_candidate = candidate
                best_entropy = entropy
        return best_candidate


if __name__ == '__main__':
    all_digits = list('0123456789')
    if len(sys.argv) < 4:
        print(
            'Usage: guess the number of length secret_len chosen from digits with size digit_size (max {})'
            .format(len(all_digits)),
            file=sys.stderr)
        print('    {} secret_len digit_size [simple|random|smart]'.format(
            sys.argv[0]),
              file=sys.stderr)
        sys.exit(1)
    secret_len, digit_size, solver_name = int(sys.argv[1]), int(
        sys.argv[2]), sys.argv[3]
    assert secret_len <= digit_size
    assert digit_size <= len(all_digits)
    digits = all_digits[:digit_size]
    if solver_name == 'simple':
        SimpleSolver(digits, secret_len).run_with_stats()
    elif solver_name == 'random':
        RandomSolver(digits, secret_len).run_with_stats()
    elif solver_name == 'smart':
        SmartSolver(digits, secret_len).run_with_stats()
    else:
        print('Unknown solver name "%s", must be in [simple|random|smart]'.
              format(solver_name),
              file=sys.stderr)
