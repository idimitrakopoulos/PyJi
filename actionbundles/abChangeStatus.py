from util.Toolkit import log, jiraAuth, scriptGlobals
from actionbundles.ActionBundle import ActionBundle


class abChangeStatus(ActionBundle):
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

            jira = jiraAuth(scriptGlobals.jiraURL, scriptGlobals.jiraUsername, scriptGlobals.jiraPassword)

            # Get an issue.
            issue = jira.issue(k)

            # Get its valid transitions
            transitions = jira.transitions(issue, None, True)
            for t in transitions:
                print [(t['id'], t['name'])]

                print 'Deploy Issue' in transitions[1]

            log.info("Issue Key       : " + k)
            log.info("Current Status  : " + str(issue.fields.status))

            if str(issue.fields.status) in ('Resolved') and u'Deploy' in transitions:
                jira.transition_issue(issue, u'Deploy')
                log.info("New Status      : " + 'Ready To Test')

            elif str(issue.fields.status) in ('Resolved') and u'Deploy Issue' in transitions:
                jira.transition_issue(issue, u'Deploy Issue')
                log.info("New Status      : " + 'Ready To Test')

            elif str(issue.fields.status) in ('Ready for Release'):
                jira.transition_issue(issue, u'Deploy on UAT')
                log.info("New Status      : " + 'Deploy on UAT')

            else:
                log.info("No transition identified")

        except:
            raise
