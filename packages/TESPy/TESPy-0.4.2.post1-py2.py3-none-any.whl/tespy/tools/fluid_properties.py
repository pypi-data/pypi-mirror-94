# -*- coding: utf-8

"""Module for fluid property integration.

TESPy uses the CoolProp python interface for all fluid property functions. The
TESPyFluid class allows the creation of lookup table for custom fluid
mixtures.


This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location tespy/tools/fluid_properties.py

SPDX-License-Identifier: MIT
"""

import logging
import os
from collections import OrderedDict

import CoolProp as CP
import numpy as np
import pandas as pd
from CoolProp.CoolProp import PropsSI as CPPSI
from scipy import interpolate

from tespy.tools.global_vars import err
from tespy.tools.global_vars import gas_constants
from tespy.tools.global_vars import molar_masses
from tespy.tools.helpers import molar_mass_flow
from tespy.tools.helpers import newton
from tespy.tools.helpers import reverse_2d
from tespy.tools.helpers import reverse_2d_deriv
from tespy.tools.helpers import single_fluid

# %%


class TESPyFluid:
    r"""
    Allow the creation of lookup tables for specified mixtures.

    The created fluid property lookup table adress an ideal mixture of real
    fluids.

    Parameters
    ----------
    alias : str
        Alias for the fluid. Please note: The alias of a TESPyFluid class
        object will always start with :code:`TESPy::`. See the example for more
        information!

    fluid : dict
        Fluid vector specifying the fluid composition of the TESPy fluid.

    p_range : list/ndarray
        Pressure range for the new fluid lookup table.

    T_range : list/ndarray
        Temperature range for the new fluid lookup table (optional).

    path : str
        Path to importing tespy fluid from.

    Note
    ----
    Creates lookup tables for

    - enthalpy (h),
    - entropy (s),
    - density (d) and
    - viscoity (visc)

    from pressure and temperature. Additionally molar mass and gas constant
    will be calculated. Inverse functions, e.g. entropy from pressure and
    enthalpy are calculated via newton algorithm from these tables.

    Example
    -------
    Create a custom fluid from specified composition within defined pressure
    and temperature limits. We define dry air component wise as our custom
    fluid.

    >>> from tespy.tools.fluid_properties import (TESPyFluid, h_mix_pT,
    ... s_mix_pT, v_mix_pT, visc_mix_pT)
    >>> from tespy.networks import Network
    >>> import shutil
    >>> fluidvec = {'N2': 0.7552, 'O2': 0.2314, 'CO2': 0.0005, 'Ar': 0.0129}
    >>> p_arr = np.array([0.1, 10]) * 1e5
    >>> myfluid = TESPyFluid('dry air', fluid=fluidvec, p_range=p_arr,
    ... T_range=[300, 1200])

    Check if the fluid creation was successful and compare some fluid
    properties to the CoolProp air implementation. We have to add the CoolProp
    air implementation to the memorise class first. The relative deviation
    should be very small (< 0.01), we check for enthalpy, volume, entropy and
    viscosity. Specific volume and viscosity are absolute values, thus no
    difference is calculated.

    >>> Memorise.add_fluids({'air': 'HEOS'})

    >>> type(myfluid)
    <class 'tespy.tools.fluid_properties.TESPyFluid'>
    >>> p = 3e5
    >>> fluid_props = [0, p, 0, {myfluid.alias: 1}]
    >>> T1 = 400
    >>> T2 = 1000
    >>> delta_h_tespy = h_mix_pT(fluid_props, T2) - h_mix_pT(fluid_props, T1)
    >>> fluid_props_CP = [0, p, 0, {'air': 1}]
    >>> delta_h = h_mix_pT(fluid_props_CP, T2) - h_mix_pT(fluid_props_CP, T1)
    >>> round(abs(delta_h_tespy - delta_h) / delta_h, 2)
    0.0

    >>> v_tespy = v_mix_pT(fluid_props, T2)
    >>> v = v_mix_pT(fluid_props_CP, T2)
    >>> round(abs(v_tespy - v) / v, 2)
    0.0

    >>> s_tespy = s_mix_pT(fluid_props, T2) - s_mix_pT(fluid_props, T1)
    >>> s = s_mix_pT(fluid_props_CP, T2) - s_mix_pT(fluid_props_CP, T1)
    >>> round(abs(s_tespy - s) / s, 2)
    0.0

    >>> visc_tespy = visc_mix_pT(fluid_props, T2)
    >>> visc = visc_mix_pT(fluid_props_CP, T2)
    >>> round(abs(visc_tespy - visc) / visc, 2)
    0.0

    The fluid had been saved automatically, load it now.

    >>> loadfluid = TESPyFluid('dry air', fluid=fluidvec, p_range=p_arr,
    ... path='./LUT')
    >>> type(loadfluid)
    <class 'tespy.tools.fluid_properties.TESPyFluid'>
    >>> shutil.rmtree('./LUT', ignore_errors=True)
    """

    def __init__(self, alias, fluid, p_range, T_range=None, path=None):

        if not isinstance(alias, str):
            msg = 'Alias must be of type String.'
            logging.error(msg)
            raise TypeError(msg)

        # process parameters
        if '::' in alias:
            msg = 'The sequence "::" is not allowed in your fluid alias.'
            logging.error(msg)
            raise ValueError(msg)
        else:
            self.alias = alias

        self.fluid = fluid

        # path for loading
        self.path = path

        # create look up tables
        TESPyFluid.fluids[self.alias] = self

        self.fluids_back_ends = OrderedDict()

        for fluid in sorted(list(self.fluid.keys()) + [self.alias]):
            try:
                data = fluid.split('::')
                back_end = data[0]
                fluid = data[1]
            except IndexError:
                back_end = 'HEOS'
            if fluid != self.alias:
                self.fluids_back_ends[fluid] = back_end

        Memorise.add_fluids(self.fluids_back_ends)

        # set up grid
        self.p = np.geomspace(p_range[0], p_range[1], 100)

        if T_range is None:
            T_range = [max([Memorise.value_range[f][2] for f
                            in self.fluids_back_ends.keys()]) + 1, 2000]

        self.T = np.geomspace(T_range[0], T_range[1], 100)

        Memorise.add_fluids({self.alias: 'TESPy'})

        params = {}
        params['h_pT'] = h_mix_pT
        params['s_pT'] = s_mix_pT
        params['d_pT'] = d_mix_pT
        params['visc_pT'] = visc_mix_pT

        self.funcs = {}

        if self.path is None:
            # generate fluid properties
            msg = 'Generating lookup-tables from CoolProp fluid properties.'
            logging.debug(msg)
            for key in params.keys():
                self.funcs[key] = self.generate_lookup(key, params[key])
                msg = 'Loading function values for function ' + key + '.'
                logging.debug(msg)

        else:
            # load fluid properties from specified path
            msg = ('Generating lookup-tables from base path ' + self.path +
                   '/' + self.alias + '/.')
            logging.debug(msg)
            for key in params.keys():
                self.funcs[key] = self.load_lookup(key)
                msg = 'Loading function values for function ' + key + '.'
                logging.debug(msg)

        msg = ('Successfully created look-up-tables for custom fluid ' +
               self.alias + '.')
        logging.debug(msg)

    def generate_lookup(self, name, func):
        r"""
        Create lookup table from CoolProp-database.

        Parameters
        ----------
        name : str
            Name of the lookup table.

        func : function
            Function to create lookup table from.
        """
        x1 = self.p
        x2 = self.T

        y = np.empty((0, x1.shape[0]), float)

        # iterate
        for p in x1:
            row = []
            for T in x2:
                row += [func([0, p, 0, self.fluid], T)]

            y = np.append(y, [np.array(row)], axis=0)

        self.save_lookup(name, x1, x2, y)

        func = interpolate.RectBivariateSpline(x1, x2, y)
        return func

    def save_lookup(self, name, x1, x2, y):
        r"""
        Save lookup table to working dir :code:`./LUT/fluid_alias/`.

        Parameters
        ----------
        name : str
            Name of the lookup table.

        x1 : ndarray
            Pressure.

        x2 : ndarray
            Temperature.

        y : ndarray
            Lookup value (enthalpy, entropy, density or viscosity)
        """
        df = pd.DataFrame(y, columns=x2, index=x1)
        alias = self.alias.replace('::', '_')
        path = './LUT/' + alias + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        df.to_csv(path + name + '.csv')

    def load_lookup(self, name):
        r"""
        Load lookup table from specified path base path and alias.

        Parameters
        ----------
        name : str
            Name of the lookup table.
        """
        alias = self.alias.replace('::', '_')
        path = self.path + '/' + alias + '/' + name + '.csv'
        df = pd.read_csv(path, index_col=0)

        x1 = df.index.values
        x2 = np.array(list(map(float, list(df))))
        y = df.values

        func = interpolate.RectBivariateSpline(x1, x2, y)
        return func


