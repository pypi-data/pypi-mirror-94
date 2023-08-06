"""
PySoleno by Mariusz Wozniak
Soleno was originally developed at Twente University by Gert Mulder, and upgraded in 1999 by Erik Krooshoop
This code is based on Jeroen van Nugteren C++ implementation of original soleno.
The test are comparing to Jeroen results generated in matlab and saved to text file.

"""

import numpy as np


class PySoleno:

    def __init__(self):
        self.Eps = 1e-12  # calculation accuracy
        self.Tmax = 50  # max number of loops (?)

    # ---------- Field ------------

    def _Sol_Rekenb(self, Zmh, Rm, Rp):
        Hulp = np.sqrt(Rp * Rp + Zmh * Zmh)
        Kc = np.sqrt(Rm * Rm + Zmh * Zmh) / Hulp
        if np.any(Kc < self.Eps):
            Kc = self.Eps
        Mj = 1
        Nj = Kc
        Aj = -1
        Bj = 1
        Pj = Rm / Rp
        Cj = Pj + 1
        if np.any(np.abs(Rm / Rp) < self.Eps):
            Pj = 1
        Dj = Cj * np.sign(Pj)
        Pj = np.abs(Pj)
        Tel = 1
        while np.any(np.abs(Mj - Nj) > (self.Eps * Mj)):
            if np.any(Tel > self.Tmax):
                print("Solution does not converge")
            Xmn = Mj * Nj
            Xmp = Xmn / Pj
            D0 = Dj
            Dj = 2 * (Dj + Xmp * Cj)
            Cj = Cj + D0 / Pj
            B0 = Bj
            Bj = 2 * (Bj + Nj * Aj)
            Aj = Aj + B0 / Mj
            Pj = Pj + Xmp
            Mj = Mj + Nj
            Nj = 2 * np.sqrt(Xmn)
            Tel = Tel + 1
        Brh = (Aj + Bj / Mj) / (Mj * Hulp)
        Bzh = (Cj + Dj / Mj) / ((Mj + Pj) * Hulp) * Zmh
        return Brh, Bzh

    def _Sol_CalcB(self, R, Z, Rin, Rout, Zlow, Zhigh, It, Nlayers):
        # Original Soleno Function (used by improved version)
        Brd = 0
        Bzd = 0
        if np.any(Rin != Rout) and np.any(Zlow != Zhigh):
            Factor = It / (Zhigh - Zlow) / Nlayers
            if np.any(Factor != 0):
                Zm1 = Z - Zlow
                Zm2 = Z - Zhigh
                dR = (Rout - Rin) / Nlayers
                dH = dR / 2
                dE = dH
                for tt in range(1, Nlayers + 1):
                    Rs = Rin - dH + dR * tt
                    if np.any(np.abs(R - Rs) >= dE):
                        # extern
                        Rp = Rs + R
                        Rm = Rs - R
                        Br1, Bz1 = self._Sol_Rekenb(Zm1, Rm, Rp)
                        Br2, Bz2 = self._Sol_Rekenb(Zm2, Rm, Rp)
                        Brd = Brd + (Br2 - Br1) * Factor * Rs
                        Bzd = Bzd + (Bz1 - Bz2) * Factor
                    else:
                        # intern
                        Rp = Rs + Rs - dE
                        Rm = dE
                        Weeg = (Rs - R + dE) / dE / 2
                        Br1, Bz1 = self._Sol_Rekenb(Zm1, Rm, Rp)
                        Br2, Bz2 = self._Sol_Rekenb(Zm2, Rm, Rp)
                        Brd = Brd + (Br2 - Br1) * Weeg * Factor * Rs
                        Bzd = Bzd + (Bz1 - Bz2) * Weeg * Factor
                        Weeg = 1 - Weeg
                        Rp = Rs + Rs + dE
                        Rm = -dE
                        Br1, Bz1 = self._Sol_Rekenb(Zm1, Rm, Rp)
                        Br2, Bz2 = self._Sol_Rekenb(Zm2, Rm, Rp)
                        Brd = Brd + (Br2 - Br1) * Weeg * Factor * Rs
                        Bzd = Bzd + (Bz1 - Bz2) * Weeg * Factor
        return Brd * np.pi * 1e-7, Bzd * np.pi * 1e-7

    def _Sol_CalcB_new(self, R2d, Z2d, Rin, Rout, Zlow, Zhigh, I, Nlayers):
        if Nlayers < 1:  # set layers if not set remotely 5 is default value
            Nlayers = 5
        R = np.ravel(R2d)
        Z = np.ravel(Z2d)
        internal_mask = ((R >= Rin) & (R <= Rout))

        def internal(R, Z, Rin, Rout, Zlow, Zhigh, I, Nlayers):
            Brt_l = []
            Bzt_l = []
            for R, Z in zip(list(R), list(Z)):
                A = (R - Rin) / (Rout - Rin)
                NL1 = int(Nlayers * A) + 1
                NL2 = int(Nlayers * (1 - A)) + 1
                # deel1
                Br2, Bz2 = self._Sol_CalcB(R, Z, Rin, R, Zlow, Zhigh, I * A, NL1)
                Brt, Bzt = self._Sol_CalcB(R, Z, Rin, R, Zlow, Zhigh, I * A, NL1 * 2)
                BZtemp = Bzt + (Bzt - Bz2) / 3  # Extrapolatie naar 1/Nl/Nl=0
                BRtemp = Brt + (Brt - Br2) / 3
                # deel2
                Br2, Bz2 = self._Sol_CalcB(R, Z, R, Rout, Zlow, Zhigh, I * (1 - A), NL2)
                Brt, Bzt = self._Sol_CalcB(R, Z, R, Rout, Zlow, Zhigh, I * (1 - A), NL2 * 2)
                Brt_l.append(BRtemp + Brt + (Brt - Br2) / 3)
                Bzt_l.append(BZtemp + Bzt + (Bzt - Bz2) / 3)  # Extrapolatie naar 1/Nl/Nl=0
            return np.array(Brt_l), np.array(Bzt_l)

        def external(R, Z, Rin, Rout, Zlow, Zhigh, I, Nlayers):
            Br2, Bz2 = self._Sol_CalcB(R, Z, Rin, Rout, Zlow, Zhigh, I, Nlayers)
            Brt, Bzt = self._Sol_CalcB(R, Z, Rin, Rout, Zlow, Zhigh, I, Nlayers * 2)
            Bzt = Bzt + (Bzt - Bz2) / 3  # Extrapolatie naar 1/Nl/Nl=0
            Brt = Brt + (Brt - Br2) / 3
            return Brt, Bzt

        Brt = np.zeros_like(R)
        Bzt = np.zeros_like(R)
        Brt[internal_mask], Bzt[internal_mask] = internal(R[internal_mask], Z[internal_mask], Rin, Rout, Zlow, Zhigh, I,
                                                          Nlayers)
        # Brt[internal_mask], Bzt[internal_mask] = external(R[internal_mask], Z[internal_mask], Rin, Rout, Zlow, Zhigh, I,
        #                                                   Nlayers)
        Brt[~internal_mask], Bzt[~internal_mask] = external(R[~internal_mask], Z[~internal_mask], Rin, Rout, Zlow,
                                                            Zhigh, I, Nlayers)
        Brt = np.reshape(Brt, R2d.shape)
        Bzt = np.reshape(Bzt, R2d.shape)
        return Brt, Bzt

    # ---------- Inductance ------------
    def _Sol_CI(self, R1, R2, ZZ):
        # Function for calculating elliptical integrals
        Imax = 25
        Itel = 0
        Ci = 0
        Rm = R1 - R2
        Rp = R1 + R2
        Zkw = ZZ * ZZ
        Rkw = 4 * R1 * R2
        Kkw = (Rm * Rm + Zkw) / (Rp * Rp + Zkw)
        if Kkw < self.Eps:
            Ci = 1 / (6 * np.arctan(1.0))  # f was removed not sure what it did
        else:
            Kc = np.sqrt(Rkw / (Rp * Rp + Zkw))
            Alfa1 = 1
            Beta1 = np.sqrt(Kkw)
            Q1 = np.abs(Rm / Rp)
            R1eqR2 = Q1 <= self.Eps
            A1 = 1 / (3 * Kc)
            B1 = -Kkw * A1
            C1 = Kc * Zkw / Rkw
            D1 = 0
            A1 = A1 - C1
            if R1eqR2:
                A1 = A1 + C1
                B1 = -B1 - B1
                C1 = 0
            while (abs(Alfa1 - Beta1) > Alfa1 * self.Eps and Itel < Imax):  # && replaced with and
                Itel = Itel + 1
                AlfBe1 = Alfa1 * Beta1
                if not R1eqR2:
                    C2 = C1 + D1 / Q1
                    D2 = AlfBe1 * C1 / Q1 + D1
                    D2 = D2 + D2
                    Q2 = Q1 + AlfBe1 / Q1
                    C1 = C2
                    D1 = D2
                    Q1 = Q2
                Alfa2 = Alfa1 + Beta1
                Beta2 = 2 * np.sqrt(AlfBe1)
                A2 = B1 / Alfa1 + A1
                B2 = B1 + Beta1 * A1
                B2 = B2 + B2
                Alfa1 = Alfa2
                Beta1 = Beta2
                A1 = A2
                B1 = B2
            Ci = (A1 + B1 / Alfa1) / (Alfa1 + Alfa1) + (C1 + D1 / Alfa1) / (Alfa1 + Q1)
            if Itel >= Imax:
                print("No Convergence")
        return Ci

    # Main mutual inductance function returns mutual inductance between coil I and J
    def _CalcMutSub(self, SD, I, J, NlI, NlJ):
        S1 = np.abs(SD['Zh'][I] - SD['Zl'][J])
        S2 = np.abs(SD['Zl'][I] - SD['Zl'][J])
        S3 = np.abs(SD['Zl'][I] - SD['Zh'][J])
        S4 = np.abs(SD['Zh'][I] - SD['Zh'][J])
        S3neS1 = (S3 != S1)
        S4neS2 = (S4 != S2)
        RdivNE = (SD['Ri'][I] != SD['Ri'][J]) or (SD['Ro'][I] != SD['Ro'][J]) or (NlI != NlJ)
        Factor = 0.0000008 * np.pi * np.pi * SD['Nw'][I] / NlI / (SD['Zh'][I] - SD['Zl'][I]) * SD['Nw'][J] / NlJ / (
                SD['Zh'][J] - SD['Zl'][J])
        DrI = (SD['Ro'][I] - SD['Ri'][I]) / NlI
        DrJ = (SD['Ro'][J] - SD['Ri'][J]) / NlJ
        Som = 0

        for K in range(1, NlI + 1):
            R1 = SD['Ri'][I] + (K - 0.5) * DrI
            for L in range(1, NlJ + 1):
                R2 = SD['Ri'][J] + (L - 0.5) * DrJ
                if RdivNE or L <= K:
                    C1 = self._Sol_CI(R1, R2, S1)
                    C2 = self._Sol_CI(R1, R2, S2)
                    C3 = C1
                    C4 = C2
                    if (S3neS1):
                        C3 = self._Sol_CI(R1, R2, S3)
                    if (S4neS2):
                        C4 = self._Sol_CI(R1, R2, S4)
                    HH = R1 * R2
                    HH = np.sqrt(HH * HH * HH)
                    if not RdivNE and (L < K):
                        HH = 2 * HH
                    Som = Som + (C1 - C2 + C3 - C4) * HH
        return Som * Factor

    def _CalcMut(self, SD, Ns, N1, CalcE):
        Mut = np.zeros(shape=(Ns, Ns))  # new
        # Mut = [0]*Ns*Ns
        Msom = 0
        if N1 == Ns:
            N2 = 0
        else:
            N2 = N1
        for I in range(0, Ns):
            for J in range(I, Ns):
                if J < N2 or I >= N1:
                    Hulp = 0
                else:
                    if SD['NN'][I] > 0 or SD['NN'][J] > 0 or CalcE:
                        NlI = SD['NL'][I]
                        NlJ = SD['NL'][J]
                        Hulp2 = self._CalcMutSub(SD, I, J, NlI, NlJ)  # opgegeven aantal lagen
                        Hulp = self._CalcMutSub(SD, I, J, NlI * 2, NlJ * 2)  # dubbel aantal lagen
                        Hulp = Hulp + (Hulp - Hulp2) / 3  # extrapolatie naar 1/NLI/NLJ=0
                        Mut[I, J] = Hulp
                        Mut[J, I] = Hulp
                        # Mut[I+J*Ns] = Hulp
                        # Mut[J+I*Ns] = Hulp
                    # Hulp = Mut[I+J*Ns]
                if (N1 == Ns and I != J):
                    Hulp = 2 * Hulp
                # if (CalcE):
                #     Hulp = Hulp * SD[I].Iw * SD[J].Iw
                # Msom = Msom + Hulp
        if N1 == Ns:
            for I in range(0, Ns):
                SD['NN'][I] = 0
        # return Msom
        return Mut

    # ----------- Public methods ----------------

    def calcB(self, rr, zz, Rin, Rout, Zlow, Zhigh, I, Nturn, Nloop):
        """
        Calculate magnetic field components of a solenoid(s) at points
        :param rr: radial grid coordinates where field to be calculated in m
        :param zz: axial grid coordinates where field to be calculated in m
        :param Rin: (list of) inner radius(es) of solenoid(s) in m
        :param Rout: (list of) outer radius(es) of solenoid(s) in m
        :param Zlow: (list of) lower axial position(s) of solenoid(s) in m
        :param Zhigh: (list of) higher axial position(s) of solenoid(s)in m
        :param I: (list of) current(s) of solenoid(s) in A
        :param Nturn: (list of) number of turn(s) of solenoid(s) - integer
        :param Nloop: number of loops in calculations - higher number = higher accuracy, 5 is usually okay
        :return: Br and Bz are field in the radial and axial direction in T
        """
        rr1 = np.ravel(rr)
        pos_mask = rr1 > 0.
        rrp = rr1[pos_mask]
        rrn = rr1[~pos_mask]
        zz1 = np.ravel(zz)
        zzp = zz1[pos_mask]
        zzn = zz1[~pos_mask]
        Itot = [n * i for n, i in zip(Nturn, I)]
        if len(set(map(len, [Rin, Rout, Zlow, Zhigh, Itot, Nloop]))) == 1:  # check if input lists are the same length
            # print("Inputs are the same length")
            Br = np.zeros_like(rr1)
            Bz = np.zeros_like(rr1)
            for ri, ro, zl, zh, it, nl in zip(Rin, Rout, Zlow, Zhigh, Itot, Nloop):
                br, bz = self._Sol_CalcB_new(rrp, zzp, ri, ro, zl, zh, it, nl)
                Br[pos_mask] = Br[pos_mask] + br
                Bz[pos_mask] = Bz[pos_mask] + bz
                if np.min(rr1) < 0:
                    br, bz = self._Sol_CalcB_new(-rrn, zzn, ri, ro, zl, zh, it, nl)
                    Br[~pos_mask] = Br[~pos_mask] - br
                    Bz[~pos_mask] = Bz[~pos_mask] + bz
            Br = np.reshape(Br, rr.shape)
            Bz = np.reshape(Bz, rr.shape)
        else:
            raise SystemExit("Inputs are not the same length!")
        return Br, Bz

    def calcM(self, Rin, Rout, Zlow, Zhigh, I, Nturn, Nloop):  # kept I to make inputs for calcB and calcM the same
        """
        Calculate mutual inductance of solenoid(s)
        :param Rin: (list of) inner radius(es) of solenoid(s) in m
        :param Rout: (list of) outer radius(es) of solenoid(s) in m
        :param Zlow: (list of) lower axial position(s) of solenoid(s) in m
        :param Zhigh: (list of) higher axial position(s) of solenoid(s)in m
        :param I: (list of) current(s) of solenoid(s) - this is not needed for calculations, added for consistency with calcB method
        :param Nturn: (list of) number of turn(s) of solenoid(s) - integer
        :param Nloop: number of loops in calculations - higher number = higher accuracy, 5 is usually okay
        :return: matrix  is in a standard form in H
        """
        Ns = len(Rin)  # number of coils = total size of matrix i.e. for 2 coils Ns = 4
        SD = {'Ri': Rin, 'Ro': Rout, 'Zl': Zlow, 'Zh': Zhigh, 'Nw': Nturn, 'NL': Nloop,
              'NN': [1] * len(Rin)}  # Nw - number of turns, NL - number of layers, NN - not calculated coil
        return self._CalcMut(SD, Ns, Ns, False)
