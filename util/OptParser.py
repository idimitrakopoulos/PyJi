from optparse import OptionParser, OptionGroup, Option
from lib.Toolkit import log, checkFileExists, checkUrlExists, downloadFile, logging,\
    scriptGlobals
import sys

validActions = ['add-comment']
action = None
mandatoryOptions = []
fileOptions = []

def actionUsage():
    print '''Usage: pyji.py [options]

Options:
  -h, --help            Using this switch combined with an action will give you the options required for it
  -a <ACTION>, --action=<ACTION>
                        Choose one of the following actions '%s' (mandatory)
''' % (", ".join(validActions))



# Pseudoparser (overcomes limitation of default python OptParser module)
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-a') or (sys.argv[i] == '--action'):
        action = sys.argv[i+1]

if action == None:
    actionUsage()
    sys.exit()

# Make sure actions are recognised
found = 0
for va in validActions:
    if (action == va) or ((action) and (action).startswith("_")): # this way we allow any custom _XXXX actions
        found=1
        break
if found != 1:
    if (action): log.critical("Unrecognized action '" + action + "'\n")
    actionUsage()
    sys.exit()

# Init Optparser
parser = OptionParser(version="%prog \n\n version: '"+ scriptGlobals.version + "'\n revision: '"+ scriptGlobals.revision + "'\n build date: '" + scriptGlobals.buildDate + "'")

# Init Action Specific Options (but don't add them to the parser yet)
envpropsOption = Option("-e", "--envprops",       dest="envprops",       help="Environment specific properties file (mandatory)",                                                 metavar="<FILENAME>")
moduleOption = Option("-f", "--module",         dest="module",         help="Deployable module filename or file URL (mandatory)",                                               metavar="<FILENAME>")
rollbackOption = Option("-r", "--rollback",       dest="rollback",       help="Rollback filename (mandatory)",                                                                    metavar="<FILENAME>")

# Add common options
if (action):
    # The pinnacle of all options :-) (determines what other options will be added to the parser)
    parser.add_option("-a", "--action",         dest="action",         help="Choose one of the following actions '" +", ".join(validActions) + "' (mandatory)",      metavar="<ACTION>")

    # Common Options
    commonOptionsGroup = OptionGroup(parser, "Common Options", "(Common throughout all actions supported by Fireworks)")
    commonOptionsGroup.add_option("-u", "--unattended",     action="store_true",         dest="unattended",            default=False,     help="Unattended installation (no step-by-step questions)")
    commonOptionsGroup.add_option("-c", "--compatibility",  action="store_true",         dest="compatibility",         default=False,     help="Compatibility mode (ignore existing Python version)")
    commonOptionsGroup.add_option("-s", "--silent",         action="store_true",         dest="silent",                default=False,     help="Silent mode (don't send any email notifications)")
    parser.add_option_group(commonOptionsGroup)

    # Logging Options
    loggingOptionsGroup = OptionGroup(parser, "Logging Options", "(Regulate the logging of Fireworks. Default loglevel: INFO)")
    loggingOptionsGroup.add_option("-v", "--verbose",        action="store_const",       const=1, dest="verbose",        help="Verbose mode (loglevel: DEBUG)")
    loggingOptionsGroup.add_option("-V", "--vverbose",       action="store_const",       const=2, dest="verbose",        help="Very verbose mode (loglevel: DEBUG+)")
    parser.add_option_group(loggingOptionsGroup)

# Add options per action specified
if (action in ['install-clean', 'install-update', 'install-nodb', 'configure', 'backup', 'start', 'stop', 'kill', 'restart', 'status', 'info', 'log', 'debug'] or (action).startswith("_")):
    parser.add_option(envpropsOption)
    parser.add_option(moduleOption)

    mandatoryOptions = ['envprops', 'module']
    fileOptions = ['envprops', 'module']

elif (action in ['rollback']):
    parser.add_option(envpropsOption)
    parser.add_option(moduleOption)
    parser.add_option(rollbackOption)

    mandatoryOptions = ['envprops', 'module', 'rollback']
    fileOptions = ['envprops', 'module', 'rollback']

else:
    log.critical("Action '" + action + "' is allowed but there is no implementation for it at this point")
    sys.exit()

# Parse arguments
(options, args) = parser.parse_args()

# Make sure all mandatory options are provided
for m in mandatoryOptions:
    if not options.__dict__[m]:
        log.critical("Mandatory option '" + m + "' is missing\n")
        parser.print_help()
        sys.exit()

# If file is URL download it and use it
if vars().has_key('options.module') and (checkUrlExists(options.module) == True):
    fileLocation = downloadFile(options.module, scriptGlobals.workingDir)
    options.module = fileLocation

# Make sure all mandatory fileOptions exist
for f in fileOptions:
    if checkFileExists(options.__dict__[f]):
        log.critical("The following file is missing '" + options.__dict__[f] +"'\n")
        parser.print_help()
        sys.exit()

# Set logging level
if options.verbose == 1:
    log.root.handlers[0].setLevel(logging.DEBUG)
elif options.verbose == 2:
    log.root.handlers[0].setLevel(logging.DEBUG) # same logging level as verbose BUT its value also controls the logIfVerbose method