# create dict for tespy fluids
TESPyFluid.fluids = {}

# %%


class Memorise:
    r"""Memorization of fluid properties."""

    @staticmethod
    def add_fluids(fluids, memorise_fluid_properties=True):
        r"""
        Add list of fluids to fluid memorisation class.

        - Generate arrays for fluid property lookup if memorisation is
          activated.
        - Calculate/set fluid property value ranges for convergence checks.

        Parameters
        ----------
        fluids : dict
            Dict of fluid and corresponding CoolProp back end for fluid
            property memorization.

        memorise_fluid_properties : boolean
            Activate or deactivate fluid property value memorisation. Default
            state is activated (:code:`True`).

        Note
        ----
        The Memorise class creates globally accessible variables for different
        fluid property calls as dictionaries:

        - T(p,h)
        - T(p,s)
        - v(p,h)
        - visc(p,h)
        - s(p,h)

        Each dictionary uses the list of fluids passed to the Memorise class as
        identifier for the fluid property memorisation. The fluid properties
        are stored as numpy array, where each column represents the mass
        fraction of the respective fluid and the additional columns are the
        values for the fluid properties. The fluid property function will then
        look for identical fluid property inputs (p, h, (s), fluid mass
        fraction). If the inputs are in the array, the first column of that row
        is returned, see example.

        Example
        -------
        T(p,h) for set of fluids ('water', 'air'):

        - row 1: [282.64527752319697, 10000, 40000, 1, 0]
        - row 2: [284.3140698256616, 10000, 47000, 1, 0]
        """
        # number of fluids
        num_fl = len(fluids)
        if memorise_fluid_properties and num_fl > 0:
            fl = tuple(fluids.keys())
            # fluid property tables
            Memorise.T_ph[fl] = np.empty((0, num_fl + 4), float)
            Memorise.T_ps[fl] = np.empty((0, num_fl + 5), float)
            Memorise.v_ph[fl] = np.empty((0, num_fl + 4), float)
            Memorise.visc_ph[fl] = np.empty((0, num_fl + 4), float)
            Memorise.s_ph[fl] = np.empty((0, num_fl + 4), float)

            msg = (
                'Added fluids ' + ', '.join(fl) +
                ' to memorise lookup tables.')
            logging.debug(msg)

        for f, back_end in fluids.items():
            if f not in Memorise.state.keys() and back_end != 'TESPy':
                # create CoolProp.AbstractState object
                try:
                    Memorise.state[f] = CP.AbstractState(back_end, f)
                    Memorise.back_end[f] = back_end
                except ValueError:
                    msg = (
                        'Could not find the fluid "' + f + '" in the fluid '
                        'property database. If you are using a stoichimetric '
                        'combustion chamber, this warning can be ignored in '
                        'case the fluid is your fuel, your flue gas or your '
                        'air.')
                    logging.warning(msg)
                    continue

                msg = (
                    'Created CoolProp.AbstractState object for fluid ' +
                    f + ' with back end ' + back_end + '.')
                logging.debug(msg)
                # pressure range
                try:
                    pmin = Memorise.state[f].trivial_keyed_output(CP.iP_min)
                    pmax = Memorise.state[f].trivial_keyed_output(CP.iP_max)
                except ValueError:
                    pmin = 1e4
                    pmax = 1e8
                    msg = (
                        'Could not find values for maximum and minimum '
                        'pressure.')
                    logging.warning(msg)

                # temperature range
                Tmin = Memorise.state[f].trivial_keyed_output(CP.iT_min)
                Tmax = Memorise.state[f].trivial_keyed_output(CP.iT_max)

                # value range for fluid properties
                Memorise.value_range[f] = [pmin, pmax, Tmin, Tmax]

                try:
                    molar_masses[f] = Memorise.state[f].molar_mass()
                    gas_constants[f] = Memorise.state[f].gas_constant()
                except ValueError:
                    try:
                        molar_masses[f] = CPPSI('M', f)
                        gas_constants[f] = CPPSI('GAS_CONSTANT', f)
                    except ValueError:
                        molar_masses[f] = 1
                        gas_constants[f] = 1
                        msg = (
                            'Could not find values for molar mass and gas '
                            'constant.')
                        logging.warning(msg)

                msg = (
                    'Specifying fluid property ranges for pressure and '
                    'temperature for convergence check of fluid ' + f + '.')
                logging.debug(msg)

            elif back_end == 'TESPy':
                pmin = TESPyFluid.fluids[f].p[0]
                pmax = TESPyFluid.fluids[f].p[-1]
                Tmin = TESPyFluid.fluids[f].T[0]
                Tmax = TESPyFluid.fluids[f].T[-1]
                msg = (
                    'Loading fluid property ranges for TESPy-fluid ' + f + '.')
                logging.debug(msg)
                # value range for fluid properties
                Memorise.value_range[f] = [pmin, pmax, Tmin, Tmax]
                molar_masses[f] = 1 / molar_mass_flow(
                    TESPyFluid.fluids[f].fluid)
                gas_constants[f] = (
                    gas_constants['uni'] / molar_masses[f])
                msg = ('Specifying fluid property ranges for pressure and '
                       'temperature for convergence check.')
                logging.debug(msg)

    @staticmethod
    def del_memory(fluids):
        r"""
        Delete non frequently used fluid property values from memorise class.

        Parameters
        ----------
        fluids : list
            List of fluid for fluid property memorization.
        """
        fl = tuple(fluids)
        threshold = 3
        try:
            # delete memory
            Memorise.s_ph[fl] = Memorise.s_ph[fl][
                Memorise.s_ph[fl][:, -1] > threshold]
            Memorise.s_ph[fl][:, -1] = 0

            Memorise.T_ph[fl] = Memorise.T_ph[fl][
                Memorise.T_ph[fl][:, -1] > threshold]
            Memorise.T_ph[fl][:, -1] = 0

            Memorise.T_ps[fl] = Memorise.T_ps[fl][
                Memorise.T_ps[fl][:, -1] > threshold]
            Memorise.T_ps[fl][:, -1] = 0

            Memorise.v_ph[fl] = Memorise.v_ph[fl][
                Memorise.v_ph[fl][:, -1] > threshold]
            Memorise.v_ph[fl][:, -1] = 0

            Memorise.visc_ph[fl] = Memorise.visc_ph[fl][
                Memorise.visc_ph[fl][:, -1] > threshold]
            Memorise.visc_ph[fl][:, -1] = 0

            msg = ('Dropping not frequently used fluid property values from '
                   'memorise class for fluids ' + ', '.join(fl) + '.')
            logging.debug(msg)
        except KeyError:
            pass


