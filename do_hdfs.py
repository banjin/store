# coding:utf-8

from hdfs import *
from json import dump, load
import paramiko
import time
import os

HDFS_URL = ""
TEMP_BASE_DIR = "/home/qsadmin/panadit"
HDFS_BASE_DIR = "/panadit"
SHELL_DIR = "/home/qsadmin/panadit_hdfs.sh"
# 私钥文件
pkey_file = '/Users/songhaiming/Downloads/songhm/songhm'
#私钥密码
pkey_file_pwd = 'Qssec@2015!@#'


def do_hdfs():
    # 链接不上集群，集群只有一个出口IP，找不到具体的机器。
    client=Client('http://139.219.236.98:8020', root='/', proxy='', timeout=3)
    client.list('/')
    client.makedirs('/a/b/c')
    client.delete('/2017', recursive=True)
    # def upload(self, hdfs_path, local_path, overwrite=False, n_threads=1,
    # temp_dir=None, chunk_size=2 ** 16, progress=None, cleanup=True, **kwargs)
    client.upload('/2017/02/test.txt', 'D:/tmp/test.txt', overwrite=True)


def copy_file(host, port, user):
    """
    将文件传到hdfs系统中
    :return: 
    """
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
    stdin, stdout, stderr = ssh.exec_command(SHELL_DIR)
    print stdout.read()

    # 在SSH服务器上启动交互式shell会话
    # channel = ssh.invoke_shell()

    # 获取所有的二级目录
    # command_1 = "ls\n"
    """
    # for sub_dir in sub_dir_list:
        command_2 = "sudo su\n"
        command_3 = "su - hdfs\n"
        command_4 = "hadoop fs -ls /xxxxxx/yyyy/panadit\n"
        # if sub_dir not in hdfs_sub_list:
        command_5 = "hadoop dfs -mkdir /home\n"
        command_6 = "hadoop dfs -mkdir /home\n"
        command_7 = "exit\n"
        command_8 = "ls sub_dir\n"
        command_9 = "su - hdfs\n"
        # for file_name in file_list:
            # temp_file_path = sub_dir + file_name
            # hdfs_file_path = hdfs_sub_dir + file_name
            # command_10 = "hadoop fs -put /home/qsadmin/out.log /bdp/user_1/out.csv\n"
    """

    # channel.send('ls {}\n'.format(TEMP_BASE_DIR))
    # while not channel.recv_ready():
    #     print "Working..."
    #     time.sleep(5)
    # print channel.recv(5120)

    # print "sub_dir_list...", sub_dir_list

    # channel.send('sudo su\n')
    # while not channel.recv_ready():
    #     # print "Working..."
    #     time.sleep(5)
    # print channel.recv(1024)
    #
    # channel.send('su - hdfs\n')
    # while not channel.recv_ready():
    #     # print "Working..."
    #     time.sleep(5)
    # print channel.recv(1024)

    # for sub_dir in sub_dir_list:
    #     temp_sub_dir = os.path.join(TEMP_BASE_DIR, sub_dir)
    #     channel.send('hadoop fs -ls {}\n'.format(HDFS_BASE_DIR))
    #     while not channel.recv_ready():
    #         print "Working..."
    #         time.sleep(2)
    #     hdfs_sub_dir_list = channel.recv(1024)
    #     if sub_dir not in hdfs_sub_dir_list:
    #         new_hdfs_dir = os.path.join(HDFS_BASE_DIR, sub_dir)
    #         channel.send('hadoop fs -mkdir -p {}\n'.format(new_hdfs_dir))
    #         while not channel.recv_ready():
    #             print "Working..."
    #             time.sleep(2)
    #         print channel.recv(1024)
    #
    #     channel.send('ls {}\n'.format(temp_sub_dir))
    #     while not channel.recv_ready():
    #         print "Working..."
    #         time.sleep(2)
    #     temp_file_list = channel.recv(1024)
    #
    #     channel.send('hadoop fs -ls {}\n'.format(new_hdfs_dir))
    #     while not channel.recv_ready():
    #         print "Working..."
    #         time.sleep(2)
    #     hdfs_file_list = channel.recv(1024)
    #
    #     for t_f in temp_file_list:
    #         tem_file_path = os.path.join(temp_sub_dir, t_f)
    #         hdfs_file_path = os.path.join(new_hdfs_dir, t_f)
    #         if t_f not in hdfs_file_list:
    #             channel.send('hadoop fs -put {} {}\n'.format(tem_file_path,hdfs_file_path))
    #             while not channel.recv_ready():
    #                 print "Working..."
    #                 time.sleep(2)
    #             hdfs_file_list = channel.recv(1024)

if __name__ == "__main__":
    # do_hdfs()
    copy_file("139.219.239.98", 62226, "qsadmin")
