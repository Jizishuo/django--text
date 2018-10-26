#定义索引

from haystack import indexes
from .models import GoodsSKU #导入模型

class Goodsindex(indexes.SearchIndex, indexes.Indexable):
    #索引字段  use_template指定表字段建立索引说明文件放在文件中
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        #返回模型类
        return GoodsSKU

    #建立索引的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()