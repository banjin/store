hdfs dfs -rm /hadoop/qsdata/ipdevicemap/ipdevicemap.json
hdfs dfs -rm /hadoop/qsdata/ipdevicemipcitymapap/ipcitymap.json

hdfs dfs -mkdir /hadoop/qsdata/ids20161129/
hdfs dfs -put ids.json /hadoop/qsdata/ids20161129/ids.json
hdfs dfs -mkdir /hadoop/qsdata/flow20161129/
hdfs dfs -put flow.json /hadoop/qsdata/flow20161129/flow.json
hdfs dfs -mkdir /hadoop/qsdata/ipdevicemap/
hdfs dfs -put ipdevicemap.json /hadoop/qsdata/ipdevicemap/ipdevicemap.json
hdfs dfs -mkdir /hadoop/qsdata/ipcitymap
hdfs dfs -put ipcitymap.json /hadoop/qsdata/ipcitymap/ipcitymap.json