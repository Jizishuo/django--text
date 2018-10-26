from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client

#重写这个方法
class FDFSStorage(Storage):

    def __init__(self,client_conf=None, base_url=None):
        #初始化多2个属性
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONG

        if base_url is None:
            base_url = settings.FDFS_URL

        self.client_conf = client_conf
        self.base_url = base_url

    #fdfs文件存储类

    def open(self,name, mode ='rb'):
        #打开文件使用
        pass

    def save(self, name, content, max_length = None):
        #保存使用, name 选择上传文件的名字 content包含上传文件内容的file对象
        client = Fdfs_client(self.client_conf)
        #上传 返回字典
        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed':
            #上传失败
            raise Exception('上传文件到fdfs失败')
        #获取返回的文件id
        file_name = res.get('Remote file_id')
        return file_name

    def exists(self, name):
        #django判断文件可不可以用
        return False

    def url(self, name):
        #不写会出错,返回url self.base_url = 'https//xxxxxxx'
        return self.base_url + name
