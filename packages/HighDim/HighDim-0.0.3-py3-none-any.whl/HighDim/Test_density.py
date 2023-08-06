import unittest
import numpy as np
import density


class Test_density(unittest.TestCase):

    def test_marginal_pdf(self):

        data = np.random.rand(100, 10)
        val = 0.3

        distribution = density.marginal_density(data,val)

        print(distribution)



