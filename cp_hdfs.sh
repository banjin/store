#!/bin/bash

# sudo su
# su - hdfs

for sub_dir in `ls /home/qsadmin/panadit`
do
    count=0
    for ${hdfs_sub_dir} in `hadoop fs -ls /panadit | ask { print $NF }`
    do
        if (${sub_dir} eq ${hdfs_sub_dir})
        then
             ((count++))
    done
    if [count -ne 0]
    then
        `hadoop fs mkdir /panadit/${sub_dir}`
    fi

    for sub_file in `ls /home/qsadmin/panadit/${sub_dir}`
    do
        if ${sub_file} not in `hadoop fs -ls /panadit/${sub_dir} | ask { print $NF }`
        then
            hadoop fs -put /home/qsadmin/panadit/${sub_dir}/${sub_file} /panadit/${sub_dir}/${sub_file}
        fi
    done
done
