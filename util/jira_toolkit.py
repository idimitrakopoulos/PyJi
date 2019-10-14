#!/usr/bin/env python
from jira import JIRA
import ipdb
from dateutil.parser import *
import datetime
from util.toolkit import log, calc_working_seconds


class Issue(object):
    """__init__() functions as the class constructor"""
    def __init__(self, key=None, lead_time=None):
        self.key = key
        self.lead_time = lead_time


def run_jql(jira, jql, max=False, debug=False):
    if debug:
        log.debug("JQL -> {}".format(jql))
    return jira.search_issues(jql, maxResults=max)


def count_status(status_name, changelog):
    count = 0
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.toString == status_name:
                count += 1
    return count

def count_status_after_status(status_name, status_to_count_from, changelog):
    count = 0
    start_count=False
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.toString == status_name and start_count:
                count += 1
            elif item.toString == status_to_count_from and not start_count:
                start_count = True
    return count


def count_transitions(status_from, status_to, changelog):
    count = 0
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.fromString == status_from and item.toString == status_to:
                count += 1
    return count


def count_reopen_reasons(changelog):
    result = {}
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.field == 'Reopen Reason':
                reasons = [(x.strip()).encode("ascii") for x in item.toString.split(',')]
                for r in reasons:
                    if r in result and r is not "":
                        result[r] += 1
                        # log.debug("Reopened {} times due to '{}' (Total Reopens: {})".format(str(result[r]), r, sum(result.values())))
                    elif r not in result and r is not "":
                        result[r] = 1
                        # log.debug("Reopened 1 time due to '{}' (Total Reopens: {})".format(r, sum(result.values())))


    return result


def get_time_between_transitions(from_status_a, to_status_a, from_status_b, to_status_b, changelog):
    in_flag = False
    transition_a_date = None
    transition_b_date = None
    result = None
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.fromString == from_status_a and item.toString == to_status_a and not in_flag:
                in_flag = True
                transition_a_date = parse(history.created)
            elif item.fromString == from_status_b and item.toString == to_status_b and in_flag:
                transition_b_date = parse(history.created)
                result = calc_working_seconds(transition_a_date, transition_b_date)
                # log.debug("{}->{} ...... {}->{} = {} sec ({})".format(from_status_a, to_status_a, from_status_b, to_status_b, result, datetime.timedelta(seconds=result)))

    return result


def get_time_between_transition_status(from_status_a, to_status_a, to_status_b, changelog):
    in_flag = False
    transition_a_date = None
    transition_b_date = None
    result = 0
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.fromString == from_status_a and item.toString == to_status_a and not in_flag:
                in_flag = True
                transition_a_date = parse(history.created)
            elif item.toString == to_status_b and in_flag:
                transition_b_date = parse(history.created)
                result = calc_working_seconds(transition_a_date, transition_b_date)
                # log.debug("{}->{} ...... {} = {} sec ({})".format(from_status_a, to_status_a, to_status_b, result, datetime.timedelta(seconds=result)))


    return result


def get_time_between_transitions_after_milestone_transition(from_milestone_status, to_milestone_status, from_status_a, to_status_a, from_status_b, to_status_b, changelog):
    in_flag = False
    in_milestone = False
    transition_a_date = None
    transition_b_date = None
    result = 0
    # log.debug("Looking for occurrences of {}->{} up to {}->{} after the first {}->{} transition".format(from_status_a, to_status_a, from_status_b, to_status_b, from_milestone_status, to_milestone_status))
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.fromString == from_milestone_status and item.toString == to_milestone_status and not in_milestone:
                in_milestone = True
                # log.debug("Milestone status {}->{} found on {}.".format(from_milestone_status, to_milestone_status,history.created))

                # After the milestone is found proceed finding the rest of the occurences
            if item.fromString == from_status_a and item.toString == to_status_a and not in_flag and in_milestone:
                # log.debug("1st Transition {}->{} found on {}.".format(from_status_a, to_status_a, history.created))
                in_flag = True
                transition_a_date = parse(history.created)
            elif item.fromString == from_status_b and item.toString == to_status_b and in_flag and in_milestone:
                # log.debug("2nd Transition {}->{} found on {}.".format(from_status_b, to_status_b, history.created))
                in_flag = False
                transition_b_date = parse(history.created)
                result = result + calc_working_seconds(transition_a_date, transition_b_date)

    # log.debug("{}->{} ...... {}->{} = {} sec ({})".format(from_status_a, to_status_a, from_status_b, to_status_b, result, datetime.timedelta(seconds=result)))

    return result


