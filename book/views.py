# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import codecs
import common
import io
import os
import json
import uuid
from django.conf import settings
from models import FileInfo, Question
from dwebsocket import require_websocket
from django.http import StreamingHttpResponse

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
    import time
    start_time = time.time()
    print "start_time..",start_time
    # user = request.user
    file_name = 'eggs.xlsx'
    file_size = 22000
    hash_str = '5c2bcdd6e86d4bcfa668d163ba7345d2' # 文件特征值
    offset_size = 123
    # 暂时都是上传新的文件
    offset_size = 0
    file_folder = settings.EXECL_TMP_FILE_DIR.format("user_" + str(2))
    # 判断用户的磁盘大小
    # total_space = user.user_level.max_total_size
    # 暂时写个固定值
    total_space = 12345678

    upload_obj = _Upload(file_name, file_size, offset_size, hash_str, file_folder, total_space)

    # if not upload_obj.bool_save:
    #     return_data = {
    #         'return_code': 5,
    #         'message': u'空间不足或者上传文件过大.'
    #     }
    #     return JsonResponse(return_data)
    print "DDDDD"
    file = request.FILES.get('csv_file')
    temp_file_path = settings.EXECL_TMP_FILE_DIR.format("user_" + str(2))
    print "oooooooooo"
    print "ppppppppp....", os.path.splitext(file_name)[1]
    if file_name.endswith('.csv'):
        csv_coding = 'gbk'
        try:
            dialect = csv.Sniffer().sniff(codecs.EncodedFile(file, csv_coding).read(1024))
            print "1"
            file.open()
            reader = csv.reader(codecs.EncodedFile(file, csv_coding), delimiter=str(','), dialect=dialect)
            print "2"
            header = reader.next()
            print "3"
            header = [h.decode(csv_coding) for h in header]
            print "4"
        except Exception as e:
            print "ccccccc"
            context = {
                "return_code": 5,
                "message": u"上传文件错误,文件格式错误"
            }
            return JsonResponse(context)
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
    end_time = time.time()
    print "start_time..", end_time
    print "cost_time...", end_time-start_time
    return HttpResponse("success")


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
        print "request.POST", request.body
        content = json.loads(request.body)
        question_text = content.get('question')
    else:
        question_text = "ask"
    t = datetime.datetime.now()
    Question.objects.create(question_text=question_text, pub_date=t)
    return HttpResponse({"status": 0})


@require_websocket
def echo_once(request):
    message = request.websocket.wait()
    request.websocket.send(message)



from store_user.models import UserInfo
from dwebsocket import require_websocket, accept_websocket

room = common.RoomServer()

def _who_is_login(req):
    '''
    return login user or None if not found
    '''
    uid = req.session.get('uid', None)
    if uid:
        users = UserInfo.manager.filter(pk=uid)
        if len(users) == 1:
            return users[0]
    else:
        return None

@require_websocket
def ws(req):
    user = _who_is_login(req)
    # 获得 ws 对象
    ws = req.websocket
    # 获得 sid 作为 键存储
    sid = req.session.session_key
    ctx = room.get_ctx(sid)
    if ctx:
        room.update(sid, user, ws)
    else:
        room.add_user_broadcast(sid, user, ws)
    # 接受消息
    for raw_msg in ws:
        if raw_msg:
            room.handle_msg(user, raw_msg)
    # 断开连接 向所有用户发送广播
    room.remove_user_broadcast(sid)


def down_work_table(request):
    """
    下载工作表
    :param request:
    :return:
    """
    user = request.user
    # form = forms.DownWorkTableForm(getattr(request, request.method))
    # if not form.is_valid():
    #     return_data = {
    #         'return_code': 3,
    #         'message': u'参数错误。'
    #     }
    #     return return_data
    # cld = form.cleaned_data
    #
    # work_table_ids = cld['work_table_ids']
    # work_table_id_list = work_table_ids.split(',')
    #
    # work_table_set = WorkTable.objects.filter(id__in=work_table_id_list).values("work_table_uuid", "work_table_rename")
    #
    # # file_dir = settings.WORKTABLE_TEMPLATE_PATH + "user_{}/".format(user.id)
    work_table_set = [{"work_table_uuid":"42bc23ae_9abf_11e7_8cda_f45c89a97b13.csv","work_table_rename":"change_work_table_name"}]
    file_dir = '/data/test_django/store/user_2/'
    for work_table in work_table_set:
        file_path = os.path.join(file_dir, work_table['work_table_uuid'])

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        the_file_name = work_table['work_table_rename'] + ".csv"
        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response.write(codecs.BOM_UTF8)  # 加入BOM头才能在csv文件中添加中文，否则在excel中是乱码，此句必须加在下句的前
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

        # response = StreamingHttpResponse("文件不存在！")
        # response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format("")
        # return response

        return response
