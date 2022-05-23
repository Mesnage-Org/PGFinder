"""Functions for validation of data."""
from typing import Union
import io
import pkgutil
import numpy as np
import pandas as pd


def allowed_modifications(config_file: Union[str, Path] = "config/allowed_modifications.csv") -> List:
    """
    Loads allowable modifications from a csv file as a list.

    `.csv` is chosen for consistency of data storage over the project.

    Parameters
    ----------
    config_file: Union[str, Path]
        Path to a configuration file. Default 'config/allowed_modifications.csv'

    Returns
    -------
    list
        List of permissible modifications.
    """
    data = pkgutil.get_data(__name__, "config/allowed_modifications.csv")
    allowed_modifications_df = pd.read_csv(io.BytesIO(data), header=None)
    return allowed_modifications_df[0].tolist()


def validate_raw_data_df(raw_data_df: pd.DataFrame) -> Union[None, ValueError]:
    """Validate that the raw data is a Pandas Dataframe with specific column names and that it has attributes.

    Parameters
    ----------
    raw_data_df : pd.DataFrame
        Data frame to be validated.

    Returns
    -------
    Union[None, ValueError]
        Error specific to the problem encountered with the data frame if any are encountered.

    Raises
    ------
    ValueError
    """

    if not isinstance(raw_data_df, pd.DataFrame):
        raise ValueError("raw_data_df must be a DataFrame.")

    if not raw_data_df.attrs["file"]:
        raise ValueError("raw_data_df must have a file attribute.")

    colnames = ["ID", "rt", "mwMonoisotopic", "theo_mwMonoisotopic", "inferredStructure", "maxIntensity"]

    if not set(colnames).issubset(set(raw_data_df.columns.to_list())):
        raise ("raw_data_df column names are incorrect")


def validate_theo_masses_df(theo_masses_df: pd.DataFrame) -> Union[None, ValueError]:
    """Validate that the theoretical masses data is a Pandas Dataframe with specific column names and that it has
    attributes.

    Parameters
    ----------
    raw_data_df : pd.DataFrame
        Data frame to be validated.

    Returns
    -------
    Union[None, ValueError]
        Error specific to the problem encountered with the data frame if any are encountered.

    Raises
    ------
    ValueError
    """

    if not isinstance(theo_masses_df, pd.DataFrame):
        raise ValueError("theo_masses_df must be a DataFrame.")

    if not theo_masses_df.attrs["file"]:
        raise ValueError("theo_masses_df must have a file attribute.")

    colnames = ["Structure", "Monoisotopicmass"]

    if theo_masses_df.columns.to_list() != colnames:
        raise ValueError("theo_masses_df column names are incorrect")

    coltypes = [np.dtype("O"), np.dtype("float64")]

    if theo_masses_df.dtypes.to_list() != coltypes:
        raise ValueError("theo_masses_df column data types are incorrect")


def validate_rt_window(rt_window: float) -> Union[None, ValueError]:
    """Validate that rt_window is an float.

    Parameters
    ----------
    rt_window : int
        Value of rt_window to be validated.

    Returns
    -------
    Union[None, ValueError]
        If no error nothing is returned, otherwise a ValueError is raised.

    Raises
    ------
    ValueError
    """

    if not isinstance(rt_window, float):
        raise ValueError("rt_window must be a float.")
    # todo: range?


def validate_enabled_mod_list(enabled_mod_list: list) -> Union[None, ValueError]:
    """Validate that enabled_mod_list is a list and modifications are allowed.

    Parameters
    ----------
    enabled_mod_list : int
        Value of enabled_mod_list to be validated.

    Returns
    -------
    Union[None, ValueError]
        If no error nothing is returned, otherwise a ValueError is raised.

    Raises
    ------
    ValueError
    """

    if not isinstance(enabled_mod_list, list):
        raise ValueError("enabled_mod_list must be a list.")

    allowed_mods = allowed_modifications()

    if not all(item in allowed_mods for item in enabled_mod_list):
        raise ValueError("Requested modification(s) not recognised.")


def validate_user_ppm(user_ppm: int) -> Union[None, ValueError]:
    """Validate that user_ppm is an integer.

    Parameters
    ----------
    user_ppm : int
        Value of user_ppm to be validated.

    Returns
    -------
    Union[None, ValueError]
        If no error nothing is returned, otherwise a ValueError is raised.

    Raises
    ------
    ValueError
    """

    if not isinstance(user_ppm, int):
        raise ValueError("user_ppm must be an int.")
    # todo: range?
