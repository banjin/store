# coding:utf-8

from pyhive import hive
import paramiko
import sys
import os
import time

HIVE_HOST = '139.219.239.98'
HIVE_PORT = 10000
HIVE_USER = 'hdfs'

# 私钥文件
pkey_file = '/Users/songhaiming/Downloads/songhm/songhm'
#私钥密码
pkey_file_pwd = 'Qssec@2015!@#'


def send_command(*commands):
    hive_cursor = hive.connect(host=HIVE_HOST, port=HIVE_PORT, username=HIVE_USER).cursor()
    for cd in commands:
        hive_cursor.execute(cd, async=False)
        print hive_cursor.fetchall()


# send_command('create external table if not exists do_test (id int, name string)')
# send_command('select * from do_test')
# send_command('desc do_test')

def ssh2(ip, port, username, passwd, cmd):
    """ 使用用户名密码链接 """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, passwd)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print stdout.read()
    ssh.close()


def ssh_key(host, port, user, cmd):
    """使用未加密的key链接"""
    key = paramiko.RSAKey.from_private_key_file(pkey_file)
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user, pkey=key, timeout=5)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print stdout.read()


def ssh_key_with_passwd(host,port,user,cmd):
    """使用加密的key链接"""

    paramiko.util.log_to_file('ssh_key-login.log')
    try:
        key = paramiko.RSAKey.from_private_key_file(pkey_file)
    except paramiko.PasswordRequiredException:
        # 需要密钥口令
        key = paramiko.RSAKey.from_private_key_file(pkey_file, password=pkey_file_pwd)

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user, pkey=key, timeout=5)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print stdout.read()
    ssh.close()


def demo_sftp(host, port, user, base_dir=''):
    """使用sftp上传文件"""
    try:
        key = paramiko.RSAKey.from_private_key_file(pkey_file)
    except paramiko.PasswordRequiredException:
        # 需要密钥口令
        key = paramiko.RSAKey.from_private_key_file(pkey_file, password=pkey_file_pwd)

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user, pkey=key, timeout=5)
    # 实例化sftp客户端
    # sftp = paramiko.SFTPClient.from_transport(ssh)
    sftp = ssh.open_sftp()
    # print dir(ftp)

    # 在SSH服务器上启动交互式shell会话
    channel = ssh.invoke_shell()
    # print dir(channel)
    channel.send('ls\n')
    while not channel.recv_ready():
        print "Working..."
        time.sleep(2)
    dir_list = channel.recv(1024)
    if "panadit" not in dir_list:
        channel.send('mkdir panadit\n')
        while not channel.recv_ready():
            print "Working..."
            time.sleep(1)
        print channel.recv(1024)

    channel.send('cd panadit\n')
    while not channel.recv_ready():
        print "Working..."
        time.sleep(1)
    print channel.recv(1024)

    # 首先将文件上传到Hadoop机器上
    t = os.listdir(base_dir)
    print "t..", t
    for d in t:
        # 二级目录
        sub_d = os.path.join(base_dir, d)
        print "base_d...", sub_d
        channel.send('ls\n')
        while not channel.recv_ready():
            # print "ls..."
            time.sleep(10)
        sub_dir_list = channel.recv(1024)
        print "sub_dir_list", sub_dir_list
        if d not in sub_dir_list:
            channel.send('mkdir {}\n'.format(d))
            while not channel.recv_ready():
                print "mkdir...{}".format(d)
                time.sleep(10)

            # print channel.recv(1024)
        # channel.send('pwd\n')
        # while not channel.recv_ready():
        #     print "Working..."
        #     time.sleep(1)
        # cur_dir = channel.recv(1024)
        print "111"
        file_list = os.listdir(sub_d)
        print "file_list", file_list
        for file_name in file_list:
            base_file = os.path.join(sub_d, file_name)
            cur_dir = '/home/qsadmin/panadit/' + d
            channel.send('ls {}\n'.format(cur_dir))
            while not channel.recv_ready():
                # print "ls..."
                time.sleep(10)
            sub_file_list = channel.recv(1024)
            if file_name not in sub_file_list:
                print "base_file...", base_file
                remotepath = os.path.join('/home/qsadmin/panadit/' + d, file_name)
                print remotepath
                sftp.put(base_file, remotepath)
                time.sleep(10)
            else:
                break
    # channel.send('sudo su\n')
    # while not channel.recv_ready():
    #     print "Working..."
    #     time.sleep(2)
    # print channel.recv(1024)

    # channel.send('su - hdfs\n')
    # while not channel.recv_ready():
    #     print "Working..."
    #     time.sleep(2)
    # print channel.recv(1024)

    # channel.send('ls\n')
    # while not channel.recv_ready():
    #     print "Working..."
    #     time.sleep(2)
    # print channel.recv(1024)

    # channel.send('whoami\n')
    # while not channel.recv_ready():
    #     print "Working..."
    #     time.sleep(2)
    # print channel.recv(1024)

    # channel.send('hadoop fs -ls /bdp/user_1\n')
    # while not channel.recv_ready():
    #     print "Working..."
    #     time.sleep(5)
    # print channel.recv(1024)

    # 将文件放置到hdfs中
    # channel.send('hadoop fs -put /home/qsadmin/out.log /bdp/user_1/out.csv \n')
    # while not channel.recv_ready():
    #     print "Working..."
    #     time.sleep(10)
    # print channel.recv(1024)


if __name__ == "__main__":
    # ssh2("10.10.10.39", 22, "root", "qssec.com")
    # ssh_key("10.10.10.39", 22, "root", "ifconfig")
    # ssh_key_with_passwd("139.219.239.98", 62226, "qsadmin", "ifconfig")
    demo_sftp("139.219.239.98", 62226, "qsadmin", base_dir='/data/test_django/store/panadit/')
