from util.toolkit import log, jira_authenticate
from actionbundles.action_bundle import ActionBundle


class ABCreateIssue(ActionBundle):
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
            s = parser.options.summary
            d = parser.options.description
            t = parser.options.type
            a = parser.options.assignee
            i = parser.options.identifier

            jira = jira_authenticate(parser.options.jiraURL, parser.options.jiraUsername, parser.options.jiraPassword)

            issue_dict = {
                'project': {'key': k},
                'summary': s,
                'description': d,
                # 'assignee': a,
                'issuetype': {'name': t},
            }

            issue = jira.create_issue(fields=issue_dict)

            issue.update(assignee={'name': a})

        except:
            raise
