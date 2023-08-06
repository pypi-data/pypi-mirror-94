"""
This module is responsible for reading and interpreting the ``conf.yml`` file.
The file's specification can be found on the `yaml_files` page.
"""
import logging
from copy import copy
from pathlib import Path
from socket import gethostname
from types import SimpleNamespace

from . import mpl_config  # noqa: F401

import yaml
from archapp.interactive import EpicsArchive
from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.callbacks.core import LiveTable
from bluesky.callbacks.mpl_plotting import initialize_qt_teleporter
from elog import HutchELog
from pcdsdaq.daq import Daq
from pcdsdaq.scan_vars import ScanVars
from pcdsdevices.interface import setup_preset_paths

from . import calc_defaults, plan_defaults, sim
from .cache import LoadCache
from .cam_load import read_camviewer_cfg
from .constants import CAMVIEWER_CFG, VALID_KEYS
from .exp_load import get_exp_objs
from .happi import get_happi_objs, get_lightpath
from .lcls import global_devices
from .namespace import class_namespace
from .qs_load import get_qs_objs
from .user_load import get_user_objs
from .utils import get_current_experiment, hutch_banner, safe_load

logger = logging.getLogger(__name__)


def load(cfg=None, args=None):
    """
    Read the config file and convert the yaml format into a ``dict``.

    This method:

    - Finds the hutch's launch directory
    - Modify the conf if specified by args
      - ``exp`` is an override for the experiment key
    - Loads the hutch's objects by calling `load_conf.load_conf`

    Parameters
    ----------
    cfg: ``str``, optional
        Path to the ``conf.yml`` file.
        If this is missing, we'll end up with a very empty environment.

    args: ``Namespace``, optional
        All of the arguments from the cli.

    Returns
    -------
    objs: ``dict{str: object}``
        All objects defined by ``conf.yml``. The strings are the names
        that will be accessible in the global namespace.
    """
    if cfg is None:
        conf = {}
        hutch_dir = None
    else:
        with open(cfg, 'r') as f:
            conf = yaml.safe_load(f)
        conf_path = Path(cfg)
        hutch_dir = conf_path.parent

    if args is not None and args.exp is not None:
        logger.debug('forcing experiment=%s', args.exp)
        conf['experiment'] = args.exp

    return load_conf(conf, hutch_dir=hutch_dir)


