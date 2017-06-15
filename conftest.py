from pathlib import Path

import pytest
import appdirs

CACHE_DIR = Path(appdirs.user_cache_dir(appname='ukgeo', appauthor='eeci'))


def pytest_addoption(parser):
    parser.addoption(
        "--nocache",
        action="store_true",
        help="run tests with clear cache"
    )


@pytest.fixture
def cache(request):
    if request.config.getoption("--nocache"):
        for path in CACHE_DIR.rglob('*'):
            path.unlink()
