from __future__ import absolute_import

import ConfigParser
import os, errno
import logging
import traceback


def setup_logger():

    logger = logging.getLogger("py4j")
    logger.setLevel(logging.INFO)
    # avoid adding multiple handlers which would cause one message to be printed multiple times
    logger.handlers[0] = logging.StreamHandler()

    logging.root = logger
    logging.Logger.manager.root = logger

    return logger


def process_product(product, args):

    import icor.landsat8
    import icor.sentinel2
    import getpass

    logger = setup_logger()

    conf = ConfigParser.SafeConfigParser()
    try:
        icor_dir = str(os.environ['ICOR_DIR'])
        logger.info('Using iCOR dir %s', icor_dir)
    except Exception:
        icor_dir = '/data/icor/v1.0.0'
        os.environ['ICOR_DIR'] = icor_dir
        logger.info('Using default iCOR dir %s', icor_dir)

    conf.set("DEFAULT", "install_dir", icor_dir)

    if args.data_type == "L8":
        conf.read(icor_dir + "/src/config/local_landsat8_simec.ini")
    elif args.data_type == "S2":
        conf.read(icor_dir + "/src/config/local_sentinel2_simec.ini")

    output_dir = "/data/users/Private/" + getpass.getuser() + "/icor_results/"
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    params = {}

    params["keep_intermediate"] = "false"

    # convert to params for context
    context = icor.context.SimpleContext(params, logger=logger)
    # status
    params["cirrus"] = args.cirrus
    params["aot"] = args.aot
    params["simec"] = args.simec
    params["watervapor"] = args.watervapor
    params["bg_window"] = args.bg_window
    params["cirrus_threshold"] = args.cirrus_threshold
    params["aot_override"] = args.aot_override
    params["ozone_override"] = args.ozone_override
    params["watervapor_override"] = args.wv_override

    params["output_file"] = output_dir

    params["low_band"] = args.cloud_low_band
    params["average_threshold"] = args.cloud_average_threshold
    params["low_threshold"] = args.cloud_low_threshold

    params["aot_window_size"] = args.aot_window_size

    params["water_band"] = args.water_band
    params["water_threshold"] = args.water_threshold

    for param, value in conf.items("DEFAULT"):
        params[param] = value

    for section in conf.sections():
        for param, value in conf.items(section):
            params[section + "_" + param] = value

    try:
        working_folder = os.getcwd()
        if context["instrument"] == "landsat8":
            if context["workflow"] == "simec":
                icor.landsat8.process_tgz(context, product, working_folder)
            else:
                raise ValueError("Unknown 'instrument'")
        elif context["instrument"] == "sentinel2":
            if context["workflow"] == "simec":
                icor.sentinel2.process_tar(context, product, working_folder)
            else:
                raise ValueError("Unknown 'instrument'")
        else:
            raise ValueError("Unknown 'workflow'")

    except:
        logger.error(traceback.format_exc())
