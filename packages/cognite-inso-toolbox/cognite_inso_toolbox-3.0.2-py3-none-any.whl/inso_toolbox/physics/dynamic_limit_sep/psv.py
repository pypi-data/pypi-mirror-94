import logging

import pandas as pd
from scipy.interpolate import LinearNDInterpolator

logger = logging.getLogger(__name__)


def _check_psv_data(inputs, output, grid):
    # Check to see if output dictionary has too many entries
    if len(output) != 1:
        raise ValueError("outputs dictionary contains too many entries. Should only be 1.")

    # Check if keys for inputs and outputs match grid columns
    keys = set(inputs.keys()).union(set(output.keys()))
    keys_do_not_match = keys - set(grid.columns)
    if keys_do_not_match:
        raise KeyError("input keys do not match grid column names")

    # Check if input values are outside the bounds of the grid
    for key, val in inputs.items():
        max_val = max(grid[key])
        min_val = min(grid[key])
        if max_val < val < min_val:
            raise ValueError(f"Input value for {key}:{val} is out of bounds min: {min_val}, max: {max_val}")


def psv_utilization(inputs, output, grid: pd.DataFrame, obey_threshold=False, max_psv_util=200.0):
    """
    Generic method for calculating pressure safety valve (PSV) utilization
    input and output keys must match the column names in the grid

    Args:
        inputs (dict): Independent variables, must match column names of grid
        output (dict): Dependent variable, must match the column name of grid
        grid (pd.DataFrame): PSV grid
        obey_threshold (bool, optional): Specifies whether a threshold is placed on the calculation. Default is False.
        max_psv_util (float, optional): Threshold value. Default if 200%.

    Returns:
        float: PSV utilization (percentage 0-100)
    """
    _check_psv_data(inputs, output, grid)

    # Generate the interpolator
    try:
        x = grid[inputs.keys()]
        y = grid[output.keys()]
        f = LinearNDInterpolator(x, y)
    except Exception as e:  # Raise errors due to LinearNDInterpolator
        logger.error("Unable to generate PSV grid interpolation function.")
        raise e

    # Calculate the actual utilization
    actual_util = f(list(inputs.values()))
    max_util = list(output.values())[0]
    psv_util = actual_util / max_util * 100
    logger.debug(f"actual util = {actual_util}, max util = {max_util}, PSV utilization = {psv_util}")

    # If PSV value is higher than specified threshold, give error message and return threshold instead of value.
    if obey_threshold:
        if psv_util > max_psv_util:
            logger.warning(f"PSV utlization is very high ({psv_util})! Returning {max_psv_util}%")
            return max_psv_util
        else:
            return psv_util
    else:
        return psv_util
