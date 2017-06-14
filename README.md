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
```

## Developer Guide

### Installation

Best install `ukgeo` in editable mode:

    $ pip install -e .

### Run the test suite

Run the test suite with py.test:

    $ py.test
