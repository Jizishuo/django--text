
'''
#广播
import socket, sys

dest = ('<broadcast>', 7788)
#192.168.1.255 (发送广播的地址) 或 <broadcast>

s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#发送广播需要这一句
s.setsockopt(socket.SOL_SOCKET ,socket.SO_BROADCAST, 1)

s.send('hi', dest)

print("等待对方回复")

while True:
    (buf, address) = s.recvfrom(2048)
    print('received from %s: %s' % (address, buf))
'''


'''
#单进程非堵塞服务器
from socket import *

sersocket = socket(AF_INET, SOCK_STREAM)

localaddr = ('', 7788)
sersocket.bind(localaddr)

#让这个sock变为非堵塞--并发
sersocket.setblocking(False)

sersocket.listen(5)

newsocketlist = []

while True:
    print("等待客户端")
    try:
        newsocket, destaddr = sersocket.accept() #等待3次握手
    except:
        pass
    else:
        #新客户到来

        print("新客户，数据处理 ;%s" % str(destaddr))
        newsocket.setblocking(False)
        newsocketlist.append((newsocket, destaddr)) #元组


    for newsocket, destaddr in newsocketlist: #取
        try:
            recvdata = newsocket.recv(1024)
        except:
            pass
        else:
            if len(destaddr) <0: #关闭
                print('recv%s : %s' % (str(destaddr), recvdata))
            else:
                newsocketlist.remove((newsocket, destaddr))
                print("%s下线" % destaddr)
    sersocket.close()
'''


