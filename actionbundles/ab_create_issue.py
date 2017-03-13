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
            l = parser.options.remotelinks
            L = parser.options.simplelinks

            jira = jira_authenticate(parser.options.jiraURL, parser.options.jiraUsername, parser.options.jiraPassword)

            issue_dict = {
                'project': {'key': k},
                'summary': s,
                'description': d,
                # 'assignee': a,
                'issuetype': {'name': t},
            }

            issue = jira.create_issue(fields=issue_dict)
            log.info("Issue " + str(issue) + " was created.")

            # Assign issue
            issue.update(assignee={'name': a})

            # Simple Links
            if L:
                slDict = dict(item.split("|") for item in L.split(","))
                for key in slDict.keys():
                    log.debug("Adding simple link to issue " + str(issue) + " with title: " + key + " and value: " + slDict[key])
                    #issue2 = jira.issue(linkedIssue)
                    #jira.add_remote_link(issue, issue2)
                    #obj = {'url': 'http://www.google.com', 'title': 'sometitle'}
                    #jira.add_simple_link(issue, obj)

                    #obj = {"object": {'url': parser.options.jiraURL + '/browse/' + simpleLinkedIssue, 'title': simpleLinkedIssue}}
                    obj = {"object": {'url': slDict[key], 'title': key}}
                    jira.add_simple_link(issue, object=obj)

            # Remote Links
            if l:
                for i in l.split(","):
                    issue2 = jira.issue(i)
                    jira.add_remote_link(issue, issue2)

        except:
            raise
