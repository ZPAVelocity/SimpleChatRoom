# !/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import threading


condition = threading.Condition()  # 判断条件 线程同步 锁

host = input('input server ip address:')
port = 8888
data = ''  # 发送或接收文本

s = socket.socket()
print('Socket created')
s.bind((host, port))
s.listen(5)

print('Socket new listening')


def NotifyAll(ss):
    global data
    if condition.acquire():  # 获取锁
        data = ss
        condition.notifyAll()  # 当前线程放弃对资源的占有并通知其他线程从wait方法执行
        condition.release()  # 释放锁


def threadOut(conn, nick):  # 发送消息
    global data
    while True:
        if condition.acquire():
            condition.wait()  # 放弃对当前资源的占有并等消息通知
            if data:
                try:
                    conn.send(data)
                    condition.release()
                except:
                    condition.release()
                    return


def threadIn(conn, nick):  # 接收消息
    while True:
        try:
            temp = conn.recv(1024)
            if not temp:
                conn.close()
                return
            NotifyAll(temp)
            print(data)
        except:
            NotifyAll(nick + 'error')
            print(data)
            return


while True:
    conn, addr = s.accept()
    print('Connected with' + addr[0] + ':' + str(addr[1]))
    nick = conn.recv(1024)
    NotifyAll('Welcome ' + nick.decode('utf-8') + ' to the room! ')
    print(data)
    conn.send(data.encode('utf-8'))
    threading.Thread(target=threadOut, args=(conn, nick)).start()
    threading.Thread(target=threadIn, args=(conn, nick)).start()