# create memorise dictionaries
Memorise.state = {}
Memorise.back_end = {}
Memorise.T_ph = {}
Memorise.T_ps = {}
Memorise.v_ph = {}
Memorise.visc_ph = {}
Memorise.s_ph = {}
Memorise.value_range = {}

# %%


def T_mix_ph(flow, T0=300):
    r"""
    Calculate the temperature from pressure and enthalpy.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    T : float
        Temperature T / K.

    Note
    ----
    First, check if fluid property has been memorised already.
    If this is the case, return stored value, otherwise calculate value and
    store it in the memorisation class.

    Uses CoolProp interface for pure fluids, newton algorithm for mixtures:

    .. math::

        T_{mix}\left(p,h\right) = T_{i}\left(p,h_{i}\right)\;
        \forall i \in \text{fluid components}\\

        h_{i} = h \left(pp_{i}, T_{mix} \right)\\
        pp: \text{partial pressure}
    """
    # check if fluid properties have been calculated before
    fl = tuple(flow[3].keys())
    memorisation = fl in Memorise.T_ph.keys()
    if memorisation:
        a = Memorise.T_ph[fl][:, :-2]
        b = np.array([flow[1], flow[2]] + list(flow[3].values()))
        ix = np.where(np.all(abs(a - b) <= err, axis=1))[0]

        if ix.size == 1:
            # known fluid properties
            Memorise.T_ph[fl][ix, -1] += 1
            return Memorise.T_ph[fl][ix, -2][0]

    # unknown fluid properties
    fluid = single_fluid(flow[3])
    if fluid is None:
        # calculate the fluid properties for fluid mixtures
        valmin = max(
            [Memorise.value_range[f][2] for f in fl if flow[3][f] > err]
        ) + 0.1
        if T0 < valmin or np.isnan(T0):
            T0 = valmin * 1.1

        val = newton(h_mix_pT, dh_mix_pdT, flow, flow[2], val0=T0,
                     valmin=valmin, valmax=3000, imax=10)
    else:
        # calculate fluid property for pure fluids
        val = T_ph(flow[1], flow[2], fluid)

    if memorisation:
        # memorise the newly calculated value
        new = np.asarray(
            [[flow[1], flow[2]] + list(flow[3].values()) + [val, 0]])
        Memorise.T_ph[fl] = np.append(Memorise.T_ph[fl], new, axis=0)

    return val


def T_ph(p, h, fluid):
    r"""
    Calculate the temperature from pressure and enthalpy for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    h : float
        Specific enthalpy h / (J/kg).

    fluid : str
        Fluid name.

    Returns
    -------
    T : float
        Temperature T / K.
    """
    if fluid in TESPyFluid.fluids.keys():
        db = TESPyFluid.fluids[fluid].funcs['h_pT']
        return newton(reverse_2d, reverse_2d_deriv, [db, p, h], 0)
    elif Memorise.back_end[fluid] == 'IF97':
        return entropy_iteration_IF97(p, h, fluid, 'T')
    else:
        Memorise.state[fluid].update(CP.HmassP_INPUTS, h, p)
        return Memorise.state[fluid].T()


def dT_mix_dph(flow, T0=300):
    r"""
    Calculate partial derivate of temperature to pressure.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    dT / dp : float
        Partial derivative of temperature to pressure dT /dp / (K/Pa).

        .. math::

            \frac{\partial T_{mix}}{\partial p} = \frac{T_{mix}(p+d,h)-
            T_{mix}(p-d,h)}{2 \cdot d}
    """
    d = 1
    up = flow.copy()
    lo = flow.copy()
    up[1] += d
    lo[1] -= d
    return (T_mix_ph(up, T0=T0) - T_mix_ph(lo, T0=T0)) / (2 * d)


def dT_mix_pdh(flow, T0=300):
    r"""
    Calculate partial derivate of temperature to enthalpy.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    dT / dh : float
        Partial derivative of temperature to enthalpy dT /dh / ((kgK)/J).

        .. math::

            \frac{\partial T_{mix}}{\partial h} = \frac{T_{mix}(p,h+d)-
            T_{mix}(p,h-d)}{2 \cdot d}
    """
    d = 1
    up = flow.copy()
    lo = flow.copy()
    up[2] += d
    lo[2] -= d
    return (T_mix_ph(up, T0=T0) - T_mix_ph(lo, T0=T0)) / (2 * d)


