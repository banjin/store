#  -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch, helpers
import logging
import re
import time
import datetime
import MySQLdb
import json

logger = logging.getLogger('sync_mysql')


# 每天同步一次的数据库列表, index根据数据库名和表名联合创建
day_sync_list = ["taobao", "fetion", "sinawb", 'user_account',
                 'share_ip', 'offpic_new', 'keylist', 'qqwb',
                 'msnlogin', 'pop3login', 'area_flow', 'http_flow', 'yys_info',
                 'wxdns', 'app_info']

# 每小时需要同步一次的数据库列表
hour_sync_list = ["ipinfo_", "dstipinfo_", 'iphost_', 'topdns_']

# 每分钟需要同步的
minute_sync_list = ["ipnode", 'urlevent', 'session', 'dnsquery']


# 数据库和表名称不变的情况
no_change_list = ['palog']

# 暂时没想好怎么处理
do_not_konw = ['flowlog_20150716']


es = Elasticsearch()
# es_hosts = ['http://es-2146840482.cn-north-1.elb.amazonaws.com.cn:59200/']
es_hosts = ['10.10.10.22:9200/']
es = Elasticsearch(
        hosts=es_hosts
)

# print es.indices.get_mapping('ossec-2016.06.11')
# print es.indices.get_mapping('securitybigdata')


def make_mapping(doc_type, index, field_list, data_list):
        properties = {}
        print "data_list........",data_list
        for i, value in enumerate(data_list):
            field = field_list[i]
            if field not in ['_type', '_index']:
                if value is not None:
                    if isinstance(value, unicode):
                        field_type = 'string'
                    if isinstance(value, str):
                        field_type = 'string'
                    if isinstance(value, int):
                        field_type = 'long'
                    if isinstance(value, long):
                        field_type = 'long'
                    if isinstance(value, float):
                        field_type = 'float'
                else:
                    field_type = 'string'

                # print "field.......",field
                # print "field_type......",field_type
                if field_type == 'string':
                    properties[field] = {'type': field_type, "index": "not_analyzed"}
                else:
                    properties[field] = {'type': field_type}
                # print "properties", properties

        mapping = {
                "mappings": {
                    doc_type: {
                      "properties": properties
                    }
                }
        }
        es.indices.create(index=index, body=mapping)


def add_doc(doc, doc_type, index):
    # 数据单条写入
    res = es.index(doc_type=doc_type,
                   index=index,
                   body=doc)
    print res


def insert_data(num):
    """
    插入数据
    :return: 
    """
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root',
                         passwd='123456', db='store', charset='utf8')
    cursor = db.cursor()
    i=200000
    sql = "insert into book_person VALUES(%s,%s,%s)"
    params = []
    import time
    s_t = time.time()
    print s_t
    while i < num:
        params.append((i, str(i), '1'))
        i += 1
    print "m..", time.time()
    params = tuple(params)
    print i
    cursor.executemany(sql, params)
    db.commit()
    print "end", time.time()


def test():
    pattern = re.compile(r'world')

    # 使用search()查找匹配的子串，不存在能匹配的子串时将返回None
    # 这个例子中使用match()无法成功匹配
    match = pattern.search('hello world!')

    if match:
        # 使用Match获得分组信息
        print match.group()


def create_date(data):
    """
    同步数据时候记录同步状态
    :return: 
    """
    with open('sync_process.json', 'w+') as f:
        print 'ccc'
        json.dump(data, f, indent=2)


def get_data():
    """
    获取所有的同步记录数据
    :return: 
    """
    with open('sync_process.json') as f:
        data = json.load(f)
        print data
        return data


def get_record(index):
    """
    获取某一个index的同步记录
    :return: 
    """
    data = get_data()
    for d in data:
        if d['index'] == index:
            return d


