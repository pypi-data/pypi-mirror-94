def k_factor(gas_velocity: float, liquid_density: float, vapor_density: float):
    """
    Calculating the actual k-factor, aka system load factor or vapor load factor
    Ref: https://en.wikipedia.org/wiki/Souders%E2%80%93Brown_equation
    Ref: GPSA Engineering Data Book [Gas Processing] 12th ed p.7-12

    Args:
        gas_velocity (float): gas velocity, m/s
        liquid_density (float): liquid density, kg/m3
        vapor_density (float): vapor / gas density, kg/m3
    Returns:
        float: k-factor, m/s
    """
    k_factor = gas_velocity * (vapor_density / (liquid_density - vapor_density)) ** (0.5)
    return k_factor
