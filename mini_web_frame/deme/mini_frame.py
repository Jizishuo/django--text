import time
import re
from pymysql import *

URL_FUNC_DICT = dict()

#路由装饰器
def route(url):
    #print(url)
    def set_func(func):
        URL_FUNC_DICT[url] = func  #{'/index.py': index(),}
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func


@route('/index.html')
def index(ret):
    with open('./templates/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    my_stick_info = '哈哈哈哈哈哈哈我是index'
    content = re.sub(r'\{% content %\}', my_stick_info, content)
    return content

@route('/home.html')
def home(ret):
    with open('./templates/home.html', 'r', encoding='utf-8') as f:
        content = f.read()

    my_stick_info = '哈哈哈哈哈哈哈我是home'
    content = re.sub(r'\{% content %\}', my_stick_info, content)

    conn = connect(host='localhost', port=3306, user='root', password='root', database='text')#, charset='utf-8'
    cs = conn.cursor()
    cs.execute('select * from mini_web;')
    text_info = cs.fetchall()
    cs.close()
    conn.close()

    t_tem = '''<tr><td>序号:</td><td>name:%s</td><td>like:%s</td><td>age:%s</td></tr>
    <button type="submit">添加</button>'''
    html = ''
    for i in text_info:
        html += t_tem % (i[0], i[1], i[2])

    content = re.sub(r'\{% mysql_info %\}', html, content)

    return content

@route(r'/add/(\d+)\.html')
def add_focus(ret):
    stock_code = ret.group(1)


    conn = connect(host='localhost', port=3306, user='root', password='root', database='text')#, charset='utf-8'
    cs = conn.cursor()
    sql = """select * from mini_web where id = %s;"""
    cs.execute(sql, (stock_code,))
    #判断有木有
    if not cs.fetchall():
        cs.close()
        conn.close()
        return "木有这个数据,手下留情"

    #判断是否添加过
    '''
    sql = """select * from mini_web where id = %s;"""
    cs.execute(sql, (stock_code,))
    #判断是否重复
    if cs.fetchall():
        cs.close()
        conn.close()
        return "添加过数据,手下留情"  
    '''


    cs.close()
    conn.close()

    return "add ok--%s" % stock_code


@route('/register.html')
def register(ret):
    return "我是register%s" % time.ctime()

'''
URL_FUNC_DICT = {
    '/index.py': index,
    '/home.py': home,
    '/register': register,
}
'''

def application(env, strart_response):
    strart_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])

    file_name = env['PATH_INFO']
    '''
    if file_name == '/index.py':
        return index()
    elif file_name == '/login.py':
        return login()
    elif file_name == '/register.py':
        return register()
    elif file_name == '/profile.py':
        return profile()
    else:
        return 'not found you page..'
    '''
    try:
        for url, func in URL_FUNC_DICT.items():
            ret = re.match(url, file_name)
            if ret:
                return func(ret)
        else:
            return '请求的url%s没有对应的函数' % file_name
        #return URL_FUNC_DICT[file_name]()
    except Exception as e:
        return '有异常:%s' % str(e)