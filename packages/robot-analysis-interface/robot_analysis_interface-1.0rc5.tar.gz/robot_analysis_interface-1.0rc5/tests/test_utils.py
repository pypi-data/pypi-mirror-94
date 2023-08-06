import random
from unittest import TestCase

import numpy as np

from RAI.utils import are_zeros_and_ones


class TestUtils(TestCase):
    """Check the utility functions."""

    def test_are_zeros_and_ones(self):
        """Check the are_zeros_and_ones function."""

        # Arrays of 0s and 1s
        length = random.randint(1, 1000)
        x = np.array([random.choice((0.0, 1.0)) for _ in range(length)])
        y = np.copy(x)

        # Check
        self.assertTrue(are_zeros_and_ones(x))

        # Insert a number close to 0
        x[random.randint(0, length - 1)] = 1e-6
        self.assertFalse(are_zeros_and_ones(x))

        # Insert a number close to 1
        y[random.randint(0, length - 1)] = 0.999999
        self.assertFalse(are_zeros_and_ones(y))
