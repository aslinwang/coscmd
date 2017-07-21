# -*- coding=utf-8
import cos_client
import logging
import random
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN, stream=sys.stdout, format="%(asctime)s - %(message)s")
access_id = "AKID15IsskiBQKTZbAo6WhgcBqVls9SmuG00"
access_key = "ciivKvnnrMvSvQpMAWuIz12pThGGlWRW"
file_id = str(random.randint(0, 1000)) + str(random.randint(0, 1000))
file_list = []
test_num = 20


def gen_file(path, size):
    file = open(path, 'w')
    file.seek(1024*1024*size)
    file.write('\x00')
    file.close()


def setUp():
    print "config"
    conf = cos_client.CosConfig(
        appid="1252448703",
        bucket="lewzylu05",
        region="cn-north",
        access_id=access_id,
        access_key=access_key,
        part_size=1,
        max_thread=5
    )
    client = cos_client.CosS3Client(conf)
    global obj_int
    obj_int = client.obj_int()

    conf = cos_client.CosConfig(
                appid="1252448703",
                bucket="buckettest",
                region="cn-north",
                access_id=access_id,
                access_key=access_key,
                part_size=1,
                max_thread=5)
    client = cos_client.CosS3Client(conf)
    global buc_int
    buc_int = client.buc_int()


def tearDown():
    print "function teardown"


def Test_upload_object():
    for i in range(test_num):
        file_size = 3.1 * i + 0.1
        file_name = "tmp" + file_id + "_" + str(file_size) + "MB"
        print "Test upload " + file_name
        sys.stdout.flush()
        gen_file(file_name, file_size)
        file_list.append([file_name, os.path.getsize(file_name)])
        global obj_int
        rt = obj_int.upload_file(file_name, file_name)
        assert rt
        os.remove(file_name)


def Test_download_object():
    for i in range(test_num):
        file_name = file_list[i][0]
        print "Test download " + file_name
        sys.stdout.flush()
        global obj_int
        rt = obj_int.download_file(file_name, file_name)
        assert rt
        print "Test object size with " + file_name
        assert os.path.getsize(file_name) == file_list[i][1]
        os.remove(file_name)


def Test_delete_object():
    for i in range(test_num):
        file_name = file_list[i][0]
        print "Test delete " + file_name
        sys.stdout.flush()
        global obj_int
        rt = obj_int.delete_file(file_name)
        assert rt


def Test_create_bucket():
    print "Test create bucket"
    global buc_int
    rt = buc_int.create_bucket()
    assert rt


def Test_get_bucket():
    print "Test get bucket"
    global buc_int
    rt = buc_int.get_bucket()
    assert rt


def Test_delete_bucket():
    print "Test delete bucket"
    global buc_int
    rt = buc_int.delete_bucket()
    assert rt


if __name__ == "__main__":
    setUp()
    Test_upload_object()
    Test_download_object()
    Test_delete_object()