def dT_mix_ph_dfluid(flow, T0=300):
    r"""
    Calculate partial derivate of temperature to fluid composition.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    dT / dfluid : ndarray
        Partial derivatives of temperature to fluid composition
        dT / dfluid / K.

        .. math::

            \frac{\partial T_{mix}}{\partial fluid_{i}} =
            \frac{T_{mix}(p,h,fluid_{i}+d)-
            T_{mix}(p,h,fluid_{i}-d)}{2 \cdot d}
    """
    d = 1e-5
    up = flow.copy()
    lo = flow.copy()
    vec_deriv = []
    for fluid, x in flow[3].items():
        if x > err:
            up[3][fluid] += d
            lo[3][fluid] -= d
            vec_deriv += [
                (T_mix_ph(up, T0=T0) - T_mix_ph(lo, T0=T0)) / (2 * d)]
            up[3][fluid] -= d
            lo[3][fluid] += d
        else:
            vec_deriv += [0]

    return vec_deriv

# %%


def T_mix_ps(flow, s, T0=300):
    r"""
    Calculate the temperature from pressure and entropy.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    s : float
        Entropy of flow in J / (kgK).

    Returns
    -------
    T : float
        Temperature T / K.

    Note
    ----
    First, check if fluid property has been memorised already.
    If this is the case, return stored value, otherwise calculate value and
    store it in the memorisation class.

    Uses CoolProp interface for pure fluids, newton algorithm for mixtures:

    .. math::

        T_{mix}\left(p,s\right) = T_{i}\left(p,s_{i}\right)\;
        \forall i \in \text{fluid components}\\

        s_{i} = s \left(pp_{i}, T_{mix} \right)\\
        pp: \text{partial pressure}

    """
    # check if fluid properties have been calculated before
    fl = tuple(flow[3].keys())
    memorisation = fl in Memorise.T_ps.keys()
    if memorisation:
        a = Memorise.T_ps[fl][:, :-2]
        b = np.asarray([flow[1], flow[2]] + list(flow[3].values()) + [s])
        ix = np.where(np.all(abs(a - b) <= err, axis=1))[0]
        if ix.size == 1:
            # known fluid properties
            Memorise.T_ps[fl][ix, -1] += 1
            return Memorise.T_ps[fl][ix, -2][0]

    # unknown fluid properties
    fluid = single_fluid(flow[3])
    if fluid is None:
        # calculate the fluid properties for fluid mixtures
        valmin = max(
            [Memorise.value_range[f][2] for f in fl if flow[3][f] > err]
        ) + 0.1
        if T0 < valmin or np.isnan(T0):
            T0 = valmin * 1.1

        val = newton(s_mix_pT, ds_mix_pdT, flow, s, val0=T0,
                     valmin=valmin, valmax=3000, imax=10)

    else:
        # calculate fluid property for pure fluids
        val = T_ps(flow[1], s, fluid)

    if memorisation:
        new = np.asarray(
            [[flow[1], flow[2]] + list(flow[3].values()) + [s, val, 0]])
        # memorise the newly calculated value
        Memorise.T_ps[fl] = np.append(Memorise.T_ps[fl], new, axis=0)

    return val


def T_ps(p, s, fluid):
    r"""
    Calculate the temperature from pressure and entropy for a pure fluid.

    Parameters
    ----------
    p : float
       Pressure p / Pa.

    s : float
       Specific entropy h / (J/(kgK)).

    fluid : str
       Fluid name.

    Returns
    -------
    T : float
       Temperature T / K.
    """
    if fluid in TESPyFluid.fluids.keys():
        db = TESPyFluid.fluids[fluid].funcs['s_pT']
        return newton(reverse_2d, reverse_2d_deriv, [db, p, s], 0)
    else:
        Memorise.state[fluid].update(CP.PSmass_INPUTS, p, s)
        return Memorise.state[fluid].T()

# %%


def h_mix_pT(flow, T, force_gas=False):
    r"""
    Calculate the enthalpy from pressure and Temperature.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    T : float
        Temperature of flow T / K.

    Returns
    -------
    h : float
        Enthalpy h / (J/kg).

    Note
    ----
    Calculation for fluid mixtures.

    .. math::

        h_{mix}(p,T)=\sum_{i} h(pp_{i},T,fluid_{i})\;
        \forall i \in \text{fluid components}\\
        pp: \text{partial pressure}
    """
    n = molar_mass_flow(flow[3])

    h = 0
    for fluid, x in flow[3].items():
        if x > err:
            ni = x / molar_masses[fluid]
            h += h_pT(flow[1] * ni / n, T, fluid, force_gas) * x

    return h


def h_pT(p, T, fluid, force_gas=False):
    r"""
    Calculate the enthalpy from pressure and temperature for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    T : float
        Temperature T / K.

    fluid : str
        Fluid name.

    Returns
    -------
    h : float
        Specific enthalpy h / (J/kg).
    """
    if fluid in TESPyFluid.fluids.keys():
        return TESPyFluid.fluids[fluid].funcs['h_pT'].ev(p, T)
    else:
        if force_gas:
            if T < Memorise.state[fluid].trivial_keyed_output(CP.iT_critical):
                Memorise.state[fluid].update(CP.PT_INPUTS, p, T)
                h = Memorise.state[fluid].hmass()
                Memorise.state[fluid].update(CP.QT_INPUTS, 1, T)
                h_sat = Memorise.state[fluid].hmass()
                return max(h, h_sat)

        Memorise.state[fluid].update(CP.PT_INPUTS, p, T)
        return Memorise.state[fluid].hmass()


def dh_mix_pdT(flow, T):
    r"""
    Calculate partial derivate of enthalpy to temperature.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    T : float
        Temperature T / K.

    Returns
    -------
    dh / dT : float
        Partial derivative of enthalpy to temperature dh / dT / (J/(kgK)).

        .. math::

            \frac{\partial h_{mix}}{\partial T} =
            \frac{h_{mix}(p,T+d)-h_{mix}(p,T-d)}{2 \cdot d}
    """
    d = 0.1
    return (h_mix_pT(flow, T + d) - h_mix_pT(flow, T - d)) / (2 * d)

# %%


def h_mix_ps(flow, s, T0=300):
    r"""
    Calculate the enthalpy from pressure and temperature.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    s : float
        Specific entropy of flow s / (J/(kgK)).

    Returns
    -------
    h : float
        Specific enthalpy h / (J/kg).

    Note
    ----
    Calculation for fluid mixtures.

    .. math::

        h_{mix}\left(p,s\right)=h\left(p, T_{mix}\left(p,s\right)\right)
    """
    return h_mix_pT(flow, T_mix_ps(flow, s, T0=T0))


