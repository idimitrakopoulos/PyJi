import ast
import datetime

from util.toolkit import log, jira_authenticate, read_property_from_file, check_file_exists, die
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
            # Input File
            self.input_file = parser.options.input_file

            # Output File
            self.output_file = parser.options.output_file

            # Estimate To Complete
            self.estimate_to_complete = parser.options.estimate_to_complete

            # Time spent
            _t = 0.0

            # Check if input file exists
            if check_file_exists(self.input_file) == 1:
                die("File '" + self.input_file + "' doesn't exist. Fatal.")

            self.project_name = read_property_from_file("project_name", "project", self.input_file)
            self.baseline_md = read_property_from_file("baseline_md", "project", self.input_file)
            self.date_format = read_property_from_file("date_format", "project", self.input_file)
            self.kick_off_date = datetime.datetime.strptime(
                read_property_from_file("kick_off_date", "project", self.input_file), self.date_format).date()
            self.uat_start_baseline = datetime.datetime.strptime(
                read_property_from_file("uat_start_baseline", "project", self.input_file), self.date_format).date()
            self.uat_start_actual = datetime.datetime.strptime(
                read_property_from_file("uat_start_actual", "project", self.input_file), self.date_format).date()
            self.go_live_baseline = datetime.datetime.strptime(
                read_property_from_file("go_live_baseline", "project", self.input_file), self.date_format).date()
            self.go_live_actual = datetime.datetime.strptime(
                read_property_from_file("go_live_actual", "project", self.input_file), self.date_format).date()
            self.issue_jql = list(ast.literal_eval(read_property_from_file("issue_jql", "project", self.input_file)))

            jira = jira_authenticate(parser.options.jiraURL, parser.options.jiraUsername, parser.options.jiraPassword)

            log.info("--------------------------------------------------------")
            log.info("| " + self.project_name)
            log.info("--------------------------------------------------------")

            log.info("Kick-off                      : " + str(self.kick_off_date))
            log.info("UAT Start (Baseline)          : " + str(self.uat_start_baseline))
            log.info("UAT Start (Actual)            : " + str(self.uat_start_actual))
            log.info("GoLive (Baseline)             : " + str(self.go_live_baseline))
            log.info("GoLive (Actual)               : " + str(self.go_live_actual))
            log.info("Effort (Baseline)             : " + str(self.baseline_md) + " md")
            #############################################
            # TIME SPENT
            #############################################
            # Iterate JQL Filters
            for f in self.issue_jql:
                log.debug("Processing JQL: " + f)
                r = jira.search_issues(f, 0, False)
                # Iterate Issues
                for k in r:
                    # Get each issue from filter
                    issue = jira.issue(k)
                    # Get issue's timespent in seconds and add it to the overall sum
                    if issue.fields.timespent is not None:
                        _t = _t + issue.fields.timespent
                log.debug("Time spent so far is     : " + str(("%.2f" % ((_t / 3600) / 8))))

            # Switch timespent to md and round it off to 2 digits
            _t = "%.2f" % ((_t / 3600) / 8)

            log.info("Effort (Actual)               : " + str(_t) + " md")

            #############################################
            # ESTIMATE TO COMPLETE
            #############################################
            _etc = 0
            if self.baseline_md < _t and self.estimate_to_complete is None:
                die("Time spent " + str(
                    _t) + " md is higher than the baseline " + self.baseline_md + " md so an estimate to complete calculation cannot take place, please use -e switch to provide a manual E.t.C.")
            elif self.estimate_to_complete is None:
                _etc = float(self.baseline_md) - float(_t)
            else:
                _etc = self.estimate_to_complete

            log.info("Effort (Remaining)            : " + str(_etc) + " md")


            #############################################
            # EFFORT AT COMPLETION
            #############################################

            # Calculate Estimate At Completion
            _eac = float(_t) + float(_etc)

            log.info("Effort (At Completion)        : " + str(_eac) + " md")

            #############################################
            # ON TIME
            #############################################
            _a = self.go_live_actual - self.kick_off_date
            _b = self.go_live_baseline - self.kick_off_date

            # On Time
            _ot = (_a.total_seconds() / _b.total_seconds())

            log.info("--------------------------------------------------------")
            log.info("On Time                       : " + str("%.2f" % _ot))


            #############################################
            # IN EFFORT
            #############################################

            # In Effort
            _ie = _eac / float(self.baseline_md)

            log.info("In Effort                     : " + str("%.2f" % _ie))
            log.info("--------------------------------------------------------")

        except:
            raise
