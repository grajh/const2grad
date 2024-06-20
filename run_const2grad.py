#-*- coding: utf-8 -*-

import os

import numpy as np

import src.vel_const2grad as cgl
import src.veldist as vd


# Input velocity model.
VELMOD_IN = "in/MINMOD_MPS3_r2.4.3.mod"
# Desired depths for the output gradient velocity model.
ZN = [-5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 28.0, 36.0, 46.0, 80.0]


oned_bpath = os.path.splitext(VELMOD_IN)[0]
oned_name = os.path.split(oned_bpath)[1]


# Read velocities from 1-D model file.
# One format for conversion (const), one for plotting (step).
const_pdepths, const_pvels, const_sdepths, const_svels = vd.read_mod(
    VELMOD_IN)
step_pdepths, step_pvels, step_sdepths, step_svels = vd.read_mod(
    VELMOD_IN, step=True)


# Calculate vp/vs ratio.
const_vpvs = np.array(const_pvels) / np.array(const_svels)
step_vpvs = list(np.array(step_pvels) / np.array(step_svels))

# Uncomment for a constant vp/vs ratio of ~1.73.
# const_vpvs = [3**0.5] * len(const_vpvs)
# step_vpvs = [3**0.5] * len(step_vpvs)


# Convert to gradient model.
gradient_pmap = cgl.extract_const(const_pdepths, const_pvels)
gradient_vpvsmap = cgl.extract_const(const_pdepths, const_vpvs)

gradient_pdepths, gradient_pvels = cgl.return_gradient(ZN, gradient_pmap)
gradient_vpvsdepths, gradient_vpvs = cgl.return_gradient(ZN, gradient_vpvsmap)


# Plot.
# P-velocity
cgl.plot_conversion(
    step_pdepths, step_pvels, [gradient_pdepths], [gradient_pvels],
    oned_bpath, labels=['gradient P5D'])
# vp/vs
cgl.plot_conversion(
    step_pdepths, step_vpvs, [gradient_vpvsdepths], [gradient_vpvs],
    oned_bpath, which='vpvs', labels=['gradient P5D'])

