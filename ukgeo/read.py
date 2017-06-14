import geopandas as gpd

HB_MIN_X = 500000
HB_MAX_X = 600000
HB_MIN_Y = 100000
HB_MAX_Y = 200000
NOT_HB_ERROR_MESSAGE = ("Supports only HB production block reference. " +
                        "Please refer to dataset manual.")

BLOCK_SIDE_LENGTH = 5000


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
