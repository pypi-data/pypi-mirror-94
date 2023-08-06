Welcome to udkm1Dsim documentation!
=======================================

.. toctree::
    :hidden:
   
    Project Page <https://github.com/dschick/udkm1Dsim>
    Download from PyPI <http://pypi.python.org/pypi/udkm1Dsim>
    User Guide <user_guide>
    Examples <examples>
    API Documentation <api>

The *udkm1Dsim* toolbox is a collection of Python classes and routines to
simulate the thermal, structural, and magnetic dynamics after laser excitation
as well as the according X-ray scattering response in one-dimensional sample
structures after ultrafast excitation.

The toolbox provides the capabilities to define arbitrary layered structures
on the atomic level including a rich database of element-specific physical
properties. 
The excitation of ultrafast dynamics is represented by an
:math:`N`-temperature-model which is commonly applied for ultrafast optical
excitations. 
Structural dynamics due to thermal stresses are calculated by a linear-chain
model of masses and springs.
The implementation of magnetic dynamics can be easily accomplished by the user
for the individual problem.

The resulting X-ray diffraction response is computed by kinematical or
dynamical X-ray theory which can also include magnetic scattering.

The *udkm1Dsim* toolbox is highly modular and allows to introduce user-defined
results at any step in the simulation procedure.

The *udkm1Dsim* toolbox was initially developed for MATLAB® in the
*Ultrafast Dynamics in Condensed Matter* group of Prof. Matias Bargheer at the
*University of Potsdam*, Germany.
The MATLAB® source code is still available at
`github.com/dschick/udkm1DsimML <https://github.com/dschick/udkm1DsimML>`_.

The current toolbox, written in Python, is maintained by Daniel Schick at the
*Max-Born-Institute*, Berlin, Germany.

Citation
========

Please cite the original publication if you use the *udkm1Dsim* toolbox for your
own publications:

D. Schick, A. Bojahr, M. Herzog, R. Shayduk, C. von Korff Schmising & M. Bargheer,
*udkm1Dsim - A Simulation Toolkit for 1D Ultrafast Dynamics in Condensed Matter*,
`Comput. Phys. Commun. 185, 651 (2014) <http://doi.org/10.1016/j.cpc.2013.10.009>`_
`(preprint) <http://www.udkm.physik.uni-potsdam.de/medien/udkm1Dsim/udkm1DsimManuscriptPrePrint.pdf>`_.


Installation
============

You can either install directly from pypi.org using the command

::

    pip install udkm1Dsim

or if you want to work on the latest develop release you can clone 
udkm1Dsim from the main git repository:

::

    git clone https://github.com/dschick/udkm1Dsim.git udkm1Dsim

To work in editable mode (source is only linked 
but not copied to the python site-packages), just do:

::

    pip install -e ./udkm1Dsim

Or to do a normal install with

::

    pip install ./udkm1Dsim
   
You can have the following optional installation to enable parallel
computations, unit tests, as well as building the documentation:

::

    pip install udkm1Dsim[parallel]
    pip install udkm1Dsim[testing]
    pip install udkm1Dsim[documentation]

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
