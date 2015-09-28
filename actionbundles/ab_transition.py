from util.toolkit import log, jira_authenticate, get_string_from_list
from actionbundles.action_bundle import ActionBundle


class ABTransition(ActionBundle):
    '''
    classdocs.
    '''

    def __init__(self, parser):
        '''
        Constructor
        '''
        self.parser = parser

        log.info(self.__class__.__name__ + " initialized")

        try:
            k = parser.options.key
            s = parser.options.status

            jira = jira_authenticate(parser.options.jiraURL, parser.options.jiraUsername, parser.options.jiraPassword)

            # Get an issue.
            issue = jira.issue(k)

            # Get its valid transitions
            transitions = jira.transitions(issue)

            log.info("Issue Key       : " + k)
            log.info("Current Status  : " + str(issue.fields.status))
            log.info("Requested Status: " + str(s))

            if get_string_from_list(transitions, 'name', s):
                jira.transition_issue(issue, s)
                log.info("New Status      : " + s)

            else:
                log.debug("Ticket can only do the following transitions:")
                for t in transitions:
                    log.debug(t['name'])
                log.warn("Exiting without transition")

        except:
            raise
