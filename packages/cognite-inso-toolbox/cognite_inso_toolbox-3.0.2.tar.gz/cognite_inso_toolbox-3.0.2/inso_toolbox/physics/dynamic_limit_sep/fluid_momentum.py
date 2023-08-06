import logging

import numpy as np

logger = logging.getLogger(__name__)


# Base physics calculations needed for rhov2


def mass_rate_liq(rate, density):
    """
    Method to calculates the mass of a liquid given rate and density
    Args:
        rate (float): rate (m3/s)
        density (float): density (kg/m3)
    Returns:
        float: mass rate (kg/s)
    """
    mass_rate = rate * density
    return mass_rate


def mass_rate_gas(rate, M=22.4, z_std=0.9956, p_std=101.325, t_std=288):
    """
    Method to calculates the mass of a gas given rate (mmscfd), based on ideal gas law
    Args:
        rate (float): gas rate (m3/s)
        M (float, optional): Molar mass (kg/mol)
        z_std (float, optional): z-factor at standard conditions (unitless)
        p_std (float, optional): pressure at standard conditions (kPa)
        t_std (float, optional): temperature at standard conditions (Kelvin)
    Returns:
        float: mass rate in kg/s
    """
    R = 8.314  # universal gas constant, J / mol·K
    mass_rate = rate * p_std * M / (z_std * t_std * R)
    return mass_rate  # kg/s


def velocity(rate: float, nozz_id: float):
    """
    Method to calculate velocity given a rate
    Args:
        rate (float): fluid rate (m3/s)
        nozz_id (float): nozzle inner diameter (mm)
    Returns:
        float: velocity in m/s
    """
    nozz_area = np.pi / 4 * (nozz_id / 1000) ** 2  # m2
    return rate / nozz_area  # m/s


def fluid_momentum(density: float, velocity: float):
    """
    Standard equation for calculating fluid momentum
    Ref: https://petrowiki.spe.org/Separator_sizing#Nozzle_sizing
    Args:
        density (float): density of the fluid (kg/m3)
        velocity (float): velocity of the fluid (m/s)
    Returns:
        float: fluid momentum in Newton (N)
    """
    return density * velocity ** 2
