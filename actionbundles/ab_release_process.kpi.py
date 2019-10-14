from util.toolkit import log, jira_authenticate, merge_dicts_adding_values
from actionbundles.action_bundle import ActionBundle
from util.jira_toolkit import run_jql, get_time_between_statuses, get_time_between_extreme_statuses, \
    print_issue_changelog, count_status_after_status, count_transitions, get_time_between_transition_status, \
    filter_versions, get_older_versions_csv, get_version, get_time_between_transitions_after_milestone_transition, \
    get_time_between_possible_transitions_after_milestone_transition, count_reopen_reasons
from dateutil.parser import *
import datetime, time
import csv
import ipdb
from enum import Enum

class JiraIssueType(Enum):
    RELEASE = 4


class ABReleaseProcessKpi(ActionBundle):
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

            release_key = parser.options.release_key


            jira = jira_authenticate(parser.options.jira_url, parser.options.jira_username, parser.options.jira_password)

            # JQL Queries that will be executed
            jql_lst = [
                {
                    "jql": '"issuekey" = "{}" AND issuetype = "Release" AND status IN ("Closed")'.format(release_key),
                    "issuetype": JiraIssueType.RELEASE,
                    "details": "release_ticket_with_key_{0}".format(release_key),
                },

            ]

            # Initial csv row offset
            row_offset = 3

            for jql_dict in jql_lst:

                csv_filename = jql_dict['details'] + ".csv"
                log.debug("CSV Filename: {}".format(csv_filename))

                # Open CSV in write mode
                with open(csv_filename, 'wb') as file:
                    csv_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

                    log.debug("--------------------------------------------------------------------------------------------")
                    jql_exec = run_jql(jira, jql_dict['jql'], False, True)
                    log.debug("--------------------------------------------------------------------------------------------")

                    # Skip execution for this JQL if it's empty
                    if len(jql_exec) == 0:
                        log.warn("No results for query '{}'. {} file will be empty.".format(jql_dict['jql'], csv_filename))
                        continue

                    # Write JQL
                    csv_file.writerow([jql_dict['jql']])
                    csv_file.writerow([""])

                    # Write CSV Header
                    csv_file.writerow([
                        'Issue_Key',
                        'Issue_Type',
                        'Issue_Summary',
                        # 'Affected_Version(s)'
                        # 'Fix_Version(s)'
                        'Story_Points',
                        'Reopened_Times_by_QA (QA->REOPENED)',
                        'Reopened_Times_after_QA_signoff (DONE->REOPENED)',
                        'Reopened_Times_by_U1AT (UAT->REOPENED)',
                        'Reopened_Times_after_CLOSED (CLOSED->REOPENED)',
                        'Lead_Time (OPEN->CLOSED)',
                        'Dev QA Cycle Time (IN PROGRESS->DONE)',
                        'Initial_Specs_Time (OPEN->IN PROGRESS)',
                        'Initial_Development_Time (IN PROGRESS->DEV OK)',
                        'Initial_Dev_End_To_QA_Start_Time (DEV OK->QA)',
                        'Initial_QA_Time (QA->REOPEN or DONE)',
                        'Lost_Dev_Time_after_Initial_QA_Reopen (Total time between REOPENED->IN PROGRESS and DEMO OK->DEV OK)',
                        'Lost_QA_Time_after_Initial_QA_Reopen (Total time between DEV OK->QA and QA->DONE or QA->REOPENED)',
                        'Lost_Lag_Time_after_Initial_QA_Reopen (Time lag time between Development and QA processes)',
                        'Initial_QA_End_To_UAT_Start_Time (DONE->UAT)',
                        'Initial_UAT_Time (UAT->REOPEN or CLOSED)',
                    ])

                    skipped_issues_count = 0
                    overall_reopen_reasons = {}

                    for issue in jql_exec:
                        log.debug("{} | {} | {}".format(issue, issue.fields.issuetype.name.encode('ascii'), issue.fields.summary))

                        i = jira.issue(issue.key, expand='changelog')
                        changelog = i.changelog

                        # print_issue_changelog(changelog)
                        # print_issue_changelog2(changelog, i)

                        # ipdb.set_trace()

                        # Reopen Reasons
                        reopen_reasons = count_reopen_reasons(changelog)
                        overall_reopen_reasons = merge_dicts_adding_values(reopen_reasons, overall_reopen_reasons)

                        # Times Reopened by QA
                        times_reopened_qa = count_transitions("QA", "Reopened", changelog)

                        # Times Reopened by UAT
                        times_reopened_after_qa_signoff = count_transitions("Done", "Reopened", changelog)

                        # Times Reopened after QA OK
                        times_reopened_uat = count_transitions("UAT", "Reopened", changelog)

                        # Times Reopened after CLOSED
                        times_reopened_after_closed = count_transitions("Closed", "Reopened", changelog)

                        # Lead Time
                        lead_time = get_time_between_extreme_statuses("Open", "Closed", changelog)

                        # Dev/QA Cycle Time
                        dev_qa_cycle_time = get_time_between_extreme_statuses("In Progress", "Done", changelog)

                        # Initial Specs Time
                        specs_time_lst = get_time_between_statuses("Open", "In Progress", changelog)
                        initial_specs_time = specs_time_lst[0] if specs_time_lst != [] else 0

                        # Initial Development Time
                        dev_time_lst = get_time_between_statuses("In Progress", "Dev OK", changelog)
                        initial_dev_time = dev_time_lst[0] if dev_time_lst != [] else 0

                        # Development End to QA Start Time
                        dev_end_qa_start_time_lst = get_time_between_statuses("Dev OK", "QA", changelog)
                        dev_end_qa_start_time = dev_end_qa_start_time_lst[0] if dev_end_qa_start_time_lst != [] else 0

                        # Initial QA Time and Lost time after reopen calculations
                        lost_dev_time_after_reopen = 0
                        lost_qa_time_after_reopen = 0
                        lost_lag_time_after_reopen = 0
                        if times_reopened_qa > 0:
                            initial_qa_time_lst = get_time_between_statuses("QA", "Reopened", changelog)
                            lost_dev_time_after_reopen = get_time_between_transitions_after_milestone_transition("QA", "Reopened", "Reopened", "In Progress", "Demo OK", "Dev OK", changelog)
                            lost_qa_time_after_reopen = get_time_between_possible_transitions_after_milestone_transition("QA", "Reopened", "Dev OK", "QA", "QA", "Reopened", "Done", changelog)
                            lost_lag_time_after_reopen = abs(get_time_between_transition_status("QA", "Reopened", "Done", changelog) - (lost_dev_time_after_reopen + lost_qa_time_after_reopen))
                        else:
                            initial_qa_time_lst = get_time_between_statuses("QA", "Done", changelog)

                        initial_qa_time = initial_qa_time_lst[0] if initial_qa_time_lst != [] else 0

                        # QA End to UAT Start Time
                        qa_signoff_to_uat_start_time_lst = get_time_between_statuses("Done", "UAT", changelog)
                        qa_signoff_to_uat_start_time = qa_signoff_to_uat_start_time_lst[0] if qa_signoff_to_uat_start_time_lst != [] else 0

                        # Initial UAT Time
                        if times_reopened_uat > 0:
                            initial_uat_time_lst = get_time_between_statuses("UAT", "Reopened", changelog)
                        else:
                            initial_uat_time_lst = get_time_between_statuses("UAT", "Closed", changelog)
                        initial_uat_time = initial_uat_time_lst[0] if initial_uat_time_lst != [] else 0


                        # Write CSV row for every issue
                        csv_file.writerow([
                            issue,
                            issue.fields.issuetype.name.encode('ascii'),
                            issue.fields.summary.replace('"', "'"),
                            # issue.fields.versions,
                            # issue.fields.fixVersions,
                            eval("issue.fields.{}".format(story_points_cf)),
                            times_reopened_qa,
                            times_reopened_after_qa_signoff,
                            times_reopened_uat,
                            times_reopened_after_closed,
                            lead_time,
                            dev_qa_cycle_time,
                            initial_specs_time,
                            initial_dev_time,
                            dev_end_qa_start_time,
                            initial_qa_time,
                            lost_dev_time_after_reopen,
                            lost_qa_time_after_reopen,
                            lost_lag_time_after_reopen,
                            qa_signoff_to_uat_start_time,
                            initial_uat_time,
                        ])

                    csv_file.writerow([""])
                    csv_file.writerow([""])

                    row_actual_total = len(jql_exec) - skipped_issues_count

                    # CSV Row: SUM
                    csv_file.writerow([
                        "",
                        "SUM",
                        "",
                        "=SUM(D{}:D{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(E{}:E{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(F{}:F{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(G{}:G{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(H{}:H{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(I{}:I{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(J{}:J{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(K{}:K{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(L{}:L{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(M{}:M{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(N{}:N{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(O{}:O{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(P{}:P{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(Q{}:Q{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(R{}:R{})".format(row_offset, row_actual_total + row_offset),
                        "=SUM(S{}:S{})".format(row_offset, row_actual_total + row_offset),

                    ])

                    # CSV Row: AVG
                    csv_file.writerow([
                        "",
                        "AVG",
                        "",
                        "=AVERAGE(D{}:D{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(E{}:E{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(F{}:F{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(G{}:G{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(H{}:H{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(I{}:I{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(J{}:J{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(K{}:K{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(L{}:L{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(M{}:M{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(N{}:N{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(O{}:O{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(P{}:P{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(Q{}:Q{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(R{}:R{})".format(row_offset, row_actual_total + row_offset),
                        "=AVERAGE(S{}:S{})".format(row_offset, row_actual_total + row_offset),
                    ])

                    # CSV Row: MAX
                    csv_file.writerow([
                        "",
                        "MAX",
                        "",
                        "=MAX(D{}:D{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(E{}:E{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(F{}:F{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(G{}:G{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(H{}:H{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(I{}:I{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(J{}:J{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(K{}:K{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(L{}:L{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(M{}:M{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(N{}:N{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(O{}:O{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(P{}:P{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(Q{}:Q{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(R{}:R{})".format(row_offset, row_actual_total + row_offset),
                        "=MAX(S{}:S{})".format(row_offset, row_actual_total + row_offset),
                    ])

                    # CSV Row: MIN
                    csv_file.writerow([
                        "",
                        "MIN",
                        "",
                        "=MIN(D{}:D{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(E{}:E{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(F{}:F{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(G{}:G{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(H{}:H{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(I{}:I{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(J{}:J{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(K{}:K{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(L{}:L{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(M{}:M{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(N{}:N{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(O{}:O{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(P{}:P{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(Q{}:Q{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(R{}:R{})".format(row_offset, row_actual_total + row_offset),
                        "=MIN(S{}:S{})".format(row_offset, row_actual_total + row_offset),
                    ])

                    csv_file.writerow([""])


                    # CSV Row: Reopen Rate
                    csv_file.writerow([
                        "",
                        "Reopen Rate %",
                        "",
                        "",
                        "=ROUND(ABS((SUM(E{}:E{})*100)/{}),2)".format(row_offset, row_actual_total + row_offset, len(jql_exec)),
                        "=ROUND(ABS((SUM(F{}:F{})*100)/{}),2)".format(row_offset, row_actual_total + row_offset, len(jql_exec)),
                        "=ROUND(ABS((SUM(G{}:G{})*100)/{}),2)".format(row_offset, row_actual_total + row_offset, len(jql_exec)),
                        "=ROUND(ABS((SUM(H{}:H{})*100)/{}),2)".format(row_offset, row_actual_total + row_offset, len(jql_exec)),
                        "",
                        "Total Reopen Rate %",
                        "",
                        "",
                        "=SUM(INDIRECT(ADDRESS(ROW(),5)):INDIRECT(ADDRESS(ROW(),8)))",
                    ])

                    csv_file.writerow([""])

                    # Reopen Reasons
                    if bool(overall_reopen_reasons):
                        csv_file.writerow(["", "Reopen Reasons"])


                    for rr in overall_reopen_reasons:
                        csv_file.writerow([
                            "",
                            rr,
                            "",
                            "",
                            overall_reopen_reasons[rr],
                        ])


                    csv_file.writerow([""])


            # Open CSV in write mode
            with open("report_epic_metrics_for_{}.csv".format(release_key), 'wb') as file:
                csv_file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

                csv_file.writerow(["Epic",
                                   "",
                                   "",
                                   release_key,
                                   ])

                csv_file.writerow([""])

                csv_file.writerow(["User Stories"])
                csv_file.writerow(["--------------------------------------------"])
                csv_file.writerow([""])


                # Stories Completed
                jql = '"Epic Link" = "{}" AND issuetype = "Story" AND resolution IN ("Done", EMPTY) AND status = "Closed"'.format(release_key)
                number_of_stories_completed_in_release = len(run_jql(jira, jql))

                csv_file.writerow([
                    "Stories Completed",
                    "",
                    "",
                    number_of_stories_completed_in_release,
                    "",
                    "JQL: ",
                    "",
                    jql,
                ])

                # Total Story Points
                csv_file.writerow([
                    "Total Story Points",
                    "",
                    "",
                    "='{}'!$D${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                ])


                # Story Reopen Rate
                csv_file.writerow([
                    "Story Reopen Rate %",
                    "",
                    "",
                    "='{}'!$M${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 8),
                ])

                # Avg Lead Time
                csv_file.writerow([
                    "Average Lead Time",
                    "",
                    "",
                    "='{}'!$I${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 4),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Dev QA Cycle Time
                csv_file.writerow([
                    "Dev QA Cycle Time",
                    "",
                    "",
                    "='{}'!$J${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Avg Time per Story Point
                csv_file.writerow([
                    "Avg Time per Story Point",
                    "",
                    "",
                    "='{0}'!$J${1}/'{0}'!$D${1}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Total Specs Time
                csv_file.writerow([
                    "Total Specs Time (initial)",
                    "",
                    "",
                    "='{}'!$K${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Avg Specs Time
                csv_file.writerow([
                    "Average Specs Time (initial)",
                    "",
                    "",
                    "='{}'!$K${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 4),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Total Development Time
                csv_file.writerow([
                    "Total Development Time (initial)",
                    "",
                    "",
                    "='{}'!$L${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Avg Development Time
                csv_file.writerow([
                    "Average Development Time (initial)",
                    "",
                    "",
                    "='{}'!$L${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 4),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Total QA Time
                csv_file.writerow([
                    "Total QA Time (initial)",
                    "",
                    "",
                    "='{}'!$N${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Avg QA Time
                csv_file.writerow([
                    "Average QA Time (initial)",
                    "",
                    "",
                    "='{}'!$N${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 4),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Total Lost Development Time
                csv_file.writerow([
                    "Total Lost Development Time",
                    "",
                    "",
                    "='{}'!$O${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Total Lost QA Time
                csv_file.writerow([
                    "Total Lost QA Time",
                    "",
                    "",
                    "='{}'!$P${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Total Lost Lag Time
                csv_file.writerow([
                    "Total Lost Lag Time",
                    "",
                    "",
                    "='{}'!$Q${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Total UAT Time
                csv_file.writerow([
                    "Total UAT Time (initial)",
                    "",
                    "",
                    "='{}'!$S${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Avg UAT Time
                csv_file.writerow([
                    "Average UAT Time (initial)",
                    "",
                    "",
                    "='{}'!$S${}".format(jql_lst[0]['details'] + ".csv", len(run_jql(jira, jql_lst[0]['jql']))+ row_offset + 4),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])


                csv_file.writerow([""])
                csv_file.writerow([""])
                csv_file.writerow(["Development Tasks"])
                csv_file.writerow(["--------------------------------------------"])
                csv_file.writerow([""])

                # Development Tasks Completed
                jql = '"Epic Link" = "{}" AND issuetype = "Development Task" AND resolution IN ("Done", EMPTY) AND status = "Closed"'.format(release_key)
                number_of_devtasks_fixed_in_release = len(run_jql(jira, jql))

                csv_file.writerow([
                    "Dev Tasks Completed",
                    "",
                    "",
                    number_of_devtasks_fixed_in_release,
                    "",
                    "JQL: ",
                    "",
                    jql,
                ])

                # Total Story Points
                csv_file.writerow([
                    "Total Story Points",
                    "",
                    "",
                    "='{}'!$D${}".format(jql_lst[1]['details'] + ".csv", len(run_jql(jira, jql_lst[1]['jql']))+ row_offset + 3),
                ])

                # Bug Reopen Rate
                csv_file.writerow([
                    "Dev Task Reopen Rate %",
                    "",
                    "",
                    "='{}'!$M${}".format(jql_lst[1]['details'] + ".csv", len(run_jql(jira, jql_lst[1]['jql']))+ row_offset + 8),
                ])

                # Dev QA Cycle Time
                csv_file.writerow([
                    "Dev QA Cycle Time",
                    "",
                    "",
                    "='{}'!$J${}".format(jql_lst[1]['details'] + ".csv", len(run_jql(jira, jql_lst[1]['jql']))+ row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])

                # Avg Time per Story Point
                csv_file.writerow([
                    "Avg Time per Story Point",
                    "",
                    "",
                    "='{0}'!$J${1}/'{0}'!$D${1}".format(jql_lst[1]['details'] + ".csv", len(run_jql(jira, jql_lst[1]['jql'])) + row_offset + 3),
                    '=INT(INDIRECT(ADDRESS(ROW(),4))/86400)&" days "&TEXT(INDIRECT(ADDRESS(ROW(),4))/86400,"hh:mm:ss")',
                ])



        except:
            raise