def h_ps(p, s, fluid):
    r"""
    Calculate the enthalpy from pressure and entropy for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    s : float
        Specific entropy h / (J/(kgK)).

    fluid : str
        Fluid name.

    Returns
    -------
    h : float
        Specific enthalpy h / (J/kg).
    """
    if fluid in TESPyFluid.fluids.keys():
        db = TESPyFluid.fluids[fluid].funcs['s_pT']
        T = newton(reverse_2d, reverse_2d_deriv, [db, p, s], 0)
        return TESPyFluid.fluids[fluid].funcs['h_pT'].ev(p, T)
    else:
        Memorise.state[fluid].update(CP.PSmass_INPUTS, p, s)
        return Memorise.state[fluid].hmass()


def h_ps_IF97(params, s):
    r"""
    Calculate the enthalpy from pressure and entropy for IF97 backend.

    Parameters
    ----------
    fluid : str
        Fluid name.

    p : float
        Pressure p / Pa.

    s : float
        Specific entropy h / (J/(kgK)).

    Returns
    -------
    h : float
        Specific enthalpy h / (J/kg).
    """
    Memorise.state[params[0]].update(CP.PSmass_INPUTS, params[1], s)
    return Memorise.state[params[0]].hmass()


def dh_pds_IF97(params, s):
    r"""
    Calculate the derivative of enthalpy to entropy at constant pressure.

    For pure fluids only, required for IF97 entropy iteration only.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    s : float
        Specific entropy h / (J/(kgK)).

    fluid : str
        Fluid name.

    Returns
    -------
    dh : float
        Derivative of specific enthalpy dh / ds / K.
    """
    d = 1e-2
    Memorise.state[params[0]].update(CP.PSmass_INPUTS, params[1], s + d)
    h_upper = Memorise.state[params[0]].hmass()

    Memorise.state[params[0]].update(CP.PSmass_INPUTS, params[1], s - d)
    h_lower = Memorise.state[params[0]].hmass()

    return (h_upper - h_lower) / (2 * d)
# %%


def h_mix_pQ(flow, Q):
    r"""
    Calculate the enthalpy from pressure and vapour mass fraction.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Q : float
        Vapour mass fraction Q / 1.

    Returns
    -------
    h : float
        Specific enthalpy h / (J/kg).

    Note
    ----
    This function works for pure fluids only!
    """
    fluid = single_fluid(flow[3])
    if fluid is None:
        msg = 'The function h_mix_pQ can only be used for pure fluids.'
        logging.error(msg)
        raise ValueError(msg)

    try:
        Memorise.state[fluid].update(CP.PQ_INPUTS, flow[1], Q)
    except ValueError:
        pcrit = Memorise.state[fluid].trivial_keyed_output(CP.iP_critical)
        Memorise.state[fluid].update(CP.PQ_INPUTS, pcrit * 0.99, Q)

    return Memorise.state[fluid].hmass()


def dh_mix_dpQ(flow, Q):
    r"""
    Calculate partial derivate of enthalpy to vapour mass fraction.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Q : float
        Vapour mass fraction Q / 1.

    Returns
    -------
    dh / dQ : float
        Partial derivative of enthalpy to vapour mass fraction
        dh / dQ / (J/kg).

        .. math::

            \frac{\partial h_{mix}}{\partial p} =
            \frac{h_{mix}(p+d,Q)-h_{mix}(p-d,Q)}{2 \cdot d}\\
            Q: \text{vapour mass fraction}

    Note
    ----
    This works for pure fluids only!
    """
    d = 1
    up = flow.copy()
    lo = flow.copy()
    up[1] += d
    lo[1] -= d
    return (h_mix_pQ(up, Q) - h_mix_pQ(lo, Q)) / (2 * d)

# %%


def T_bp_p(flow):
    r"""
    Calculate temperature from boiling point pressure.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    T : float
        Temperature at boiling point.

    Note
    ----
    This function works for pure fluids only!
    """
    fluid = single_fluid(flow[3])
    pcrit = Memorise.state[fluid].trivial_keyed_output(CP.iP_critical)
    if flow[1] > pcrit:
        Memorise.state[fluid].update(CP.PQ_INPUTS, pcrit * 0.99, 1)
    else:
        Memorise.state[fluid].update(CP.PQ_INPUTS, flow[1], 1)
    return Memorise.state[fluid].T()


def dT_bp_dp(flow):
    r"""
    Calculate partial derivate of temperature to boiling point pressure.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    dT / dp : float
        Partial derivative of temperature to boiling point pressure in K / Pa.

        .. math::

            \frac{\partial h_{mix}}{\partial p} =
            \frac{T_{bp}(p+d)-T_{bp}(p-d)}{2 \cdot d}\\
            Q: \text{vapour mass fraction}

    Note
    ----
    This works for pure fluids only!
    """
    d = 1
    up = flow.copy()
    lo = flow.copy()
    up[1] += d
    lo[1] -= d
    return (T_bp_p(up) - T_bp_p(lo)) / (2 * d)

# %%


def v_mix_ph(flow, T0=300):
    r"""
    Calculate the specific volume from pressure and enthalpy.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    v : float
        Specific volume v / (:math:`\mathrm{m}^3`/kg).

    Note
    ----
    First, check if fluid property has been memorised already.
    If this is the case, return stored value, otherwise calculate value and
    store it in the memorisation class.

    Uses CoolProp interface for pure fluids, newton algorithm for mixtures:

    .. math::

        v_{mix}\left(p,h\right) = v\left(p,T_{mix}(p,h)\right)
    """
    # check if fluid properties have been calculated before
    fl = tuple(flow[3].keys())
    memorisation = fl in Memorise.v_ph.keys()
    if memorisation:
        a = Memorise.v_ph[fl][:, :-2]
        b = np.asarray([flow[1], flow[2]] + list(flow[3].values()))
        ix = np.where(np.all(abs(a - b) <= err, axis=1))[0]
        if ix.size == 1:
            # known fluid properties
            Memorise.v_ph[fl][ix, -1] += 1
            return Memorise.v_ph[fl][ix, -2][0]

    # unknown fluid properties
    fluid = single_fluid(flow[3])
    if fluid is None:
        # calculate the fluid properties for fluid mixtures
        val = v_mix_pT(flow, T_mix_ph(flow, T0=T0))
    else:
        # calculate fluid property for pure fluids
        val = 1 / d_ph(flow[1], flow[2], fluid)

    if memorisation:
        # memorise the newly calculated value
        new = np.asarray(
            [[flow[1], flow[2]] + list(flow[3].values()) + [val, 0]])
        Memorise.v_ph[fl] = np.append(Memorise.v_ph[fl], new, axis=0)

    return val


