"""
运行程序的方式：python mini_wsgi.py 端口 框架包:函数名 默认:python mini_wsgi.py 8080 mini_frame:application
"""


import socket
import re
import multiprocessing
import time
import sys


#from deme import mini_frame


class WSGIServer(object):
    def __init__(self, port, app, static_path):
        # 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 3次握手4次挥手

        # 绑定
        self.tcp_server_socket.bind(('', port))

        # 变为监听套接字
        self.tcp_server_socket.listen(128)

        self.application = app
        self.static_path = static_path


    def service_client(self, new_socket):
        """为这个客户端返回数据"""
        #接受浏览器发来的请求 http请求
        request = new_socket.recv(1024).decode('utf-8')
        print(request)

        request_lines = request.splitlines()
        print(request_lines)

        file_name = ""
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        if ret:
            file_name = ret.group(1)
            print(file_name)
            if file_name == '/':
                file_name = '/index.html'

        #返回http格式的数据创给浏览器
        if not file_name.endswith(".html"):  # py结尾的请求（动态）
            #print(file_name.endswith(".py"))
            try:
                f = open(self.static_path + file_name, 'rb')
            except:
                #打不开404
                response = 'HTTP/1.1 404 NOT FOUND\r\n'
                response += '\r\n'
                response += '.........file not found........'
                new_socket.send(response.encode('utf-8'))
            else:
                #打开了返回
                html_content = f.read()
                f.close()
                #准备发生数据给浏览器 header
                response = 'HTTP/1.1 200 OK\r\n'
                response += '\r\n'

                new_socket.send(response.encode('utf-8'))
                new_socket.send(html_content)

        else:
            # （动态）.py
            env = dict()
            env['PATH_INFO'] = file_name
            #body = mini_frame.application(env, self.set_response_header)
            body = self.application(env, self.set_response_header)

            header = 'HTTP/1.1 %s\r\n' % self.status
            for temp in self.headers:
                header += '%s:%s\r\n' % (temp[0], temp[1])

            header += '\r\n'

            response = header + body
            new_socket.send(response.encode('utf-8'))

        #关闭套接
        new_socket.close()

    def set_response_header(self, status, headers):
        self.status = status
        self.headers = [('server', 'mini_web v6666')]
        self.headers += headers

    def run_forver(self):

        while True:
            #等待客户端连接
            new_socket, clinet_addr = self.tcp_server_socket.accept()

            #为这个客户端提供服务
            p = multiprocessing.Process(target=self.service_client, args=(new_socket, ))
            p.start()

            new_socket.close()

        #关闭监听套接字
        self.tcp_server_socket.close()



def main():
    """
    控制整体，创建一个web服务器，调用这个对象用run-forever方法运行
    :return:
    """
    if len(sys.argv) >= 2:
        try:
            port = int(sys.argv[1])
            frame_app_name = sys.argv[2]

            ret = re.match(r'([^:]+):(.*)', frame_app_name)
            if ret:
                frame_name = ret.group(1)
                app_name = ret.group(1)
        except Exception as e:
            print("端口输入错误, ")
    else:
        port = 8080
        frame_name = 'mini_frame'
        app_name = 'application'

    with open('./web_server.conf') as f:
        conf_info = eval(f.read())
        #static_path

    sys.path.append(conf_info['deme_path'])

    frame = __import__(frame_name) #返回值导入的这个模块
    app = getattr(frame, app_name) #from deme import mini_frame
    #print(app)


    wsgi_server = WSGIServer(port, app, conf_info['static_path'])
    wsgi_server.run_forver()

if __name__ == "__main__":
    main()