def load_conf(conf, hutch_dir=None):
    """
    Step through the object loading procedure, given a configuration.

    The procedure is:

    - Check the configuration for errors
    - Display the banner by calling `hutch_banner`
    - Use ``hutch`` key to create ``hutch.db`` importable namespace to
      stash the objects. This will be literally ``hutch.db`` if hutch is
      not provided, or the hutch name e.g. ``mfx.db``.
    - Create a ``RunEngine``, ``RE``
    - Import ``plan_defaults`` and include as ``p``, ``plans``
    - Create a ``daq`` object with ``RE`` registered.
    - Create a ``scan_pvs`` object, and ``enable`` it.
    - Use ``hutch`` and ``daq_platform`` keys to create the ``elog`` object
      and configure it to match the correct experiment.
    - Use ``db`` key to load devices from the ``happi`` beamline database
      and create a ``hutch_beampath`` object from ``lightpath``
    - Use ``hutch`` key to load detector objects from the ``camviewer``
      configuration file.
    - Use ``experiment`` key to select the current experiment

        - If ``experiment`` was missing, autoselect experiment using
          ``hutch`` key

    - Use current experiment to load experiment objects from questionnaire
    - Use ``load`` key to bring up the user's ``beamline`` modules
    - Use current experiment to load experiment file

    If a conf key is missing, we'll note it in a ``logger.info`` message.
    If an extra conf entry is found, we'll note it in a ``logger.warning``
    message.
    If an automatically selected file is missing, we'll note it in a
    ``logger.info`` message.
    All other errors will be noted in a logger.error message.

    Parameters
    ----------
    conf: ``dict``
        ``dict`` interpretation of the original yaml file

    hutch_dir: ``Path`` or ``str``, optional
        ``Path`` object that points to the hutch's launch directory. This is
        the directory that includes the ``experiments`` directory and a
        hutchname directory e.g. ``mfx``
        If this is missing, we'll be unable to write the ``db.txt`` file,
        do relative filepath database selection for ``happi``,
        or establish a preset positions directory.

    Returns
    ------
    objs: ``dict{str: object}``
        See the return value of `load`
    """
    # Warn user about excess config entries
    for key in conf:
        if key not in VALID_KEYS:
            txt = ('Found %s in configuration, but this is not a valid key. '
                   'The valid keys are %s')
            logger.warning(txt, key, VALID_KEYS)

    # Grab configurations from dict, set defaults, show missing
    try:
        hutch = conf['hutch']
        if isinstance(hutch, str):
            hutch = hutch.lower()
        else:
            logger.error('Invalid hutch conf %s, must be string.', hutch)
            hutch = None
    except KeyError:
        hutch = None
        logger.info(('Missing hutch from conf. Will skip elog '
                     'and cameras.'))

    # Display the banner
    if hutch is None:
        hutch_banner()
    else:
        hutch_banner(hutch)

    try:
        db = conf['db']
        if isinstance(db, str):
            if db[0] == '/':
                db = Path(db)
            else:
                db = Path(hutch_dir) / db
        else:
            logger.error('Invalid db conf %s, must be string.', db)
            db = None
    except KeyError:
        db = None
        logger.info(('Missing db from conf. Will skip loading from shared '
                     'database.'))
    try:
        load = conf['load']
        if not isinstance(load, (str, list)):
            logger.error('Invalid load conf %s, must be string or list', load)
            load = None
    except KeyError:
        load = None
        logger.info('Missing load from conf. Will skip loading hutch files.')

    try:
        experiment = conf['experiment']
        if not isinstance(experiment, str):
            logger.error('Invalid experiment selection %s, must be a string '
                         'matching the elog experiment name.', experiment)
            experiment = None
    except KeyError:
        experiment = None
        if hutch is None:
            logger.info(('Missing hutch and experiment from conf. Will not '
                         'load objects from questionnaire or experiment '
                         'file.'))

    try:
        # This is an internal variable here for note-keeping. The ELog uses
        # this to determine if we are in the secondary or primary DAQ mode
        default_platform = True
        platform_info = conf['daq_platform']
        hostname = gethostname()
        try:
            daq_platform = platform_info[hostname]
            logger.info('Selected %s daq platform: %s',
                        hostname, daq_platform)
            default_platform = False
        except KeyError:
            daq_platform = platform_info['default']
            logger.info('Selected default %s daq platform: %s',
                        hutch, daq_platform)
    except KeyError:
        daq_platform = 0
        logger.info('Selected default hutch-python daq platform: 0')

    # Make cache namespace
    cache = LoadCache((hutch or 'hutch') + '.db', hutch_dir=hutch_dir)

    # Make RunEngine
    with safe_load('run engine'):
        RE = RunEngine({})
        initialize_qt_teleporter()
        bec = BestEffortCallback()
        RE.subscribe(bec)
        # Enable scientific notation for big/small numbers in LiveTable
        LiveTable._FMT_MAP['number'] = 'g'
        cache(RE=RE, bec=bec)

    # Collect Plans
    with safe_load('bluesky plans'):
        cache(bp=plan_defaults.plans)
        cache(bps=plan_defaults.plan_stubs)
        cache(bpp=plan_defaults.preprocessors)

    # Inline calculations
    with safe_load('calc utils'):
        cache(calc=calc_defaults.calc_namespace)

    # Daq
    with safe_load('daq'):
        cache(daq=Daq(RE=RE, hutch_name=hutch))

    # Scan PVs
    if hutch is not None:
        with safe_load('scan_pvs'):
            scan_pvs = ScanVars('{}:SCAN'.format(hutch.upper()),
                                name='scan_pvs', RE=RE)
            scan_pvs.enable()
            cache(scan_pvs=scan_pvs)

    # Elog
    if hutch is not None:
        with safe_load('elog'):
            # Use the fact if we we used the default_platform or not to decide
            # whether we are in a specialty station or not
            if default_platform:
                logger.debug("Using primary experiment ELog")
                kwargs = dict()
            else:
                logger.info("Configuring ELog to post to secondary experiment")
                kwargs = {'station': '1'}
            cache(elog=HutchELog.from_conf(hutch.upper(), **kwargs))

    # Shared global devices for LCLS
    with safe_load('lcls PVs'):
        cache(**global_devices())

    # Happi db and Lightpath
    if db is not None:
        with safe_load('database'):
            happi_objs = get_happi_objs(db, hutch)
            cache(**happi_objs)
            bp = get_lightpath(db, hutch)
            if bp.devices:
                cache(**{"{}_beampath".format(hutch.lower()): bp})

    # ArchApp
    with safe_load('archapp'):
        cache(archive=EpicsArchive())

    # Camviewer
    if hutch is not None:
        with safe_load('camviewer config'):
            objs = read_camviewer_cfg(CAMVIEWER_CFG.format(hutch))
            cache(camviewer=SimpleNamespace(**objs))

    # Simulated hardware
    with safe_load('simulated hardware'):
        cache(sim=sim.get_hw())

    # Auto select experiment if we need to
    if experiment is None:
        if hutch is not None:
            try:
                # xpplp1216
                experiment = get_current_experiment(hutch)
                logger.info('Selected active experiment %s', experiment)
            except Exception:
                err = 'Failed to select experiment automatically'
                logger.error(err)
                logger.debug(err, exc_info=True)

    # Process experiment name a bit
    if experiment is not None:
        if hutch in experiment:
            full_expname = experiment
            raw_expname = experiment.replace(hutch, '', 1)
        else:
            full_expname = hutch + experiment
            raw_expname = experiment

    # Load questionnaire
    if experiment is not None:
        qs_objs = get_qs_objs(full_expname)
        cache(**qs_objs)

    # Load user/beamline files
    if load is not None:
        load_objs = get_user_objs(load)
        cache(**load_objs)

    # Load experiment file
    if experiment is not None:
        user = get_exp_objs(raw_expname)
        for name, obj in qs_objs.items():
            setattr(user, name, obj)
        cache(x=user, user=user)

    # Default namespaces
    with safe_load('default groups'):
        default_class_namespace('ophyd.PositionerBase', 'motors', cache)
        default_class_namespace('Slits', 'slits', cache)
        default_class_namespace('pcdsdaq.ami.AmiDet', 'detectors', cache)

        # Hotfix/disabled until we fix issues here
        # Tree namespace can cause havoc and break top-level devices
        #
        # if hutch is not None:
        #     tree = tree_namespace(scope='hutch_python.db')
        #     # Prune meta, remove branches with only one object
        #     for name, space in tree.__dict__.items():
        #         if count_ns_leaves(space) > 1:
        #             cache(**{name: space})

        all_objs = copy(cache.objs)
        cache(a=all_objs, all_objects=all_objs)

    # Install Presets
    if hutch_dir is not None:
        with safe_load('position presets'):
            presets_dir = Path(hutch_dir) / 'presets'
            beamline_presets = presets_dir / 'beamline'
            preset_paths = [presets_dir, beamline_presets]
            if experiment is not None:
                experiment_presets = presets_dir / raw_expname
                preset_paths.append(experiment_presets)
            for path in preset_paths:
                if not path.exists():
                    path.mkdir()
                    path.chmod(0o777)
            if experiment is None:
                setup_preset_paths(hutch=beamline_presets)
            else:
                setup_preset_paths(hutch=beamline_presets,
                                   exp=experiment_presets)

    # Write db.txt info file to the user's module
    try:
        cache.write_file()
    except OSError:
        logger.warning('No permissions to write db.txt file')

    return cache.objs.__dict__


def default_class_namespace(cls, name, cache):
    """
    Create a class namespace and add it to the cache.

    This is an internal utility function for `load_conf.load_conf` that creates
    an `IterableNamespace`, names it, gives it a shortened name, and then
    registers both names to the `LoadCache` if the namespace isn't empty.

    Parameters
    ----------
    cls: ``type`` or ``str``
        The class to use for the namespace

    name: ``str``
        The name of the namespace

    cache: `LoadCache`
    """
    objs = class_namespace(cls, scope='hutch_python.db')
    if len(objs) > 0:
        cache(**{name: objs, name[0]: objs})
