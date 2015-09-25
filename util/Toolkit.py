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

from util.ColorFormatter import ColorFormatter


def die(msg="Error"):
    log.warn(msg)
    sys.exit()

def raiseNotImplementedException():
    raise NotImplementedError, "Oops! This part of the functionality has not been implemented ... Bye bye!"

def killProcess(pid):
    log.warn("kill -9 " + pid)
    os.kill(int(pid), signal.SIGKILL)

def terminateProcess(pid):
    log.warn("kill " + pid)
    os.kill(int(pid), signal.SIGTERM)


def printOsInformation():
    log.info("Script running on '" + " ".join(platform.uname()) + "' from within '" + os.getcwd() +"' by user '" + getpass.getuser() + "'" )

def printsScriptInformation():
    log.info("PyJi Script version  '" + scriptGlobals.version + "  r" + scriptGlobals.revision +"' built on '" + scriptGlobals.buildDate + "'" )


def readPropertyFromPropertiesFile(propertyName, propertiesSectionName, propertiesFilename, warnIfEmpty = True):
    result = ""
    if (os.path.isfile(propertiesFilename)):
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
        if (globals().has_key('log')):
            log.warn("Properties file '" + propertiesFilename + "' does not exist.")
        result = None

    return result


def getCurrentHostname():
    result = ""
    try:
        result = socket.gethostbyname(socket.gethostname())
    except Exception:
        result = socket.gethostname()

    return result

def generateGUID( *args ):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    t = long( time.time() * 1000 )
    r = long( random.random()*100000000000000000L )
    try:
        a = getCurrentHostname()
    except:
        # if we can't get a network address, just imagine one
        a = random.random()*100000000000000000L

    data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
    import hashlib
    data = hashlib.md5(data).hexdigest()
    return data


def checkFileExists(filename):
    if os.path.isfile(filename):
        return 0
    else:
        return 1


def checkDirExists(path):
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


def abPathToClass(abPath, p):
    cName = abPath.split(".")[1]
    c = get_class(abPath, cName, cName, p)
    return c


def abSubclassPathFromAction(s):
    switcher = {
        'add-comment': "actionbundles.abAddComment",
        'change-status': "actionbundles.abChangeStatus",
    }
    abPath = switcher.get(s, "n/a")
    log.debug("Action '" + s + "' maps to AB class '" + abPath + "'")
    return abPath


def jiraAuth(url, u, p):
    try:
        log.info("Attempting to authenticate to '" + url + "' (username: '" + u + "'" + "' password: '" + p + "')")
        j = JIRA(url, basic_auth=(u, p))
        log.info("Successful authentication!")
    except:
        log.error(
            "Error when trying to authenticate to '" + url + "' (username: '" + u + "'" + "' password: '" + p + "')")
        raise
    return j


def findStringInList(lst, n, s):
    r = False
    for i in lst:
        # log.debug("Comparing '", str(i[n]), "' with '", s, "'")
        if i[n] == s:
            r = True
            break
    return r






class ScriptGlobals(object):
    '''
    classdocs
    '''

    globalProperties = "conf/global.properties"

    def __init__(self):
        '''
        Constructor
        '''

        # Get properties from global.properties
        # [propertyFiles]
        self.logProperties = readPropertyFromPropertiesFile("logProperties", "propertyFiles", self.globalProperties)
        self.jiraProperties = readPropertyFromPropertiesFile("jiraProperties", "propertyFiles", self.globalProperties)

        # [variousProperties]
        self.defaultLogger = readPropertyFromPropertiesFile("defaultLogger", "variousProperties", self.globalProperties)
        self.manifestFile = readPropertyFromPropertiesFile("manifestFile", "variousProperties", self.globalProperties)
        self.manifestTemplateFile = readPropertyFromPropertiesFile("manifestTemplateFile", "variousProperties",
                                                                   self.globalProperties)
        self.scriptVarSectionName = readPropertyFromPropertiesFile("scriptVarSectionName", "variousProperties",
                                                                   self.globalProperties)

        # [loggingProperties]
        self.customLoggingFormat = readPropertyFromPropertiesFile("customLoggingFormat", "loggingProperties", self.globalProperties)

        # [jiraProperties]
        self.jiraURL = readPropertyFromPropertiesFile("jiraURL", "jiraProperties", self.jiraProperties)
        self.jiraUsername = readPropertyFromPropertiesFile("jiraUsername", "jiraProperties", self.jiraProperties)
        self.jiraPassword = readPropertyFromPropertiesFile("jiraPassword", "jiraProperties", self.jiraProperties)

        # MANIFEST.MF
        if checkFileExists(self.manifestFile) == 1:
            print "File '" + self.manifestFile + "' does not exist. Sorry, you cannot work with an unreleased version of PyJi. If you must work with it please execute 'cp " + self.manifestTemplateFile + " " + self.manifestFile + "' and retry running the script."
            sys.exit()
        self.version = readPropertyFromPropertiesFile("version", self.scriptVarSectionName, self.manifestFile)
        self.revision = readPropertyFromPropertiesFile("revision", self.scriptVarSectionName, self.manifestFile)
        self.buildDate = readPropertyFromPropertiesFile("buildDate", self.scriptVarSectionName, self.manifestFile)

# Initialize script global properties
scriptGlobals = ScriptGlobals()

# Initialize loggers
logging.ColorFormatter = ColorFormatter
logging.config.fileConfig(scriptGlobals.logProperties)
log = logging.getLogger(scriptGlobals.defaultLogger)