class SyncMysql(object):
    """ 同步数据库数据
    """

    def __init__(self, host='', port=3306, user='', password='', database_name='mysql', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = password
        self.database_name = database_name
        self.charset = charset

    def connect_mysql(self):
        """
        链接数据库
        :return: 
        """
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user,
                             passwd=self.passwd, db=self.database_name, charset=self.charset)
        cursor = db.cursor()

        return db, cursor

    def get_database_list(self, cursor):
        """
        获取所有的数据库名称
        :return: 
        """

        if self.database_name == "mysql":
            cursor.execute("show databases")
            database_names = cursor.fetchall()
            database_name_list = [db_name[0] for db_name in database_names]
        else:
            database_name_list = [self.database_name]
        return database_name_list

    def get_table_list(self, database_name, cursor):
        """
        获取某一个数据库下的数据表名称
        :return: 
        """
        cursor.execute("use {}".format(database_name))
        cursor.execute("show tables")
        table_names = cursor.fetchall()
        table_name_list = [table_name[0] for table_name in table_names]
        return table_name_list

    @staticmethod
    def get_all_index():
        """
        获取所有的index
        :return: [u'ossec-2016.06.21', u'ossec-2016.06.20', u'ossec-2016.06.23']
        """
        return es.indices.get_aliases().keys()

    @staticmethod
    def get_now():
        now = datetime.datetime.now().strftime('%Y%m%d%H%M')
        return now

    @staticmethod
    def re_db(database_name):
        # 寻找到每天产生的数据库
        # database_name = 'iphost_20150629'
        ret = re.compile(r'\d{8}')
        res = re.search(ret, database_name)
        if res:
            return res.group()
        return res

    @staticmethod
    def re_table(table_name):
        """
        获取数据表
        :param table_name: 
        :return: 
        """
        # table_name = 'iphost201506291010'
        ret = re.compile(r'\d{12}')
        res = re.search(ret, table_name)
        if res:
            return res.group()
        return res

    @staticmethod
    def re_start_word(database_name):
        """
        获取数据库开头
        :return: 
        """
        pattern = re.compile(r'(\w.*?)(\d)')
        match = pattern.match(database_name)
        if match:
            # 使用Match获得分组信息
            return match.group(1)
        return match

    def create_index_by_dbname(self, database_name, cursor):
        """
        同步数据
        :return: 
        """
        database_name = database_name
        # 某一个数据库中的所有的数据表
        table_name_list = self.get_table_list(database_name, cursor)

        # 根据数据库名字建立index
        index = database_name
        doc_type = index
        # index 不存在

        if len(table_name_list) > 0:
            # 根据第一张表创建index
            first_table_name = table_name_list[0]
            last_table_name = table_name_list[-1]
            field_list = []
            if first_table_name.isdigit():
                cursor.execute("desc {}".format("`" + first_table_name + "`"))
            else:
                cursor.execute("desc {}".format(first_table_name))
            for field in cursor.fetchall():
                field_list.append(field[0])
            field_list.extend(['_type', '_index'])

            all = []
            for table_name in table_name_list:
                print "table_name", table_name
                if table_name.isdigit():
                    cursor.execute("select * from {}".format("`" + table_name + "`"))
                else:
                    try:
                        cursor.execute("select * from {}".format(table_name))
                    except _mysql_exceptions.OperationalError, e:
                        raise e
                ff = cursor.fetchall()
                for i in ff:
                    all.append(list(i) + [doc_type, index])
            if all:
                make_mapping(doc_type, index, field_list, all[0])

            write_data = []
            for rs in all:
                write_data.append(dict(zip(field_list, rs)))
            helpers.bulk(es, write_data)
            sync_data = get_data()
            add_data = {'database_name': database_name,
                        'table_name': last_table_name, 'cols': '', 'index': database_name}
            sync_data.append(add_data)
            create_date(sync_data)

    def create_index_by_tbname(self, database_name, table_name, cursor):
        """
        数据库结合数据表创建index
        :param self: 
        :param database_name: 
        :param table_name: 
        :param cursor: 
        :return: 
        """

        index = database_name + "_" + table_name
        doc_type = index

        field_list = []
        if table_name.isdigit():
            cursor.execute("desc {}".format("`" + table_name + "`"))
        else:
            cursor.execute("desc {}".format(table_name))
        for field in cursor.fetchall():
            field_list.append(field[0])
        field_list.extend(['_type', '_index'])
        all = []
        if table_name.isdigit():
            cursor.execute("select * from {}".format("`" + table_name + "`"))
        else:
            cursor.execute("select * from {}".format(table_name))
        ff = cursor.fetchall()
        for i in ff:
            all.append(list(i) + [doc_type, index])
        if all:
            make_mapping(doc_type, index, field_list, all[0])

        write_data = []
        for rs in all:
            write_data.append(dict(zip(field_list, rs)))
        helpers.bulk(es, write_data)

        sync_data = get_data()
        if database_name == "palog":
            cols = len(ff)
            add_data = {'database_name': database_name,
                        'table_name': table_name, 'cols': cols, 'index': index}
        else:
            add_data = {'database_name': database_name,
                        'table_name': table_name, 'cols': '', 'index': index}
        sync_data.append(add_data)
        create_date(sync_data)

    def add_data(self, database_name, cursor, index, doc_type):
        """
        index 已经存在，添加数据
        :param self: 
        :param database_name: 
        :param cursor: 
        :return: 
        """

        table_name_list = self.get_table_list(database_name, cursor)
        sync_records = get_data()
        cur_record = {"index": '', 'table_name': ''}
        cur_col = ''
        # 获取当前同步的数据表
        for record in sync_records:
            if index == record['index']:
                cur_record = record
                break
        cur_sync_table = cur_record['table_name']

        # last_sync_table = "sess201708021212"
        wiil_sync_table_list = []
        if cur_sync_table.isdigit():
            # 每小时创建一张数据表
            now = datetime.datetime.now().strftime("%Y%m%d%H")
            for table_name in table_name_list:
                if table_name > cur_sync_table and table_name < now:
                    wiil_sync_table_list.append(table_name)
        elif database_name == "palog":
            # 数据库和数据表是固定的
                cur_col = cur_record['cols']
                #  去掉  "palog_"
                cur_sync_table = index[6:]
        else:
            # 每分钟创建一张数据表
            now = self.get_now()
            # 需要一个数据库记录同步的进度
            # last_sync_table = "sess201708011212"
            last_sync = self.re_table(cur_sync_table)

            p = re.compile(r'\d{12}')
            last_new_table = p.sub(now, cur_sync_table)

            if last_sync:
                # 获取需要同步的数据表
                for table_name in table_name_list:
                    if table_name > cur_sync_table and table_name < last_new_table:
                        print 'table....', table_name
                        wiil_sync_table_list.append(table_name)

        # 获取field_list
        field_list = []
        if cur_sync_table.isdigit():
            cursor.execute("desc {}".format("`" + cur_sync_table + "`"))
        else:
            cursor.execute("desc {}".format(cur_sync_table))
        for field in cursor.fetchall():
            field_list.append(field[0])
        field_list.extend(['_type', '_index'])
        print "last_sync_table", wiil_sync_table_list
        if wiil_sync_table_list:
            last_sync_table = wiil_sync_table_list[-1]
            # 同步数据
            all = []
            for sync_table_name in wiil_sync_table_list:
                if sync_table_name.isdigit():

                    cursor.execute("select * from {}".format("`" + sync_table_name+ "`"))
                else:
                    cursor.execute("select * from {}".format(sync_table_name))
                ff = cursor.fetchall()
                for i in ff:
                    all.append(list(i) + [doc_type, index])
            write_data = []
            for rs in all:
                write_data.append(dict(zip(field_list, rs)))
            helpers.bulk(es, write_data)

            cur_record.update(table_name=last_sync_table)
            create_date(sync_records)
        elif cur_col:
            print "cur_col", cur_col
            # 数据库和数据表不变化
            all = []
            if cur_sync_table.isdigit():
                cursor.execute("select count(1) from {0}".format("`" + cur_sync_table + "`"))
                count = cursor.fetchone()[0]
                cursor.execute("select * from {0} limit {1}, {2}".format("`" + cur_sync_table + "`", cur_col, count))
            else:
                cursor.execute("select count(1) from {0}".format(cur_sync_table))
                count = cursor.fetchone()[0]
                cursor.execute("select * from {0} limit {1}, {2}".format(cur_sync_table, cur_col, count))
            ff = cursor.fetchall()
            all_col = cur_col + len(ff)
            for i in ff:
                all.append(list(i) + [doc_type, index])
            write_data = []
            for rs in all:
                write_data.append(dict(zip(field_list, rs)))
            helpers.bulk(es, write_data)

            cur_record.update(cols=all_col)
            create_date(sync_records)


