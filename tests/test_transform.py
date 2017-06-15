import os
from pathlib import Path

import pytest

import ukgeo

TEST_DIR = Path(os.path.abspath(__file__)).parent
PATH_TO_RESOURCES = TEST_DIR / 'resources'
PATH_TO_UKBUILDINGS = PATH_TO_RESOURCES / 'ukbuildings.shp'


def test_cut_out_haringey_from_ukbuildings(cache):
    data = ukgeo.read_ukbuildings(PATH_TO_UKBUILDINGS.as_posix())
    haringey = ukgeo.reduce_to_borough(borough_name='Haringey', data=data)
    assert len(haringey.index) < 45 * 45
    assert len(haringey.index) > 0
