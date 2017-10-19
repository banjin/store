# coding:utf-8


from hdfs.client import Client
from json import dump, dumps

client = Client("http://139.219.239.98:50070")
print dir(client)


# with open('5566cfa1-6c65-11e7-9a96-f45c89a97b13.csv') as f:
#     data = f.read()
# with client.write('/hadoop/qsweblog/20170922/00/test.csv', data=data, encoding='utf-8') as f:
#     pass

records = [
    {'name': 'foo', 'weight': 1},
    {'name': 'bar', 'weight': 2},
]

# As a context manager:
with client.write('/hadoop/qsweblog/20170922/00/records.jsonl', encoding='utf-8') as writer:
    dump(records, writer)

# Or, passing in a generator directly:
# client.write('/hadoop/qsweblog/20170922/00/records.jsonl', data=dumps(records), encoding='utf-8')


