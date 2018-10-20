'''
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):  #name=user,bases=(),attrs={'uid':(..)...}
        mappings = dict()
        #判断是否需要保存
        #例如type('AAA', (), {'num ':1, 'num2':2}) 创建类
        for k, v in attrs.items():
            if isinstance(v, tuple):
                #print("mappings %s--->%s" % (k, v))
                mappings[k] = v

        #删除这些存在字典中的属性
        for k in mappings.keys():
            attrs.pop(k)

        #将之前的uid/name..以及对应的对象引用，类名
        attrs['__mappings__'] = mappings #雷属性与列名字的映射关系
        attrs['__table__'] = name
        #tuple(attrs)
        return type.__new__(cls, name, bases, attrs)


class User(metaclass=ModelMetaclass):
    uid = ('uid', 'int unsigned')
    name = ('username', 'varchar(30)')
    email = ('email', 'varchar(30)')
    password = ('password', 'varchar(30)')
    #经过modelmetaclas后变
    #__mappings__ = {
        #'uid' : ('uid', 'int unsigned'),
        #'name' : ('username', 'varchar(30)'),
        #'email' : ('email', 'varchar(30)'),
        #'password' : ('password', 'varchar(30)'),
    #}
    #__table__ = 'User'

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
            #uid=123 name=uid,value=123的name=value...

    def save(self):
        fields = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v[0])
            args.append(getattr(self, k, None))
        #这个不完美
        #sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join([str(i) for i in args]))
        # insert into User (uid,username,email,password) values (123,root,xxx@xxx,xxxx)
        args_temp = list()
        for temp in args:   #['123', "'root'", "'xxx@xxx'", "'xxxx'"]
            #判断插入的如果是数字
            if isinstance(temp, int):
                args_temp.append(str(temp))
            elif isinstance(temp, str):
                args_temp.append("""'%s'""" % temp)
        print(args_temp)
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(args_temp))

        print(sql)
        #insert into User (uid,username,email,password) values (123,'root','xxx@xxx','xxxx')


u = User(uid=123, name='root', email='xxx@xxx', password='xxxx')
u.save()
'''

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):  #name=user,bases=(),attrs={'uid':(..)...}
        mappings = dict()
        #判断是否需要保存
        #例如type('AAA', (), {'num ':1, 'num2':2}) 创建类
        for k, v in attrs.items():
            if isinstance(v, tuple):
                #print("mappings %s--->%s" % (k, v))
                mappings[k] = v

        #删除这些存在字典中的属性
        for k in mappings.keys():
            attrs.pop(k)

        #将之前的uid/name..以及对应的对象引用，类名
        attrs['__mappings__'] = mappings #雷属性与列名字的映射关系
        attrs['__table__'] = name
        #tuple(attrs)
        return type.__new__(cls, name, bases, attrs)


class Model(metaclass=ModelMetaclass):
    #经过modelmetaclas后变
    #__mappings__ = {
        #'uid' : ('uid', 'int unsigned'),
        #'name' : ('username', 'varchar(30)'),
        #'email' : ('email', 'varchar(30)'),
        #'password' : ('password', 'varchar(30)'),
    #}
    #__table__ = 'User'

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
            #uid=123 name=uid,value=123的name=value...

    def save(self):
        fields = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v[0])
            args.append(getattr(self, k, None))
        #这个不完美
        #sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join([str(i) for i in args]))
        # insert into User (uid,username,email,password) values (123,root,xxx@xxx,xxxx)
        args_temp = list()
        for temp in args:   #['123', "'root'", "'xxx@xxx'", "'xxxx'"]
            #判断插入的如果是数字
            if isinstance(temp, int):
                args_temp.append(str(temp))
            elif isinstance(temp, str):
                args_temp.append("""'%s'""" % temp)
        print(args_temp)
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(args_temp))

        print(sql)
        #insert into User (uid,username,email,password) values (123,'root','xxx@xxx','xxxx')

class User(Model):
    uid = ('uid', 'int unsigned')
    name = ('username', 'varchar(30)')
    email = ('email', 'varchar(30)')
    password = ('password', 'varchar(30)')


u = User(uid=123, name='root', email='xxx@xxx', password='xxxx')
u.save()