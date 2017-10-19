#!/usr/local/python
#coding:utf-8
import hashlib
import os
def md5sum(fname, fsize='1024'):
    """ 计算文件的MD5值 """
    def read_chunks(fh):
        fh.seek(0,0)
        chunk = fh.read(1024)
        while chunk:
            yield chunk
            fh.seek(10240, 1)
            chunk = fh.read(1024)
        else: #最后要将游标放回文件开头
            fh.seek(0,0)
    m = hashlib.md5()
    if isinstance(fname, basestring) and os.path.exists(fname):
        with open(fname, "rb") as fh:
            for chunk in read_chunks(fh):
                m.update(chunk)
    else:
        return ""
    m.update(str(fsize))
    return m.hexdigest()

if __name__ == "__main__":
    print md5sum('/data/test_django/store/user_2/d16cbaa6_9daf_11e7_bc5c_f45c89a97b13.xlsx')