def test_json():

    data = get_data()
    for t in data:
        if isinstance(t, dict):
            print "haha"
        t.update(database_name='hah')
    create_date(data)


def main():
    sync_mysql = SyncMysql(host='10.2.4.236', port=3306, user='root',
                           password='d4r9q8v6@panabit.com', database_name='mysql', charset='utf8')
    db, cursor = sync_mysql.connect_mysql()
    database_name_list = sync_mysql.get_database_list(cursor)
    for database_name in database_name_list:
        print "database_name....", database_name
        es_table_list = sync_mysql.get_all_index()
        # 根据数据库名成建立index，每分钟创建一个数据表和每小时创建一张表
        if (sync_mysql.re_start_word(database_name) in minute_sync_list or
                    sync_mysql.re_start_word(database_name) in hour_sync_list):
            database_name = database_name
            index = database_name
            doc_type = index
            if database_name not in es_table_list:
                print "create index"
                sync_mysql.create_index_by_dbname(database_name, cursor)
            else:
                print "add data"
                sync_mysql.add_data(database_name, cursor, index, doc_type)
        # 根据数据库名和工作表建立index， 每天创建一个数据表
        elif database_name in day_sync_list or database_name.startswith('qqinfo'):
            table_name_list = sync_mysql.get_table_list(database_name, cursor)
            for table_name in table_name_list:
                if table_name < datetime.datetime.now().strftime("%Y%m%d"):
                    index = database_name + "_" + table_name
                    doc_type = index
                    if index not in es_table_list:
                        sync_mysql.create_index_by_tbname(database_name, table_name, cursor)
        elif database_name == "palog":
            table_name_list = sync_mysql.get_table_list(database_name, cursor)
            for table_name in table_name_list:
                index = database_name + "_" + table_name
                doc_type = index
                if index not in es_table_list:
                    sync_mysql.create_index_by_tbname(database_name, table_name, cursor)
                else:
                    # 追加数据,["database_name", "table_name", "cols"]
                    sync_mysql.add_data(database_name, cursor, index, doc_type)
        else:
            pass
    db.close()

