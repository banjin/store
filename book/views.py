# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import codecs
import common
import io
import os
import uuid
from django.conf import settings
from models import FileInfo, Question

# Create your views here.
"""
@csrf_exempt
def get_page(request):
    print "hahaha"
    #print request.body
    #print request.FILES
    servers_file = request.FILES.get('csv_file')

    handle_uploaded_file(servers_file)
    # print "server....", servers_file
    # csv_coding = 'gbk'
    # try:
    #     dialect = csv.Sniffer().sniff(codecs.EncodedFile(servers_file, csv_coding).read(1024))
    #     servers_file.open()
    #     reader = csv.reader(codecs.EncodedFile(servers_file, csv_coding), delimiter=str(','), dialect=dialect)
    #     header = reader.next()
    #     header = [h for h in header]
    # except Exception as e:
    #     return HttpResponse("Bad file")
    # print header
    #
    # lines = []
    # for line in reader:
    #     print line
    #     line = [li for li in line]
    #     lines.append(line)
    # with open('stocks4.csv', 'w+') as f:
    #     f_csv = csv.writer(f)
    #     f_csv.writerow(header)
    #     f_csv.writerows(lines)
    # print lines
    # common.md5sum('stocks4.csv')

    return HttpResponse("Hello, world. You're at the polls index.")
"""


def handle_uploaded_file(f):
    with open('stocks10.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        common.md5sum('stocks6.xlsx')


@csrf_exempt
def get_page(request):
    # user = request.user
    file_name = 'file_name_2.csv'
    file_size = 22000
    hash_str = '5eef0c399c75b1afbbafc5011be141f2' # 文件特征值
    offset_size = 123
    # 暂时都是上传新的文件
    offset_size = 0
    DATA_BASE_DIR = '/var/temp/bdpdata/user_5'
    file_folder = settings.EXECL_TMP_FILE_DIR.format("user_" + str(2))
    # 判断用户的磁盘大小
    # total_space = user.user_level.max_total_size
    # 暂时写个固定值
    total_space = 12345678

    upload_obj = _Upload(file_name, file_size, offset_size, hash_str, file_folder, total_space)
    if not upload_obj.bool_save:
        return_data = {
            'return_code': 5,
            'message': u'空间不足或者上传文件过大.'
        }
        return return_data
    file = request.FILES.get('csv_file')
    temp_file_path = settings.EXECL_TMP_FILE_DIR.format("user_" + str(2))
    if file_name.endswith('.csv'):
        csv_coding = 'gbk'
        try:
            dialect = csv.Sniffer().sniff(codecs.EncodedFile(file, csv_coding).read(1024))
            file.open()
            reader = csv.reader(codecs.EncodedFile(file, csv_coding), delimiter=str(','), dialect=dialect)
            header = reader.next()
            header = [h.decode(csv_coding) for h in header]
        except Exception as e:
            context = {
                "return_code": 5,
                "message": u"上传文件错误,文件格式错误"
            }
            return context
    elif os.path.splitext(file_name)[1] in ['.xlsx', '.xlsm', '.xltx', '.xltm', '.xlsb', '.xlam']:
        pass
    else:
        context = {
            "return_code": 5,
            "message": u"上传文件错误,文件格式错误",
        }
        return context
    file_info = FileInfo.objects.create(hash_key=hash_str, user_id=2, file_status=3,
                                        file_name=file_name, file_total_size=file_size, file_curl_size=file_size)

    str_uuid = '_'.join(str(uuid.uuid1()).split('-'))
    store_file_name = str_uuid + os.path.splitext(file_name)[1]
    file_info.file_name_uuid = store_file_name
    file_info.save()

    temp_file = os.path.join(temp_file_path, store_file_name)
    common.handle_uploaded_file(file, temp_file, 'wb+')
    # 最后还需要计算文件的MD5值
    end_md5_sum = common.md5sum(temp_file)
    if end_md5_sum == hash_str:
        context = {
            "return_code": 0,
            "message": u"上传文件完成",
            "data": {"file_id": file_info.id}
        }
    else:
        context = {
            "return_code": 6,
            "message": u"上传文件未完成",
            "data": {"file_id": file_info.id}
        }
    return context


class _Upload(object):
    """
    上传操作
    """

    def __init__(self, file_name, file_size, offset_size, hash_str, file_folder, total_space):
        self.file_name = file_name
        self.file_size = file_size
        self.offset_size = offset_size
        self.hash_str = hash_str
        # 文件目录
        self.file_folder = file_folder
        # 用户能够使用的最大空间
        self.total_space = total_space
        print "fffff", self.file_folder

    @property
    def bool_save(self):
        """判断是否能够上传文件"""

        if self.file_name.endswith('csv'):
            # 单个CSV 文件最大为200
            if self.file_size > 1024 * 1024 * 200:
                return False
        elif os.path.splitext(self.file_name)[1] in ['.xlsx', '.xlsm', '.xltx', '.xltm', '.xlsb', 'xlam', '.xls']:
            # 单个execl文件最大为100M
            if self.file_size > 1024 * 1024 * 100:
                return False
        else:
            # 暂时不支持其他格式文件
            return False

        used_space = 0
        if os.path.exists(self.file_folder):
            # 获取已经使用的空间大小
            for root, dirs, files in os.walk(self.file_folder):
                used_space += sum([os.path.getsize(os.path.join(root, name)) for name in files])

            all_size = used_space + self.file_size
            # 空间不足
            if all_size > self.total_space:
                return False
        else:
            # 创建文件夹
            print "111111111111111"
            os.makedirs(self.file_folder)
        return True


@csrf_exempt
def create_question(request):
    import datetime
    """
    提出问题
    :param request: 
    :return: 
    """
    if request.method == 'POST':
        question_text = request.POST.get('question')
    else:
        question_text = "ask"
    t = datetime.datetime.now()
    Question.objects.create(question_text=question_text, pub_date=t)
    return HttpResponse({"status": 0})
