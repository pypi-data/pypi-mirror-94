import unittest
import numpy as np

import pysoleno.pysoleno as pysol
from tests import matlab_files_handler as mfh


class Test_pysoleno(unittest.TestCase):

    test_number = 1
    s = pysol.PySoleno()

    def test_B(self):
        """
        Checks if Br and Bz differ by less than specified thresholds
        """
        B_err = 1e-6  # maximum allowed field error (compared to matlab) - just a guess
        D_m = mfh.read_matlab_magnet(self.test_number)  # data for magnet from matlab
        rr_m, zz_m, Br_m, Bz_m = mfh.read_matlab_field(self.test_number)
        Br_p, Bz_p = self.s.calcB(rr_m, zz_m, *D_m)
        Br_e = Br_m - Br_p
        Bz_e = Bz_m - Bz_p
        Br_e_m = np.max(Br_e)
        Bz_e_m = np.max(Bz_e)
        self.assertLessEqual(Br_e_m, B_err)
        self.assertLessEqual(Bz_e_m, B_err)
        if Br_e_m < B_err and Bz_e_m < B_err:
            print(f'OKAY - Field calculation is test passed with error below Br={Br_e_m:.2e} T and Bz= {Bz_e_m:.2e} T')
        else:
            raise Exception("Field calculation calculation error")

    def test_M(self):
        """
        Checks if M differ by less than specified thresholds
        """
        M_err = 1e-6  # maximum allowed inductance error (compared to matlab) - just a guess
        D_m = mfh.read_matlab_magnet(self.test_number)  # data for magnet from matlab
        M_m = mfh.read_matlab_inductance(self.test_number)
        M_p = self.s.calcM(*D_m)
        M_e = M_m - M_p
        M_e_s = np.max(M_e)
        self.assertLessEqual(M_e_s, M_err)
        if M_e_s < M_err:
            print(f"OKAY - Self-mutual inductance calculation test passed with errors below {M_e_s:.2e} H")
        else:
            raise Exception("Self-mutual inductance calculation error")

if __name__ == '__main__':
    unittest.main()