if __name__ == "__main__":
    main()

    # 如何纪录数据库是否被已经被同步？
    # 如何监测数据库的数据是否发生变化
    # 如何监测新增加的数据库
    # 如何监测新增加的数据表
    # 数据库使用分表机制，使用通配符
    # 大量数据如何知道哪些已经被统计

    # insert_data(100000)
    # create_index()
    # re_e('iphost_20150629')
    # get_all_index()
    # get_now()
    # 获取所有的index
    # re_table("xx")

    # import re
    #
    # now = get_now()
    # last_sync_table = "sess201507162379"
    # last_sync = re_table(last_sync_table)
    # p = re.compile(r'\d{12}')
    # last_new_table = p.sub(now, last_sync_table)
    # table_name = 'sess201507162356'
    # print last_new_table
    # if last_sync_table < table_name < last_new_table:
    #     print "1"
    # raw()
    # re_start_word('ipinfo_20150818')

    pass

    # data = [{"database_name": "test", "table_name": "t_name", "cols": 10}]
    # create_date(data)

    # get_data()
    # test_json()

    # db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root',
    #                      passwd='123456', db='mysql', charset='utf8')
    # cursor = db.cursor()
    # cursor.execute("use bdp")
    # cursor.execute("select count(1) from folder")
    # count = cursor.fetchone()[0]
    # print count