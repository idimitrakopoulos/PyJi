from util.toolkit import log, jira_authenticate
from actionbundles.action_bundle import ActionBundle


class ABComment(ActionBundle):
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
            c = parser.options.comment
            i = parser.options.identifier

            jira = jira_authenticate(parser.options.jiraURL, parser.options.jiraUsername, parser.options.jiraPassword)

            # Get an issue.
            issue = jira.issue(k)

            log.info("Issue Key  : " + str(k))
            log.info("Comment    : " + str(c))
            log.info("Identifier : " + str(i))

            # Add a comment to the issue
            if i:
                jira.add_comment(issue, "[" + str(i) + "]: " + str(c))
            else:
                jira.add_comment(issue, str(c))

        except:
            raise
