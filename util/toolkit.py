import os
import sys
import signal
import platform
import getpass
import time
import socket
import random
import logging
import logging.config
from ConfigParser import RawConfigParser

from jira import JIRA

from util.fun_stuff import SpinCursor
from util.color_formatter import ColorFormatter


def die(msg="Error"):
    log.warn(msg)
    sys.exit()


def raise_NotImplementedException():
    raise NotImplementedError, "Oops! This part of the functionality has not been implemented ... Bye bye!"


def kill_process(pid):
    log.warn("kill -9 " + pid)
    os.kill(int(pid), signal.SIGKILL)


def terminate_process(pid):
    log.warn("kill " + pid)
    os.kill(int(pid), signal.SIGTERM)


def print_os_information():
    log.info("Script running on '" + " ".join(platform.uname()) + "' from within '" + os.getcwd() +"' by user '" + getpass.getuser() + "'" )


def print_script_information():
    log.info(
        "PyJi Script version  '" + properties.version + "  r" + properties.revision + "' built on '" + properties.build_date + "'")


def read_property_from_file(propertyName, propertiesSectionName, propertiesFilename, warnIfEmpty=True):
    result = ""
    if os.path.isfile(propertiesFilename):
        try:
            cfg = RawConfigParser()
            cfg.read(propertiesFilename)
            result = cfg.get(propertiesSectionName, propertyName)
            if (globals().has_key('log')):
                log.warn(
                    "Value of '" + propertyName + "' from '[" + propertiesSectionName + "]' in '" + propertiesFilename + "' = '" + result + "'")
                if result == "" and warnIfEmpty:
                    log.warn("No value exists for '" + propertyName + "' on section '[" + propertiesSectionName + "]' inside file '" + propertiesFilename + "'")
                elif result == "" and not warnIfEmpty:
                    log.info("No value exists for '" + propertyName + "' on section '[" + propertiesSectionName + "]' inside file '" + propertiesFilename + "' however empty values for this property are expected and some times intentional.")
        except:
            raise
    else:
        if globals().has_key('log'):
            log.warn("Properties file '" + propertiesFilename + "' does not exist.")
        result = None

    return result


def get_current_hostname():
    result = ""
    try:
        result = socket.gethostbyname(socket.gethostname())
    except Exception:
        result = socket.gethostname()

    return result


def generate_guid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    t = long( time.time() * 1000 )
    r = long( random.random()*100000000000000000L )
    try:
        a = get_current_hostname()
    except:
        # if we can't get a network address, just imagine one
        a = random.random()*100000000000000000L

    data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
    import hashlib
    data = hashlib.md5(data).hexdigest()
    return data


def check_file_exists(filename):
    if os.path.isfile(filename):
        return 0
    else:
        return 1


def check_folder_exists(path):
    if os.path.isdir(path):
        return 0
    else:
        return 1


def get_class(fully_qualified_path, module_name, class_name, *instantiation):
    """
    Returns an instantiated class for the given string descriptors
    :param fully_qualified_path: The path to the module eg("Utilities.Printer")
    :param module_name: The module name eg("Printer")
    :param class_name: The class name eg("ScreenPrinter")
    :param instantiation: Any fields required to instantiate the class
    :return: An instance of the class
    """
    p = __import__(fully_qualified_path)
    m = getattr(p, module_name)
    c = getattr(m, class_name)
    instance = c(*instantiation)
    return instance


def ab_path_to_class(path, p):
    # pkg.module.ClassName
    _p_name = path.split(".")[0] + "." + path.split(".")[1]  # pkg.module
    _m_name = path.split(".")[1]  # module
    _c_name = path.split(".")[2]  # ClassName

    # Instantiate class
    c = get_class(_p_name, _m_name, _c_name, p)
    return c


def ab_subclass_path_from_action(s):
    switcher = {
        'comment': "actionbundles.ab_comment.ABComment",
        'transition': "actionbundles.ab_transition.ABTransition",
        'autotransition': "actionbundles.ab_auto_transition.ABAutoTransition",
    }
    abPath = switcher.get(s, "n/a")
    log.debug("Action '" + s + "' maps to AB class '" + abPath + "'")
    return abPath


def jira_authenticate(url, u, p):
    try:
        log.info("Attempting to authenticate to '" + url + "' (username: '" + u + "'" + "' password: '" + p + "')")
        j = JIRA(url, basic_auth=(u, p))
        log.info("Successful authentication!")
    except:
        log.error(
            "Error when trying to authenticate to '" + url + "' (username: '" + u + "'" + "' password: '" + p + "')")
        raise
    return j


def get_string_from_list(lst, n, s):
    r = False
    for i in lst:
        # log.debug("Comparing '", str(i[n]), "' with '", s, "'")
        if i[n] == s:
            r = True
            break
    return r


def start_busy_indicator(msg):
    spin = SpinCursor(msg)
    spin.start()
    return spin


def stop_busy_indicator(busyIndicator):
    busyIndicator.stop()


class PropertyReader(object):
    '''
    classdocs
    '''

    property_file = "conf/global.properties"

    def __init__(self):
        '''
        Constructor
        '''

        # Get properties from global.properties
        # [propertyFiles]
        self.log_properties = read_property_from_file("logProperties", "propertyFiles", self.property_file)
        self.jira_properties = read_property_from_file("jiraProperties", "propertyFiles", self.property_file)

        # [variousProperties]
        self.default_logger = read_property_from_file("defaultLogger", "variousProperties", self.property_file)
        self.manifest_file = read_property_from_file("manifestFile", "variousProperties", self.property_file)
        self.manifest_template_file = read_property_from_file("manifestTemplateFile", "variousProperties",
                                                              self.property_file)
        self.script_name = read_property_from_file("scriptName", "variousProperties", self.property_file)

        # [loggingProperties]
        self.custom_logging_format = read_property_from_file("customLoggingFormat", "loggingProperties",
                                                             self.property_file)


        # MANIFEST.MF
        if check_file_exists(self.manifest_file) == 1:
            print "File '" + self.manifest_file + "' does not exist. Sorry, you cannot work with an unreleased version of PyJi. If you must work with it please execute 'cp " + self.manifest_template_file + " " + self.manifest_file + "' and retry running the script."
            sys.exit()
        self.version = read_property_from_file("version", self.script_name, self.manifest_file)
        self.revision = read_property_from_file("revision", self.script_name, self.manifest_file)
        self.build_date = read_property_from_file("buildDate", self.script_name, self.manifest_file)

# Initialize script global properties
properties = PropertyReader()

# Initialize loggers
logging.ColorFormatter = ColorFormatter
logging.config.fileConfig(properties.log_properties)
log = logging.getLogger(properties.default_logger)
