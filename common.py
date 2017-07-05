# coding:utf-8
import functools

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
        headers = next(f_csv)
        for row in f_csv:
            print row[0].decode('gbk').encode('utf-8')

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

if __name__ == '__main__':
    # t_warps()
    # p = Pizza(55)
    # print Pizza.get_size(p)
    # print p.get_size()

    # A.fun3(A)
    # B.fun3()
    #parse_csv('/Users/songhaiming/Downloads/servers_template.csv')
    #parse_execl('/Users/songhaiming/Downloads/测试版本一.xlsx')
    upload_progress(30,79)

