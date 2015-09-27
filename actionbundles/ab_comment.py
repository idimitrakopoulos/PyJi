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

            jira = jira_authenticate(parser.options.jiraURL, parser.options.jiraUsername, parser.options.jiraPassword)

            # Get an issue.
            issue = jira.issue(k)

            log.info("Issue Key: " + k)
            log.info("Comment  : " + c)

            # Add a comment to the issue
            jira.add_comment(issue, c)

        except:
            raise
