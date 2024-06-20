# const2grad
Seismological Python tool for converting constant-layer velocity model (e.g. from 1-D hypocenter-velocity inversion) to gradient velocity model required for 3-D hypocenter-velocity inversion or any other purpose in seismology. Sometimes, the velocity model at hand is parameterized by layers with constant velocities (constant-velocity layers) and we need to transform this model into the best-fitting gradient model. For example, the former needs to be transformed in order to be used as the initial model for the 3-D inversion. Since this cannot be done exactly, we have approached the problem by implementing the algorithm that finds the best-fitting gradient model by successively calculating the slope between the newly constructed points. The resulting velocities are adjusted when velocity jumps occur that do not match the input velocity model.

Dependencies:

    * Matplotlib
    * NumPy
