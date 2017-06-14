import pytest

from ukgeo.read import production_blocks


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
    assert set(production_blocks(minx, miny, maxx, maxy)) == set(expected_result)


@pytest.mark.parametrize("minx,miny,maxx,maxy", [
    (499999, 100000, 500001, 100001),
    (500000, 100000, 600001, 100001),
    (500000, 99999, 500001, 100001),
    (500000, 100000, 500001, 200001),
])
def test_fails_when_outside_hb_production_block_reference(minx, miny, maxx, maxy):
    with pytest.raises(ValueError):
        set(production_blocks(minx, miny, maxx, maxy))
