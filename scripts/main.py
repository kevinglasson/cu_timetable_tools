#!/usr/bin/env python

import requests
import requests.packages.urllib3
import getpass
import pandas as pd
from CurtinUnit import CurtinUnit
from CUeStudentSession import CUeStudentSession, LoginFailedError


def print_units(unit_list):
    for key, value in unit_list.iteritems():
        print "------------------------------------------------------------------\n"
        value.to_string()


def print_timetable(timetable):
    for dict_ in timetable:
        for key, value in dict_.iteritems():
            print "------------------------------------------------------------------\n"
            # value.to_string()
            print(value.class_list[0].date)


def get_timetable(studentid, password):
    session = CUeStudentSession()
    session.login(studentid, password)
    return session.get_timetable()


def get_all_timetables(studentid, password):
    session = CUeStudentSession()
    session.login(studentid, password)
    return session.get_all_timetables()


def main():
    # Just for me so I don't have to see warning about my python being old!
    requests.packages.urllib3.disable_warnings()

    username = raw_input("USERNAME: ")
    password = getpass.getpass("PASSWORD: ")

    try:
        # This should be a list of CurtinUnit objects
        timetable = get_all_timetables(username, password)
        print_timetable(timetable)
    except LoginFailedError:
        print('{"error":"Login failed. Wrong username or password?"}')


if __name__ == '__main__':
    main()
