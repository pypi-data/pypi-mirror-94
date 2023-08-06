import os.path
import logging
import simplejson
import tempfile

from lightpath.config import beamlines

from hutch_python.happi import get_happi_objs, get_lightpath

logger = logging.getLogger(__name__)


def test_happi_objs():
    logger.debug("test_happi_objs")
    db = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                      'happi_db.json')
    # Only select active objects
    objs = get_happi_objs(db, 'tst')
    assert len(objs) == 2
    assert all([obj.active for obj in objs.values()])
    # Check that we can get upstream devices
    beamlines['RBD'] = {'TST': {}}
    objs = get_happi_objs(db, 'rbd')
    assert len(objs) == 2
    assert all([obj.active for obj in objs.values()])
    # Make sure we can handle an empty JSON file
    with tempfile.NamedTemporaryFile('w+') as tmp:
        simplejson.dump(dict(), tmp)
        tmp.seek(0)
        assert get_happi_objs(tmp.name, 'tst') == {}


def test_get_lightpath():
    logger.debug("test_get_lightpath")
    db = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                      'happi_db.json')
    obj = get_lightpath(db, 'tst')
    # Check that we created a valid BeamPath with no inactive objects
    assert obj.name == 'TST'
    assert len(obj.devices) == 2
