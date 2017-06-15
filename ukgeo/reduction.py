import io
from pathlib import Path
import tempfile
import zipfile

import appdirs
import geopandas as gpd
import requests
import requests_cache
from shapely.prepared import prep

LONDON_BOUNDARY_FILE_URL = ('https://files.datapress.com/london/dataset/statistical-gis-boundary-'
                            'files-london/2016-10-03T13:52:28/statistical-gis-boundaries-'
                            'london.zip')
BOROUGH_SHAPE_FILE_PATH = Path(
    './statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp'
)
CACHE = Path(appdirs.user_cache_dir(appname='ukgeo', appauthor='eeci')) / 'web-cache'
CACHE.parent.mkdir(parents=True, exist_ok=True)


def reduce_to_borough(borough_name, data):
    """Filters all elements of the data set that lie in the specified borough."""
    haringey = _read_borough_geometry(borough_name)
    haringey_prep = prep(haringey) # improves performace for the next step
    in_haringey_mask = data.geometry.map(haringey_prep.contains)
    return data[in_haringey_mask]


def _read_borough_geometry(borough_name):
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
