from optparse import OptionParser, OptionGroup
import sys
import getpass

from util.Toolkit import checkFileExists, scriptGlobals, log, logging

validActions = ['add-comment', 'change-status']
action = None
mandatoryOptions = ['action', 'jiraURL', 'jiraUsername', 'jiraPassword']
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

# Add common options
if (action):
    # The pinnacle of all options :-) (determines what other options will be added to the parser)
    parser.add_option("-a", "--action",         dest="action",         help="Choose one of the following actions '" +", ".join(validActions) + "' (mandatory)",      metavar="<ACTION>")

    # Jira Options
    jiraOptionsGroup = OptionGroup(parser, "JIRA Options", "(JIRA location and credentials)")
    jiraOptionsGroup.add_option("-U", "--jiraURL", dest="jiraURL",
                                help="The JIRA URL you are connecting to (e.g. https://jira.atlassian.net)",
                                metavar="<JIRAURL>")
    jiraOptionsGroup.add_option("-u", "--jiraUsername", dest="jiraUsername",
                                help="The JIRA Username you are using to connect",
                                metavar="<JIRAUSERNAME>")
    jiraOptionsGroup.add_option("-p", "--jiraPassword", dest="jiraPassword",
                                help="The JIRA Password you are using to connect",
                                metavar="<JIRAPASSWORD>")
    jiraOptionsGroup.add_option("-P", "--promptForJiraPassword", action="store_const", const=1,
                                dest="promptForJiraPassword",
                                help="Prompt for JIRA password instead of specifying in the command line")

    parser.add_option_group(jiraOptionsGroup)


    # Common Options
    commonOptionsGroup = OptionGroup(parser, "Common Options", "(Common throughout all actions supported by PyJi)")
    commonOptionsGroup.add_option("-C", "--compatibility", action="store_true", dest="compatibility", default=False,
                                  help="Compatibility mode (ignore existing Python version)")
    commonOptionsGroup.add_option("-S", "--silent", action="store_true", dest="silent", default=False,
                                  help="Silent mode (don't send any email notifications)")

    commonOptionsGroup.add_option("-i", "--identifier", dest="identifier", help="A unique identifier",
                                  metavar="<IDENTIFIER>")

    parser.add_option_group(commonOptionsGroup)

    # Logging Options
    loggingOptionsGroup = OptionGroup(parser, "Logging Options",
                                      "(Regulate the logging of PyJi. Default loglevel: INFO)")
    loggingOptionsGroup.add_option("-v", "--verbose",        action="store_const",       const=1, dest="verbose",        help="Verbose mode (loglevel: DEBUG)")
    loggingOptionsGroup.add_option("-V", "--vverbose",       action="store_const",       const=2, dest="verbose",        help="Very verbose mode (loglevel: DEBUG+)")
    parser.add_option_group(loggingOptionsGroup)

# Add options per action specified
if (action in validActions or (action).startswith("_")):
    log.info("Action that was requested to execute '" + action + "'")

    if (action in 'add-comment'):
        parser.add_option("-k", "--key", dest="key", help="The jira issue key (mandatory)", metavar="<KEY>")
        parser.add_option("-c", "--comment", dest="comment", help="The comment you want to add (mandatory)",
                          metavar="<COMMENT>")
        mandatoryOptions.append('key')
        mandatoryOptions.append('comment')


    elif (action in 'change-status'):
        parser.add_option("-k", "--key", dest="key", help="The jira issue key (mandatory)", metavar="<KEY>")
        parser.add_option("-s", "--status", dest="status", help="The jira ticket status (mandatory)",
                          metavar="<STATUS>")

        mandatoryOptions.append('key')
        mandatoryOptions.append('status')
else:
    log.critical("Action '" + action + "' is allowed but there is no implementation for it at this point :-(")
    sys.exit()

# Parse arguments
(options, args) = parser.parse_args()

# If Jira passsword prompt is requested, then prompt
if options.promptForJiraPassword:
    log.info("Enter your JIRA password for " + options.jiraUsername + "@" + options.jiraURL + ": ")
    options.jiraPassword = getpass.getpass("> ")

# Make sure all mandatory options are provided
for m in mandatoryOptions:
    if not options.__dict__[m]:
        log.critical("Mandatory option '" + m + "' is missing\n")
        parser.print_help()
        sys.exit()


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
