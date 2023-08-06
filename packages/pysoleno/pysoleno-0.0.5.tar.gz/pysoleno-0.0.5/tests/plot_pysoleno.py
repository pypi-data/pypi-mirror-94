import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

import pysoleno.pysoleno as pysol
import matlab_files_handler as mfh

def plot_field(test_number, comp):
    """
    Plot magnetic field or coordinates and compare to matlab output saved as text files
    :param comp: 'Br' or 'Bz' or 'Bmod' or "coor"
    :return: plot on screen
    """

    plots = ['matlab', 'python', '(matlab-python)']
    fig, axs = plt.subplots(nrows=1, ncols=len(plots), figsize=(15, 5))
    rr_m, zz_m, Br_m, Bz_m = mfh.read_matlab_field(test_number)
    Bmod_m = np.sqrt(np.square(Br_m) + np.square(Bz_m))
    B_m = {'Br': Br_m, 'Bz': Bz_m, 'Bmod': Bmod_m, "coor": rr_m + zz_m}
    D_m = mfh.read_matlab_magnet(test_number)  # data for magnet from matlab
    s = pysol.PySoleno()
    Br_p, Bz_p = s.calcB(rr_m, zz_m, *D_m)
    Bmod_p = np.sqrt(np.square(Br_p) + np.square(Bz_p))
    B_p = {'Br': Br_p, 'Bz': Bz_p, 'Bmod': Bmod_p, "coor": rr_m + zz_m}
    B_e = {'Br': Br_m - Br_p, 'Bz': Bz_m - Bz_p, 'Bmod': Bmod_m - Bmod_p, "coor": rr_m + zz_m - (rr_m + zz_m)}
    sets = {}
    data = [B_m, B_p, B_e]
    for pl, d in zip(plots, data):
        sets[pl] = [rr_m, zz_m, d[comp]]
    for ax, title in zip(axs, plots):
        im = ax.pcolor(*sets[title], shading='auto', cmap=cm.get_cmap('jet'))
        # im = ax.pcolormesh(*sets[title], shading='auto', cmap=cm.get_cmap('jet'))
        ax.set_aspect(1)
        ax.set_title(f'{title}: {comp} [T]')
        ax.set_xlim(np.min(sets[title][0]), np.max(sets[title][0]))
        ax.set_ylim(np.min(sets[title][1]), np.max(sets[title][1]))
        ax.set_xlabel("r (m)")
        ax.set_ylabel("z (m)")
        cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')
    plt.tight_layout()
    plt.show()

def manual_magnet_output(calc_pos=True):
    """
    This is dummy output, not used by any functions above :return: tuple with magnet definition, can be unpacked
    in calcB function or inside M function if B is set to false
    :param calc_pos: Set to true to return field calculation positions in return tuple
    :return: Tuple that can be unpacked in Soleno calcB and calcM function
    """
    # definition of magnet
    Rin = [0.13, 0.13]
    Rout = [0.15, 0.15]
    Zlow = [-0.1, 0.05]
    Zhigh = [-0.05, 0.1]
    Nturn = [200, 200]
    I = [200, 200]
    Nloop = [5, 5]
    # definition of target points
    Rmin = -0.4
    Rmax = 0.4
    Zmin = -0.4
    Zmax = 0.4
    r_d = 50
    z_d = 50
    rr, zz = np.meshgrid(np.linspace(Rmin, Rmax, r_d), np.linspace(Zmin, Zmax, z_d))
    if calc_pos:
        return rr, zz, Rin, Rout, Zlow, Zhigh, I, Nturn, Nloop
    else:
        return Rin, Rout, Zlow, Zhigh, I, Nturn, Nloop

if __name__ == '__main__':
    test_number = 1
    for comp in ['Br', 'Bz', 'Bmod']:
        plot_field(1, comp)
