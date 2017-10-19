#!/usr/bin/python
# coding:utf-8

import os
import sys
import commands
import os
# TEMP_BASE_DIR = "/home/qsadmin/panadit"
TEMP_BASE_DIR = "/data"


def cp_to_hdfs():

    (status, output) = commands.getstatusoutput('sudo su')
    if not status:
        pass
    (status, output) = commands.getstatusoutput('su - hdfs')
    if not status:
        pass
    all_sub_dir = os.listdir(TEMP_BASE_DIR)
    for sub_dir in all_sub_dir:
        # if sub_dir in commands.getoutput("hadoop fs -ls /panadit | ask { print $NF }"):
            pass
    print all_sub_dir

if __name__ == "__main__":
    cp_to_hdfs()
