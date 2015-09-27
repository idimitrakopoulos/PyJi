from optparse import OptionParser, OptionGroup
import sys
import getpass

from util.toolkit import check_file_exists, properties, log, logging

valid_actions = ['comment', 'transition', 'autotransition']
action = None
mandatory_options = ['action', 'jiraURL', 'jiraUsername', 'jiraPassword']
file_options = []


def action_usage():
    print '''Usage: pyji.py [options]

Options:
  -h, --help            Using this switch combined with an action will give you the options required for it
  -a <ACTION>, --action=<ACTION>
                        Choose one of the following actions '%s' (mandatory)
''' % (", ".join(valid_actions))


# Pseudoparser (overcomes limitation of default python OptParser module)
for i in range(len(sys.argv)):
    if (sys.argv[i] == '-a') or (sys.argv[i] == '--action'):
        action = sys.argv[i+1]

if action == None:
    action_usage()
    sys.exit()

# Make sure actions are recognised
found = 0
for va in valid_actions:
    if (action == va) or ((action) and (action).startswith("_")): # this way we allow any custom _XXXX actions
        found=1
        break
if found != 1:
    if (action): log.critical("Unrecognized action '" + action + "'\n")
    action_usage()
    sys.exit()

# Init Optparser
parser = OptionParser(
    version="%prog \n\n version: '" + properties.version + "'\n revision: '" + properties.revision + "'\n build date: '" + properties.build_date + "'")

# Add common options
if (action):
    # The pinnacle of all options :-) (determines what other options will be added to the parser)
    parser.add_option("-a", "--action", dest="action",
                      help="Choose one of the following actions '" + ", ".join(valid_actions) + "' (mandatory)",
                      metavar="<ACTION>")

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
if (action in valid_actions or (action).startswith("_")):
    log.info("Action that was requested to execute '" + action + "'")

    if (action in 'comment'):
        parser.add_option("-k", "--key", dest="key", help="The jira issue key (mandatory)", metavar="<KEY>")
        parser.add_option("-c", "--comment", dest="comment", help="The comment you want to add (mandatory)",
                          metavar="<COMMENT>")
        mandatory_options.append('key')
        mandatory_options.append('comment')


    elif (action in 'transition'):
        parser.add_option("-k", "--key", dest="key", help="The jira issue key (mandatory)", metavar="<KEY>")
        parser.add_option("-s", "--status", dest="status", help="The jira ticket status (mandatory)",
                          metavar="<STATUS>")

        mandatory_options.append('key')
        mandatory_options.append('status')

    elif (action in 'autotransition'):
        parser.add_option("-k", "--key", dest="key", help="The jira issue key (mandatory)", metavar="<KEY>")

        mandatory_options.append('key')


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
for m in mandatory_options:
    if not options.__dict__[m]:
        log.critical("Mandatory option '" + m + "' is missing\n")
        parser.print_help()
        sys.exit()


# Make sure all mandatory file_options exist
for f in file_options:
    if check_file_exists(options.__dict__[f]):
        log.critical("The following file is missing '" + options.__dict__[f] +"'\n")
        parser.print_help()
        sys.exit()

# Set logging level
if options.verbose == 1:
    log.root.handlers[0].setLevel(logging.DEBUG)
elif options.verbose == 2:
    log.root.handlers[0].setLevel(logging.DEBUG) # same logging level as verbose BUT its value also controls the logIfVerbose method