def d_ph(p, h, fluid):
    r"""
    Calculate the density from pressure and enthalpy for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    h : float
        Specific enthalpy h / (J/kg).

    fluid : str
        Fluid name.

    Returns
    -------
    d : float
        Density d / (kg/:math:`\mathrm{m}^3`).
    """
    if fluid in TESPyFluid.fluids.keys():
        db = TESPyFluid.fluids[fluid].funcs['h_pT']
        T = newton(reverse_2d, reverse_2d_deriv, [db, p, h], 0)
        return TESPyFluid.fluids[fluid].funcs['d_pT'].ev(p, T)
    elif Memorise.back_end[fluid] == 'IF97':
        return entropy_iteration_IF97(p, h, fluid, 'rho')
    else:
        Memorise.state[fluid].update(CP.HmassP_INPUTS, h, p)
        return Memorise.state[fluid].rhomass()

# %%


def Q_ph(p, h, fluid):
    r"""
    Calculate vapor mass fraction from pressure and enthalpy for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    h : float
        Specific enthalpy h / (J/kg).

    fluid : str
        Fluid name.

    Returns
    -------
    x : float
        Vapor mass fraction.
    """
    try:
        Memorise.state[fluid].update(CP.HmassP_INPUTS, h, p)
        return Memorise.state[fluid].Q()
    except (KeyError, ValueError):
        return np.nan

# %%


def dv_mix_dph(flow, T0=300):
    r"""
    Calculate partial derivate of specific volume to pressure.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    dv / dp : float
        Partial derivative of specific volume to pressure
        dv /dp / (:math:`\mathrm{m}^3`/(Pa kg)).

        .. math::

            \frac{\partial v_{mix}}{\partial p} = \frac{v_{mix}(p+d,h)-
            v_{mix}(p-d,h)}{2 \cdot d}
    """
    d = 1
    up = flow.copy()
    lo = flow.copy()
    up[1] += d
    lo[1] -= d
    return (v_mix_ph(up, T0=T0) - v_mix_ph(lo, T0=T0)) / (2 * d)


def dv_mix_pdh(flow, T0=300):
    r"""
    Calculate partial derivate of specific volume to enthalpy.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    dv / dh : float
        Partial derivative of specific volume to enthalpy
        dv /dh / (:math:`\mathrm{m}^3`/J).

        .. math::

            \frac{\partial v_{mix}}{\partial h} = \frac{v_{mix}(p,h+d)-
            v_{mix}(p,h-d)}{2 \cdot d}
    """
    d = 1
    up = flow.copy()
    lo = flow.copy()
    up[2] += d
    lo[2] -= d
    return (v_mix_ph(up, T0=T0) - v_mix_ph(lo, T0=T0)) / (2 * d)

# %%


def v_mix_pT(flow, T):
    r"""
    Calculate the specific volume from pressure and temperature.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    T : float
        Temperature T / K.

    Returns
    -------
    v : float
        Specific volume v / (:math:`\mathrm{m}^3`/kg).

    Note
    ----
    Calculation for fluid mixtures.

    .. math::

        v_{mix}(p,T)=\frac{1}{\sum_{i} \rho(pp_{i}, T, fluid_{i})}\;
        \forall i \in \text{fluid components}\\
        pp: \text{partial pressure}
    """
    n = molar_mass_flow(flow[3])

    d = 0
    for fluid, x in flow[3].items():
        if x > err:
            ni = x / molar_masses[fluid]
            d += d_pT(flow[1] * ni / n, T, fluid)

    return 1 / d


def d_mix_pT(flow, T):
    r"""
    Calculate the density from pressure and temperature.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    T : float
        Temperature T / K.

    Returns
    -------
    d : float
        Density d / (kg/:math:`\mathrm{m}^3`).

    Note
    ----
    Calculation for fluid mixtures.

    .. math::

        \rho_{mix}\left(p,T\right)=\frac{1}{v_{mix}\left(p,T\right)}
    """
    return 1 / v_mix_pT(flow, T)


def d_pT(p, T, fluid):
    r"""
    Calculate the density from pressure and temperature for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    T : float
        Temperature T / K.

    fluid : str
        Fluid name.

    Returns
    -------
    d : float
        Density d / (kg/:math:`\mathrm{m}^3`).
    """
    if fluid in TESPyFluid.fluids.keys():
        return TESPyFluid.fluids[fluid].funcs['d_pT'].ev(p, T)
    else:
        Memorise.state[fluid].update(CP.PT_INPUTS, p, T)
        return Memorise.state[fluid].rhomass()

# %%


def visc_mix_ph(flow, T0=300):
    r"""
    Calculate the dynamic viscorsity from pressure and enthalpy.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    visc : float
        Dynamic viscosity visc / Pa s.

    Note
    ----
    First, check if fluid property has been memorised already.
    If this is the case, return stored value, otherwise calculate value and
    store it in the memorisation class.

    Uses CoolProp interface for pure fluids, newton algorithm for mixtures:

    .. math::

        \eta_{mix}\left(p,h\right) = \eta\left(p,T_{mix}(p,h)\right)
    """
    # check if fluid properties have been calculated before
    fl = tuple(flow[3].keys())
    memorisation = fl in Memorise.visc_ph.keys()
    if memorisation:
        a = Memorise.visc_ph[fl][:, :-2]
        b = np.asarray([flow[1], flow[2]] + list(flow[3].values()))
        ix = np.where(np.all(abs(a - b) <= err, axis=1))[0]
        if ix.size == 1:
            # known fluid properties
            Memorise.visc_ph[fl][ix, -1] += 1
            return Memorise.visc_ph[fl][ix, -2][0]

    # unknown fluid properties
    fluid = single_fluid(flow[3])
    if fluid is None:
        # calculate the fluid properties for fluid mixtures
        val = visc_mix_pT(flow, T_mix_ph(flow, T0=T0))
    else:
        # calculate the fluid properties for pure fluids
        val = visc_ph(flow[1], flow[2], fluid)

    if memorisation:
        # memorise the newly calculated value
        new = np.asarray(
            [[flow[1], flow[2]] + list(flow[3].values()) + [val, 0]])
        Memorise.visc_ph[fl] = np.append(Memorise.visc_ph[fl], new, axis=0)
    return val


