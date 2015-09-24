from util.Toolkit import log, jiraAuth, scriptGlobals
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
            jira = jiraAuth(scriptGlobals.jiraURL, scriptGlobals.jiraUsername, scriptGlobals.jiraPassword)

            # Get an issue.
            issue = jira.issue(parser.options.key)



        except:
            raise
