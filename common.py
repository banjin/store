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

def gg():
    import csv
    l = [['1', 'Wonderful Spam'], ['2', 'Lovely Spam']]
    # 模拟数据写入一个csv
    with open('eggs.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in l:
            spamwriter.writerow(row)
    # 从文件读取
    l = []
    with open('eggs.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            l = l + [row]
            print l
    # 把两列拼接增加为第三列写回到文件
    with open('eggs1.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in l:
            print(row)
            spamwriter.writerow(row + [row[0] + row[1]])


class RoomServer:
    '''msg:
    ADD:to_name:from_name:msg:data_type
    DEL:to_name:from_name:msg:data_type
    SEND:to_name:from_name:msg:data_type
    data_type:[utf8, ...]
    '''

    def __init__(self):
        '''
        {
            sessionid:{
                user: user,
                ws: ws
            },
            sessionid:{
                user: user,
                ws: ws
            },
            ...
        }
        使用字典来存储 ws 方便检索, 键值是 sessionid
        '''
        self.online = dict()

    def get_all_users(self):
        '''
        return unique_users
        '''
        users = [i['user'] for i in self.online.values()]
        unique_users = set(users)
        return unique_users

    def update(self, sid, user, ws):
        self.online[sid] = dict(user=user, ws=ws)

    def get_ctx(self, sid):
        '''
        return (user, ws) / none
        '''
        return self.online.get(sid, None)

    def del_ctx(self, sid):
        '''删除在线用户'''
        try:
            del self.online[sid]
        except:
            print('WARN', sid, 'not in the online list')

    def add_user_broadcast(self, sid, user, ws):
        '''添加用户并向在线用户广播'''
        self.update(sid, user, ws)
        raw_msg = 'ADD::{from_}:{from_}:utf8'.format(from_=user.name)
        self._send(raw_msg)

    def remove_user_broadcast(self, sid):
        '''
        广播删除用户 并删除用户
        如果没找到, 打印异常
        '''
        ctx = self.get_ctx(sid)
        if ctx:
            raw_msg = 'DEL::{from_}:{from_}:utf8'.format(from_=ctx['user'].name)
            self.del_ctx(sid)
            self._send(raw_msg)
        else:
            print('WARN', sid, 'not in the online list')

    def send_msg(self, sid, msg, to=None):
        '''
        to 默认是 None 向所有在线用户发送消息
        '''
        ctx = self.get_ctx(sid)
        if ctx:
            raw_msg = 'SEND:{to}:{from_}:{msg}:utf8'.format(to=to, from_=ctx['user'].name, msg=msg)
        self._send(msg, to=to)

    def handle_msg(self, from_user, raw_msg):
        '''处理接受的数据'''
        raw_msg = raw_msg.decode('utf-8')
        print(raw_msg)
        option, to, from_, msg, type_ = raw_msg.split(':')
        if option == 'SEND':
            to_name = to if to else None
            self._send(raw_msg, name=to_name)
        else:
            print('WARN: unknown option {}'.format(option))

    def _send(self, raw_msg, name=None):
        '''
        raw_msg 是包装以后的消息
        name 默认是 None 向所有在线用户发送消息
        '''
        to_sid = []
        if name:
            for k, v in self.online.items():
                if v['user'].name == name:
                    to_sid.append(k)
        else:
            to_sid = self.online.keys()
        del_sid = []
        # 发送失败, 从列表里面删除该用户
        for i in to_sid:
            ws = self.online[i]['ws']
            try:
                ws.send(raw_msg.encode('utf-8'))
            except:
                del_sid.append(i)
        print(to_sid, del_sid)
        for i in del_sid:
            self.remove_user_broadcast(i)

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

    md5sum('eggs2.csv')
    # import os
    # print os.stat('stocks6.xlsx').st_size
    # table_append('/Users/songhaiming/Downloads/servers_template.csv')


    # f = ['\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe5\x90\x8d', 'IDC', 'SN\xe7\xbc\x96\xe5\x8f\xb7',
    #      '\xe6\x9c\xba\xe6\x9f\x9c', '\xe7\x94\xa8\xe9\x80\x94', '\xe7\xb1\xbb\xe5\x9e\x8b',
    #      '\xe5\x85\xac\xe7\xbd\x91IP\xe5\x9c\xb0\xe5\x9d\x80', '\xe5\x86\x85\xe7\xbd\x91IP\xe5\x9c\xb0\xe5\x9d\x80',
    #      '\xe5\x8e\x82\xe5\x95\x86', '\xe5\x9e\x8b\xe5\x8f\xb7', 'U\xe6\x95\xb0']
    # g = ','.join(f)
    # print g

    # gg()