def visc_ph(p, h, fluid):
    r"""
    Calculate dynamic viscosity from pressure and enthalpy for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    h : float
        Specific enthalpy h / (J/kg).

    fluid : str
        Fluid name.

    Returns
    -------
    visc : float
        Viscosity visc / Pa s.
    """
    if fluid in TESPyFluid.fluids.keys():
        db = TESPyFluid.fluids[fluid].funcs['h_pT']
        T = newton(reverse_2d, reverse_2d_deriv, [db, p, h], 0)
        return TESPyFluid.fluids[fluid].funcs['visc_pT'].ev(p, T)
    elif Memorise.back_end[fluid] == 'IF97':
        return entropy_iteration_IF97(p, h, fluid, 'visc')
    else:
        Memorise.state[fluid].update(CP.HmassP_INPUTS, h, p)
        return Memorise.state[fluid].viscosity()

# %%


def visc_mix_pT(flow, T):
    r"""
    Calculate dynamic viscosity from pressure and temperature.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    T : float
        Temperature T / K.

    Returns
    -------
    visc : float
        Dynamic viscosity visc / Pa s.

    Note
    ----
    Calculation for fluid mixtures.

    .. math::

        \eta_{mix}(p,T)=\frac{\sum_{i} \left( \eta(p,T,fluid_{i}) \cdot y_{i}
        \cdot \sqrt{M_{i}} \right)}
        {\sum_{i} \left(y_{i} \cdot \sqrt{M_{i}} \right)}\;
        \forall i \in \text{fluid components}\\
        y: \text{volume fraction}\\
        M: \text{molar mass}

    Reference: :cite:`Herning1936`.
    """
    n = molar_mass_flow(flow[3])

    a = 0
    b = 0
    for fluid, x in flow[3].items():
        if x > err:
            bi = x * np.sqrt(molar_masses[fluid]) / (molar_masses[fluid] * n)
            b += bi
            a += bi * visc_pT(flow[1], T, fluid)

    return a / b


def visc_pT(p, T, fluid):
    r"""
    Calculate dynamic viscosity from pressure and temperature for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    T : float
        Temperature T / K.

    fluid : str
        Fluid name.

    Returns
    -------
    visc : float
        Viscosity visc / Pa s.
    """
    if fluid in TESPyFluid.fluids.keys():
        return TESPyFluid.fluids[fluid].funcs['visc_pT'].ev(p, T)
    else:
        Memorise.state[fluid].update(CP.PT_INPUTS, p, T)
        return Memorise.state[fluid].viscosity()

# %%


def s_mix_ph(flow, T0=300):
    r"""
    Calculate the entropy from pressure and enthalpy.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    s : float
        Specific entropy s / (J/(kgK)).

    Note
    ----
    First, check if fluid property has been memorised already.
    If this is the case, return stored value, otherwise calculate value and
    store it in the memorisation class.

    Uses CoolProp interface for pure fluids, newton algorithm for mixtures:

    .. math::

        s_{mix}\left(p,h\right) = s\left(p,T_{mix}(p,h)\right)
    """
    # check if fluid properties have been calculated before
    fl = tuple(flow[3].keys())
    memorisation = fl in Memorise.s_ph.keys()
    if memorisation:
        a = Memorise.s_ph[fl][:, :-2]
        b = np.asarray([flow[1], flow[2]] + list(flow[3].values()))
        ix = np.where(np.all(abs(a - b) <= err, axis=1))[0]
        if ix.size == 1:
            # known fluid properties
            Memorise.s_ph[fl][ix, -1] += 1
            return Memorise.s_ph[fl][ix, -2][0]

    # unknown fluid properties
    fluid = single_fluid(flow[3])
    if fluid is None:
        # calculate the fluid properties for fluid mixtures
        val = s_mix_pT(flow, T_mix_ph(flow, T0=T0))
    else:
        # calculate fluid property for pure fluids
        val = s_ph(flow[1], flow[2], fluid)

    if memorisation:
        # memorise the newly calculated value
        new = np.asarray(
            [[flow[1], flow[2]] + list(flow[3].values()) + [val, 0]])
        Memorise.s_ph[fl] = np.append(Memorise.s_ph[fl], new, axis=0)

    return val


def s_ph(p, h, fluid):
    r"""
    Calculate the entropy from pressure and enthalpy for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    h : float
        Specific enthalpy h / (J/kg).

    fluid : str
        Fluid name.

    Returns
    -------
    s : float
        Specific entropy s / (J/(kgK)).
    """
    if fluid in TESPyFluid.fluids.keys():
        db = TESPyFluid.fluids[fluid].funcs['h_pT']
        T = newton(reverse_2d, reverse_2d_deriv, [db, p, h], 0)
        return TESPyFluid.fluids[fluid].funcs['s_pT'].ev(p, T)
    elif Memorise.back_end[fluid] == 'IF97':
        return entropy_iteration_IF97(p, h, fluid, 's')
    else:
        Memorise.state[fluid].update(CP.HmassP_INPUTS, h, p)
        return Memorise.state[fluid].smass()

# %%


def s_mix_pT(flow, T, force_gas=False):
    r"""
    Calculate the entropy from pressure and temperature.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    T : float
        Temperature T / K.

    Returns
    -------
    s : float
        Specific entropy s / (J/(kgK)).

    Note
    ----
    Calculation for fluid mixtures.

    .. math::

        s_{mix}(p,T)=\sum_{i} x_{i} \cdot s(pp_{i},T,fluid_{i})-
        \sum_{i} x_{i} \cdot R_{i} \cdot \ln \frac{pp_{i}}{p}\;
        \forall i \in \text{fluid components}\\
        pp: \text{partial pressure}\\
        R: \text{gas constant}
    """
    n = molar_mass_flow(flow[3])

    fluid_comps = {}

    tespy_fluids = [
        s for s in flow[3].keys() if s in TESPyFluid.fluids.keys()]
    for f in tespy_fluids:
        for it, x in TESPyFluid.fluids[f].fluid.items():
            if it in fluid_comps.keys():
                fluid_comps[it] += x * flow[3][f]
            else:
                fluid_comps[it] = x * flow[3][f]

    fluids = [s for s in flow[3].keys() if s not in TESPyFluid.fluids.keys()]
    for f in fluids:
        if f in fluid_comps.keys():
            fluid_comps[f] += flow[3][f]
        else:
            fluid_comps[f] = flow[3][f]

    # print(fluid_comps)

    s = 0
    for fluid, x in fluid_comps.items():
        if x > err:
            pp = flow[1] * x / (molar_masses[fluid] * n)
            s += s_pT(pp, T, fluid, force_gas) * x
            s -= (x * gas_constants[fluid] / molar_masses[fluid] *
                  np.log(pp / flow[1]))

    return s


