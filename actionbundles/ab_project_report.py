import ast
import datetime

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
                       in_effort):
        """

        :rtype : HTML
        """
        return '''
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
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
                    <div class="col-lg-12">
                        <h1 class="page-header">
                            {0}
                        </h1>
                    </div>
                </div>
                <!-- /.row -->
                <!-- /.row -->
                <div class="row">
                       <div class="col-lg-4 col-md-6">
                           <div class="panel panel-primary">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-hourglass-1 fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{1}</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">Kick Off</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-primary">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-users fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{2}</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">UAT Start (Baseline)</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6">
                        <div class="panel panel-primary">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-users fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{3}</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">UAT Start (Actual)</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                </div>

                <!-- /.row -->
                 <!-- /.row -->
                <div class="row">
                                        <div class="col-lg-4 col-md-6">
                       <div class="panel panel-primary">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-hourglass-3 fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{4}</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">GoLive (Baseline)</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6">
                        <div class="panel panel-primary">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-hourglass-3 fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{5}</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">GoLive (Actual)</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>


                    <div class="col-lg-4 col-md-6">
                        <div class="panel panel-green">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-clock-o fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="huge">{6}</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">OnTime</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                </div>
                <!-- /.row -->
                 <div class="row">
                    <div class="progress">
                        <div class="progress-bar progress-bar-danger" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%;">
                    </div>
                </div>
                <!-- /.row -->
                <div class="row">

                    <div class="col-lg-6 col-md-6">
                       <div class="panel panel-yellow">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-briefcase fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{7} md</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">Effort (Baseline)</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-6">
                        <div class="panel panel-yellow">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-bomb fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{8} md</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">Effort (Actual)</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>

                </div>

                <!-- /.row -->
                 <!-- /.row -->
                <div class="row">

                    <div class="col-lg-4 col-md-6">
                       <div class="panel panel-yellow">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-thumbs-up fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{9} md</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">Effort (Remaining)</span>
                                    <div class="clearfix"></div>
                                </div>
                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6">
                        <div class="panel panel-yellow">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-code fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="largeF">{10} md</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">Effort (At Completion)</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                    <div class="col-lg-4 col-md-6">
                        <div class="panel panel-green">
                            <div class="panel-heading">
                                <div class="row">
                                    <div class="col-xs-3">
                                        <i class="fa fa-clock-o fa-3x"></i>
                                    </div>
                                    <div class="col-xs-9 text-right">
                                        <div class="huge">{11}</div>
                                    </div>
                                </div>
                            </div>
                                <div class="panel-footer">
                                    <span class="pull-left largeF">inEffort</span>
                                    <div class="clearfix"></div>
                                </div>

                        </div>
                    </div>
                </div>
                <!-- /.row -->


            </div>
            <!-- /.container-fluid -->

        </div>
        <!-- /#page-wrapper -->


    <!-- /#wrapper -->

    <!-- jQuery -->
    <script src="js/jquery.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

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
               str(in_effort))

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
            self.output_location = read_property_from_file("output_location", "project", self.input_file)

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

            html_code = self.export_to_html(self.project_name,
                                            self.kick_off_date,
                                            self.uat_start_baseline,
                                            self.uat_start_actual,
                                            self.go_live_baseline,
                                            self.go_live_actual,
                                            _ot,
                                            self.baseline_md,
                                            _t,
                                            _etc,
                                            _eac,
                                            _ie, )

            with open(self.output_location, "w") as text_file:
                text_file.write(html_code)

        except:
            raise
