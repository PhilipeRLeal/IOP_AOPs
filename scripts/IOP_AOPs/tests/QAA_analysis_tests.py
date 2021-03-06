import numpy as np
import pandas as pd
from unittest import TestCase

from .IOP_AOPs.QAA_analysis import apply_QAA

class Testgcdistance(TestCase):
    def test_apply_QAA(self):
        """
        This is a function to evaluate the QAA algorithm

        """
        try:
            N_samples = 10

            Bandas = [412, 443, 489, 510, 555, 670]

            size = (N_samples, len(Bandas)) / 1000

            Random_data = np.random.randint(low=0,
                                            high=800,
                                            size=size
                                            )

            Rrs_Data = pd.DataFrame(Random_data, columns=Bandas)

            QAA_Results = apply_QAA(Rrs_Data)

            for k, v in QAA_Results.items():
                print(str(k), '\n' * 3, '-' * 50,
                      '\n', v, '\n' * 3)

            R = isinstance(Rrs_Data, pd.DataFrame)

        except BaseException:
            R = False

        self.assertTrue(R)