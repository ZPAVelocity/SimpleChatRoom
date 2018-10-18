# !/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import threading


def client_send(sock):
    global outString
    while True:
        outString = input('> ')
        outString = nick + ':' + outString
        sock.send(outString.encode('utf-8'))


def client_accept(sock):
    global inString
    while True:
        try:
            inString = sock.recv(1024)
            if not inString:
                break
            if outString != inString:
                print(inString)
        except:
            break


nick = input('input your nickname: ')
ip = input('input the server ip address:')
port = 8888

sock = socket.socket()
sock.connect((ip, port))

sock.send(nick.encode('utf-8'))

th_send = threading.Thread(target=client_send, args=(sock, ))  # 发送消息的线程
th_send.start()

th_accept = threading.Thread(target=client_accept, args=(sock, ))  # 接受消息的线程
th_accept.start()
