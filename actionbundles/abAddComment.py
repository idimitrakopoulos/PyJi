from util.Toolkit import log, jiraAuth
from actionbundles.ActionBundle import ActionBundle


class abAddComment(ActionBundle):
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

            jira = jiraAuth(parser.options.jiraURL, parser.options.jiraUsername, parser.options.jiraPassword)

            # Get an issue.
            issue = jira.issue(k)

            log.info("Issue Key: " + k)
            log.info("Comment  : " + c)

            # Add a comment to the issue
            jira.add_comment(issue, c)

        except:
            raise