def get_time_between_possible_transitions_after_milestone_transition(from_milestone_status, to_milestone_status, from_status_a, to_status_a, from_status_b, to_status_b1, to_status_b2, changelog):
    in_flag = False
    in_milestone = False
    transition_a_date = None
    transition_b_date = None
    result = 0
    # log.debug("Looking for occurrences of {0}->{1} up to {2}->{3} or {2}->{4} after the first {5}->{6} transition".format(from_status_a, to_status_a, from_status_b, to_status_b1, to_status_b2, from_milestone_status, to_milestone_status))
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.fromString == from_milestone_status and item.toString == to_milestone_status and not in_milestone:
                in_milestone = True
                # log.debug("Milestone status {}->{} found on {}.".format(from_milestone_status, to_milestone_status, history.created))

            # After the milestone is found proceed finding the rest of the occurences
            if item.fromString == from_status_a and item.toString == to_status_a and not in_flag and in_milestone:
                # log.debug("1st Transition {}->{} found on {}.".format(from_status_a, to_status_a, history.created))
                in_flag = True
                transition_a_date = parse(history.created)
            elif item.fromString == from_status_b and (item.toString == to_status_b1 or item.toString == to_status_b2) and in_flag and in_milestone:
                # log.debug("2nd Transition {}->{} found on {}.".format(from_status_b, item.toString, history.created))
                in_flag = False
                transition_b_date = parse(history.created)
                result += calc_working_seconds(transition_a_date, transition_b_date)
                # log.debug("{0}->{1} ...... {2}->{3} = {4} sec ({5})".format(from_status_a, to_status_a, from_status_b, item.toString, result, datetime.timedelta(seconds=result)))

    return result


def get_time_between_statuses(from_status, to_status, changelog):
    in_flag = False
    in_time = ""
    result = []

    # log.debug("Getting time between {} -> {}".format(from_status, to_status))

    for history in reversed(changelog.histories):
        for item in history.items:
            if item.field == 'status':
                if item.toString == from_status and not in_flag:
                    in_flag = True
                    in_time = parse(history.created)
                    # log.debug("Found  " + item.toString + " on  " + history.created)
                elif item.toString == to_status and in_flag:
                    in_flag = False
                    out_time = parse(history.created)
                    # log.debug("Found  " + item.toString + " on  " + history.created)
                    result.append(calc_working_seconds(in_time, out_time))

                    # log.debug("get_time_between_statuses {} -> {} = {} sec (working: {} actual: {})".format(from_status, to_status, result[len(result)-1], datetime.timedelta(seconds=result[len(result)-1]), str(out_time-in_time)))

    return result



def get_time_between_extreme_statuses(from_status, to_status, changelog):
    in_flag = False
    in_time = ""
    result = 0

    # log.debug("Getting time between first occurence of {} -> last occurence of {}".format(from_status, to_status))

    for history in reversed(changelog.histories):
        for item in history.items:
            if item.field == 'status':
                if from_status == "Open" and not in_flag:
                    in_flag = True
                    in_time = parse(history.created)
                elif item.toString == from_status and not in_flag:
                    in_flag = True
                    in_time = parse(history.created)
                elif item.toString == to_status and in_flag:
                    out_time = parse(history.created)
                    result = calc_working_seconds(in_time, out_time)

    # log.debug("{} -> {} = {} sec (working: {} actual: {})".format(from_status, to_status, result, datetime.timedelta(seconds=result), str(out_time - in_time)))

    return result




def print_issue_changelog(changelog):
    keep_date = None
    diff = None
    log.debug(">>> Issue History_____________________________________________________________")
    for history in reversed(changelog.histories):
        for item in history.items:
            if item.field == 'status':
                if keep_date != None:
                    diff = parse(history.created) - keep_date
                log.debug(item.fromString + ' -> ' + item.toString + " (Transition took: " + str(diff) + " on " + str(history.created) + ")")

                keep_date = parse(history.created)
                diff = None
    log.debug("<<< _________________________________________________________________________")

# def print_issue_changelog2(changelog, issue):
#     keep_date = None
#     diff = None
#     for history in reversed(changelog.histories):
#         for item in history.items:
#             if item.field == 'status':
#                 if keep_date != None:
#                     diff = parse(history.created) - keep_date
#                 print (str(issue) + ', ' + str(issue.fields.issuetype) + ', ' + str(issue.fields.customfield_10039) + ', ' + item.fromString + ', ' + item.toString + ', ' + history.created)
#
#                 keep_date = parse(history.created)
#                 diff = None

def filter_versions(versions, starts_with):
    result = []

    for v in versions:
        if v.name.startswith(starts_with):
            result.append(v)

    return result


def get_older_versions_csv(versions, new_version):
    result = ""

    for v in versions:
        if str(v.name).encode("ascii") != new_version:
            result = result + '"' + str(v.name).encode("ascii") + '",'
        result = result[:-1]

    return result


def get_version(versions, version_name):
    result = None
    log.debug(version_name)
    for v in versions:
        if v.name == version_name:
            result = v
            break

    return result