#!/usr/bin/env python

# author: Daniel Scheiermann
# email: daniel.scheiermann@stud.uni-hannover.de
# license: MIT
# Please feel free to use and modify this, but keep the above information.

"""
Animation for the numerical solver for the non-linear
time-dependent Schrodinger equation for 1D, 2D and 3D.

"""

import argparse
import functools
from pathlib import Path
from typing import Callable, Optional

import numpy as np

from supersolids.Animation.Animation import Animation
from supersolids.Schroedinger import Schroedinger
from supersolids.helper.simulate_case import simulate_case
from supersolids.tools.cut_1d import prepare_cuts
from supersolids.helper import constants
from supersolids.helper import functions

# Script runs, if script is run as main script (called by python *.py)
if __name__ == "__main__":
    # Use parser to
    parser = argparse.ArgumentParser(description="Define constants for Schrödinger equation")
    parser.add_argument("-dt", metavar="dt", type=float, default=2 * 10 ** -3, nargs="?",
                        help="Length of timestep to evolve Schrödinger system")
    parser.add_argument("-Res", metavar="Res", type=int,
                        default=[2 ** 8, 2 ** 7, 2 ** 5], nargs="*",
                        help="List of resolutions for the box (1D, 2D, 3D). Needs to be 2 ** int.")
    parser.add_argument("-Box", metavar="Box", type=float, default=[-10, 10, -5, 5, -4, 4],
                        nargs="*", help=("Box dimensionality. "
                        "Two values per dimension to set start and end (1D, 2D, 3D)."))
    parser.add_argument("-N", metavar="N", type=int, default=6 * 10 ** 4,
                        help="Number of particles in box")
    parser.add_argument("-m", metavar="m", type=int, default=164.0 * constants.u_in_kg,
                        help="Mass of a particle")
    parser.add_argument("-a_dd", metavar="a_dd", type=float, default=130.0 * constants.a_0,
                        help="Constant a_dd")
    parser.add_argument("-a_s", metavar="a_s", type=float, default=85.0 * constants.a_0,
                        help="Constant a_s")
    parser.add_argument("-w_x", metavar="w_x", type=float, default=2.0 * np.pi * 33.0,
                        help="Frequency of harmonic trap in x direction")
    parser.add_argument("-w_y", metavar="w_y", type=float, default=2.0 * np.pi * 80.0,
                        help="Frequency of harmonic trap in y direction")
    parser.add_argument("-w_z", metavar="w_z", type=float, default=2.0 * np.pi * 167.0,
                        help="Frequency of harmonic trap in z direction")
    parser.add_argument("-max_timesteps", metavar="max_timesteps", type=int, default=80001,
                        help="Simulate until accuracy is reached")
    parser.add_argument("-accuracy", metavar="accuracy", type=float, default=10 ** -12,
                        help="Simulate until accuracy is reached")
    parser.add_argument("-dir_path", metavar="dir_path", type=str, default="~/supersolids/results",
                        help="Absolute path to save data to")
    args = parser.parse_args()
    print(f"args: {args}")

    assert len(args.Res) <= 3, "Dimension of Res needs to be smaller than 3."
    assert len(args.Box) <= 6, ("Dimension of Box needs to be smaller than 6, "
                               "as the maximum dimension of the problem is 3.")
    try:
        dir_path = Path(args.dir_path).expanduser()
    except Exception:
        dir_path = args.dir_path

    keys = ["x", "y", "z"][:len(args.Res)]
    keys_box = ["x0", "x1", "y0", "y1", "z0", "z1"][:len(args.Box)]
    dict_res = dict(zip(keys, args.Res))
    dict_box = dict(zip(keys_box, args.Box))
    print(dict_res)
    print(dict_box)
    Res = functions.Resolution(**dict_res)
    Box = functions.Box(**dict_box)

    print(f"Res: {Res.x}, {Res.y}, {Res.z}")
    print(f"Box: {Box.x0}, {Box.x1}, {Box.y0}, {Box.y1}, {Box.z0}, {Box.z1}")

    alpha_y, alpha_z = functions.get_alphas(w_x=args.w_x, w_y=args.w_y, w_z=args.w_z)
    g, g_qf, e_dd, a_s_l_ho_ratio = functions.get_parameters(
        N=args.N, m=args.m, a_s=args.a_s, a_dd=args.a_dd, w_x=args.w_x)
    print(f"g, g_qf, e_dd, alpha_y, alpha_z: "
          f"{g, g_qf, e_dd, alpha_y, alpha_z}")

    # Define functions (needed for the Schroedinger equation)
    # (e.g. potential: V, initial wave function: psi_0)
    V_1d = functions.v_harmonic_1d
    V_2d = functools.partial(functions.v_harmonic_2d, alpha_y=alpha_y)
    V_3d = functools.partial(
        functions.v_harmonic_3d,
        alpha_y=alpha_y,
        alpha_z=alpha_z)

    V_3d_ddi = functools.partial(functions.dipol_dipol_interaction,
                                 r_cut=1.0 * Box.min_length() / 2.0)

    # functools.partial sets all arguments except x, y, z,
    # psi_0_1d = functools.partial(
    #     functions.psi_0_rect, x_min=-0.25, x_max=-0.25, a=2.0)
    psi_0_1d = functools.partial(
        functions.psi_gauss_1d, a=3.0, x_0=0.0, k_0=0.0)
    psi_0_2d = functools.partial(functions.psi_gauss_2d_pdf,
                                 mu=[0.0, 0.0],
                                 var=np.array([[1.0, 0.0], [0.0, 1.0]])
                                 )

    psi_0_3d = functools.partial(
        functions.psi_gauss_3d,
        a_x=3.5, a_y=1.5, a_z=1.2,
        x_0=0.0, y_0=0.0, z_0=0.0,
        k_0=0.0)
    # psi_0_3d = functools.partial(functions.prob_in_trap, R_r=R_r, R_z=R_z)

    psi_0_noise_3d = functions.noise_mesh(
        min=0.8, max=1.4, shape=(Res.x, Res.y, Res.z))

    # Used to remember that 2D need the special pos function (g is set inside
    # of Schroedinger for convenience)
    psi_sol_1d = functions.thomas_fermi_1d
    psi_sol_2d = functions.thomas_fermi_2d_pos

    # psi_sol_3d = functions.thomas_fermi_3d
    if Box.dim == 3:
        psi_sol_3d: Optional[Callable] = prepare_cuts(functions.density_in_trap,
                                                      args.N, alpha_z, e_dd,
                                                      a_s_l_ho_ratio)
    else:
        psi_sol_3d = None

    System: Schroedinger = Schroedinger(args.N,
                                        Box,
                                        Res,
                                        max_timesteps=args.max_timesteps,
                                        dt=args.dt,
                                        g=g,
                                        g_qf=g_qf,
                                        w_y=args.w_y,
                                        w_z=args.w_z,
                                        e_dd=e_dd,
                                        a_s=args.a_s,
                                        imag_time=True,
                                        mu=1.1,
                                        E=1.0,
                                        psi_0=psi_0_3d,
                                        V=V_3d,
                                        V_interaction=V_3d_ddi,
                                        psi_sol=psi_sol_3d,
                                        mu_sol=functions.mu_3d,
                                        psi_0_noise=None,
                                        )

    Anim: Animation = Animation(Res=System.Res,
                                plot_psi_sol=False,
                                plot_V=False,
                                alpha_psi=0.8,
                                alpha_psi_sol=0.5,
                                alpha_V=0.3,
                                camera_r_func=functools.partial(
                                    functions.camera_func_r,
                                    r_0=40.0, phi_0=45.0, z_0=50.0,
                                    r_per_frame=0.0),
                                camera_phi_func=functools.partial(
                                    functions.camera_func_phi,
                                    r_0=40.0, phi_0=45.0, z_0=50.0,
                                    phi_per_frame=5.0),
                                camera_z_func=functools.partial(
                                    functions.camera_func_z,
                                    r_0=40.0, phi_0=45.0, z_0=50.0,
                                    z_per_frame=0.0),
                                filename="anim.mp4",
                                )

    if Box.dim == 3:
        slice_indices = [int(Res.x / 2), int(Res.y / 2), int(Res.z / 2)]
    else:
        slice_indices = [None, None, None]

    # TODO: get mayavi lim to work
    # 3D works in single core mode
    SystemResult: Schroedinger = simulate_case(
                                    System,
                                    Anim,
                                    accuracy=args.accuracy,
                                    delete_input=False,
                                    dir_path=dir_path,
                                    slice_indices=slice_indices, # from here just mayavi
                                    interactive=True,
                                    x_lim=(-2.0, 2.0), # from here just matplotlib
                                    y_lim=(-2.0, 2.0),
                                    z_lim=(0, 0.5),
                                    )

    print("Single core done")
