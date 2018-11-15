from socket import *
from threading import Thread

def recvdata():
    while True:
        recvinfo = udpSocket.recvfrom(1024)
        print(">>>%s:::%s"%(str(recvinfo[1]), str(recvinfo[0])))

def senddata():
    while True:
        sendinfo = input("<<<")
        udpSocket.sendto(sendinfo.encode('gb2312'), (destip, destpost))

udpSocket = None
destip = 0
destpost = 0

def main():

    global destip
    global destpost
    global udpSocket

    destip = int(input("对方的ip:"))
    destpost = int(input("对方的端口"))

    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind(('', 4567))


    tr = Thread(target=recvdata)
    ts = Thread(target=recvdata)

    tr.start()
    ts.start()

    tr.join()
    ts.join()

if __name__ == '__main__':
    main()