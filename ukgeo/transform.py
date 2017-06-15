from shapely.prepared import prep

from .read import read_borough_geometry


def reduce_to_borough(borough_name, data):
    """Filters all elements of the data set that lie in the specified borough."""
    borough_geometry = read_borough_geometry(borough_name)
    prep_borough_geometry = prep(borough_geometry) # improves performace for the next step
    in_borough_mask = data.geometry.map(prep_borough_geometry.contains)
    return data[in_borough_mask]
