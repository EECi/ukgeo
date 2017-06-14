import os
from pathlib import Path

import pytest

from ukgeo.read import production_block_chunked_files
import ukgeo

TEST_DIR = Path(os.path.abspath(__file__)).parent
PATH_TO_RESOURCES = TEST_DIR / 'resources'
PATH_TO_PRODUCTION_BLOCK_FILES = PATH_TO_RESOURCES / 'productionblockfiles'
PATH_TO_PRODUCTION_BLOCK_HB0101 = PATH_TO_PRODUCTION_BLOCK_FILES / 'HB0101-something.shp'
PATH_TO_PRODUCTION_BLOCK_HB0102 = PATH_TO_PRODUCTION_BLOCK_FILES / 'somethingHB0102more.shp'


@pytest.mark.parametrize("minx,miny,maxx,maxy,expected_result", [
    (500000, 100000, 500001, 100001, ['HB0101']),
    (500000, 100000, 500000.1, 100000.1, ['HB0101']),
    (505000, 100000, 505001, 100001, ['HB0201']),
    (500000, 105000, 500001, 105001, ['HB0102']),
    (500000, 100000, 505000, 100001, ['HB0101', 'HB0201']),
    (500000, 100000, 500001, 105000, ['HB0101', 'HB0102']),
    (504999, 100000, 505001, 100001, ['HB0101', 'HB0201']),
    (504999.9, 100000, 505001, 100001, ['HB0101', 'HB0201'])
])
def test_production_blocks(minx, miny, maxx, maxy, expected_result):
    assert set(ukgeo.production_blocks(minx, miny, maxx, maxy)) == set(expected_result)


@pytest.mark.parametrize("minx,miny,maxx,maxy", [
    (499999, 100000, 500001, 100001),
    (500000, 100000, 600001, 100001),
    (500000, 99999, 500001, 100001),
    (500000, 100000, 500001, 200001),
])
def test_fails_when_outside_hb_production_block_reference(minx, miny, maxx, maxy):
    with pytest.raises(ValueError):
        set(ukgeo.production_blocks(minx, miny, maxx, maxy))


def test_production_block_file_generator():
    files = production_block_chunked_files(
        root_folder=PATH_TO_PRODUCTION_BLOCK_FILES,
        production_blocks=['HB0101', 'HB0102']
    )
    assert set(files) == set([PATH_TO_PRODUCTION_BLOCK_HB0101, PATH_TO_PRODUCTION_BLOCK_HB0102])


def test_read_ukmap_files():
    data = ukgeo.read_ukmap(PATH_TO_PRODUCTION_BLOCK_FILES, ['HB0101', 'HB0102'])
    assert len(data.index) == 16 * 2
