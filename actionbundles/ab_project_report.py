from util.toolkit import log, jira_authenticate
from actionbundles.action_bundle import ActionBundle


class ABProjectReport(ActionBundle):
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

            i = parser.options.input_file
            o = parser.options.output_file

            jira = jira_authenticate(parser.options.jiraURL, parser.options.jiraUsername, parser.options.jiraPassword)




        except:
            raise
