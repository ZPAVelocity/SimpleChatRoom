from threading import Thread
from socket import *

udpSocket = None  # None 存储对象类型
destIp = ''
destPort = 0


def recvData():
    global udpSocket
    while True:
        recvInfo = udpSocket.recvfrom(1024)
        print('\r>> %s:%s\r\n<< ' % (str(recvInfo[1]), recvInfo[0].decode('gb2312')), end='')


def sendData():
    global udpSocket
    global destIp
    global destPort
    while True:
        try:
            sendInfo = input('<< ')
            udpSocket.sendto(sendInfo.encode('gb2312'), (destIp, destPort))
        except:
            print('ERROR: Cannot connect. ')
            break


def main():
    global udpSocket
    global destIp
    global destPort

    usePort = int(input('Use port: '))
    destIp = input('Target ip: ')
    destPort = int(input('Target port: '))

    
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind(('', usePort))
    
    tr = Thread(target=recvData)
    ts = Thread(target=sendData)

    tr.start()
    ts.start()

    tr.join()
    ts.join()


if __name__ == '__main__':
    main()
