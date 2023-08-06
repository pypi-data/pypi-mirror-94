from typing import List, Optional, Union

import pandas as pd

from inso_toolbox.utils import pipeline_function

from .units import _UNITS
from .utils.units_docstring import list_units_docstring


@pipeline_function
@list_units_docstring
def convert(
    data: Union[float, int, pd.DataFrame],
    from_unit: str,
    to_unit: Optional[str] = None,
    columns: Optional[List] = None,
    inplace: bool = False,
) -> Union[float, int, pd.DataFrame]:
    """
    Convert specified columns in data from given unit to another unit.
    
    Args:
        data (float, int, pd.DataFrame): Data to be converted.
        columns (List[str], optional): List of columns to convert.
        from_unit (str): Current unit of the specified columns.
        to_unit (str, optional): Specifies which unit the columns should be converted to.
            Default is to convert to SI units.
        inplace (bool, optional): Specifies whether to convert the data inplace or not.
    
    Returns:
        pd.DataFrame: Data with converted columns.
    """  # noqa
    f = _UNITS.get_converter(from_unit=from_unit, to_unit=to_unit)

    if isinstance(data, pd.DataFrame):
        if not inplace:
            data = data.copy(deep=True)

        data[columns] = f(data[columns])
    else:
        data = f(data)

    return data
