from util.toolkit import log, jira_authenticate, properties, get_string_from_list
from actionbundles.action_bundle import ActionBundle


class ABAutoTransition(ActionBundle):
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

            jira = jira_authenticate(properties.jiraURL, properties.jiraUsername, properties.jiraPassword)

            # Get an issue.
            issue = jira.issue(k)

            # Get its valid transitions
            transitions = jira.transitions(issue)

            for t in transitions:
                print t['name']

            log.info("Issue Key       : " + k)
            log.info("Current Status  : " + str(issue.fields.status))

            if str(issue.fields.status) in ('Resolved') and get_string_from_list(transitions, 'name', 'Deploy'):
                jira.transition_issue(issue, u'Deploy')
                log.info("New Status      : " + 'Ready To Test')

            elif str(issue.fields.status) in ('Resolved') and get_string_from_list(transitions, 'name', 'Deploy Issue'):
                jira.transition_issue(issue, u'Deploy Issue')
                log.info("New Status      : " + 'Ready To Test')

            elif str(issue.fields.status) in ('Ready for Release'):
                jira.transition_issue(issue, u'Deploy on UAT')
                log.info("New Status      : " + 'Deploy on UAT')

            else:
                log.debug("Ticket can only do the following transitions:")
                for t in transitions:
                    log.debug(t['name'])
                log.warn("Exiting without transition")

        except:
            raise
