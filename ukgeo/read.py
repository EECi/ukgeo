import io
from pathlib import Path
import tempfile
import zipfile

import appdirs
import geopandas as gpd
import requests
import requests_cache

from .datatypes import convert_to_proper_ukbuilding_types

HB_MIN_X = 500000
HB_MAX_X = 600000
HB_MIN_Y = 100000
HB_MAX_Y = 200000
NOT_HB_ERROR_MESSAGE = ("Supports only HB production block reference. " +
                        "Please refer to dataset manual.")
BLOCK_SIDE_LENGTH = 5000
LONDON_BOUNDARY_FILE_URL = ('https://files.datapress.com/london/dataset/statistical-gis-boundary-'
                            'files-london/2016-10-03T13:52:28/statistical-gis-boundaries-'
                            'london.zip')
BOROUGH_SHAPE_FILE_PATH = Path(
    './statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp'
)
CACHE = Path(appdirs.user_cache_dir(appname='ukgeo', appauthor='eeci')) / 'web-cache'
CACHE.parent.mkdir(parents=True, exist_ok=True)


def production_blocks(minx, miny, maxx, maxy):
    """Generator of GeoInformationGroup production blocks.

    Based on a rectangular bounding box defined in OS national grid,
    this generator will yield all GeoInformationGroup production blocks
    that are touched by the box.

    Supports only bounding boxes entirely in the HB production block
    reference.

    Parameters:
        * minx, miny, maxx, maxy: the parameters of the bounding box
                                  defined in OS national grid

    Yields:
        The string name of each bounding box.
    """
    if minx < HB_MIN_X or miny < HB_MIN_Y or maxx > HB_MAX_X or maxy > HB_MAX_Y:
        raise ValueError(NOT_HB_ERROR_MESSAGE)
    start_x = (int(minx) - HB_MIN_X) // BLOCK_SIDE_LENGTH + 1
    end_x = (int(maxx) - HB_MIN_X) // BLOCK_SIDE_LENGTH + 1
    start_y = (int(miny) - HB_MIN_Y) // BLOCK_SIDE_LENGTH + 1
    end_y = (int(maxy) - HB_MIN_Y) // BLOCK_SIDE_LENGTH + 1
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            yield 'HB{:0>2}{:0>2}'.format(x, y)


def borough_production_blocks(borough_name):
    """Generator of GeoInformationGroup production blocks for a certain borough of London."""
    borough_geometry = read_borough_geometry(borough_name)
    return production_blocks(*borough_geometry.bounds)


def production_block_chunked_files(root_folder, production_blocks):
    """Generator of shape file paths of GeoInformationGroup files chunked by production blocks.

    Parameters:
        * root_folder:       the root folder containing all shape files
        * production_blocks: an iterable of production block names

    Yields:
        * file path of each file containing the production block
    """
    for production_block in production_blocks:
        yield list(root_folder.glob('*{}*.shp'.format(production_block)))[0]


def read_ukmap(root_folder, production_blocks):
    """Reads UKMAP data for the provided production blocks.

    Parameters:
        * root_folder:       the root folder containing all shape files
        * production_blocks: an iterable of production block names

    Returns:
        * a GeoPandas GeoDataFrame containing all data
    """
    raw_data = None
    for shape_file_path in production_block_chunked_files(root_folder, production_blocks):
        print('Reading {}'.format(shape_file_path))
        shape_file_data = gpd.read_file(shape_file_path.as_posix())
        if raw_data is None:
            raw_data = shape_file_data
        else:
            raw_data = raw_data.append(shape_file_data)
    return raw_data


def read_ukbuildings(path_to_file, convert_types=True):
    """Reads UKBuildings data from the provided file.

    Parameters:
        * path_to_file:  the path to the shape file containing all data
        * convert_types: (optional, default True) if True converts datatypes to more
                         appropriate ones to save memory space and ease the handling
                         with the data; for example converts flags from int64 to bool8,
                         and converts strings to categoricals.
    """
    path_to_file = Path(path_to_file)
    data = gpd.read_file(path_to_file.as_posix())
    if convert_types:
        data = convert_to_proper_ukbuilding_types(data)
    return data


def read_borough_geometry(borough_name):
    requests_cache.install_cache(CACHE.as_posix())
    r = requests.get(LONDON_BOUNDARY_FILE_URL)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    with tempfile.TemporaryDirectory(prefix='london-boundary-files') as tmpdir:
        z.extractall(path=tmpdir)
        shape_file = Path(tmpdir) / BOROUGH_SHAPE_FILE_PATH
        data = gpd.read_file(shape_file.as_posix())
    data.set_index('NAME', inplace=True)
    try:
        return data.ix[borough_name].geometry
    except KeyError:
        raise ValueError("Unknown borough '{}'.".format(borough_name))
