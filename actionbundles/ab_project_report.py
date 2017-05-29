import ast
import sys
from datetime import datetime, timedelta

from util.toolkit import log, jira_authenticate, read_property_from_file, check_file_exists, die
from actionbundles.action_bundle import ActionBundle


class ABProjectReport(ActionBundle):
    '''
    classdocs.
    '''

    def export_to_html(self, project_name,
                       kick_off_date,
                       uat_start_baseline_date,
                       uat_start_actual_date,
                       golive_baseline_date,
                       golive_actual_date,
                       on_time,
                       effort_baseline_md,
                       effort_actual_md,
                       effort_remaining_md,
                       effort_at_completion_md,
                       in_effort,
                       revenue,
                       md_rate_offer,
                       md_rate_internal,
                       md_cost_baseline,
                       md_cost_eac,
                       other_costs_baseline,
                       other_costs_actual,
                       pnl_baseline,
                       pnl_eac,
                       in_budget,
                       execution_params):
        """

        :rtype : HTML
        """
        return '''


<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="X-Frame-Options" content="allow">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Exus - Web & Mobile</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/sb-admin.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>
        <!-- Navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <a class="navbar-brand" href="#">Exus - Web & Mobile</a>
            </div>
            <!-- Top Menu Items -->
        </nav>
        <div id="page-wrapper">

            <div class="container-fluid">

                <!-- Page Heading -->
                <div class="row">
                    <div class="col-lg-8">
                        <h1 class="page-header">
                           {0}
                        </h1>
                    </div>
                    <div class="col-lg-4">
                            <button type="button" class="btn btn-outline btn-primary pull-right page-header"   data-toggle="modal" data-target="#myModal"><i class="fa fa-tasks fa-fw"></i> Execution Parameters</button>

                             <!-- Modal -->
                            <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                            <h4 class="modal-title" id="myModalLabel">Execution Parameters</h4>
                                        </div>
                                        <div class="modal-body">
                                            {22}
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                    <!-- /.modal-content -->
                                </div>
                                <!-- /.modal-dialog -->
                            </div>
                            <!-- /.modal -->
                    </div>
                </div>
                <!-- /.row -->
                <!-- /.row -->
                <div class="row">
                       <div class="col-lg-4 col-md-6">
                           <div class="panel panel-primary">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">Kick Off</span>
                                    <span class="pull-right largeF">{1}</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>

                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-yellow">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">Effort (Baseline)</span>
                                      <span class="pull-right largeF">{7}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">Revenue</span>
                                      <span class="pull-right largeF">{12}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                </div>
   <div class="row">

  <div class="col-lg-4 col-md-6">
                       <div class="panel panel-primary">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">GoLive (Baseline)</span>
                                     <span class="pull-right largeF">{4}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>


                    </div>
                    <div class="col-lg-4 col-md-6">
                        <div class="panel panel-yellow">

                                <div class="panel-footer panel-darker">
                                    <span class="pull-left largeF"><strong>Effort (Actual)</strong></span>
                                    <span class="pull-right largeF "><strong>{8}</strong></span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>

                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">md Rate (Offer)</span>
                                    <span class="pull-right largeF">{13}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-lg-4 col-md-6">
                        <div class="panel panel-primary">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">GoLive (Actual)</span>
                                    <span class="pull-right largeF">{5}</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                     <div class="col-lg-4 col-md-6">
                       <div class="panel panel-yellow">

                                <div class="panel-footer panel-darker">
                                    <span class="pull-left largeF"><strong>Effort (Remaining)</strong></span>
                                    <span class="pull-right largeF"><strong>{9}</strong> </span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>

                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">md Rate (Internal)</span>
                                    <span class="pull-right largeF">{14}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                 </div>
                 <div class="row">
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-primary">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">UAT Start (Baseline)</span>
                                    <span class="pull-right largeF">{2}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                     <div class="col-lg-4 col-md-6">
                        <div class="panel panel-yellow">

                                <div class="panel-footer panel-darker">
                                    <span class="pull-left largeF"><strong>Effort (At Completion)</strong></span>
                                    <span class="pull-right largeF"><strong>{10}</strong> </span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>

                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer panel-darker">
                                    <span class="pull-left largeF"><strong>md Cost (Baseline)</strong></span>
                                    <span class="pull-right largeF"><strong>{15}</strong></span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-4 col-md-6">
                        <div class="panel panel-primary">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">UAT Start (Actual)</span>
                                    <span class="pull-right largeF">{3}</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                      <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer panel-darker">
                                    <span class="pull-left largeF"><strong>md Cost (at Completion)</strong></span>
                                    <span class="pull-right largeF"><strong>{16}</strong></span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                </div>

                <!-- /.row -->
            <div class="row">
                <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">Other Costs (Baseline)</span>
                                    <span class="pull-right largeF">{17}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
            </div>
            <div class="row">
                <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer">
                                    <span class="pull-left largeF">Other Costs (Actual)</span>
                                    <span class="pull-right largeF">{18}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
            </div>
            <div class="row">
                <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer panel-darker">
                                    <span class="pull-left largeF"><strong>PnL (Baseline)</strong></span>
                                    <span class="pull-right largeF"><strong>{19}</strong></span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
            </div>
            <div class="row">
                <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">

                    </div>
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-info">

                                <div class="panel-footer panel-darker">
                                    <span class="pull-left largeF"><strong>PnL (at Completion)</strong></span>
                                    <span class="pull-right largeF"><strong>{20}</strong></span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
            </div>

                 <!-- /.row -->
                <div class="row">

                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-green">

                                <div class="panel-heading panel-green">
                                    <span class="pull-left largeF">OnTime</span>
                                    <span class="pull-right largeF OnTime">{6}</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                     <div class="col-lg-4 col-md-6">
                        <div class="panel panel-green">

                                <div class="panel-heading panel-green">
                                    <span class="pull-left largeF">inEffort</span>
                                    <span class="pull-right largeF inEffort">{11}</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-green">

                                <div class="panel-heading panel-green">
                                    <span class="pull-left largeF">In Budget</span>
                                    <span class="pull-right largeF InBudget">{21}</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                </div>
                <!-- /.row -->
                 <!-- /.row
                <div class="row">
                <div class="col-lg-12">
                    <div class="panel panel-red">
                        <div class="panel-heading largeF">
                            Risks
                        </div>

                        <div class="panel-body">
                            <div class="dataTable_wrapper">
                                <table class="table table-striped table-bordered table-hover">
                                    <thead>
                                        <tr>
                                            <th>Risk</th>
                                            <th>Created</th>
                                            <th>Est. Resolution</th>
                                            <th>Mitigation</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr class="odd">
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                        <tr class="even">
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                        <tr class="odd">
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                        <tr class="even">
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                        <tr class="odd">
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                        <tr class="even">
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                        <tr class="odd">
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                        <tr class="even">
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                   </div>
                   </div>
                </div>

            </div>
            <!-- /.container-fluid -->

        </div>
        <!-- /#page-wrapper -->


    <!-- /#wrapper -->

    <!-- jQuery -->
    <script src="js/jquery.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

    <script>
    function colors(value,pos) {{
        if (eval(value)>1) {{
            eval(value)<=1.1 ? $( "."+pos ).parent("div").parent("div").removeClass("panel-green").addClass("panel-yellow") : $( "."+pos ).parent("div").parent("div").removeClass("panel-green").addClass("panel-red") ;
        }}
    }}
    colors($( ".OnTime" ).text(),"OnTime");
    colors($( ".inEffort" ).text(),"inEffort");
    colors($( ".InBudget" ).text(),"InBudget");


    </script>

</body>

</html>



    '''.format(str(project_name),
               str(kick_off_date),
               str(uat_start_baseline_date),
               str(uat_start_actual_date),
               str(golive_baseline_date),
               str(golive_actual_date),
               str(on_time),
               str(effort_baseline_md),
               str(effort_actual_md),
               str(effort_remaining_md),
               str(effort_at_completion_md),
               str(in_effort),
               str(revenue),
               str(md_rate_offer),
               str(md_rate_internal),
               str(md_cost_baseline),
               str(md_cost_eac),
               str(other_costs_baseline),
               str(other_costs_actual),
               str(pnl_baseline),
               str(pnl_eac),
               str(in_budget),
               str(execution_params))

    def __init__(self, parser):
        '''
        Constructor
        '''
        self.parser = parser

        log.info(self.__class__.__name__ + " initialized")

        try:
            # Input File
            self.input_file = parser.options.input_file

            # Estimate To Complete
            self.estimate_to_complete = parser.options.estimate_to_complete


            # Time spent
            _effort_actual_md = 0.0

            # Check if input file exists
            if check_file_exists(self.input_file) == 1:
                die("File '" + self.input_file + "' doesn't exist. Fatal.")
            self.euro_sign_encoded = u" \u20AC"
            self.euro = " eur"
            self.project_name = read_property_from_file("project_name", "project", self.input_file)
            self.baseline_md = read_property_from_file("baseline_md", "project", self.input_file)
            self.date_format = read_property_from_file("date_format", "project", self.input_file)

            # Datelimit
            self.date_limit = None
            if parser.options.date_limit is not None:
                self.date_limit = datetime.strptime(parser.options.date_limit, self.date_format) + timedelta(hours=23,
                                                                                                             minutes=59,
                                                                                                             seconds=59)

            # Project related values
            self.kick_off_date = datetime.strptime(
                read_property_from_file("kick_off_date", "project", self.input_file), self.date_format).date()
            self.uat_start_baseline = datetime.strptime(
                read_property_from_file("uat_start_baseline", "project", self.input_file), self.date_format).date()
            self.uat_start_actual = datetime.strptime(
                read_property_from_file("uat_start_actual", "project", self.input_file), self.date_format).date()
            self.go_live_baseline = datetime.strptime(
                read_property_from_file("go_live_baseline", "project", self.input_file), self.date_format).date()
            self.go_live_actual = datetime.strptime(
                read_property_from_file("go_live_actual", "project", self.input_file), self.date_format).date()
            self.issue_jql = list(ast.literal_eval(read_property_from_file("issue_jql", "project", self.input_file)))
            self.output_path = read_property_from_file("output_path", "project", self.input_file)
            self.output_filename = read_property_from_file("output_filename", "project", self.input_file)

            # Add the date limit in the filename
            if self.date_limit is not None:
                self.output_location_datelimit = str(self.output_path
                                                     + "latest_DL"
                                                     + self.date_limit.strftime("%Y%m%d")
                                                     + "_"
                                                     + self.output_filename)
            else:
                # Add "latest" in the filename
                self.output_location_latest = str(self.output_path
                                                  + "latest_"
                                                  + self.output_filename)

            self.revenue_offer = read_property_from_file("revenue_offer", "project", self.input_file)
            self.md_rate_offer = read_property_from_file("md_rate_offer", "project", self.input_file)
            self.md_rate_internal = read_property_from_file("md_rate_internal", "project", self.input_file)
            self.other_costs_baseline = read_property_from_file("other_costs_baseline", "project", self.input_file)
            self.other_costs_actual = read_property_from_file("other_costs_actual", "project", self.input_file)

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
            _effort_spent_in_future_sec = 0.0
            # Iterate JQL Filters
            for f in self.issue_jql:
                log.debug("Processing JQL: " + f)
                r = jira.search_issues(f, 0, False)
                # Iterate Issues in each JQL
                for k in r:
                    # Get each issue from filter
                    issue = jira.issue(k)
                    # log.debug("Working on issue: " + issue.key)

                    # Iterate Workogs in each Issue
                    for worklog in jira.worklogs(issue.key):
                        # log.debug(issue.key + ": " + str(worklog.id))
                        # pprint (vars(worklog))

                        # Get datetime that the worklog is about
                        _started = datetime.strptime(worklog.started[:10], "%Y-%m-%d")


                        # Check entries against date limit from the command line
                        if self.date_limit is not None and _started <= self.date_limit:
                            log.debug(
                                "Issue [" + str(issue.key) + "] Worklog [" + str(worklog.id) + "] with date " + str(
                                    _started) + " will be counted because date limit is " + str(self.date_limit))
                            _effort_actual_md = _effort_actual_md + worklog.timeSpentSeconds
                        elif self.date_limit is not None and _started > self.date_limit:
                            log.warn(
                                "Issue [" + str(issue.key) + "] Worklog [" + str(worklog.id) + "] with date " + str(
                                    _started) + " will be added to EFFORT REMAINING because date limit is " + str(
                                    self.date_limit))
                            _effort_spent_in_future_sec = _effort_spent_in_future_sec + worklog.timeSpentSeconds
                        elif self.date_limit is None:
                            log.debug(
                                "Issue [" + str(issue.key) + "] Worklog [" + str(worklog.id) + "] with date " + str(
                                    _started) + " will be counted because date limit hasn't been provided")
                            _effort_actual_md = _effort_actual_md + worklog.timeSpentSeconds

                    # Get issue's timespent in seconds and add it to the overall sum
                            # if issue.fields.timespent is not None:
                            #     _effort_actual_md = _effort_actual_md + issue.fields.timespent

                log.debug("Time spent so far is     : " + str(("%.2f" % ((_effort_actual_md / 3600) / 8))))

            # Switch timespent to md and round it off to 2 digits
            _effort_actual_md = "%.2f" % ((_effort_actual_md / 3600) / 8)

            log.info("Effort (Actual)               : " + str("%.2f" % float(_effort_actual_md)) + " md")

            #############################################
            # ESTIMATE TO COMPLETE
            #############################################


            _effort_remaining_md = 0.0  #
            if float(_effort_actual_md) > float(self.baseline_md) and self.estimate_to_complete is None:
                die("Time spent " + str(
                    _effort_actual_md) + " md is higher than the baseline " + self.baseline_md + " md so an estimate to complete calculation cannot take place, please use -e switch to provide a manual E.t.C.")
            elif self.estimate_to_complete is None:
                _effort_remaining_md = _effort_remaining_md + (float(self.baseline_md) - float(_effort_actual_md))
            else:
                # _effort_remaining_md = ((_effort_spent_in_future_sec / 3600) / 8) + float(self.estimate_to_complete)
                _effort_remaining_md = float(self.estimate_to_complete)

            log.info("Effort (Remaining)            : " + str("%.2f" % float(_effort_remaining_md)) + " md")

            if _effort_spent_in_future_sec > 0.0:
                log.warn("(Effort remaining doesn't contain time spent in the future: " + "%.2f" % (
                (_effort_spent_in_future_sec / 3600) / 8) + " md)")

            #############################################
            # EFFORT AT COMPLETION
            #############################################

            # Calculate Estimate At Completion
            _effort_at_completion_md = float(_effort_actual_md) + float(_effort_remaining_md)

            log.info("Effort (At Completion)        : " + str("%.2f" % float(_effort_at_completion_md)) + " md")

            #############################################
            # ON TIME
            #############################################
            _a = self.go_live_actual - self.kick_off_date
            _b = self.go_live_baseline - self.kick_off_date

            # On Time
            _on_time = (_a.total_seconds() / _b.total_seconds())



            #############################################
            # IN EFFORT
            #############################################

            # In Effort
            _in_effort = _effort_at_completion_md / float(self.baseline_md)




            #############################################
            # BUDGET
            #############################################
            log.info("Revenue                       : " + str(self.revenue_offer) + self.euro_sign_encoded)
            log.info("md Rate (Offer)               : " + str(self.md_rate_offer) + self.euro_sign_encoded)
            log.info("md Rate (Internal)            : " + str(self.md_rate_internal) + self.euro_sign_encoded)

            _md_cost_baseline = float(self.md_rate_internal) * float(self.baseline_md)
            log.info("md Cost (Baseline)            : " + str(_md_cost_baseline) + self.euro_sign_encoded)

            _md_cost_eac = float(self.md_rate_internal) * float(_effort_at_completion_md)
            log.info("md Cost (At Completion)       : " + str(_md_cost_eac) + self.euro_sign_encoded)
            log.info("Other Costs (Baseline)        : " + str(self.other_costs_baseline) + self.euro_sign_encoded)
            log.info("Other Costs (Actual)          : " + str(self.other_costs_actual) + self.euro_sign_encoded)

            _pnl_baseline = ((float(self.revenue_offer) - float(_md_cost_baseline) - float(
                self.other_costs_baseline)) / float(self.revenue_offer)) * 100
            log.info("PnL (Baseline)                : " + str("%.2f" % _pnl_baseline) + "%")

            _pnl_eac = ((float(self.revenue_offer) - float(_md_cost_eac) - float(self.other_costs_actual)) / float(
                self.revenue_offer)) * 100
            log.info("PnL (At Completion)           : " + str("%.2f" % _pnl_eac) + "%")



            #############################################
            # IN BUDGET
            #############################################
            _in_budget = 1 + (float(_pnl_baseline / 100) - float(_pnl_eac / 100))

            log.info("--------------------------------------------------------")
            log.info("On Time                       : " + str("%.2f" % _on_time))
            log.info("In Effort                     : " + str("%.2f" % _in_effort))
            log.info("In Budget                     : " + str("%.2f" % _in_budget))
            log.info("--------------------------------------------------------")


            html_code = self.export_to_html(self.project_name,
                                            self.kick_off_date.strftime(self.date_format),
                                            self.uat_start_baseline.strftime(self.date_format),
                                            self.uat_start_actual.strftime(self.date_format),
                                            self.go_live_baseline.strftime(self.date_format),
                                            self.go_live_actual.strftime(self.date_format),
                                            "%.2f" % _on_time,
                                            self.baseline_md,
                                            _effort_actual_md,
                                            _effort_remaining_md,
                                            _effort_at_completion_md,
                                            "%.2f" % _in_effort,
                                            str(self.revenue_offer) + self.euro,
                                            str(self.md_rate_offer) + self.euro,
                                            str(self.md_rate_internal) + self.euro,
                                            str(_md_cost_baseline) + self.euro,
                                            str(_md_cost_eac) + self.euro,
                                            str(self.other_costs_baseline) + self.euro,
                                            str(self.other_costs_actual) + self.euro,
                                            str("%.2f" % _pnl_baseline) + "%",
                                            str("%.2f" % _pnl_eac) + "%",
                                            str("%.2f" % _in_budget),
                                            str(" ".join(sys.argv)))


            # Output in either location
            if self.date_limit is not None:
                with open(self.output_location_datelimit, "w") as text_file:
                    text_file.write(html_code)
                    log.debug("Output added to " + self.output_location_datelimit)
            else:
                with open(self.output_location_latest, "w") as text_file:
                    text_file.write(html_code)
                    log.debug("Output added to " + self.output_location_latest)


        except:
            raise
