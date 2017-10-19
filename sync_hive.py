# coding:utf-8

# from pyhive import hive
import MySQLdb
import csv
import os
import sys
import time

HIVE_HOST = ''
HIVE_PORT = ''
HIVE_USER = ''

OUT_DATABASE = ["information_schema", "mysql"]

#
# def connect_hive():
#     cursor = hive.connect(host=HIVE_HOST, port=HIVE_PORT, username=HIVE_USER).cursor()

BASE_DIR = "/data/test_django/store/panadit/"


def connect_mysql(host='', port=3306, user='', password='', database='', charset=''):
    db = MySQLdb.connect(host=host, port=port, user=user,
                         passwd=password, db=database, charset=charset)
    cursor = db.cursor()
    if database == "mysql":
        cursor.execute("show databases")
        database_names = cursor.fetchall()
        database_name_list = [db_name[0] for db_name in database_names]
        print "database_name_list", database_name_list
    else:
        database_name_list = [db]
    for database_name in database_name_list:
        # print "database_name", database_name
        if database_name == "app_info":
            cursor.execute("use app_info")
            cursor.execute("show tables")
            table_names = cursor.fetchall()
            table_name_list = [tb_name[0] for tb_name in table_names]
            for table_name in table_name_list:
                print "table_name", table_name
                # 此命令可以直接在SHOW VARIABLES LIKE "secure_file_priv"配置的路径下产生相应的文件
                # 但是如何将此文件导入到hive中？？
                # cursor.execute("select * from {0} into outfile {1}".format(table_name,
                #                                                           "'" + table_name + ".txt'"))
                f = open("20170725_app.txt", 'a+')
                cursor.execute("select * from {0} limit 100".format(table_name))
                table_data = cursor.fetchall()
                if table_name == "20170725_app":
                    for t in table_data:
                        # t = ','.join([i.strip(' ') for i in t])
                        f.write(str(t)[1:-1] + '\n')
                        print str(t)
                f.close()


def create_table(host='', port=3306, user='', password='', database='', charset=''):
    db = MySQLdb.connect(host=host, port=port, user=user,
                         passwd=password, db=database, charset=charset)
    cursor = db.cursor()
    if database == "mysql":
        cursor.execute("show databases")
        database_names = cursor.fetchall()
        database_name_list = [db_name[0] for db_name in database_names]
        print "database_name_list", database_name_list
    else:
        database_name_list = [db]
    for database_name in database_name_list:
        if database_name == "app_info":
            cursor.execute("use app_info")
            cursor.execute("show tables")
            table_names = cursor.fetchall()
            table_name_list = [tb_name[0] for tb_name in table_names]
            cursor.execute("desc {}".format(table_name_list[0]))
            table_desc = cursor.fetchall()
            sql = ''
            for des in table_desc:
                des_type = change_type(des[1])
                sql += "{field_name} {field_type},".format(field_name=des[0], field_type=des_type)
                print "0,1", des[0], des_type
            sql = "(" + sql[:-1] + ")"
            cursor.execute("create external table if not exists {table_name} {sql_value}".format(table_name= database_name, sql_value=sql))


def change_type(old_type):
    if old_type.startswith('int'):
        return "int"
    elif old_type.startswith('big'):
        return "bigint"
    elif old_type.startswith('varchar'):
        return "string"


def dump_csv(table_name, cursor, file_path):
    """将一个数据表的数据导出到csv文件中"""

    # 查询并导出
    if table_name.isdigit():
        cursor.execute("select * from {}".format("`" + table_name + "`"))
    else:
        try:
            cursor.execute("select * from {}".format(table_name))
        except Exception, e:
            raise e
    with open(file_path, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        # 添加表头信息
        csv_writer.writerow([i[0] for i in cursor.description])
        # print "cursor......", cursor.fetchall()
        gg = []
        for c in cursor.fetchall():
            row = []
            for i in c:
                if isinstance(i, basestring):
                    row.append(i.encode('utf-8'))
                else:
                    row.append(i)
            gg.append(row)
        # print gg
        try:
            csv_writer.writerows(gg)
        except UnicodeEncodeError,e:
            raise e


def get_database_list(host='', port=3306, user='', password='', database_name='mysql', charset='utf8'):
    """
    获取所有的数据库名称
    :return: 
    """
    db = MySQLdb.connect(host=host, port=port, user=user,
                         passwd=password, db=database_name, charset=charset)
    cursor = db.cursor()

    if database_name == "mysql":
        cursor.execute("show databases")
        database_names = cursor.fetchall()
        database_name_list = [db_name[0] for db_name in database_names]
    else:
        database_name_list = [database_name]
    return database_name_list, db, cursor


def get_table_list(database_name, cursor):
    """
    获取某一个数据库下的数据表名称
    :return: 
    """
    cursor.execute("use {}".format(database_name))
    cursor.execute("show tables")
    table_names = cursor.fetchall()
    table_name_list = [table_name[0] for table_name in table_names]
    return table_name_list


def main():
    """根据数据库创建文件
    
    1. 需要记录同步的进程{"database_name, table_name, last_file_name:"table_name_{年月日时分秒}", rows=""}
    2. 对于固定的数据表，需要记录同步的行数
    3. 由于数据表的创建时间不一样，需要针对不行情况做不同的处理
    4. 上传时候需要根据最后一次上传文件的时间判断
    """
    start_time = time.time()
    database_name_list, db, cursor = get_database_list(host='10.2.4.236', port=3306, user='root',
                                                       password='d4r9q8v6@panabit.com',
                                                       database_name='mysql', charset='utf8')
    # with open("data_names.txt", 'a+') as f:
    #     f.write(str(database_name_list))
    # print database_name_list
    for database_name in database_name_list:
        if database_name not in OUT_DATABASE:
            print "database_name", database_name

            file_dir = os.path.join(BASE_DIR, database_name)
            if os.path.exists(file_dir):
                pass
            else:
                os.mkdir(file_dir)
            table_name_list = get_table_list(database_name, cursor)
            for table_name in table_name_list:
                # if table_name.startswith("INNODB"):
                #     continue
                print "table_name....", table_name
                file_path = os.path.join(file_dir, table_name) + ".csv"

                if os.path.exists(file_path):
                    continue
                dump_csv(table_name, cursor, file_path)

    end_time = time.time()
    db.close()
    print "all_time...", end_time-start_time
if __name__ == "__main__":
    # connect_mysql(host='10.2.4.236', port=3306, user='root',
    #               password='d4r9q8v6@panabit.com', database='mysql', charset='utf8')
    # dump_csv()
    # main()

    import os
    t = os.listdir('/data/test_django/store/panadit/')
    for i in t:
        b = os.path.join('/data/test_django/store/panadit/', i)
        # print b
        c = os.listdir(b)
        for r in c:
            base_c = os.path.join(b, r)
            print base_c


