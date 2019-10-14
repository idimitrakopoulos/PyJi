from util.toolkit import log, jira_authenticate
from actionbundles.action_bundle import ActionBundle
from util.jira_toolkit import Transition, count_status, get_time_between_extreme_statuses,get_time_between_statuses
from dateutil.parser import *

class ABIssueKpi(ActionBundle):
    '''
    classdocs.
    '''

    def __init__(self, parser):
        '''
        Constructor
        '''
        self.parser = parser

        log.info(self.__class__.__name__ + " initialized")

        # try:
        #
        #     k = parser.options.key
        #
        #     jira = jira_authenticate(parser.options.jira_url, parser.options.jira_username, parser.options.jira_password)
        #
        #     # Get an issue.
        #     issue = jira.issue(k, expand='changelog')
        #     changelog = issue.changelog
        #
        #     log.info("Issue Key  : " + str(k))
        #
        #     keep_date = None
        #     diff = None
        #     for history in reversed(changelog.histories):
        #         for item in history.items:
        #             if item.field == 'status':
        #                 if keep_date != None:
        #                     diff = parse(history.created) - keep_date
        #                 print item.fromString + ' -> ' + item.toString + " (Transition took: " + str(diff) +" on " + str(history.created) +")"
        #
        #                 keep_date = parse(history.created)
        #                 diff = None
        #
        #     reopen_count = count_status("Reopened", changelog)
        #     log.info("Reopened times: {}".format(str(reopen_count)))
        #
        #
        #     lead_time = get_time_between_extreme_statuses("Open", "Closed", changelog).interval
        #     log.info("Lead Time = {} ({} -> {})".format(lead_time, "Open", "Closed"))
        #
        #     time_spent_for_specs = get_time_between_statuses("Open", "In Progress", changelog)[0].interval
        #     log.info("Specs -> Development = {} ({} -> {})".format(time_spent_for_specs, "Open", "In Progress"))
        #
        #     # TODO: fix for new workflow
        #     time_for_initial_development = get_time_between_statuses("In Progress", "Done", changelog)[0].interval
        #     log.info("Development time - initial = {} ({} -> {})".format(time_for_initial_development, "In Progress", "Done"))
        #
        #     # TODO: fix for new workflow
        #     time_lag_to_start_qa = get_time_between_statuses("Done", "QA", changelog)[0].interval
        #     log.info("Time to start QA = {} ({} -> {})".format(time_lag_to_start_qa, "Done", "QA"))
        #
        #     if reopen_count > 0:
        #         # TODO: fix for new workflow
        #         time_for_initial_qa = get_time_between_statuses("QA", "Reopened", changelog)[0].interval
        #         log.info("QA time - initial = {} ({} -> {})".format(time_for_initial_qa, "QA", "Reopened"))
        #
        #         total_time_after_first_reopen = get_time_between_extreme_statuses("Reopened", "QA OK", changelog).interval
        #         log.info("Total time spent after first Reopen = {} ({} -> {}))".format(total_time_after_first_reopen, "Reopened", "QA OK"))
        #
        #     else:
        #
        #         # TODO: fix for new workflow
        #         time_for_initial_qa = get_time_between_statuses("QA", "QA OK", changelog)[0].interval
        #         log.info("QA time - initial = {} ({} -> {})".format(time_for_initial_qa, "QA", "QA OK"))
        #
        #
        #     # TODO: fix for new workflow
        #     time_lag_to_start_uat = get_time_between_statuses("QA OK", "UAT", changelog)[0].interval
        #     log.info("Time to start UAT = {} ({} -> {})".format(time_lag_to_start_uat, "QA OK", "UAT"))
        #
        #
        #     time_for_initial_uat = get_time_between_statuses("UAT", "Closed", changelog)[0].interval
        #     log.info("UAT time - initial = {} ({} -> {})".format(time_for_initial_uat, "UAT", "Closed"))
        #
        # except:
        #     raise
