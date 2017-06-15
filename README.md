# ukgeo

Utilities to work with the UKMap and UKBuilding datasets.

## User Guide

Convenience functions to read UKMap and UKBuildings data.

### UKMap

```Python
import ukgeo

# I know the production blocks myself.
ukmap = ukgeo.read_ukmap(
    root_folder=path_to_root_folder,
    production_blocks=['HB0101', 'HB0102']
)

# I know the bounding box in the OS national grid reference system.
ukmap = ukgeo.read_ukmap(
    root_folder=path_to_root_folder,
    production_blocks=ukgeo.production_blocks(minx=500000, maxx=504999, miny=100000, maxy=106000)
)
```

### UKBuildings

Recent versions of UKBuildings are not chunked into production blocks but
distributed as single files. Chunked reads of older UKBuildings verions
are currently not supported.

```Python
import ukgeo

ukbuildings = ukgeo.read_ukbuildings(path_to_file)
ukb_haringey = ukgeo.reduce_to_borough(borough_name='Haringey', data=ukbuildings)
```

### Notes

`ukgeo` is using data from the London data store. You will need an internet connection the first
time you are trying to use that data. For every consecutive use, the data is cached. Should there
be a problem with the cached data, delete it and run `ukgeo` again.
See the [appdirs](https://github.com/ActiveState/appdirs) documentation to understand where the
cache is stored.

## Developer Guide

### Installation

Best install `ukgeo` in editable mode:

    $ pip install -e .

### Run the test suite

Run the test suite with py.test:

    $ py.test

`ukgeo` is using a web cache in which data from the London data store is cached. To
run tests without the cache use the `--nocache` option:

    $ py.test --nocache
