import numpy as np


class Moran(object):
    """
    A neutral drift Moran process.

    args:
        n (int) = number of states

    methods:

    sample
        args:
            start (int) = initial state of the process
            n_max (int) = max number of iterations of the sample; default 1000
        returns:
            (list length n) of state values
    """

    def __init__(self, n):
        self.n = n
        self.p = self.probabilities(n)

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        if not isinstance(value, int):
            raise TypeError(
                'Number of states must be an integer.')
        if value <= 0:
            raise ValueError(
                'Number of states must be at least 3.')
        self._n = value

    def probabilities(self, n):
        p = []
        for k in range(1, n):
            p_down = 1.0 * (n - k) / n * k / n
            p_up = 1.0 * k / n * (n - k) / n
            p_same = 1 - p_down - p_up
            p.append([p_down, p_same, p_up])

        return p

    def __str__(self):
        return 'Moran process with %s states' % self.n

    def __repr__(self):
        return self.__str__()

    def sample(self, start, n_max=1000):
        """
        Generate a Moran process until absorption (state 0 or n) or provess
        reaches length n_max
        """
        if not isinstance(start, int):
            raise TypeError('Initial state must be a positive integer.')
        if start < 0 or start > self.n:
            raise ValueError(
                'Initial state must be between 0 and ' + str(self.n))

        if not isinstance(n_max, int):
            raise TypeError('Sample length must be positive integer.')
        if n_max < 1:
            raise ValueError('Sample length must be at least 1.')

        s = [start]
        increments = [-1, 0, 1]
        for k in range(n_max):
            if start in [0, self.n]:
                break
            start = start + np.random.choice(increments, p=self.p[start - 1])
            s.append(start)

        return np.array(s)