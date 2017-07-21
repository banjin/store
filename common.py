# coding:utf-8
import functools
import uuid

# ======== 装饰器 ==========


def log(f):
    @functools.wraps(f)
    def in_fun(*args):
        print "start_in_fun"
        f()
        print ("end_in_fun")
        return
    return in_fun

@log
def t_warps():
    print "start_test"
    return


# =================
can_run = True


def decorator_name(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)
    return decorated


@decorator_name
def func():
    return("Function is running")


# === 带参数的装饰器 =========


def soc_log(category, text):
    """记录日志"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            print "in_wrapper"
            return

        return wrapper

    return decorator


def logit(logfile='out.log'):
    def logging_decorator(func):
        @functools.wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile，并写入内容
            with open(logfile, 'a') as opened_file:
                # 现在将日志打到指定的logfile
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

@logit()
def myfunc1():
    pass

myfunc1()
# Output: myfunc1 was called
# 现在一个叫做 out.log 的文件出现了，里面的内容就是上面的字符串

@logit(logfile='func2.log')
def myfunc2():
    pass

myfunc2()
# Output: myfunc2 was called
# 现在一个叫做 func2.log 的文件出现了，里面的内容就是上面的字符串


# ======类装饰器 ============

class logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile并写入
            with open(self.logfile, 'a') as opened_file:
                # 现在将日志打到指定的文件
                opened_file.write(log_string + '\n')
            # 现在，发送一个通知
            self.notify()
            return func(*args, **kwargs)
        return wrapped_function

    def notify(self):
        # logit只打日志，不做别的
        pass


class email_logit(logit):
    '''
    一个logit的实现版本，可以在函数调用时发送email给管理员
    '''

    def __init__(self, email='admin@myproject.com', *args, **kwargs):
        self.email = email
        super(email_logit, self).__init__(*args, **kwargs)

    def notify(self):
        # 发送一封email到self.email
        # 这里就不做实现了
        pass


# =======  静态方法和类方法，实例方法 =========
class A(object):

    @classmethod
    def func1(cls):

        print "A.func1", cls.__name__

    @classmethod
    def func2(cls):
        cls.func1()

        print "func2", cls.__name__

    @staticmethod
    def fun3(cls):
        print "fun3", cls.__name__


class B(A):

    @classmethod
    def func1(cls):

        print "B.func1", cls.__name__

    @staticmethod
    def fun3():
        print "in B"


class Pizza(object):
    def __init__(self,size):
        self.size = size

    def get_size(self):
        return self.size


# ======= 解析csv文件 ========

def parse_csv(filename):
    """解析csv文件
    :param filename: 
    :return: 
    """
    import csv
    with open(filename) as f:
        f_csv = csv.reader(f)
        # headers = next(f_csv)
        # print headers
        # a = [i for i in headers]
        lines = []
        for row in f_csv:
            line = [i.decode('GBK').encode('utf-8') for i in row]
            print line
            lines.append(line)
    store_name = str(uuid.uuid1()) + '.csv'
    with open(store_name, 'w+') as ff:
        f_csv = csv.writer(ff, delimiter=',')
        f_csv.writerows(lines[4:])
    import os
    file_size = os.path.getsize(store_name)
    print file_size


def parse_execl(filename):
    """
    解析execl文件
    :param filename: 
    :return: 
    """
    import xlrd
    book = xlrd.open_workbook(filename)  # 获取一个xlrd对象
    print book.nsheets  # 获取所有的sheet个数
    for sheet_index in range(book.nsheets):
        print book.sheet_by_index(sheet_index)
    print [i for i in book.sheet_names()]
    sheet = book.sheet_by_index(0)  # 获取第一个sheet
    print sheet
    print sheet.name   # 获取sheet的名字
    print sheet.ncols  # 获取sheet的列
    print sheet.nrows  # 获取sheet的行
    print sheet.cell(1, 2).value


def upload_progress(offset, size):
    """
    获取上传进度
    :param offset: 已经长传大小
    :param size: 文件总的大小
    :return: 
    """
    if size == 0:
        print "upload process ... {0}".format("%5.1f%%" % (100 * 0))
    else:
        ratio = float(offset) / size
        print "upload process ... {0}".format("%5.1f%%" % (100 * ratio))


def conver_to_csv(file_path):
    import xlrd
    import csv

    data = xlrd.open_workbook(file_path)
    for sheet_index in range(data.nsheets):
        table = data.sheet_by_index(sheet_index)
        store_file = table.name.encode('utf-8') + '.csv'
        nrows = table.nrows
        ncols = table.ncols
        lines = []
        for r in xrange(nrows):
            line = []
            for c in xrange(ncols):
                if isinstance(table.cell(r, c).value, basestring):
                    line.append(table.cell(r, c).value.encode('utf-8'))
                else:
                    line.append(table.cell(r, c).value)
            print line
            lines.append(line)
        with open(store_file, 'w+') as f:
            f_csv = csv.writer(f, delimiter=',')
            f_csv.writerows(lines)


# ====== 计算文件的md5值 ===========
from hashlib import md5

def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')    #使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    print m.hexdigest()
    print len(m.hexdigest())


def md5sum(fname):
    """ 计算文件的MD5值 """
    import hashlib
    import os
    def read_chunks(fh):
        fh.seek(0)
        chunk = fh.read(1024)
        while chunk:
            yield chunk
            chunk = fh.read(1024)
        else: #最后要将游标放回文件开头
            fh.seek(0)
    m = hashlib.md5()
    if isinstance(fname, basestring) \
            and os.path.exists(fname):
        with open(fname, "rb") as fh:
            for chunk in read_chunks(fh):
                m.update(chunk)
    #上传的文件缓存 或 已打开的文件流
    elif fname.__class__.__name__ in ["StringIO", "StringO"] \
                or isinstance(fname, file):
        for chunk in read_chunks(fname):
            m.update(chunk)
    else:
        return ""
    print m.hexdigest()


def table_append(filename):

    import csv
    maping = {"服务器名": "服务器名", "b": None, "IDC": "d"}
    values = maping.values()

    with open(filename) as f:
        f_csv = csv.reader(f)
        # headers = next(f_csv)
        # print headers
        # a = [i for i in headers]
        lines = []
        for row in f_csv:
            line = [i.decode('GBK').encode('utf-8') for i in row]
            print line

            lines.append(line)
        header = lines[0]


    # str_uuid = str(uuid.uuid1())
    # print str_uuid
    # store_name = str_uuid + '.csv'
    # with open(store_name, 'w+') as ff:
    #     f_csv = csv.writer(ff, delimiter=',')
    #     f_csv.writerows(lines[4:])
    # import os
    # file_size = os.path.getsize(store_name)
    # print file_size
    # 5566cfa1-6c65-11e7-9a96-f45c89a97b13
    #         for key, value in maping.items():
    #             pass

    # # 怎么计算lines???

    # field_id = 1
    #
    with open('5566cfa1-6c65-11e7-9a96-f45c89a97b13.csv', 'w+') as ff:
        f_csv = csv.writer(ff, delimiter=',')
        f_csv.writerows(lines)


def handle_uploaded_file(f, file_url, model):
    with open(file_url, model) as destination:
        # 默认每次读取65535字节
        for chunk in f.chunks():
            destination.write(chunk)

if __name__ == '__main__':
    # t_warps()
    # p = Pizza(55)
    # print Pizza.get_size(p)
    # print p.get_size()

    # A.fun3(A)
    # B.fun3()
    # parse_csv('/Users/songhaiming/Downloads/servers_template.csv')
    # parse_execl('/Users/songhaiming/Downloads/测试版本三配置管理.xls')
    # upload_progress(30,79)
    # conver_to_csv('stocks10.xlsx')

    # md5_file('/Users/songhaiming/Downloads/测试版本三配置管理.xls')
    # 5eef0c399c75b1afbbafc5011be141f3

    # md5sum('servers_template(1).csv')
    # import os
    # print os.stat('stocks6.xlsx').st_size
    table_append('/Users/songhaiming/Downloads/servers_template.csv')