def s_pT(p, T, fluid, force_gas):
    r"""
    Calculate the entropy from pressure and temperature for a pure fluid.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    T : float
        Temperature T / K.

    fluid : str
        Fluid name.

    Returns
    -------
    s : float
        Specific entropy s / (J/(kgK)).
    """
    if fluid in TESPyFluid.fluids.keys():
        return TESPyFluid.fluids[fluid].funcs['s_pT'].ev(p, T)
    else:
        if force_gas:
            if T < Memorise.state[fluid].trivial_keyed_output(CP.iT_critical):
                Memorise.state[fluid].update(CP.PT_INPUTS, p, T)
                s = Memorise.state[fluid].smass()
                Memorise.state[fluid].update(CP.QT_INPUTS, 1, T)
                s_sat = Memorise.state[fluid].smass()
                return max(s, s_sat)

        Memorise.state[fluid].update(CP.PT_INPUTS, p, T)
        return Memorise.state[fluid].smass()


def ds_mix_pdT(flow, T):
    r"""
    Calculate partial derivate of entropy to temperature.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    T : float
        Temperature T / K.

    Returns
    -------
    ds / dT : float
        Partial derivative of specific entropy to temperature
        ds / dT / (J/(kg :math:`\mathrm{K}^2`)).

        .. math::

            \frac{\partial s_{mix}}{\partial T} =
            \frac{s_{mix}(p,T+d)-s_{mix}(p,T-d)}{2 \cdot d}
    """
    d = 0.1
    return (s_mix_pT(flow, T + d) - s_mix_pT(flow, T - d)) / (2 * d)


def isentropic(inflow, outflow, T0=300):
    r"""
    Calculate the enthalpy at the outlet after isentropic process.

    Parameters
    ----------
    inflow : list
        Inflow fluid property vector containing mass flow, pressure, enthalpy
        and fluid composition.

    outflow : list
        Outflow fluid property vector containing mass flow, pressure, enthalpy
        and fluid composition.

    Returns
    -------
    h_s : float
        Enthalpy after isentropic state change.

        .. math::

            h_\mathrm{s} = \begin{cases}
            h\left(p_{out}, s\left(p_{in}, h_{in}\right) \right) &
            \text{pure fluids}\\
            h\left(p_{out}, s\left(p_{in}, T_{in}\right) \right) &
            \text{mixtures}\\
            \end{cases}
    """
    fluid = single_fluid(inflow[3])
    if fluid is not None:
        return h_ps(outflow[1], s_ph(inflow[1], inflow[2], fluid), fluid)
    else:
        s_mix = s_mix_ph(inflow)
        return h_mix_ps(outflow, s_mix, T0=T0)


def calc_physical_exergy(conn, p0, T0):
    r"""
    Calculate specific physical exergy.

    Physical exergy is allocated to a thermal and a mechanical share according
    to :cite:`Morosuk2005`.

    Parameters
    ----------
    conn : tespy.connections.connection.Connection
        Connection to calculate specific physical exergy for.

    p0 : float
        Ambient pressure p0 / Pa.

    T0 : float
        Ambient temperature T0 / K.

    Returns
    -------
    e_ph : tuple
        Specific thermal and mechanical exergy
        (:math:`e^\mathrm{T}`, :math:`e^\mathrm{M}`) in J / kg.

        .. math::

            e^\mathrm{T} = \left( h - h \left( p, T_0 \right) \right) -
            T_0 \cdot \left(s - s\left(p, T_0\right)\right)

            e^\mathrm{M}=\left(h\left(p,T_0\right)-h\left(p_0,T_0\right)\right)
            -T_0\cdot\left(s\left(p, T_0\right)-s\left(p_0,T_0\right)\right)

            e^\mathrm{PH} = e^\mathrm{T} + e^\mathrm{M}
    """
    h_T0_p = h_mix_pT([0, conn.p.val_SI, 0, conn.fluid.val], T0)
    s_T0_p = s_mix_pT([0, conn.p.val_SI, 0, conn.fluid.val], T0)
    ex_therm = (conn.h.val_SI - h_T0_p) - T0 * (conn.s.val_SI - s_T0_p)
    h0 = h_mix_pT([0, p0, 0, conn.fluid.val], T0)
    s0 = s_mix_pT([0, p0, 0, conn.fluid.val], T0)
    ex_mech = (h_T0_p - h0) - T0 * (s_T0_p - s0)
    return ex_therm, ex_mech


def entropy_iteration_IF97(p, h, fluid, output):
    r"""
    Generate the state of IF97::water via entropy iteration.

    Parameters
    ----------
    p : float
        Pressure p / Pa.

    h : float
        Specific enthalpy h / (J/kg).

    fluid : str
        Fluid name.

    Returns
    -------
    T : float
        Temperature T / K.
    """
    # region 1 exclusive issue!
    Memorise.state[fluid].update(CP.HmassP_INPUTS, h, p)
    if p <= 16.529164252605 * 1e6:
        h_at_ph = Memorise.state[fluid].hmass()
        deviation = abs(h_at_ph - h)
        if deviation / h > 0.001:
            # region 1, where isenthalpic lines are tangent to saturation dome
            if p > 1e6 and p < 1e7 and h > 2700000 and h < 2850000:
                smin = 5750
                smax = 6500
            # bottom left corner in Ts diagram
            elif h < 10000:
                smin = 0
                smax = 50
            else:
                # proximity to saturated liquid
                Memorise.state[fluid].update(CP.PQ_INPUTS, p, 0)
                h_sat_l = Memorise.state[fluid].hmass()
                if abs(h - h_sat_l) / h_sat_l < 1e-1:
                    if p < 1000:
                        smin = 0
                    elif p < 60000:
                        smin = Memorise.state[fluid].smass() * 0.9
                    else:
                        smin = Memorise.state[fluid].smass() * 0.95

                    Memorise.state[fluid].update(CP.PQ_INPUTS, p, 0.3)
                    smax = Memorise.state[fluid].smass()
                # all others
                else:
                    Memorise.state[fluid].update(CP.HmassP_INPUTS, h, p)
                    s0 = Memorise.state[fluid].smass()
                    smin = 0.8 * s0
                    smax = 1.2 * s0

            s0 = (smax + smin) / 2
            s = newton(func=h_ps_IF97, deriv=dh_pds_IF97, params=[fluid, p],
                       y=h, val0=s0, valmin=smin, valmax=smax, max_iter=5,
                       tol_rel=1e-3, tol_mode='rel')
            Memorise.state[fluid].update(CP.PSmass_INPUTS, p, s)

    if output == 'T':
        return Memorise.state[fluid].T()
    elif output == 's':
        return Memorise.state[fluid].smass()
    elif output == 'rho':
        return Memorise.state[fluid].rhomass()
    else:
        return Memorise.state[fluid].viscosity()
