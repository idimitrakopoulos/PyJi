import os, getpass, time, random
from ConfigParser import ConfigParser, RawConfigParser

def die(msg="Error"):
    log.critical(msg)
    sys.exit()

def raiseNotImplementedException():
    raise NotImplementedError, "Oops! This part of the functionality has not been implemented ... Bye bye!"

def killProcess(pid):
    logIfVerbose("kill -9 " + pid)
    os.kill(int(pid), signal.SIGKILL)

def terminateProcess(pid):
    logIfVerbose("kill " + pid)
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
                logIfVerbose("Value of '" + propertyName +"' from '[" + propertiesSectionName +"]' in '" + propertiesFilename + "' = '" + result + "'")
                if result == "" and warnIfEmpty:
                    log.warn("No value exists for '" + propertyName + "' on section '[" + propertiesSectionName + "]' inside file '" + propertiesFilename + "'")
                elif result == "" and not warnIfEmpty:
                    log.info("No value exists for '" + propertyName + "' on section '[" + propertiesSectionName + "]' inside file '" + propertiesFilename + "' however empty values for this property are expected and some times intentional.")
        except:
            raise
    else:
        if (globals().has_key('log')):
            logIfVerbose("Properties file '" + propertiesFilename + "' does not exist.")
        result = None

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
    import md5 # deprecated annoying library for python >2.4
    data = md5.md5(data).hexdigest()
    return data

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

        # [variousProperties]
        self.workingDir = readPropertyFromPropertiesFile("workingDir", "variousProperties", self.globalProperties)
        self.defaultLogger = readPropertyFromPropertiesFile("defaultLogger", "variousProperties", self.globalProperties)

        # [loggingProperties]
        self.customLoggingFormat = readPropertyFromPropertiesFile("customLoggingFormat", "loggingProperties", self.globalProperties)




# Initialize script global properties
scriptGlobals = ScriptGlobals();

