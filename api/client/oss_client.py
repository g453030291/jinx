import oss2

from datetime import datetime
from api.conf.config import constant


class OSSClient:
    def __init__(self):
        self.auth = oss2.Auth(constant.access_key_id, constant.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, constant.oss_endpoint, constant.oss_bucket_name)

    def put_object(self, key, data):
        date_prefix = datetime.now().strftime("%Y/%m/%d")
        full_key = f"{date_prefix}/{key}"
        self.bucket.put_object(full_key, data)

    def get_object(self, key):
        return self.bucket.get_object(key).read()

    def delete_object(self, key):
        self.bucket.delete_object(key)

    def list_objects(self):
        return [obj.key for obj in oss2.ObjectIterator(self.bucket)]

    def get_object_url(self, key):
        return self.bucket.sign_url('GET', key, 0)

    def put_object_from_file(self, key, file_path):
        self.bucket.put_object_from_file(key, file_path)

    def get_object_to_file(self, key, file_path):
        self.bucket.get_object_to_file(key, file_path)

    def delete_objects(self, keys):
        self.bucket.batch_delete_objects(keys)

    def delete_bucket(self):
        oss2.Bucket(self.auth, self.bucket.bucket_name).delete_bucket()

if __name__ == '__main__':
    oss_client = OSSClient()
    oss_client.put_object("test.txt", b"hello world")
    print(oss_client.get_object_url("test.txt"))
