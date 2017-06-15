"""Contains data type definition and conversion.

This is to save memory space and ease the handling of the data by:

* converting all numerical data to the appropriate format, e.g. flags are
  converted from int64 to bool8
* converts all strings to categoricals.
"""
import numpy as np
import geopandas as gpd

UKBUILDING_DATA_TYPES = {
    'BASE': np.bool8,
    'BEC': np.int8,
    'BUNG': np.bool8,
    'DOR': np.int16,
    'DPS': np.int16,
    'GET': 'category',
    'MBN': 'category',
    'NAB': 'category',
    'RBCA': 'category',
    'RBCAT': 'category',
    'RBCC': 'category',
    'RBCS': 'category',
    'RBCT': 'category',
    'RBCTT': 'category',
    'RBN': np.int8,
    # TODO RBQ ??
    # TODO KBD ??
    'RDT': 'category',
    'RDTT': 'category',
    'RNR': 'category',
    'RRN': np.int8,
    'RRT': 'category',
    'RRTT': 'category',
    'RWN': np.int8,
    'RWT': 'category',
    'RWTT': 'category',
    'SBC': 'category'
}


def convert_to_proper_ukbuilding_types(data):
    """Converts UKBuilding data types to the ones defined in this file."""
    crs = data.crs
    existing_data_types = {col_name: dtype for col_name, dtype in UKBUILDING_DATA_TYPES.items()
                           if col_name in data.columns}
    data = data.astype(existing_data_types)
    data = gpd.GeoDataFrame(data)
    data.crs = crs
    return data
